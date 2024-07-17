import requests
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from .models import Book, Author, Genre

def search_books_by_title(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(url)
    return response.json()

def save_book_from_open_library(book_info):
    author_name = book_info['author_name']
    genres = book_info['genres']
    title = book_info['title']
    isbn = book_info['isbn']
    rating = book_info['rating']
    cover_url = book_info['cover_url']

    if not isbn:
        print(f"Book titled '{title}' does not have a valid ISBN. Skipping.")
        return

    if Book.objects.filter(isbn=isbn).exists():
        print(f"Book with ISBN {isbn} already exists. Skipping.")
        return

    author, created = Author.objects.get_or_create(author_name=author_name)

    try:
        book = Book.objects.create(
            book_title=title,
            book_author=author,
            book_rating=rating,
            isbn=isbn
        )

        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(genre_name=genre_name)
            book.book_genre.add(genre)

        if cover_url:
            """
            Uloží cover.
            """
            response = requests.get(cover_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                book.book_cover.save(f"{isbn}.jpg", ContentFile(image_data.getvalue()), save=True)
            else:
                print(f"Failed to fetch cover image for book with ISBN {isbn}")

        book.save()
        print(f"Saved book with ISBN {isbn} successfully.")
    except IntegrityError as e:
        print(f"Failed to save book with ISBN {isbn}: {e}")
