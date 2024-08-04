from django.urls import path
from .views import forum_home, thread_detail_view, create_thread_view, edit_thread_view, delete_thread_view, edit_post_view, delete_post_view

urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('thread/<int:pk>/', thread_detail_view, name='thread_detail'),
    path('thread/create/', create_thread_view, name='create_thread'),
    path('thread/<int:pk>/edit/', edit_thread_view, name='edit_thread'),
    path('thread/<int:pk>/delete/', delete_thread_view, name='delete_thread'),
    path('post/<int:pk>/edit/', edit_post_view, name='edit_post'),
    path('post/<int:pk>/delete/', delete_post_view, name='delete_post'),
]
