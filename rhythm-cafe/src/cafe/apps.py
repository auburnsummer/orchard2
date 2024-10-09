from django.apps import AppConfig


class CafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe'

    def ready(self):
        # only using it as a side effect
        import cafe.db_signals
        assert cafe.db_signals
        del cafe.db_signals