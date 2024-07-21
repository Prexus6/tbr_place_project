from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from tbr_place.models import PromptType, Prompt, Reader, MyPromptType, MyPrompt, Author, Genre, Book

class MyPromptTypeModelTest(TestCase):

    def setUp(self):
        self.reader = Reader.objects.create(user_id=1)

    def test_create_myprompt_type(self):
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        self.assertEqual(myprompt_type.myprompt_type_name, 'User Defined Type')
        self.assertEqual(myprompt_type.reader, self.reader)

    def test_myprompt_type_str(self):
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='Custom Type',
            reader=self.reader
        )
        self.assertEqual(str(myprompt_type), 'Custom Type')

    def test_create_duplicate_myprompt_type_name(self):
        MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        with self.assertRaises(IntegrityError):
            MyPromptType.objects.create(
                myprompt_type_name='User Defined Type',
                reader=self.reader
            )

class PromptTypeModelTest(TestCase):
    def setUp(self):
        self.prompt_type_name = "Fiction"
        self.prompt_type = PromptType.objects.create(prompt_type_name=self.prompt_type_name)

    def test_prompt_type_creation(self):
        self.assertEqual(self.prompt_type.prompt_type_name, self.prompt_type_name)
        self.assertIsInstance(self.prompt_type, PromptType)

    def test_prompt_type_name_max_length(self):
        prompt_type = PromptType.objects.create(prompt_type_name='a' * 250)
        max_length = prompt_type._meta.get_field('prompt_type_name').max_length
        self.assertEqual(max_length, 250)

    def test_create_prompt_type_with_empty_name(self):
        with self.assertRaises(ValidationError):
            prompt_type = PromptType(prompt_type_name='')
            prompt_type.full_clean()  # volá clean metodu

    def test_create_prompt_type_with_long_name(self):
        long_name = 'a' * 251
        with self.assertRaises(ValidationError):
            prompt_type = PromptType(prompt_type_name=long_name)
            prompt_type.full_clean()  # volá clean metodu

class PromptModelTest(TestCase):
    def setUp(self):
        self.prompt_type = PromptType.objects.create(prompt_type_name='Example Type')

    def test_create_prompt(self):
        prompt = Prompt.objects.create(prompt_name='Example Prompt', prompt_type=self.prompt_type)
        self.assertIsNotNone(prompt.id)
        self.assertEqual(prompt.prompt_name, 'Example Prompt')
        self.assertEqual(prompt.prompt_type, self.prompt_type)

    def test_prompt_str(self):
        prompt = Prompt.objects.create(prompt_name='Example Prompt', prompt_type=self.prompt_type)
        self.assertEqual(str(prompt), 'Example Prompt')

    def test_prompt_without_name(self):
        prompt = Prompt(prompt_name='', prompt_type=self.prompt_type)
        with self.assertRaises(ValidationError):
            prompt.full_clean()  # volá clean metodu

    def test_prompt_without_type(self):
        prompt = Prompt(prompt_name='Example Prompt', prompt_type=None)
        with self.assertRaises(ValidationError):
            prompt.full_clean()  # volá clean metodu

class AuthorModelTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(author_name='John Doe')
        self.assertEqual(author.author_name, 'John Doe')

    def test_author_str(self):
        author = Author.objects.create(author_name='Jane Smith')
        self.assertEqual(str(author), 'Jane Smith')

    def test_create_duplicate_author_name(self):
        Author.objects.create(author_name='John Doe')
        with self.assertRaises(IntegrityError):
            Author.objects.create(author_name='John Doe')

class GenreModelTest(TestCase):
    def test_create_genre(self):
        genre = Genre.objects.create(genre_name='Fantasy')
        self.assertEqual(genre.genre_name, 'Fantasy')

    def test_genre_str(self):
        genre = Genre.objects.create(genre_name='Science Fiction')
        self.assertEqual(str(genre), 'Science Fiction')

    def test_create_duplicate_genre_name(self):
        Genre.objects.create(genre_name='Fantasy')
        with self.assertRaises(IntegrityError):
            Genre.objects.create(genre_name='Fantasy')

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(author_name='John Doe')
        self.genre = Genre.objects.create(genre_name='Fantasy')

    def test_create_book(self):
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

    def test_book_str(self):
        book = Book.objects.create(
            book_title='Another Book',
            book_author=self.author,
            book_rating=7.8,
            isbn='9789876543210'
        )
        self.assertEqual(str(book), 'Another Book')

    def test_create_duplicate_isbn(self):
        Book.objects.create(
            book_title='Sample Book',
            book_author=self.author,
            book_rating=8.5,
            isbn='9780123456789'
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                book_title='Another Book',
                book_author=self.author,
                book_rating=7.8,
                isbn='9780123456789'
            )

class ReaderModelTest(TestCase):
    def test_create_reader(self):
        reader = Reader.objects.create(user_id=1)
        self.assertEqual(reader.user_id, 1)

    def test_reader_str(self):
        reader = Reader.objects.create(user_id=2)
        self.assertEqual(str(reader), 'Čitateľ 2')

    def test_create_duplicate_user_id(self):
        Reader.objects.create(user_id=1)
        with self.assertRaises(IntegrityError):
            Reader.objects.create(user_id=1)

class MyPromptModelTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(user_id=1)
        self.myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )

    def test_create_myprompt(self):
        myprompt = MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        self.assertEqual(myprompt.prompt_name, 'User Defined Prompt')
        self.assertEqual(myprompt.prompt_type, self.myprompt_type)
        self.assertEqual(myprompt.reader, self.reader)

    def test_myprompt_str(self):
        myprompt = MyPrompt.objects.create(
            prompt_name='Another Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        self.assertEqual(str(myprompt), 'Another Prompt')
