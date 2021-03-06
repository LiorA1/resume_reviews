from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

from PIL import Image


class CustomUser(AbstractUser):
    """CustomUser Model"""

    def __str__(self):
        return self.username


class Profile(models.Model):
    """Profile Model associated with CustomUser"""
    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#referencing-the-user-model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    image = models.ImageField(default='profile_pics/default.jpg', upload_to="profile_pics")

    def __str__(self):
        return f'{ self.user.username } Profile'
