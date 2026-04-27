from django.db import models
from django.conf import settings
from Apps.CRM.Clientes_Lead.models import ClienteLead
from Apps.Catalogos.Estado_Cotizacion.models import EstadoCotizacion
from Apps.Catalogos.Catalogo_Servicios_Productos.models import ServicioProducto

class SolicitudCotizacion(models.Model):
    folio = models.CharField(max_length=20, unique=True, verbose_name='Folio de Cotizacion')
    cliente = models.ForeignKey(ClienteLead, on_delete=models.CASCADE, verbose_name='Cliente / Lead')
    estado = models.ForeignKey(EstadoCotizacion, on_delete=models.PROTECT, verbose_name='Estado actual')
    agente_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Agente de Ventas'
    )

    #detalles comerciales
    descripcion_requerimiento = models.TextField(verbose_name='Requerimientos del Cliente')
    monto_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto Estimado')

    #Fechas de control
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Solicitud')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        db_table = 'CRM_Solicitudes_Cotizaciones'
        verbose_name = 'Solicitud de Cotización'
        verbose_name_plural = 'Solicitudes y Cotizaciones'
        ordering = ['-fecha_solicitud'] #ordena mostrando las fechas mas recientes primero

    def __str__(self):
        return f"{self.folio} - {self.cliente.Nombre_Empresa}"
    
    def actualizar_total(self):
        """Calcula la suma de todos los detalles y actualizar el monto_estimado"""
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.monto_estimado = total
        #Usar save(updates_fields) para evitar recursividad infinita
        super(SolicitudCotizacion, self).save(update_fields=['monto_estimado'])

class DetalleCotizacion(models.Model):
    #relación con el "Padre" donde se usará related_name para acceder desde la cotización 
    cotizacion = models.ForeignKey(
        SolicitudCotizacion,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Cotización'
    )   
    servicio = models.ForeignKey(
        ServicioProducto,
        on_delete=models.PROTECT,
        verbose_name='Servicio / Producto'
    )
    cantidad=models.PositiveBigIntegerField(default=1,verbose_name='Cantidad')
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Unitario',
        blank=True,
        null=True)
    subtotal = models.DecimalField(max_digits=12,decimal_places=2,default=0.00,editable=False)

    class Meta:
        db_table = 'CRM_Detalle_Cotizaciones'
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de la Cotización'

    def save(self, *args, **kwargs):
        #Paso 1: si el presio no se escribe, tomarlo del catálogo
        if not self.precio_unitario:
            self.precio_unitario = self.servicio.precio_base
        
        #Paso 2: Calcular el subtotal automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        super(DetalleCotizacion, self).save(*args, **kwargs)

        #Paso 3: Notificar a la cotización Padre que se actualice el total 
        self.cotizacion.actualizar_total()

    def __str__(self):
        return f"{self.servicio.NombreProducto} x {self.cantidad}"