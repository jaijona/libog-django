
from django.db import models
from modelos_app.models import ModeloRegistrado

class Promedio(models.Model):
    id = models.AutoField(primary_key=True)
    #id_modelo = models.IntegerField()
    id_modelo = models.ForeignKey(ModeloRegistrado, db_column='id_modelo', on_delete=models.CASCADE)
    id_studio = models.IntegerField()
    promedio = models.FloatField()
    contador = models.IntegerField()
    users = models.IntegerField(default=0)
    fecha = models.DateTimeField()

    class Meta:
        managed = False  # <-- IMPORTANTE: Django no modificará esta tabla
        db_table = 'promedio'

class DataAllUseStr(models.Model):
    fecha = models.DateTimeField()
    strea_all = models.IntegerField(default=0)
    strea_fem = models.IntegerField(default=0)
    strea_male = models.IntegerField(default=0)
    strea_tra = models.IntegerField(default=0)
    strea_cou = models.IntegerField(default=0)
    
    users_all = models.FloatField(default=0)
    users_fem = models.FloatField(default=0)
    users_male = models.FloatField(default=0)
    users_tra = models.FloatField(default=0)
    users_cou = models.FloatField(default=0)

    contador = models.IntegerField(default=0)
    class Meta:
        db_table = 'data_all_use_str'  # nombre personalizado opcional
        managed = False  