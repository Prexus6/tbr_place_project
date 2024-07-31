from django.conf.urls.static import static
from django.urls import path

from tbr_place_project import settings
from . import views

urlpatterns = [
    path('literary_work/create/', views.literary_work_create, name='literary_work_create'),
    path('literary_work/<int:pk>/edit/', views.literary_work_edit, name='literary_work_edit'),
    path('literary_work/<int:pk>/', views.literary_work_detail, name='literary_work_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('literary_works/', views.literary_work_list, name='literary_work_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
