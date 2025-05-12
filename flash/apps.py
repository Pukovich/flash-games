from django.apps import AppConfig


class FlashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flash'

    def ready(self):
        import flash.signals
