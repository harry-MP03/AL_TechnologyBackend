from django.apps import AppConfig


class ClientesLeadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.CRM.Clientes_Lead'

    def ready(self):
        import Apps.CRM.Clientes_Lead.signals