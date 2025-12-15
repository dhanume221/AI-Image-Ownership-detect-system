from rest_framework import serializers
from .models import RegisteredContent

class RegisteredContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredContent
        fields = ['id', 'owner', 'file', 'content_hash', 'created_at']
        read_only_fields = ['owner', 'content_hash', 'embedding', 'created_at']
