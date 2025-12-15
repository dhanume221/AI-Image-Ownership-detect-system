from django.db import models
from django.contrib.auth.models import User

class RegisteredContent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='uploads/')
    content_hash = models.CharField(max_length=64, unique=True)
    embedding = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} - {self.content_hash[:8]}"
