from django.db import models

class TipoEmpresa(models.Model):
    nombre_TipoEmpresa = models.CharField(max_length=100, unique=True, verbose_name='Tipo de Empresa')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name= 'Estado Activo') 

    class Meta:
        db_table = 'Cat_Tipos_Empresa'
        verbose_name = 'Tipo de Empresa'
        verbose_name_plural = 'Tipos de Empresa'

    def __str__(self):
        return f"{self.nombre_TipoEmpresa}"