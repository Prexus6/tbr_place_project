from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Thread, Post, Category

User = get_user_model()

class ForumTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a category
        self.category = Category.objects.create(name='TestCategory', description='TestDescription')
        # Create a thread
        self.thread = Thread.objects.create(title='TestThread', content='TestContent', author=self.user, category=self.category)
        # Create a post
        self.post = Post.objects.create(content='TestPostContent', author=self.user, thread=self.thread)
        # Client for testing views
        self.client = Client()

    def test_forum_home_view(self):
        response = self.client.get(reverse('forum_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_home.html')

    def test_thread_detail_view(self):
        response = self.client.get(reverse('thread_detail', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/thread_detail.html')

    def test_create_thread_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create_thread'), {'title': 'NewThread', 'content': 'NewContent', 'category': self.category.pk})
        self.assertEqual(response.status_code, 302)  # Should redirect after creation

    def test_edit_thread_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_thread', args=[self.thread.pk]), {'title': 'UpdatedThread', 'content': 'UpdatedContent', 'category': self.category.pk})
        self.assertEqual(response.status_code, 302)  # Should redirect after editing
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'UpdatedThread')

    def test_delete_thread_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_thread', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertFalse(Thread.objects.filter(pk=self.thread.pk).exists())

    def test_edit_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_post', args=[self.post.pk]), {'content': 'UpdatedPostContent'})
        self.assertEqual(response.status_code, 302)  # Should redirect after editing
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'UpdatedPostContent')

    def test_delete_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
