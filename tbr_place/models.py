from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PromptType(models.Model):
    """
    Model predstavujúci preddefinované typy promptov.

    Atribúty:
        prompt_type_name (CharField): Názov typu promptu.
    """
    prompt_type_name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.prompt_type_name


class Prompt(models.Model):
    """
    Model predstavujúci prompt.

    Atribúty:
        prompt_name (TextField): Názov / obsah promptu.
        prompt_type (ForeignKey): Typ promptu, referencuje PromptType.
    """
    prompt_name = models.TextField()
    prompt_type = models.ForeignKey(PromptType, on_delete=models.CASCADE, related_name='prompts')

    def __str__(self):
        return self.prompt_name


class Author(models.Model):
    """
    Model predstavujúci autora.

    Atribúty:
        author_name (TextField): Meno autora.
    """
    author_name = models.TextField(unique=True)  # Meno autora musí byť jedinečné

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    """
    Model predstavujúci žáner.

    Atribúty:
        genre_name (TextField): Názov žánru.
    """
    genre_name = models.TextField(unique=True)  # Názov žánru musí byť jedinečný

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    """
    Model predstavujúci knihu.

    Atribúty:
        book_title (TextField): Názov knihy.
        book_author (ForeignKey): Autor knihy, referencuje Author.
        book_genre (ManyToManyField): Žánre knihy, referencuje Genre.
        book_rating (FloatField): Hodnotenie knihy.
        book_cover (ImageField): Obrázok obalu knihy.
        isbn (CharField): ISBN knihy (pre integráciu s Amazon API).
    """
    book_title = models.TextField()
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    book_genre = models.ManyToManyField(Genre, related_name='books')
    book_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    book_cover = models.ImageField(upload_to='book_covers/')
    isbn = models.CharField(max_length=13, unique=True)  # Predpokladáme formát ISBN-13

    def __str__(self):
        return self.book_title


class Reader(models.Model):
    """
    Model predstavujúci čitateľa.

    Atribúty:
        user_id (IntegerField): ID čitateľa.
    """
    user_id = models.IntegerField(unique=True)  # Predpokladáme, že user_id je jedinečné

    def __str__(self):
        return f'Čitateľ {self.user_id}'


class MyPromptType(models.Model):
    """
    Model predstavujúci užívateľom definovaný typ promptu.

    Atribúty:
        myprompt_type_name (CharField): Názov užívateľom definovaného typu promptu.
        reader (ForeignKey): Čitateľ spojený s týmto typom promptu, referencuje Reader.
    """
    myprompt_type_name = models.CharField(max_length=255)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='myprompt_types')

    def __str__(self):
        return self.myprompt_type_name


class MyPrompt(models.Model):
    """
    Model predstavujúci užívateľom definovaný prompt.

    Atribúty:
        prompt_name (TextField): Názov / obsah užívateľom definovaného promptu.
        prompt_type (ForeignKey): Typ promptu, referencuje PromptType.
        reader (ForeignKey): Čitateľ spojený s týmto promptom, referencuje Reader.
    """
    prompt_name = models.TextField()
    prompt_type = models.ForeignKey(MyPromptType, on_delete=models.CASCADE, related_name='my_prompts')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='my_prompts')

    def __str__(self):
        return self.prompt_name
