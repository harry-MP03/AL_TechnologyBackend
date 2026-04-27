from django.db import models

class EstadoCotizacion(models.Model):
    NombreEstado = models.CharField(max_length=50, unique=True, verbose_name='Estado')
    descripcion_Estado = models.CharField(max_length=255, blank=True, null=True)
    activo_Estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cat_Estado_Cotizacion'
        verbose_name = 'Estado de Cotización'
        verbose_name_plural = 'Estados de Cotización'
    
    def __str__(self):
        return self.NombreEstado
    