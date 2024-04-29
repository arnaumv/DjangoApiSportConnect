from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

#MODELO USUARIO

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    birthdate = models.DateField()
    description = models.TextField(blank=True, null=True)  # Nuevo campo descripción
    image_path = models.ImageField(upload_to='profile_photos', default='User_photo.png')

    instagram = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo Instagram
    twitter = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo Twitter

    is_reset_link_used = models.BooleanField(default=False)  # Add this line

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
    deleted_notify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.sport} - {self.date}"

# MODELO PARA UNIRSE A UN EVENTO
class EventsJoined(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    notify_deleted = models.BooleanField(default=False)  # Nueva columna