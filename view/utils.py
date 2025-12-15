import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import numpy as np
import hashlib

class ContentProcessor:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
            cls._model = Model(inputs=base_model.input, outputs=base_model.output)
        return cls._model

    @staticmethod
    def compute_hash(file_obj):
        sha256_hash = hashlib.sha256()
        for byte_block in iter(lambda: file_obj.read(4096), b""):
            sha256_hash.update(byte_block)
        file_obj.seek(0)
        return sha256_hash.hexdigest()

    @classmethod
    def extract_features(cls, img_path):
        model = cls.get_model()
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        return features.flatten().tolist()

    @staticmethod
    def compute_similarity(vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
