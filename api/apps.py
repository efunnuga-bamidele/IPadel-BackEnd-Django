from django.apps import AppConfig
from .tasks import updater


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if not getattr(ApiConfig, '_scheduler_started', False):
            updater.start()

            ApiConfig._scheduler_started = True
