from django.apps import AppConfig

class AnimalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Animal'

    def ready(self):
        import Animal.signals  # Import the signals module
