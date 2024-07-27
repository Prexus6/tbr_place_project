from urllib import request

import requests
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from .models import Book, Author, Genre
import re
import logging

logger = logging.getLogger(__name__)

def is_valid_isbn(isbn):
    """Validate ISBN-13 format."""
    return bool(re.match(r'^\d{13}$', isbn))

def search_books_by_title(title):
    print(f"Searching for books with title: {title}")  # Debug print
nesmysl
    response = requests.get(f'https://openlibrary.org/search.json?title={title}')
    print(f"Response from Open Library: {response.json()}")  # Debug print
    return response.json()


def save_book_from_open_library(book_info):
    """
    Uloží knihu z údajov získaných z Open Library do databázy.
    """
    if not book_info['author_name']:
        print(f"Ignoring book without author: {book_info}")
        return

    author = get_or_create_author(book_info['author_name'])

    book, created = Book.objects.get_or_create(
        isbn=book_info['isbn'],
        defaults={
            'book_title': book_info['title'],
            'book_author': author,
            'book_rating': book_info['rating'],
            'book_cover': book_info['cover_url'],
        }
    )

    if not created:
        book.book_title = book_info['title']
        book.book_author = author
        book.book_rating = book_info['rating']
        book.book_cover = book_info['cover_url']
        book.save()
        print(f"Updated existing book: {book}")  # Debug print
    else:
        print(f"Created new book: {book}")  # Debug print

    update_genres(book, book_info['genres'])

def get_or_create_author(author_name):
    """
    Získa existujúceho autora alebo vytvorí nového na základe mena.
    """
    if author_name:
        author, created = Author.objects.get_or_create(author_name=author_name)
        return author
    return None

def update_genres(book, genres):
    """
    Uloží alebo aktualizuje žánre knihy.
    """
    for genre_name in genres:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        book.book_genre.add(genre)


