from django.apps import AppConfig


class TbrPlaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tbr_place"

    def ready(self):
        import tbr_place.signals
