from django.urls import reverse, resolve
from forum.views import forum_home, thread_detail_view, create_thread_view, edit_thread_view, delete_thread_view, edit_post_view, delete_post_view

def test_forum_home_url():
    path = reverse('forum_home')
    assert resolve(path).func == forum_home

def test_thread_detail_url():
    path = reverse('thread_detail', kwargs={'pk': 1})
    assert resolve(path).func == thread_detail_view

def test_create_thread_url():
    path = reverse('create_thread')
    assert resolve(path).func == create_thread_view

def test_edit_thread_url():
    path = reverse('edit_thread', kwargs={'pk': 1})
    assert resolve(path).func == edit_thread_view

def test_delete_thread_url():
    path = reverse('delete_thread', kwargs={'pk': 1})
    assert resolve(path).func == delete_thread_view

def test_edit_post_url():
    path = reverse('edit_post', kwargs={'pk': 1})
    assert resolve(path).func == edit_post_view

def test_delete_post_url():
    path = reverse('delete_post', kwargs={'pk': 1})
    assert resolve(path).func == delete_post_view
