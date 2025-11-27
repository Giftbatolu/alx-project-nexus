from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)

    # This ensures email is treated as REQUIRED
    REQUIRED_FIELDS = ["email"]