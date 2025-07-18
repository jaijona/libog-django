# Generated by Django 5.2.1 on 2025-06-29 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promedio', '0003_alter_promedio_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAllUseStr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('strea_all', models.IntegerField(default=0)),
                ('strea_fem', models.IntegerField(default=0)),
                ('strea_male', models.IntegerField(default=0)),
                ('strea_tra', models.IntegerField(default=0)),
                ('strea_cou', models.IntegerField(default=0)),
                ('users_all', models.FloatField(default=0)),
                ('users_fem', models.FloatField(default=0)),
                ('users_male', models.FloatField(default=0)),
                ('users_tra', models.FloatField(default=0)),
                ('users_cou', models.FloatField(default=0)),
                ('contador', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'data_all_use_str',
                'managed': False,
            },
        ),
    ]
