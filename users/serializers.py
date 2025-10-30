from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'email', 'telefono', 'created_at']
        read_only_fields = ['id', 'created_at']

    # Validar que el email no esté repetido
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

    # Validar formato del teléfono (solo números)
    def validate_telefono(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("El teléfono solo debe contener números.")
        return value
