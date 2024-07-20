from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.generate_random_prompt, name='index'),  # Ukazuje na váš view pro generování promptu
    path('accounts/', include('accounts.urls')),
]
