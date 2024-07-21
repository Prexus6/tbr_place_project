from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class PromptType(models.Model):
    """
    Model predstavujúci preddefinované typy promptov.
    """
    prompt_type_name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.prompt_type_name

    def clean(self):
        if not self.prompt_type_name:
            raise ValidationError('Prompt type name cannot be empty')
        if len(self.prompt_type_name) > 250:
            raise ValidationError('Prompt type name cannot exceed 250 characters')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Prompt(models.Model):
    """
    Model predstavujúci prompt.
    """
    prompt_name = models.TextField(blank=False, null=False)
    prompt_type = models.ForeignKey(PromptType, on_delete=models.CASCADE, related_name='prompts')

    def __str__(self):
        return self.prompt_name

    def clean(self):
        if not self.prompt_name:
            raise ValidationError('Prompt name cannot be empty')
        if not self.prompt_type:
            raise ValidationError('Prompt type cannot be null')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Model predstavujúci autora.
    """
    author_name = models.TextField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    """
    Model predstavujúci žáner.
    """
    genre_name = models.TextField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    """
    Model predstavujúci knihu.
    """
    book_title = models.TextField(blank=False, null=False)
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    book_genre = models.ManyToManyField(Genre, related_name='books')
    book_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    book_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=False, null=False)

    def __str__(self):
        return self.book_title


class Reader(models.Model):
    """
    Model predstavujúci čitateľa.
    """
    user_id = models.IntegerField(unique=True, blank=False, null=False)

    def __str__(self):
        return f'Čitateľ {self.user_id}'


class MyPromptType(models.Model):
    """
    Model predstavujúci užívateľom definovaný typ promptu.
    """
    myprompt_type_name = models.CharField(max_length=255, blank=False, null=False)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='myprompt_types')

    class Meta:
        unique_together = ('myprompt_type_name', 'reader')

    def __str__(self):
        return self.myprompt_type_name

    def clean(self):
        if not self.myprompt_type_name:
            raise ValidationError('MyPromptType name cannot be empty')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class MyPrompt(models.Model):
    """
    Model predstavujúci užívateľom definovaný prompt.
    """
    prompt_name = models.TextField(blank=False, null=False)
    prompt_type = models.ForeignKey(MyPromptType, on_delete=models.CASCADE, related_name='my_prompts')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='my_prompts')

    def __str__(self):
        return self.prompt_name

    def clean(self):
        if not self.prompt_name:
            raise ValidationError('MyPrompt name cannot be empty')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
