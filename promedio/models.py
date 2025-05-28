
from django.db import models
from modelos_app.models import ModeloRegistrado

class Promedio(models.Model):
    id = models.AutoField(primary_key=True)
    #id_modelo = models.IntegerField()
    id_modelo = models.ForeignKey(ModeloRegistrado, db_column='id_modelo', on_delete=models.CASCADE)
    id_studio = models.IntegerField()
    promedio = models.FloatField()
    contador = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        managed = False  # <-- IMPORTANTE: Django no modificará esta tabla
        db_table = 'promedio'
