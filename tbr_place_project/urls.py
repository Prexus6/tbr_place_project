from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Hlavní stránka projektu
    path('index.html', views.index, name='index_html'),  # Pokud máš specifický soubor index.html
]

