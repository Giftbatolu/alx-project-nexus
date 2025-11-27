import uuid
from django.db import models
from posts.models import Post
from django.conf import settings


class Comment(models.Model):
    comment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.post}: {self.content[:20]}..."

