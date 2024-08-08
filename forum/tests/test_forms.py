from django.test import TestCase
from forum.forms import ThreadForm, PostForm
from forum.models import Category
from django.contrib.auth import get_user_model

class ThreadFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Test Category")

    def test_valid_thread_form(self):
        form_data = {
            'title': 'Test Thread',
            'content': 'Test content',
            'author': self.user.pk,
            'category': self.category.pk
        }
        form = ThreadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_thread_form(self):
        form_data = {
            'title': '',
            'content': 'Test content',
            'author': self.user.pk,
            'category': self.category.pk
        }
        form = ThreadForm(data=form_data)
        self.assertFalse(form.is_valid())

class PostFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_valid_post_form(self):
        form_data = {
            'content': 'Test Post',
            'author': self.user.pk
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form_data = {
            'content': '',
            'author': self.user.pk
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
