from django.contrib import admin
from .models import EstadoCotizacion

@admin.register(EstadoCotizacion)
class EstadoCotizacionAdmin(admin.ModelAdmin):
    list_display=['NombreEstado','activo_Estado']
    search_fields=['NombreEstado']
    list_filter=['activo_Estado']