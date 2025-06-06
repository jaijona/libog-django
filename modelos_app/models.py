"""
from django.db import models
from django.utils import timezone
from usuarios.models import InfoStudio  # Asegúrate que exista esta app y modelo

class ModeloRegistrado(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100, unique=True)
    jornada = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    fecha_registro = models.DateField(default=timezone.now)
    estado = models.BooleanField(default=True)
    studio = models.ForeignKey(InfoStudio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
"""

from django.db import models
from django.utils import timezone
from usuarios.models import InfoStudio

class ModeloRegistrado(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    jornada = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    estado = models.IntegerField(default=1)
    id_monitor = models.IntegerField(default=0)
    studio= models.ForeignKey(InfoStudio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'informacion'
        constraints = [
            models.UniqueConstraint(fields=['studio', 'usuario'], name='unique_usuario_por_studio')
        ]
        #ordering = ['-fecha_registro']

    def __str__(self):
        #return self.nombre,self.usuario
        return f"{self.nombre} ({self.usuario})"
        
