from django.contrib import admin
from .models import SolicitudCotizacion, DetalleCotizacion

#Se crea esta clase para permitir que los detalles aparezcan como una tabla editable
class DetalleCotizacionInLine(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1 #mostrando una fila vacia por defecto para agregar rapido
    fields = ['servicio','cantidad','precio_unitario','subtotal']
    readonly_fields = ['subtotal']

@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display=['folio','cliente','estado','monto_estimado','fecha_solicitud']
    search_fields=['folio','cliente__Nombre_Empresa',] #Busca por nombre de la empresa relacionada
    list_filter=['estado','fecha_solicitud']

    #Agregamos el formulario de detalles adentro de la cotización
    inlines=[DetalleCotizacionInLine]
    
    #Asegurarse de que las fechas automáticas se alteren por accidente
    readonly_fields=['monto_estimado', 'fecha_solicitud', 'fecha_actualizacion']