from django.apps import AppConfig

class RationLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ration_logs'

    def ready(self):
        import ration_logs.signals
