from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class CustomUser(AbstractUser):
    security_answer_1 = models.CharField(max_length=255, blank=True)
    security_answer_2 = models.CharField(max_length=255, blank=True)
    security_answer_3 = models.CharField(max_length=255, blank=True)

class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class PromptType(models.Model):
    prompt_type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.prompt_type_name

class Prompt(models.Model):
    prompt_name = models.CharField(max_length=255)
    prompt_type = models.ForeignKey(PromptType, on_delete=models.CASCADE)

    def __str__(self):
        return self.prompt_name
