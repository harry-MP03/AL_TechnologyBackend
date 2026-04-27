from django.contrib import admin
from Apps.CRM.Seguimiento_Soporte.models import SeguimientoSoporte

@admin.register(SeguimientoSoporte)
class SeguimientoSoporteAdmin(admin.ModelAdmin):
    list_display=['cliente','tipo_contacto','fecha_registro','registrado_por']
    search_fields=['cliente__Nombre_Empresa','detalles']
    list_filter=['tipo_contacto','fecha_registro']
    readonly_fields=['fecha_registro']