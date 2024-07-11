# tbr_place_project_ondra/urls.py
from django.contrib import admin
from django.urls import path
from tbr_place.views import CustomLoginView, index
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('', index, name='index'),
]
