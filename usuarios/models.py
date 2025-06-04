from django.db import models

class InfoStudio(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)  # Suponiendo que está guardada como texto plano
    cargo = models.CharField(max_length=150)
    id_studio = models.IntegerField()
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'info_users'  # 👈 Esto conecta directamente con tu tabla existente
        managed = False  # 👈 Le decimos a Django que NO debe crear ni modificar esta tabla
