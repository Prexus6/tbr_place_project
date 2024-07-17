from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import generate_random_prompt, search_books_view, home_view

urlpatterns = [
    path('add-book/', search_books_view, name='search_books_view'),
    path('', home_view, name='home'),
    path('random-prompt/', generate_random_prompt, name='generate_random_prompt'),
    path('search/', search_books_view, name='search_books'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)