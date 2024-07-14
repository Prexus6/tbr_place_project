from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import generate_random_prompt, add_book_view

urlpatterns = [
    path('random-prompt/', generate_random_prompt, name='generate_random_prompt'),
    path('add-book/', add_book_view, name='add_book'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)