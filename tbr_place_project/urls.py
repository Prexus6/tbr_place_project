from django.contrib import admin
from django.urls import path
from tbr_place import views  # Předpokládám, že views jsou ve složce tbr_place

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Nastavíme základní cestu pro domovskou stránku
    path('random-prompt/', views.generate_random_prompt, name='generate_random_prompt'),
]

