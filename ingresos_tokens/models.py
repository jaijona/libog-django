from django.db import models
from django.utils import timezone


class IngresoTokens(models.Model):
    id_modelo = models.ForeignKey(
        'modelos_app.ModeloRegistrado',
        on_delete=models.CASCADE,
        db_column='id_modelo'  # ← Fuerza a usar esa columna exacta
    )
    id_studio = models.PositiveIntegerField(default=0)
    token_cb = models.PositiveIntegerField(default=0)
    token_otro = models.PositiveIntegerField(default=0)
    promedio_posicion = models.FloatField(null=True, blank=True)  # ← Nuevo campo
    usuarios = models.FloatField(null=True, blank=True) # ← Nuevo campo
    fecha = models.DateField()
    

    class Meta:
        managed = False  # <-- IMPORTANTE: Django no modificará esta tabla
        db_table = 'ingreso_token'
        unique_together = ('id_modelo', 'fecha')

    def __str__(self):
        return f"{self.id_modelo.usuario} - {self.fecha}"
    
