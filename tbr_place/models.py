from django.db import models


# Create your models here.


class PromptType(models.Model):
    """
    Model predstavujúci typ promptu.

    Atribúty:
        prompt_type_name (CharField): Názov typu promptu.
    """
    prompt_type_name = models.CharField(max_length=200)

    def __str__(self):
        return self.prompt_type_name


class Prompt(models.Model):
    """
    Model predstavujúci prompt.

    Atribúty:
        prompt_name (TextField): Názov alebo obsah promptu.
        prompt_type (ForeignKey): Typ promptu, odkaz na PromptType.
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
    author_name = models.TextField()

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    """
    Model predstavujúci žáner.

    Atribúty:
        genre_name (TextField): Názov žánru.
    """
    genre_name = models.TextField()

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    """
    Model predstavujúci knihu.

    Atribúty:
        book_title (TextField): Názov knihy.
        book_author (ForeignKey): Autor knihy, odkaz na Author.
        book_genre (ForeignKey): Žáner knihy, odkaz na Genre.
        book_rating (FloatField): Hodnotenie knihy.
        book_cover (ImageField): Obrázok obalu knihy.
    """
    book_title = models.TextField()
    book_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    book_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    book_rating = models.FloatField()
    book_cover = models.ImageField(upload_to='book_covers/')

    def __str__(self):
        return self.book_title


class Reader(models.Model):
    """
    Model predstavujúci čitateľa.

    Atribúty:
        user_id (IntegerField): ID používateľa čitateľa.
    """
    user_id = models.IntegerField()

    def __str__(self):
        return f'Čitateľ {self.id}'


class MyPromptType(models.Model):
    """
    Model predstavujúci užívateľský typ promptu.

    Atribúty:
        myprompt_type_name (CharField): Názov užívateľského typu promptu.
        reader (ForeignKey): Čitateľ spojený s týmto typom promptu, odkaz na Reader.
    """
    myprompt_type_name = models.CharField(max_length=255)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='myprompt_types')

    def __str__(self):
        return self.myprompt_type_name
