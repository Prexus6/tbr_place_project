from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
gs.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# komentář haha