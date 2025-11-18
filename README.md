# Users Backend - Django REST API

> API REST para gestión de usuarios con Django y Django REST Framework

## Descripción

API REST desarrollada con Django y Django REST Framework que proporciona operaciones CRUD completas para la gestión de usuarios. Incluye validaciones robustas, integración con microservicio de notificaciones y soporte para PostgreSQL.

**Características principales:**
- API REST completa con operaciones CRUD
- Validaciones personalizadas de datos
- Integración con servicio de notificaciones
- Soporte para PostgreSQL y SQLite
- CORS configurado para frontend
- Búsqueda de usuarios
- Panel de administración de Django
- Dockerizado para producción

## Arquitectura

```
Frontend/API Gateway
        │
        ├─ GET /api/users/          → Listar todos los usuarios
        ├─ POST /api/users/         → Crear usuario + notificar
        ├─ GET /api/users/{id}/     → Obtener usuario específico
        ├─ PUT /api/users/{id}/     → Actualizar usuario
        ├─ DELETE /api/users/{id}/  → Eliminar usuario
        └─ GET /api/users/search/   → Buscar usuarios
                    │
                    ├─→ PostgreSQL (RDS)
                    └─→ Notification Service
```

## Estructura del Proyecto

```
users-backend/
├── users_project/              # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs del proyecto
│   └── wsgi.py                # Punto de entrada WSGI
├── users/                      # App de usuarios
│   ├── __init__.py
│   ├── admin.py               # Configuración del admin
│   ├── models.py              # Modelo de Usuario
│   ├── serializers.py         # Serializers para API
│   ├── views.py               # ViewSets y lógica
│   ├── urls.py                # URLs de la app
│   └── tests.py               # Tests unitarios
├── manage.py                   # Script de gestión de Django
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Configuración Docker
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
└── README.md                  # Este archivo
```

## Tecnologías

- **Django 4.2** - Framework web de alto nivel
- **Django REST Framework 3.14** - Toolkit para construir APIs REST
- **psycopg2-binary 2.9.9** - Adaptador PostgreSQL
- **django-cors-headers 4.3** - Manejo de CORS
- **python-dotenv 1.0** - Variables de entorno
- **requests 2.31** - Cliente HTTP para notificaciones

## Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15.4 (opcional, se puede usar SQLite para desarrollo)
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/NicoBonilla373/users-backend.git
cd users-backend
```

### 2. Crear entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

**Variables de entorno necesarias:**

```bash
# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos PostgreSQL (comentar para usar SQLite)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=users_db
DB_USER=postgres
DB_PASSWORD=tu_password

# Notification Service
NOTIFICATION_SERVICE_URL=http://localhost:5000

# CORS
CORS_ALLOW_ALL_ORIGINS=True
```

### 5. Ejecutar migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser

# Ingresa:
# - Username: admin
# - Email: admin@example.com
# - Password: (tu contraseña)
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000
```

## Docker

### Construir imagen

```bash
docker build -t users-backend:latest .
```

### Ejecutar contenedor (desarrollo)

```bash
docker run -d \
  --name users-backend \
  -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=5432 \
  -e DB_NAME=users_db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=password \
  -e NOTIFICATION_SERVICE_URL=http://host.docker.internal:5000 \
  users-backend:latest
```

### Construir y subir a ECR (producción)

```bash
# Login a ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Tag
docker tag users-backend:latest \
  [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/users-backend:latest

# Push
docker push [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/users-backend:latest
```

## Endpoints de la API

### Base URL (desarrollo)
```
http://localhost:8000/api/
```

### Endpoints disponibles

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/users/` | Listar todos los usuarios | No |
| `POST` | `/api/users/` | Crear un nuevo usuario | No |
| `GET` | `/api/users/{id}/` | Obtener usuario por ID | No |
| `PUT` | `/api/users/{id}/` | Actualizar usuario completo | No |
| `PATCH` | `/api/users/{id}/` | Actualizar parcialmente usuario | No |
| `DELETE` | `/api/users/{id}/` | Eliminar usuario | No |
| `GET` | `/api/users/search/?q=texto` | Buscar usuarios | No |
| `GET` | `/health/` | Health check | No |

## Ejemplos de Uso

### 1. Listar todos los usuarios

```bash
curl http://localhost:8000/api/users/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "099123456",
    "created_at": "2025-11-13T22:46:56.730635Z"
  }
]
```

### 2. Crear un usuario

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "email": "maria@example.com",
    "telefono": "098765432"
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "nombre": "María García",
  "email": "maria@example.com",
  "telefono": "098765432",
  "created_at": "2025-11-14T10:30:00.123456Z"
}
```

**Nota:** Al crear un usuario, automáticamente se envía una notificación por email mediante el Notification Service.

### 3. Obtener usuario específico

```bash
curl http://localhost:8000/api/users/1/
```

### 4. Actualizar usuario

```bash
curl -X PUT http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "email": "juan@example.com",
    "telefono": "099999999"
  }'
```

### 5. Eliminar usuario

```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

**Respuesta (204 No Content)**

### 6. Buscar usuarios

```bash
# Buscar por nombre o email
curl "http://localhost:8000/api/users/search/?q=juan"
```

### 7. Health Check

```bash
curl http://localhost:8000/health/
```

**Respuesta:**
```json
{
  "status": "ok",
  "service": "users-backend"
}
```

## Modelo de Datos

### Usuario

```python
class User(models.Model):
    nombre = models.CharField(max_length=120)        # Obligatorio
    email = models.EmailField(unique=True)           # Obligatorio, único
    telefono = models.CharField(max_length=30,       # Opcional
                               blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automático
```

### Validaciones

- **Nombre:** 
  - Obligatorio
  - Mínimo 2 caracteres
  - Se elimina whitespace al inicio y final

- **Email:**
  - Obligatorio
  - Formato válido de email
  - Único en el sistema
  - Se guarda en minúsculas

- **Teléfono:**
  - Opcional
  - Solo acepta números, espacios y guiones
  - Máximo 30 caracteres

## Pruebas

### Ejecutar tests

```bash
python manage.py test
```

### Ejecutar tests con cobertura

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Ejecutar análisis de seguridad

```bash
# SAST con Bandit
pip install bandit
bandit -r . -f txt -o bandit-report.txt

# SCA con Safety
pip install safety
safety check
```

## Seguridad

### Configuración de producción

En producción, asegúrate de:

1. **Cambiar SECRET_KEY:** Genera una clave segura
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Deshabilitar DEBUG:**
   ```python
   DEBUG = False
   ```

3. **Configurar ALLOWED_HOSTS:**
   ```python
   ALLOWED_HOSTS = ['tu-dominio.com', 'api.tu-dominio.com']
   ```

4. **Configurar CORS correctamente:**
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://tu-frontend.com",
   ]
   ```

5. **Usar PostgreSQL en lugar de SQLite**

6. **Configurar HTTPS**

### Secrets en Kubernetes

```bash
kubectl create secret generic db-credentials \
  --from-literal=DB_HOST=your-rds-endpoint \
  --from-literal=DB_PORT=5432 \
  --from-literal=DB_NAME=users_db \
  --from-literal=DB_USER=dbuser \
  --from-literal=DB_PASSWORD=secure-password \
  -n users-app
```

## Troubleshooting

### Error: "DisallowedHost"

**Solución:** Agregar el hostname a ALLOWED_HOSTS en settings.py
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tu-loadbalancer.amazonaws.com']
```

### Error: "No such table: users_user"

**Solución:** Ejecutar migraciones
```bash
python manage.py migrate
```

### Error: "Connection refused" (PostgreSQL)

**Solución:** Verificar que PostgreSQL esté corriendo y las credenciales sean correctas
```bash
psql -h localhost -U postgres -d users_db -c '\l'
```

### Error: "SMTP Authentication Failed"

**Solución:** Verificar que la URL del Notification Service sea correcta
```bash
curl http://localhost:5000/health
```

## Monitoreo

### Logs en desarrollo

```bash
# Los logs aparecen en la consola donde ejecutaste runserver
python manage.py runserver
```

### Logs en Kubernetes

```bash
# Ver logs en tiempo real
kubectl logs -f deployment/users-backend -n users-app

# Ver logs de un pod específico
kubectl logs users-backend-[pod-id] -n users-app

# Ver logs de notificaciones enviadas
kubectl logs -l app=users-backend -n users-app | grep "Notificación enviada"
```

## 🔗 Integración con otros servicios

### Notification Service

El backend se comunica con el Notification Service al crear usuarios:

```python
# En views.py
def send_notification(self, user_data):
    notification_url = f"{settings.NOTIFICATION_SERVICE_URL}/notify"
    response = requests.post(notification_url, json=user_data, timeout=5)
```

URL del servicio se configura con:
```bash
NOTIFICATION_SERVICE_URL=http://notification-service:5000
```


## Autor

**Nicolás Bonilla** - [NicoBonilla373](https://github.com/NicoBonilla373)

## Enlaces

- [Repositorio Principal](https://github.com/NicoBonilla373/infraestructura)
- [Frontend](https://github.com/NicoBonilla373/users-frontend)
- [Notification Service](https://github.com/NicoBonilla373/notification-service)
- [Manifiestos K8s](https://github.com/NicoBonilla373/k8s-manifiests)

---

⭐ Si te ha sido útil, considera darle una estrella al repositorio
