from django.db import models

class User(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True) #email con unique=True evita duplicados
    telefono = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
