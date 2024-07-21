from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import generate_random_prompt, home_view, add_to_favorites, remove_from_favorites
from . import views
from django.urls import path


urlpatterns = [
    path('', home_view, name='home'),
    path('add_to_favorites/<int:book_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:book_id>/', remove_from_favorites, name='remove_from_favorites'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)