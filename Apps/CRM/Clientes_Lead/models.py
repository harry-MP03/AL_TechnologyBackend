from django.db import models
from django.conf import settings #Importando al superusuario
from Apps.Catalogos.Tipos_Empresa.models import TipoEmpresa
from Apps.Catalogos.Catalogo_Servicios_Productos.models import ServicioProducto

class ClienteLead(models.Model):
    Nombre_Empresa = models.CharField(max_length=200, verbose_name='Empresa/Cliente')
    tipo_empresa = models.ForeignKey(
        TipoEmpresa,
        on_delete=models.PROTECT,
        verbose_name='Tipo de Empresa'
    )

    # Se usa ManyToMany porque un lead puede estar interesado en varios servicios
    servicios_interes = models.ManyToManyField(
        ServicioProducto, 
        blank=True, # Puede que al inicio no sepamos qué quiere
        verbose_name='Servicios de Interés'
    )

    contacto_principal = models.CharField(max_length=100, verbose_name='Nombre del Contacto')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')

    # --- CAMPO DE MARKETING ---
    ORIGEN_CHOICES = [
        ('Google Search', 'Google Search / Buscador'),
        ('Facebook Ads', 'Facebook Ads / Redes Sociales'),
        ('LinkedIn', 'LinkedIn / Profesional'),
        ('Directo', 'Tráfico Directo / Referencia'),
    ]
    origen_lead = models.CharField(
        max_length=50,
        choices=ORIGEN_CHOICES,
        default='Directo',
        verbose_name='Origen del Lead'
    )

    RegistradoPor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, #Se vuelve vacio este campo si el usuario deja de existir
        null=True,
        blank=True,
        verbose_name='Registrado por'
    )

    Fecha_Registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    es_cliente_activo = models.BooleanField(default=False, verbose_name='¿Ya es cliente final?')

    class Meta:
        db_table = 'CRM_ Clientes_Lead'
        verbose_name = 'Cliente o Lead'
        verbose_name_plural = 'Clientes y Leads'
    
    def __str__(self):
        return f"{self.Nombre_Empresa} ({self.contacto_principal})"