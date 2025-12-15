from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import RegisteredContent
from .serializers import RegisteredContentSerializer
from .utils import ContentProcessor
import numpy as np

class RegisterContentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Compute Hash
        content_hash = ContentProcessor.compute_hash(file_obj)
        if RegisteredContent.objects.filter(content_hash=content_hash).exists():
            return Response({'error': 'Content already registered'}, status=status.HTTP_409_CONFLICT)

        # 2. Extract Features (need to save temporarily or process in memory)
        # For simplicity, we save first using serializer then update embedding
        serializer = RegisteredContentSerializer(data=request.data)
        if serializer.is_valid():
            # Assign owner if valid (assuming auth is set up, else default/anonymous for now)
            # request.user should be used in real scenario. 
            # For now, we might need a dummy user or handle if request.user is not authenticated
            # Auto-assign to 'demo_user' for testing if not authenticated
            user = request.user
            if not user.is_authenticated:
                from django.contrib.auth.models import User
                user, _ = User.objects.get_or_create(username='demo_user')

            serializer.save(owner=user, content_hash=content_hash, embedding=[]) 
            instance = serializer.instance
            
            # Extract features from saved file
            try:
                features = ContentProcessor.extract_features(instance.file.path)
                instance.embedding = features
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                instance.delete()
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOwnershipView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Check exact hash match
        content_hash = ContentProcessor.compute_hash(file_obj)
        exact_match = RegisteredContent.objects.filter(content_hash=content_hash).first()
        
        if exact_match:
            return Response({
                'status': 'exact_match',
                'owner': exact_match.owner.username,
                'registered_at': exact_match.created_at
            }, status=status.HTTP_200_OK)

        # 2. Check similarity
        # We need to save temp file to use Keras load_img or implement in-memory processing
        # generic approach: save to temp
        import tempfile
        import os
        
        tup = tempfile.mkstemp(suffix='.jpg')
        f = os.fdopen(tup[0], 'wb')
        file_obj.seek(0)
        f.write(file_obj.read())
        f.close()
        temp_path = tup[1]

        try:
            features = ContentProcessor.extract_features(temp_path)
        except Exception as e:
            os.remove(temp_path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        os.remove(temp_path)

        # Compare with all (inefficient for large DB, but fine for prototype)
        # In production -> use pgvector
        best_score = 0
        best_match = None
        
        for item in RegisteredContent.objects.all():
            if not item.embedding:
                continue
            score = ContentProcessor.compute_similarity(features, item.embedding)
            if score > best_score:
                best_score = score
                best_match = item
        
        THRESHOLD = 0.85 # Adjustable
        
        if best_score > THRESHOLD:
             return Response({
                'status': 'similar_match',
                'score': best_score,
                'owner': best_match.owner.username,
                'registered_at': best_match.created_at
            }, status=status.HTTP_200_OK)
        
        return Response({'status': 'no_match'}, status=status.HTTP_200_OK)
