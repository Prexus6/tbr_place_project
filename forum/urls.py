from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home_view, name='forum_home'),
    path('thread/<int:pk>/', views.thread_detail_view, name='thread_detail'),
    path('thread/new/', views.create_thread_view, name='create_thread'),
]
