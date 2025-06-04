from django.core.management.base import BaseCommand
from promedio.utils import guardar_promedios

class Command(BaseCommand):
    help = 'Consulta la API y guarda los promedios'


    def handle(self, *args, **kwargs):
        guardar_promedios()
