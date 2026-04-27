from django.contrib import admin
from .models import TipoEmpresa

@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre_TipoEmpresa','activo']
    search_fields = ['nombre_TipoEmpresa']
    list_filter = ['activo']