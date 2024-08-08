from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from forum.models import Category, Thread, Post

class ForumViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name="Test Category")
        self.thread = Thread.objects.create(title="Test Thread", content="Test content", author=self.user, category=self.category)

    def test_forum_home_view(self):
        response = self.client.get(reverse('forum_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_home.html')

    def test_thread_detail_view(self):
        response = self.client.get(reverse('thread_detail', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thread_detail.html')

    def test_create_thread_view(self):
        response = self.client.get(reverse('create_thread'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_thread.html')

    def test_edit_thread_view(self):
        response = self.client.get(reverse('edit_thread', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_thread.html')

    def test_delete_thread_view(self):
        response = self.client.get(reverse('delete_thread', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_thread.html')
