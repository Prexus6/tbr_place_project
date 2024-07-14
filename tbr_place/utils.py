import requests
from django.core.files import File
from io import BytesIO
from .models import Book, Author, Genre


def get_book_details(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        book_key = f"ISBN:{isbn}"
        if book_key in data:
            book_data = data[book_key]
            return book_data
    return None


def save_book_details(isbn):
    book_data = get_book_details(isbn)
    if not book_data:
        print("No details found for this ISBN")
        return

    title = book_data.get('title', 'Unknown Title')
    authors_data = book_data.get('authors', [])
    genres_data = book_data.get('subjects', [])
    cover_url = book_data.get('cover', {}).get('large', '')

    authors = []
    for author_data in authors_data:
        author_name = author_data.get('name', 'Unknown Author')
        author, created = Author.objects.get_or_create(author_name=author_name)
        authors.append(author)

    if not authors:
        author, created = Author.objects.get_or_create(author_name="Unknown Author")
        authors.append(author)

    genres = []
    for genre_data in genres_data:
        genre_name = genre_data.get('name', 'Unknown Genre')
        genre, created = Genre.objects.get_or_create(genre_name=genre_name)
        genres.append(genre)

    book = Book(
        book_title=title,
        book_rating=0.0,
        isbn=isbn
    )

    if cover_url:
        response = requests.get(cover_url)
        if response.status_code == 200:
            image_name = f"{isbn}.jpg"
            image_data = BytesIO(response.content)
            book.book_cover.save(image_name, File(image_data))

    book.save()

    book.book_author = authors[0]
    book.save()

    book.book_genre.set(genres)
    book.save()

    print(f"Book '{title}' saved successfully.")

