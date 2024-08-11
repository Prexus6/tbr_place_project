from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .utils import search_books_by_title
from .views import generate_random_prompt, home_view,  add_my_prompt, random_quote
from . import views, utils
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),

    # QUICK PROMT GENERATOR SSEKCIA
    path('generate-random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),
    path( 'generate_filtered_prompt/', views.generate_filtered_prompt, name='generate_filtered_prompt'),


    # CUSTOM PROMPT SEKCIA
    path('generate-custom-prompt/', views.generate_custom_prompt, name='generate_custom_prompt'),
    path('add-my-prompt/', add_my_prompt, name='add_my_prompt'),
    path('edit_prompt/<int:prompt_id>/', views.edit_prompt, name='edit_prompt'),
    path('remove_prompt/<int:prompt_id>/', views.remove_prompt, name='remove_prompt'),

    #BOOK SEKCIA
    path('search-books/', search_books_by_title, name='search_books_by_title'),
    path('random-quote/', random_quote, name='random_quote'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)