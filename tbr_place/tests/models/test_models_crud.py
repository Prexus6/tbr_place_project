from django.test import TestCase
from tbr_place.models import PromptType, Prompt, Reader, MyPromptType, MyPrompt, Author, Genre, Book
from django.db import IntegrityError


class AuthorCRUDTest(TestCase):
    """CRUD testy pre model Author"""

    def test_create_author(self):
        """Vytvorenie autora"""
        author = Author.objects.create(author_name='John Doe')
        self.assertEqual(author.author_name, 'John Doe')

    def test_read_author(self):
        """Čítanie autora"""
        Author.objects.create(author_name='John Doe')
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 1)
        self.assertEqual(authors[0].author_name, 'John Doe')

    def test_update_author(self):
        """Aktualizácia autora"""
        author = Author.objects.create(author_name='John Doe')
        author.author_name = 'Jane Doe'
        author.save()
        self.assertEqual(author.author_name, 'Jane Doe')

    def test_delete_author(self):
        """Odstránenie autora"""
        author = Author.objects.create(author_name='John Doe')
        author.delete()
        self.assertEqual(Author.objects.count(), 0)


class GenreCRUDTest(TestCase):
    """CRUD testy pre model Genre"""

    def test_create_genre(self):
        """Vytvorenie žánru"""
        genre = Genre.objects.create(genre_name='Fantasy')
        self.assertEqual(genre.genre_name, 'Fantasy')

    def test_read_genre(self):
        """Čítanie žánru"""
        Genre.objects.create(genre_name='Fantasy')
        genres = Genre.objects.all()
        self.assertEqual(genres.count(), 1)
        self.assertEqual(genres[0].genre_name, 'Fantasy')

    def test_update_genre(self):
        """Aktualizácia žánru"""
        genre = Genre.objects.create(genre_name='Fantasy')
        genre.genre_name = 'Science Fiction'
        genre.save()
        self.assertEqual(genre.genre_name, 'Science Fiction')

    def test_delete_genre(self):
        """Odstránenie žánru"""
        genre = Genre.objects.create(genre_name='Fantasy')
        genre.delete()
        self.assertEqual(Genre.objects.count(), 0)


class BookCRUDTest(TestCase):
    """CRUD testy pre model Book"""

    def setUp(self):
        self.author = Author.objects.create(author_name='John Doe')
        self.genre = Genre.objects.create(genre_name='Fantasy')

    def test_create_book(self):
        """Vytvorenie knihy"""
        book = Book.objects.create(
            book_title='Sample Book',
            book_author=self.author,
            book_rating=8.5,
            isbn='9780123456789'
        )
        self.assertEqual(book.book_title, 'Sample Book')
        self.assertEqual(book.book_author, self.author)
        self.assertEqual(book.book_rating, 8.5)
        self.assertEqual(book.isbn, '9780123456789')

    def test_read_book(self):
        """Čítanie knihy"""
        book = Book.objects.create(
            book_title='Sample Book',
            book_author=self.author,
            book_rating=8.5,
            isbn='9780123456789'
        )
        books = Book.objects.all()
        self.assertEqual(books.count(), 1)
        self.assertEqual(books[0].book_title, 'Sample Book')
        self.assertEqual(books[0].book_author, self.author)
        self.assertEqual(books[0].book_rating, 8.5)
        self.assertEqual(books[0].isbn, '9780123456789')

    def test_update_book(self):
        """Aktualizácia knihy"""
        book = Book.objects.create(
            book_title='Sample Book',
            book_author=self.author,
            book_rating=8.5,
            isbn='9780123456789'
        )
        book.book_rating = 9.0
        book.save()
        self.assertEqual(book.book_rating, 9.0)

    def test_delete_book(self):
        """Odstránenie knihy"""
        book = Book.objects.create(
            book_title='Sample Book',
            book_author=self.author,
            book_rating=8.5,
            isbn='9780123456789'
        )
        book.delete()
        self.assertEqual(Book.objects.count(), 0)


class ReaderCRUDTest(TestCase):
    """CRUD testy pre model Reader"""

    def test_create_reader(self):
        """Vytvorenie čitateľa"""
        reader = Reader.objects.create(user_id=1)
        self.assertEqual(reader.user_id, 1)

    def test_read_reader(self):
        """Čítanie čitateľa"""
        Reader.objects.create(user_id=1)
        readers = Reader.objects.all()
        self.assertEqual(readers.count(), 1)
        self.assertEqual(readers[0].user_id, 1)

    def test_update_reader(self):
        """Aktualizácia čitateľa"""
        reader = Reader.objects.create(user_id=1)
        reader.user_id = 2
        reader.save()
        self.assertEqual(reader.user_id, 2)

    def test_delete_reader(self):
        """Odstránenie čitateľa"""
        reader = Reader.objects.create(user_id=1)
        reader.delete()
        self.assertEqual(Reader.objects.count(), 0)


class PromptTypeCRUDTest(TestCase):
    """CRUD testy pre model PromptType"""

    def test_create_prompt_type(self):
        """Vytvorenie typu promptu"""
        prompt_type = PromptType.objects.create(prompt_type_name='General')
        self.assertEqual(prompt_type.prompt_type_name, 'General')

    def test_read_prompt_type(self):
        """Čítanie typu promptu"""
        PromptType.objects.create(prompt_type_name='General')
        prompt_types = PromptType.objects.all()
        self.assertEqual(prompt_types.count(), 1)
        self.assertEqual(prompt_types[0].prompt_type_name, 'General')

    def test_update_prompt_type(self):
        """Aktualizácia typu promptu"""
        prompt_type = PromptType.objects.create(prompt_type_name='General')
        prompt_type.prompt_type_name = 'Specific'
        prompt_type.save()
        self.assertEqual(prompt_type.prompt_type_name, 'Specific')

    def test_delete_prompt_type(self):
        """Odstránenie typu promptu"""
        prompt_type = PromptType.objects.create(prompt_type_name='General')
        prompt_type.delete()
        self.assertEqual(PromptType.objects.count(), 0)


class PromptCRUDTest(TestCase):
    """CRUD testy pre model Prompt"""

    def setUp(self):
        self.prompt_type = PromptType.objects.create(prompt_type_name='General')

    def test_create_prompt(self):
        """Vytvorenie promptu"""
        prompt = Prompt.objects.create(prompt_name='What is your favorite book?', prompt_type=self.prompt_type)
        self.assertEqual(prompt.prompt_name, 'What is your favorite book?')
        self.assertEqual(prompt.prompt_type, self.prompt_type)

    def test_read_prompt(self):
        """Čítanie promptu"""
        Prompt.objects.create(prompt_name='What is your favorite book?', prompt_type=self.prompt_type)
        prompts = Prompt.objects.all()
        self.assertEqual(prompts.count(), 1)
        self.assertEqual(prompts[0].prompt_name, 'What is your favorite book?')
        self.assertEqual(prompts[0].prompt_type, self.prompt_type)

    def test_update_prompt(self):
        """Aktualizácia promptu"""
        prompt = Prompt.objects.create(prompt_name='What is your favorite book?', prompt_type=self.prompt_type)
        prompt.prompt_name = 'What is your favorite movie?'
        prompt.save()
        self.assertEqual(prompt.prompt_name, 'What is your favorite movie?')

    def test_delete_prompt(self):
        """Odstránenie promptu"""
        prompt = Prompt.objects.create(prompt_name='What is your favorite book?', prompt_type=self.prompt_type)
        prompt.delete()
        self.assertEqual(Prompt.objects.count(), 0)


class MyPromptTypeCRUDTest(TestCase):
    """CRUD testy pre model MyPromptType"""

    def setUp(self):
        self.reader = Reader.objects.create(user_id=1)

    def test_create_myprompt_type(self):
        """Vytvorenie užívateľom definovaného typu promptu"""
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        self.assertEqual(myprompt_type.myprompt_type_name, 'User Defined Type')
        self.assertEqual(myprompt_type.reader, self.reader)

    def test_read_myprompt_type(self):
        """Čítanie užívateľom definovaného typu promptu"""
        MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        myprompt_types = MyPromptType.objects.all()
        self.assertEqual(myprompt_types.count(), 1)
        self.assertEqual(myprompt_types[0].myprompt_type_name, 'User Defined Type')
        self.assertEqual(myprompt_types[0].reader, self.reader)

    def test_update_myprompt_type(self):
        """Aktualizácia užívateľom definovaného typu promptu"""
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        myprompt_type.myprompt_type_name = 'Updated Type'
        myprompt_type.save()
        self.assertEqual(myprompt_type.myprompt_type_name, 'Updated Type')

    def test_delete_myprompt_type(self):
        """Odstránenie užívateľom definovaného typu promptu"""
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        myprompt_type.delete()
        self.assertEqual(MyPromptType.objects.count(), 0)


class MyPromptCRUDTest(TestCase):
    """CRUD testy pre model MyPrompt"""

    def setUp(self):
        self.reader = Reader.objects.create(user_id=1)
        self.myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )

    def test_create_myprompt(self):
        """Vytvorenie užívateľom definovaného promptu"""
        myprompt = MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        self.assertEqual(myprompt.prompt_name, 'User Defined Prompt')
        self.assertEqual(myprompt.prompt_type, self.myprompt_type)
        self.assertEqual(myprompt.reader, self.reader)

    def test_read_myprompt(self):
        """Čítanie užívateľom definovaného promptu"""
        MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        myprompts = MyPrompt.objects.all()
        self.assertEqual(myprompts.count(), 1)
        self.assertEqual(myprompts[0].prompt_name, 'User Defined Prompt')
        self.assertEqual(myprompts[0].prompt_type, self.myprompt_type)
        self.assertEqual(myprompts[0].reader, self.reader)

    def test_update_myprompt(self):
        """Aktualizácia užívateľom definovaného promptu"""
        myprompt = MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        myprompt.prompt_name = 'Updated Prompt'
        myprompt.save()
        self.assertEqual(myprompt.prompt_name, 'Updated Prompt')

    def test_delete_myprompt(self):
        """Odstránenie užívateľom definovaného promptu"""
        myprompt = MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        myprompt.delete()
        self.assertEqual(MyPrompt.objects.count(), 0)


""" LAST TESTED (30.06.2024.)"""
# RESULTS: Ran 32 tests in 0.047s
#OK
