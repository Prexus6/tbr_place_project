from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Přidání related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Přidání related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    def __str__(self):
        return self.username

class PromptType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Prompt(models.Model):
    prompt_name = models.TextField(blank=False, null=False)
    prompt_type = models.ForeignKey(PromptType, on_delete=models.CASCADE, related_name='prompts')

    def __str__(self):
        return self.prompt_name

class Author(models.Model):
    author_name = models.TextField(unique=True)

    def __str__(self):
        return self.author_name

class Genre(models.Model):
    genre_name = models.TextField(unique=True)

    def __str__(self):
        return self.genre_name

class Book(models.Model):
    book_title = models.TextField()
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    book_genre = models.ManyToManyField(Genre, related_name='books')
    book_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    book_cover = models.ImageField(upload_to='book_covers/')
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.book_title

class Reader(models.Model):
    user_id = models.IntegerField(unique=True)

    def __str__(self):
        return f'Reader {self.user_id}'

class MyPromptType(models.Model):
    myprompt_type_name = models.CharField(max_length=255)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='myprompt_types')

    def __str__(self):
        return self.myprompt_type_name

class MyPrompt(models.Model):
    prompt_name = models.TextField()
    prompt_type = models.ForeignKey(MyPromptType, on_delete=models.CASCADE, related_name='my_prompts')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='my_prompts')

    def __str__(self):
        return self.prompt_name

class BrowsingHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)




