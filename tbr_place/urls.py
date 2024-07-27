from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import generate_random_prompt, home_view, add_to_favorites, remove_from_favorites, add_my_prompt
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
    path('add-to-favorites/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('search-books/', views.search_books_and_handle_favorites, name='search_books_view'),
    path('remove-from-favorites/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search-books-bytitle/<title>/', utils.search_books_by_title),



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)