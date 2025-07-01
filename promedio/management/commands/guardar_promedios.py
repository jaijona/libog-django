"""
from django.core.management.base import BaseCommand
from promedio.utils import guardar_promedios

class Command(BaseCommand):
    help = 'Consulta la API y guarda los promedios'


    def handle(self, *args, **kwargs):
        guardar_promedios()
"""
from django.core.management.base import BaseCommand
from promedio.utils import guardar_promedios  # Asegúrate de que está bien importado

class Command(BaseCommand):
    help = 'Guarda promedios desde la API'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando tarea guardar_promedios...")
        guardar_promedios()
        self.stdout.write("Tarea guardar_promedios completada.")
