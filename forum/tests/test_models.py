from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import Category, Thread, Post

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")

class ThreadModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Test Category")
        self.thread = Thread.objects.create(title="Test Thread", content="Test content", author=self.user, category=self.category)

    def test_thread_creation(self):
        self.assertEqual(self.thread.title, "Test Thread")
        self.assertEqual(self.thread.content, "Test content")
        self.assertEqual(self.thread.author.username, "testuser")
        self.assertEqual(self.thread.category.name, "Test Category")

class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Test Category")
        self.thread = Thread.objects.create(title="Test Thread", content="Test content", author=self.user, category=self.category)
        self.post = Post.objects.create(content="Test Post", author=self.user, thread=self.thread)

    def test_post_creation(self):
        self.assertEqual(self.post.content, "Test Post")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.thread.title, "Test Thread")
