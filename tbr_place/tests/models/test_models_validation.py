from django.test import TestCase
from tbr_place.models import PromptType, Prompt, Reader, MyPromptType, MyPrompt, Author, Genre, Book
from django.db import IntegrityError


# TODO - optimalizovať kód po posledných výsledkoch testov

"""Overovacie testy pre model PromptType."""


class PromptTypeModelTest(TestCase):
    """
    Testy pre model PromptType.
    """

    def setUp(self):
        """
        Nastavenie testovacích údajov.
        """
        self.prompt_type_name = "Fiction"
        self.prompt_type = PromptType.objects.create(prompt_type_name=self.prompt_type_name)

    def test_prompt_type_creation(self):
        """
        Test vytvorenia inštancie PromptType.
        """
        self.assertEqual(self.prompt_type.prompt_type_name, self.prompt_type_name)
        self.assertIsInstance(self.prompt_type, PromptType)

    def test_prompt_type_name_max_length(self):
        """
        Test obmedzenia maximálnej dĺžky pre pole prompt_type_name.
        """
        prompt_type = PromptType.objects.create(prompt_type_name='a' * 250)
        max_length = prompt_type._meta.get_field('prompt_type_name').max_length
        self.assertEqual(max_length, 250)

    def test_create_prompt_type_with_empty_name(self):
        """
        Test vytvorenia PromptType s prázdny názvom vyvolá ValueError.
        """
        with self.assertRaises(ValueError):
            PromptType.objects.create(prompt_type_name='')

    def test_create_prompt_type_with_long_name(self):
        """
        Test vytvorenia PromptType s príliš dlhým názvom vyvolá ValueError.
        """
        long_name = 'a' * 251
        with self.assertRaises(ValueError):
            PromptType.objects.create(prompt_type_name=long_name)


"""Overovacie testy pre model Prompt."""


class PromptModelTest(TestCase):
    """
    Testy pre model Prompt.
    """

    def setUp(self):
        """
        Nastavenie testovacích údajov.
        """
        self.prompt_type = PromptType.objects.create(prompt_type_name='Example Type')

    def test_create_prompt(self):
        """
        Test vytvorenia inštancie Prompt.
        """
        prompt = Prompt.objects.create(prompt_name='Example Prompt', prompt_type=self.prompt_type)
        self.assertIsNotNone(prompt.id)
        self.assertEqual(prompt.prompt_name, 'Example Prompt')
        self.assertEqual(prompt.prompt_type, self.prompt_type)

    def test_prompt_str(self):
        """
        Test reprezentácie reťazcom inštancie Prompt.
        """
        prompt = Prompt.objects.create(prompt_name='Example Prompt', prompt_type=self.prompt_type)
        self.assertEqual(str(prompt), 'Example Prompt')

    def test_prompt_without_name(self):
        """
        Test vytvorenia Prompt bez mena vyvolá ValueError.
        """
        with self.assertRaises(ValueError):
            Prompt.objects.create(prompt_name='', prompt_type=self.prompt_type)

    def test_prompt_without_type(self):
        """
        Test vytvorenia Prompt bez typu vyvolá ValueError.
        """
        with self.assertRaises(ValueError):
            Prompt.objects.create(prompt_name='Example Prompt', prompt_type=None)


"""Overovacie testy pre model Author."""


class AuthorModelTest(TestCase):
    """
    Testy pre model Author.
    """

    def test_create_author(self):
        """
        Test vytvorenia inštancie Author.
        """
        author = Author.objects.create(author_name='John Doe')
        self.assertEqual(author.author_name, 'John Doe')

    def test_author_str(self):
        """
        Test reprezentácie reťazcom inštancie Author.
        """
        author = Author.objects.create(author_name='Jane Smith')
        self.assertEqual(str(author), 'Jane Smith')

    def test_create_duplicate_author_name(self):
        """
        Test vytvorenia Author s duplicitným menom vyvolá IntegrityError.
        """
        Author.objects.create(author_name='John Doe')
        with self.assertRaises(IntegrityError):
            Author.objects.create(author_name='John Doe')


"""Overovacie testy pre model Genre."""


class GenreModelTest(TestCase):
    """
    Testy pre model Genre.
    """

    def test_create_genre(self):
        """
        Test vytvorenia inštancie Genre.
        """
        genre = Genre.objects.create(genre_name='Fantasy')
        self.assertEqual(genre.genre_name, 'Fantasy')

    def test_genre_str(self):
        """
        Test reprezentácie reťazcom inštancie Genre.
        """
        genre = Genre.objects.create(genre_name='Science Fiction')
        self.assertEqual(str(genre), 'Science Fiction')

    def test_create_duplicate_genre_name(self):
        """
        Test vytvorenia Genre s duplicitným názvom vyvolá IntegrityError.
        """
        Genre.objects.create(genre_name='Fantasy')
        with self.assertRaises(IntegrityError):
            Genre.objects.create(genre_name='Fantasy')


"""Overovacie testy pre model Book."""


class BookModelTest(TestCase):
    """
    Testy pre model Book.
    """

    def setUp(self):
        """
        Nastavenie testovacích údajov.
        """
        self.author = Author.objects.create(author_name='John Doe')
        self.genre = Genre.objects.create(genre_name='Fantasy')

    def test_create_book(self):
        """
        Test vytvorenia inštancie Book.
        """
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
        """
        Test reprezentácie reťazcom inštancie Book.
        """
        book = Book.objects.create(
            book_title='Another Book',
            book_author=self.author,
            book_rating=7.8,
            isbn='9789876543210'
        )
        self.assertEqual(str(book), 'Another Book')

    def test_create_duplicate_isbn(self):
        """
        Test vytvorenia Book s duplicitným ISBN vyvolá IntegrityError.
        """
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


"""Overovacie testy pre model Reader."""


class ReaderModelTest(TestCase):
    """
    Testy pre model Reader.
    """

    def test_create_reader(self):
        """
        Test vytvorenia inštancie Reader.
        """
        reader = Reader.objects.create(user_id=1)
        self.assertEqual(reader.user_id, 1)

    def test_reader_str(self):
        """
        Test reprezentácie reťazcom inštancie Reader.
        """
        reader = Reader.objects.create(user_id=2)
        self.assertEqual(str(reader), 'Čitateľ 2')

    def test_create_duplicate_user_id(self):
        """
        Test vytvorenia Reader s duplicitným user ID vyvolá IntegrityError.
        """
        Reader.objects.create(user_id=1)
        with self.assertRaises(IntegrityError):
            Reader.objects.create(user_id=1)


"""Overovacie testy pre model MyPromptType."""


class MyPromptTypeModelTest(TestCase):
    """
    Testy pre model MyPromptType.
    """

    def setUp(self):
        """
        Nastavenie testovacích údajov.
        """
        self.reader = Reader.objects.create(user_id=1)

    def test_create_myprompt_type(self):
        """
        Test vytvorenia inštancie MyPromptType.
        """
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        self.assertEqual(myprompt_type.myprompt_type_name, 'User Defined Type')
        self.assertEqual(myprompt_type.reader, self.reader)

    def test_myprompt_type_str(self):
        """
        Test reprezentácie reťazcom inštancie MyPromptType.
        """
        myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='Custom Type',
            reader=self.reader
        )
        self.assertEqual(str(myprompt_type), 'Custom Type')

    def test_create_duplicate_myprompt_type_name(self):
        """
        Test vytvorenia MyPromptType s duplicitným názvom vyvolá IntegrityError.
        """
        MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )
        with self.assertRaises(IntegrityError):
            MyPromptType.objects.create(
                myprompt_type_name='User Defined Type',
                reader=self.reader
            )


"""Overovacie testy pre model MyPrompt."""


class MyPromptModelTest(TestCase):
    """
    Testy pre model MyPrompt.
    """

    def setUp(self):
        """
        Nastavenie testovacích údajov.
        """
        self.reader = Reader.objects.create(user_id=1)
        self.myprompt_type = MyPromptType.objects.create(
            myprompt_type_name='User Defined Type',
            reader=self.reader
        )

    def test_create_myprompt(self):
        """
        Test vytvorenia inštancie MyPrompt.
        """
        myprompt = MyPrompt.objects.create(
            prompt_name='User Defined Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        self.assertEqual(myprompt.prompt_name, 'User Defined Prompt')
        self.assertEqual(myprompt.prompt_type, self.myprompt_type)
        self.assertEqual(myprompt.reader, self.reader)

    def test_myprompt_str(self):
        """
        Test reprezentácie reťazcom inštancie MyPrompt.
        """
        myprompt = MyPrompt.objects.create(
            prompt_name='Another Prompt',
            prompt_type=self.myprompt_type,
            reader=self.reader
        )
        self.assertEqual(str(myprompt), 'Another Prompt')


""" LAST TESTED (30.06.2024.)"""
# RESULTS: Ran 25 tests in 0.030s
#
# FAILED (failures=4, errors=1)
# Destroying test database for alias 'default'...