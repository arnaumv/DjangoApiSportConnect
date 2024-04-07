from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, EventsJoined


## SERIALIZER PARA USUARIO
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'birthdate', 'description'] 
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hashear la contraseña antes de guardar el usuario
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
    


# SERIALIZER PARA EVENTO
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

## SERIALIZER PARA UNIRSE A UN EVENTO
class EventsJoinedSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsJoined
        fields = '__all__'  # Esto incluirá todos los campos de tu modelo en la serialización