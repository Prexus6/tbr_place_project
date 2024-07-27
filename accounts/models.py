from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models

class CustomUser(AbstractUser):
    favorite_book = models.CharField(max_length=255, null=True, blank=True)
    secret_question = models.CharField(max_length=255, null=True, blank=True)
    secret_answer = models.CharField(max_length=255, null=True, blank=True)


    objects = CustomUserManager()

    def __str__(self):
        return self.username
