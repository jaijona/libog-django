

from django.core.management.base import BaseCommand
from posicion_strip.utils import guardar_promedios_stripchat

class Command(BaseCommand):
    help = 'Guarda los promedios de Stripchat por posición'

    def handle(self, *args, **kwargs):
        guardar_promedios_stripchat()
        self.stdout.write(self.style.SUCCESS("✅ Promedios Strip guardados correctamente."))