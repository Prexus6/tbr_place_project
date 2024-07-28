from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .utils import search_books_by_title
from .views import generate_random_prompt, home_view, remove_from_favorites, add_my_prompt, book_details
from . import views, utils
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),

    # QUICK PROMT GENERATOR SSEKCIA
    path('generate-random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),

    # CUSTOM PROMPT SEKCIA
    path('generate-custom-prompt/', views.generate_custom_prompt, name='generate_custom_prompt'),
    path('add-my-prompt/', add_my_prompt, name='add_my_prompt'),
    path('edit_prompt/<int:prompt_id>/', views.edit_prompt, name='edit_prompt'),
    path('remove_prompt/<int:prompt_id>/', views.remove_prompt, name='remove_prompt'),

    #BOOK SEKCIA
    path('remove-from-favorites/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('add-book-to-favorites/<str:isbn>/', views.add_book_to_favorites, name='add_book_to_favorites'),
    # path('search-books-by-title/<str:title>/', utils.search_books_by_title, name='search_books_by_title'),
    # path('autocomplete-books/', utils.autocomplete_books, name='autocomplete_books'),
    path('search-books/', search_books_by_title, name='search_books_by_title'),
    path('get-book-details/<str:key>/', utils.get_book_details, name='get_book_details'),
    path('book-details/<str:isbn>/', book_details, name='book_details'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)