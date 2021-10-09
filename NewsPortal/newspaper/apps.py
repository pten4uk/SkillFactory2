from django.apps import AppConfig


class NewspaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newspaper'

    verbose_name = 'Новости'

    def ready(self):
        import newspaper.signals
