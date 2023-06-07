from django.apps import AppConfig


class CoreEngineTenantManagementAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_engine_tenant_management_app'

    def ready(self):
        import core_engine_tenant_management_app.signals
