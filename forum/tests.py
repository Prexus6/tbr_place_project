from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Thread, Post, Category

# Získání vlastního uživatelského modelu
User = get_user_model()

class ForumTestCase(TestCase):
    """
    Testovací případ pro aplikaci fóra.
    """

    def setUp(self):
        """
        Nastavení testovacího prostředí před každým testem.
        Vytvoří uživatele, kategorii, vlákno a příspěvek.
        """
        # Vytvoření testovacího uživatele
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Vytvoření testovací kategorie
        self.category = Category.objects.create(name='TestCategory', description='TestDescription')
        # Vytvoření testovacího vlákna
        self.thread = Thread.objects.create(title='TestThread', content='TestContent', author=self.user, category=self.category)
        # Vytvoření testovacího příspěvku
        self.post = Post.objects.create(content='TestPostContent', author=self.user, thread=self.thread)
        # Klient pro testování views
        self.client = Client()

    def test_forum_home_view(self):
        """
        Testuje view pro hlavní stránku fóra.
        Kontroluje, že stavová odpověď je 200 a že je použit správný šablonový soubor.
        """
        response = self.client.get(reverse('forum_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_home.html')

    def test_thread_detail_view(self):
        """
        Testuje view pro detail vlákna.
        Kontroluje, že stavová odpověď je 200 a že je použit správný šablonový soubor.
        """
        response = self.client.get(reverse('thread_detail', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/thread_detail.html')

    def test_create_thread_view(self):
        """
        Testuje view pro vytvoření vlákna.
        Kontroluje, že uživatel může vytvořit nové vlákno a že je přesměrován po vytvoření.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create_thread'), {'title': 'NewThread', 'content': 'NewContent', 'category': self.category.pk})
        self.assertEqual(response.status_code, 302)  # Měl by přesměrovat po vytvoření

    def test_edit_thread_view(self):
        """
        Testuje view pro úpravu vlákna.
        Kontroluje, že uživatel může upravit existující vlákno a že je přesměrován po úpravě.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_thread', args=[self.thread.pk]), {'title': 'UpdatedThread', 'content': 'UpdatedContent', 'category': self.category.pk})
        self.assertEqual(response.status_code, 302)  # Měl by přesměrovat po úpravě
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'UpdatedThread')

    def test_delete_thread_view(self):
        """
        Testuje view pro smazání vlákna.
        Kontroluje, že uživatel může smazat existující vlákno a že je přesměrován po smazání.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_thread', args=[self.thread.pk]))
        self.assertEqual(response.status_code, 302)  # Měl by přesměrovat po smazání
        self.assertFalse(Thread.objects.filter(pk=self.thread.pk).exists())

    def test_edit_post_view(self):
        """
        Testuje view pro úpravu příspěvku.
        Kontroluje, že uživatel může upravit existující příspěvek a že je přesměrován po úpravě.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_post', args=[self.post.pk]), {'content': 'UpdatedPostContent'})
        self.assertEqual(response.status_code, 302)  # Měl by přesměrovat po úpravě
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'UpdatedPostContent')

    def test_delete_post_view(self):
        """
        Testuje view pro smazání příspěvku.
        Kontroluje, že uživatel může smazat existující příspěvek a že je přesměrován po smazání.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Měl by přesměrovat po smazání
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
