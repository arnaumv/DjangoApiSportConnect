from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Tus otras importaciones de vistas

urlpatterns = [
]

# Servir archivos estáticos y multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
