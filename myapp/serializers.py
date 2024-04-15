from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, EventsJoined


## SERIALIZER PARA USUARIO
from rest_framework import serializers

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        # Convierte la fecha en formato 'dd/mm/aaaa' para su representación
        return value.strftime('%d/%m/%Y')

    def to_internal_value(self, value):
        from django.utils.dateparse import parse_date
        try:
            # Intenta parsear la fecha en formato 'dd/mm/aaaa'
            return parse_date(value)
        except ValueError:
            # Si ocurre un error, devuelve un ValidationError personalizado
            raise serializers.ValidationError('Fecha con formato erróneo. Use el formato dd/mm/aaaa.')

class UserSerializer(serializers.ModelSerializer):
    birthdate = CustomDateField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'birthdate', 'description', "image_path"]
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['creator_username'] = instance.user.username
        return representation
## SERIALIZER PARA UNIRSE A UN EVENTO
class EventsJoinedSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsJoined
        fields = '__all__'  # Esto incluirá todos los campos de tu modelo en la serialización