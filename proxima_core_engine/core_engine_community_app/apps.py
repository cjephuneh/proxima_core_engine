from django.apps import AppConfig


class CoreEngineCommunityAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_engine_community_app'

    def ready(self):
        import core_engine_community_app.signals