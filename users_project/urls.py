# users_project/urls.py
from django.contrib import admin
from django.urls import path, include   # <- IMPORTANTE incluir include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),   # <- ESTA LÍNEA AGREGA TUS RUTAS
]
