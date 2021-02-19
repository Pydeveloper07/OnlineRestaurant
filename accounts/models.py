from django.db import models
from django.contrib.auth.models import AbstractUser
import os

def user_image_upload_path(instance, filename):
    filename = instance.username + '.jpg'
    return os.path.join('users', filename) 

class CustomUser(AbstractUser):
        avatar = models.ImageField(max_length=200, upload_to=user_image_upload_path, null=True, blank=True)
        phone_number = models.CharField(max_length=100)
        address = models.TextField(max_length=500)
