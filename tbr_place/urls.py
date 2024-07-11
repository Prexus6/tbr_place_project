from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Přidá cestu pro hlavní stránku
    path('random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),
    # Další cesty...
]
