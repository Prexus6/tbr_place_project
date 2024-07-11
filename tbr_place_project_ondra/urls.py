from django.contrib import admin
from django.urls import path, include
from tbr_place import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),  # Pokud máte vlastní registraci
    # nebo pokud používáte django-allauth
    path('accounts/', include('allauth.urls')),
]
