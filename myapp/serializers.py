from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'birthdate']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hashear la contraseña antes de guardar el usuario
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)