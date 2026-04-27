from django.contrib import admin
from .models import ClienteLead

@admin.register(ClienteLead)
class ClienteLeadAdmin(admin.ModelAdmin):
    list_display=['Nombre_Empresa','contacto_principal','tipo_empresa','es_cliente_activo']
    search_fields=['Nombre_Empresa','contacto_principal','email']
    list_filter=['tipo_empresa','es_cliente_activo']

    #interfaz de doble cuadro para opciones de los servicios de izquerda a derecha
    filter_horizontal=['servicios_interes']