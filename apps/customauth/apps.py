from django.apps import AppConfig


class CustomauthConfig(AppConfig):
    name = 'apps.customauth'

    def ready(self):
        import apps.customauth.signals
