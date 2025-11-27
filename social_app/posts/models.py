from django.db import models
import uuid
from django.conf import settings


class Post(models.Model):
    post_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author}"


class PostMedia(models.Model):
    MEDIA_CHOICES = [
        ('video', 'Video'),
        ('image', 'Image'),
        ('file', 'File'),
    ]

    media_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media_type = models.CharField(max_length=20, choices=MEDIA_CHOICES)
    file = models.FileField(upload_to="post_media/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for post {self.post_id}"