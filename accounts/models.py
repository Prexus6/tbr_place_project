from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from tbr_place_project import settings

# Správce uživatelů pro vlastní uživatelský model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

# Vlastní uživatelský model rozšiřující AbstractUser
class CustomUser(AbstractUser):
    favorite_book = models.CharField(max_length=100, blank=True, null=True)  # Oblíbená kniha uživatele
    secret_question = models.CharField(max_length=255)  # Bezpečnostní otázka
    secret_answer = models.CharField(max_length=255)  # Odpověď na bezpečnostní otázku

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



