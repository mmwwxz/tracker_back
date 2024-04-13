from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WorkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'
    verbose_name = _("Цех")

    def ready(self):
        import workshop.signals
