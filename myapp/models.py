from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

#MODELO USUARIO
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    birthdate = models.DateField()

    # Modificar los nombres de los accesores inversos
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)



# MODELO CREAR EVENTO
from django.db import models
from .models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255, null=True, blank=True)

# MODELO PARA UNIRSE A UN EVENTO
class EventsJoined(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
