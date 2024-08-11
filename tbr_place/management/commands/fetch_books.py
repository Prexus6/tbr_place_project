from django.core.management.base import BaseCommand
from tbr_place.utils import search_books_by_title, save_book_from_open_library


class Command(BaseCommand):
    help = 'Fetch and save books from Open Library'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Title of the book to search for')

    def handle(self, *args, **kwargs):
        title = kwargs['title']
        results = search_books_by_title(title)
        books = results.get('docs', [])

        for book_data in books:
            book_info = {
                "title": book_data.get('title'),
                "author_name": book_data.get('author_name', ''),
                "genres": book_data.get('subject', []),
                "isbn": book_data.get('isbn', [''])[0],
                "rating": 0.0,
                "cover_url": book_data.get('cover_i', None)
            }
            save_book_from_open_library(book_info)

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched and saved books with title: {title}'))
