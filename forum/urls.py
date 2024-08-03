from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home_view, name='forum_home'),
    path('category/<int:pk>/', views.category_detail_view, name='category_detail'),
    path('subcategory/<int:pk>/', views.subcategory_detail_view, name='subcategory_detail'),
    path('thread/<int:pk>/', views.thread_detail_view, name='thread_detail'),
    path('create_thread/', views.create_thread_view, name='create_thread'),
    path('edit_post/<int:pk>/', views.edit_post_view, name='edit_post'),
    path('delete_post/<int:pk>/', views.delete_post_view, name='delete_post'),
    path('vote_post/<int:pk>/<str:vote_type>/', views.vote_post_view, name='vote_post'),
    path('report_post/<int:pk>/', views.report_post_view, name='report_post'),
    path('search/', views.search_results_view, name='search_results'),
]
