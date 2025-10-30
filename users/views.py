# users/views.py
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import requests
import logging
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)  # usamos el logger configurado en settings.py

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # 1️⃣ Guardar el usuario
        user = serializer.save()

        # 2️⃣ Intentar notificar al microservicio (si está definido)
        notif_url = getattr(settings, 'NOTIFICATION_SERVICE_URL', None)
        if notif_url:
            try:
                payload = {
                    'nombre': user.nombre,
                    'email': user.email,
                    'telefono': user.telefono,
                    'created_at': user.created_at.isoformat()
                }
                requests.post(f"{notif_url}/notify", json=payload, timeout=3)
                logger.info(f"✅ Notificación enviada a {notif_url}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo notificar al servicio de notificaciones: {e}")

        # 3️⃣ Intentar enviar correo de notificación
        try:
            subject = f"Nuevo usuario registrado: {user.nombre}"
            message = f"Se registró el usuario {user.nombre} ({user.email})"
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
                logger.info(f"📧 Correo enviado a {admin_email}")
            else:
                logger.warning("⚠️ ADMIN_EMAIL no configurado en settings.py")
        except Exception as e:
            logger.error(f"❌ Error al enviar correo: {e}")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Guardar el usuario
        user = serializer.save()

        # Notificar al microservicio de notificaciones (si está activo)
        notif_url = getattr(settings, 'NOTIFICATION_SERVICE_URL', None)
        if notif_url:
            try:
                payload = {
                    'nombre': user.nombre,
                    'email': user.email,
                    'telefono': user.telefono,
                    'created_at': user.created_at.isoformat(),
                }
                requests.post(f"{notif_url}/notify", json=payload, timeout=3)
                logger.info(f"✅ Notificación enviada a {notif_url}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo notificar al servicio de notificaciones: {e}")

        # Envío del correo al administrador
        try:
            subject = f"Nuevo usuario registrado: {user.nombre}"
            message = f"Se registró el usuario {user.nombre} ({user.email})"
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
                logger.info(f"📧 Correo enviado a {admin_email}")
            else:
                logger.warning("⚠️ ADMIN_EMAIL no configurado en settings.py")
        except Exception as e:
            logger.error(f"❌ Error al enviar correo: {e}")
