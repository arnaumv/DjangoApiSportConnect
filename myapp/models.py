from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()