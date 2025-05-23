# Generated by Django 5.2.1 on 2025-05-20 03:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloRegistrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('usuario', models.CharField(max_length=100, unique=True)),
                ('jornada', models.CharField(max_length=50)),
                ('genero', models.CharField(max_length=50)),
                ('fecha_registro', models.DateField(default=django.utils.timezone.now)),
                ('estado', models.BooleanField(default=True)),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.infostudio')),
            ],
        ),
    ]
