from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'contrasena', 'ciudad', 'fecha_nacimiento']

    def create(self, validated_data):
        password = validated_data.pop('contrasena')
        user = Usuario(**validated_data)
        user.contrasena = make_password(password)
        user.save()
        return user