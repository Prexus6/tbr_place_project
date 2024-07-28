from urllib import request

import requests
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from django.http import JsonResponse

from .models import Book, Author, Genre
import re
import logging

logger = logging.getLogger(__name__)

def is_valid_isbn(isbn):
    """Validate ISBN-13 format."""
    return bool(re.match(r'^\d{13}$', isbn))


def search_books_by_title(request):
    """ Vyhľadávanie kníh cez title (všeobecné)"""
    title = request.GET.get('title', '')
    page = int(request.GET.get('page', 1))
    per_page = 10

    try:
        response = requests.get(f'https://openlibrary.org/search.json?title={title}&page={page}')
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    books = data.get('docs', [])
    book_list = []
    for book in books:
        book_info = {
            'title': book.get('title', 'No Title'),
            'author_name': book.get('author_name', ['Unknown Author'])[0],
            'isbn': book.get('isbn', [''])[0] if 'isbn' in book else 'No ISBN',
            'cover_url': book.get('cover_i', ''),
            'genres': book.get('subject', [])
        }
        book_list.append(book_info)

    total_results = data.get('numFound', 0)
    total_pages = (total_results + per_page - 1) // per_page

    return JsonResponse(
        {'docs': book_list, 'total_results': total_results, 'total_pages': total_pages, 'current_page': page},
        safe=False
    )


def search_books_by_isbn(request, isbn):
    """Vyhľadaávanie cez ISBN"""
    print(f"Searching for book with ISBN: {isbn}")  # Debug print

    if not is_valid_isbn(isbn):
        return JsonResponse({'error': 'Invalid ISBN format'}, status=400)

    response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
    print(f"Response from Open Library: {response.json()}")  # Debug print

    book_data = response.json().get(f'ISBN:{isbn}', {})

    if book_data:
        book_info = {
            'title': book_data.get('title', 'No Title'),
            'author_name': book_data.get('authors', [{}])[0].get('name', 'Unknown Author'),
            'isbn': isbn,
            'rating': book_data.get('rating', 'No Rating'),
            'cover_url': book_data.get('cover', {}).get('large', 'No Cover'),
            'genres': [genre for genre in book_data.get('subjects', [])]
        }
    else:
        book_info = {'error': 'Book not found'}

    return JsonResponse(book_info, safe=False)

def autocomplete_books(request):
    """Auto-doplňovanie výsledkov."""
    term = request.GET.get('term', '')
    if not term:
        return JsonResponse([], safe=False)

    response = requests.get(f'https://openlibrary.org/search.json?q={term}')
    data = response.json()
    books = data.get('docs', [])

    suggestions = []
    for book in books:
        title = book.get('title', 'No Title')
        author = book.get('author_name', ['Unknown Author'])[0]
        isbn = book.get('isbn', [''])[0] if 'isbn' in book else 'No ISBN'
        suggestions.append({
            'label': f"{title} by {author}",
            'value': isbn
        })

    return JsonResponse(suggestions, safe=False)


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



