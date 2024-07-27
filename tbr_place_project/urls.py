from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from tbr_place import utils, views
from tbr_place.views import add_my_prompt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', accounts_views.index_view, name='index'),
    path('search-books-bytitle/<title>/', utils.search_books_by_title),
    path('', views.home_view, name='home'),


    path('remove-from-favorites/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('generate-random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),
    path('generate-custom-prompt/', views.generate_custom_prompt, name='generate_custom_prompt'),
    path('add-my-prompt/', add_my_prompt, name='add_my_prompt'),
    path('search-books/', views.search_books_and_handle_favorites, name='search_books_view'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('search-books-bytitle/<title>/', utils.search_books_by_title),
]
