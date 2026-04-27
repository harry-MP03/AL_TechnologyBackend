from django.contrib import admin
from .models import categoria_producto

@admin.register(categoria_producto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display=['NombreCategoria','activo_Categoria']
    search_fields=['NombreCategoria']
    list_filter=['activo_Categoria']
    