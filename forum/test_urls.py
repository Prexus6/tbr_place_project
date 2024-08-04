from django.urls import reverse, resolve
from forum.views import (
    forum_home_view,
    category_detail_view,
    subcategory_detail_view,
    thread_detail_view,
    create_thread_view,
    edit_post_view,
    delete_post_view,
    vote_post_view,
    report_post_view,
    search_results_view,
)

def test_forum_home_url_is_resolved():
    url = reverse('forum_home')
    assert resolve(url).func == forum_home_view

def test_category_detail_url_is_resolved():
    url = reverse('category_detail', args=[1])
    assert resolve(url).func == category_detail_view

def test_subcategory_detail_url_is_resolved():
    url = reverse('subcategory_detail', args=[1])
    assert resolve(url).func == subcategory_detail_view

def test_thread_detail_url_is_resolved():
    url = reverse('thread_detail', args=[1])
    assert resolve(url).func == thread_detail_view

def test_create_thread_url_is_resolved():
    url = reverse('create_thread')
    assert resolve(url).func == create_thread_view

def test_edit_post_url_is_resolved():
    url = reverse('edit_post', args=[1])
    assert resolve(url).func == edit_post_view

def test_delete_post_url_is_resolved():
    url = reverse('delete_post', args=[1])
    assert resolve(url).func == delete_post_view

def test_vote_post_url_is_resolved():
    url = reverse('vote_post', args=[1, 'up'])
    assert resolve(url).func == vote_post_view

def test_report_post_url_is_resolved():
    url = reverse('report_post', args=[1])
    assert resolve(url).func == report_post_view

def test_search_results_url_is_resolved():
    url = reverse('search_results')
    assert resolve(url).func == search_results_view
