from django.db import models

class EstadisticasModelo(models.Model):
    id_modelo = models.CharField(max_length=100)
    id_studio = models.CharField(max_length=100)
    promedio = models.FloatField()
    users = models.IntegerField()
    fecha = models.DateTimeField()
