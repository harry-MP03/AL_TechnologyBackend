from django.db import models
from django.conf import settings
from Apps.CRM.Clientes_Lead.models import ClienteLead
from Apps.CRM.Solicitudes_Cotizaciones.models import SolicitudCotizacion

class SeguimientoSoporte(models.Model):
    TIPOS_CONTACTO = [
        ('WHATSAPP', 'Mensaje de WhatsApp'),
        ('CORREO', 'Correo Electrónico'),
        ('LLAMADA', 'Llamada Telefónica'),
        ('SOPORTE', 'Ticket de Soporte Técnico'),
    ]
    cliente = models.ForeignKey(ClienteLead, on_delete=models.CASCADE, verbose_name='Cliente')

    #Relacionar el seguimiento con una cotización específica 
    cotizacion_relacionada = models.ForeignKey(
        SolicitudCotizacion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Cotización Relacionada'
    )
    tipo_contacto = models.CharField(max_length=20, choices=TIPOS_CONTACTO, verbose_name='Tipo de Interacción')
    detalles = models.TextField(verbose_name='Notas de la interacción')
    
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Registrado por'
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del contacto')

    class Meta:
        db_table = 'CRM_Seguimiento_Soporte'
        verbose_name = 'Seguimiento / Soporte'
        verbose_name_plural = 'Bitácora de Seguimientos'

    def __str__(self):
        return f"{self.tipo_contacto} con {self.cliente.Nombre_Empresa} ({self.fecha_registro.strftime('%d/%m/%Y')})"