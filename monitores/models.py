from django.db import models
from django.utils import timezone
from usuarios.models import InfoStudio

class MonitorRegistrado(models.Model):
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=timezone.now)
    cargo = models.CharField(max_length=50, default='monitor')
    estado = models.IntegerField(default=1)
    id_studio = models.IntegerField(max_length=50)

    class Meta:
        db_table = 'info_users'
        constraints = [
            models.UniqueConstraint(fields=['id', 'username'], name='unique_monitor_por_studio')
        ]
        #ordering = ['-fecha_registro']

    def __str__(self):
        #return self.nombre,self.usuario
        return f"{self.name} ({self.username})"
        
