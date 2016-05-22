from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Alojamiento(models.Model):
    nombre = models.CharField(max_length=256)
    direccion = models.CharField(max_length=120)
    categoria = models.CharField(max_length=16)
    estrellas = models.CharField(max_length=12)
    url = models.CharField(max_length=120)
    descripcion = models.TextField()

class Imagen(models.Model):
    alojamiento_id = models.ForeignKey(Alojamiento)
    url = models.CharField(max_length=120)

class Comentario(models.Model):
    alojamiento_id = models.ForeignKey(Alojamiento)
    cuerpo = models.TextField()

class Alojamiento_Seleccionado(models.Model):
    alojamiento_id = models.ForeignKey(Alojamiento)
    usuario = models.ForeignKey(User, default="")
    fecha = models.DateField(auto_now=True)

class CSS(models.Model):
    usuario = models.CharField(max_length=56)
    titulo = models.CharField(max_length=56)
    tamannoFuente = models.FloatField()
    colorFondo = models.CharField(max_length=24)
