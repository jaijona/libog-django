# Generated by Django 5.2.1 on 2025-05-30 23:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorRegistrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('cargo', models.CharField(default='monitor', max_length=50)),
                ('estado', models.IntegerField(default=1)),
                ('id_studio', models.IntegerField(max_length=50)),
            ],
            options={
                'db_table': 'info_users',
                'constraints': [models.UniqueConstraint(fields=('id', 'username'), name='unique_monitor_por_studio')],
            },
        ),
    ]
