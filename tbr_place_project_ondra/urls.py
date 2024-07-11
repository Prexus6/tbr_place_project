from django.contrib import admin
from django.urls import path
from tbr_place import views  # Import views z tbr_place

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Nastavení základní cesty pro domovskou stránku
    path('random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),
    path('index.html', views.index, name='index_html'),  # Přidání konkrétní cesty pro index.html
]
