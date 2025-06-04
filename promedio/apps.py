# promedio/apps.py

from django.apps import AppConfig
import os

class PromedioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promedio'

    def ready(self):
        # Solo iniciar en producción, y solo en el proceso principal
        if os.environ.get('RUN_MAIN') == 'true' or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            from .scheduler import iniciar_scheduler
            iniciar_scheduler()
