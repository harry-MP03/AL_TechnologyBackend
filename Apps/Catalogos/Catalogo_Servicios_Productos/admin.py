from django.contrib import admin

from .models import ServicioProducto

@admin.register(ServicioProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display=['NombreProducto','categoria','precio_base','activo_producto']
    search_display=['NombreProducto']
    list_filter=['categoria','activo_producto']