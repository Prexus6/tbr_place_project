from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .utils import search_books_by_title
from .views import generate_random_prompt, home_view, remove_from_favorites, add_my_prompt,  \
    add_to_my_books, get_my_books, random_quote, goal_list, update_goal
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
    # path('add-to-my-books/', views.add_to_my_books, name='add_to_my_books'),
    # path('search-books-by-title/<str:title>/', utils.search_books_by_title, name='search_books_by_title'),
    # path('autocomplete-books/', utils.autocomplete_books, name='autocomplete_books'),
    path('search-books/', search_books_by_title, name='search_books_by_title'),
    path('add-to-my-books/', add_to_my_books, name='add_to_my_books'),
    path('my-books/', get_my_books, name='get_my_books'),

    path('random-quote/', random_quote, name='random_quote'),
    path('goals/', goal_list, name='goal_list'),
    path('update-goal/<int:id>/', update_goal, name='update_goal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)