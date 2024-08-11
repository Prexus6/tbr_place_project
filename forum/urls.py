from django.urls import path
from .views import forum_home, thread_detail_view, create_thread_view, edit_thread_view, delete_thread_view, edit_post_view, delete_post_view

# URL patterns pro aplikaci fóra
urlpatterns = [
    path('', forum_home, name='forum_home'),  # URL pro hlavní stránku fóra
    path('thread/<int:pk>/', thread_detail_view, name='thread_detail'),  # URL pro detail vlákna
    path('thread/create/', create_thread_view, name='create_thread'),  # URL pro vytvoření vlákna
    path('thread/<int:pk>/edit/', edit_thread_view, name='edit_thread'),  # URL pro editaci vlákna
    path('thread/<int:pk>/delete/', delete_thread_view, name='delete_thread'),  # URL pro smazání vlákna
    path('post/<int:pk>/edit/', edit_post_view, name='edit_post'),  # URL pro editaci příspěvku
    path('post/<int:pk>/delete/', delete_post_view, name='delete_post'),  # URL pro smazání příspěvku
]
