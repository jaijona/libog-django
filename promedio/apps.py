from django.apps import AppConfig

class PromedioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promedio'

    def ready(self):
        from .scheduler import iniciar_scheduler
        iniciar_scheduler()
