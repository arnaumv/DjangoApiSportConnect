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

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    birthdate = CustomDateField()
    image_path = serializers.SerializerMethodField()  # Añadir este campo

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'birthdate', 'description', "image_path", "instagram", "twitter"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hashear la contraseña antes de guardar el usuario
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def get_image_path(self, obj):  # Añadir este método
        if obj.image_path:
            return obj.image_path.url
        return None

    


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





from rest_framework import serializers
from .models import EventNotification

class EventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotification
        fields = ['id', 'type', 'username', 'recipient_username', 'event_title', 'event_sport', 'event_location', 'event_date', 'event_time', 'message', 'created_at']
    def validate(self, data):
        # Aquí puedes agregar cualquier lógica de validación personalizada.
        # Por ejemplo, podrías verificar que el 'type' es uno de los valores permitidos:
        if data['type'] not in ['follow', 'create', 'join']:
            raise serializers.ValidationError("Invalid type")
        # Si todo está bien, devolvemos los datos sin modificar.
        return data