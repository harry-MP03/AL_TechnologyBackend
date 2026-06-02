import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

# Importando los modelos de FactuSoft
from django.contrib.auth import get_user_model
from Apps.Catalogos.Tipos_Empresa.models import TipoEmpresa
from Apps.Catalogos.Estado_Cotizacion.models import EstadoCotizacion
from Apps.Catalogos.CategoriaProducto.models import categoria_producto
from Apps.Catalogos.Catalogo_Servicios_Productos.models import ServicioProducto
from Apps.CRM.Clientes_Lead.models import ClienteLead
from Apps.CRM.Solicitudes_Cotizaciones.models import SolicitudCotizacion, DetalleCotizacion

User = get_user_model()

class Command(BaseCommand):
    help = 'Crear datos de prueba realistas (Faker) y orientados al análisis de Marketing para BI'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Eliminando datos antiguos de CRM y Catálogos...')
        # El orden inverso es importante por las llaves foráneas
        DetalleCotizacion.objects.all().delete()
        SolicitudCotizacion.objects.all().delete()
        ClienteLead.objects.all().delete()
        ServicioProducto.objects.all().delete()
        categoria_producto.objects.all().delete()
        
        self.stdout.write('Creando nuevos datos orientados a BI...')
        fake = Faker('es_ES')

        # --- 1. PREPARAR CATÁLOGOS BÁSICOS ---
        admin_user, _ = User.objects.get_or_create(username='admin_ventas', email='admin@altech.com')
        t_salud, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Salud')
        t_comercio, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Comercio')
        t_servicios, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Servicios Profesionales')
        est_aprobada, _ = EstadoCotizacion.objects.get_or_create(NombreEstado='Aprobada')

        # --- 2. CREAR CATÁLOGO DE PRODUCTOS / SERVICIOS ---
        cat_software, _ = categoria_producto.objects.get_or_create(NombreCategoria='Licencias de Software')
        cat_hardware, _ = categoria_producto.objects.get_or_create(NombreCategoria='Hardware y Equipos')
        cat_servicios, _ = categoria_producto.objects.get_or_create(NombreCategoria='Servicios TI')

        catalogo_productos = [
            # Software
            ServicioProducto.objects.create(NombreProducto='Licencia FactuSoft ERP (Anual)', categoria=cat_software, precio_base=1200.00),
            ServicioProducto.objects.create(NombreProducto='Módulo de Facturación Electrónica', categoria=cat_software, precio_base=350.00),
            ServicioProducto.objects.create(NombreProducto='Software POS para Retail', categoria=cat_software, precio_base=800.00),
            # Hardware
            ServicioProducto.objects.create(NombreProducto='Servidor Dedicado Cloud', categoria=cat_hardware, precio_base=2500.00),
            ServicioProducto.objects.create(NombreProducto='Terminal Punto de Venta (Pantalla Táctil)', categoria=cat_hardware, precio_base=950.00),
            ServicioProducto.objects.create(NombreProducto='Lector de Código de Barras Industrial', categoria=cat_hardware, precio_base=150.00),
            # Servicios
            ServicioProducto.objects.create(NombreProducto='Mantenimiento Preventivo de Equipos', categoria=cat_servicios, precio_base=120.00),
            ServicioProducto.objects.create(NombreProducto='Bolsa de 10 Horas de Soporte Técnico', categoria=cat_servicios, precio_base=400.00),
            ServicioProducto.objects.create(NombreProducto='Auditoría de Redes y Seguridad', categoria=cat_servicios, precio_base=850.00),
        ]
        self.stdout.write(f"✓ Catálogo de productos creado exitosamente.")

        fecha_inicio = timezone.now() - timedelta(days=365)
        clientes_creados = 0

        # --- 3. GENERAR 300 CLIENTES CON LÓGICA DE MARKETING ---
        for i in range(1, 301):
            if i % 3 == 0:
                tipo = t_salud
                origen = 'Google Search'
                nombre_empresa = f"Hospital/Clínica {fake.company()}" 
            elif i % 3 == 1:
                tipo = t_comercio
                origen = 'Facebook Ads'
                nombre_empresa = f"Comercializadora {fake.company()}"
            else:
                tipo = t_servicios
                origen = 'LinkedIn'
                nombre_empresa = f"Agencia {fake.company()}"

            fecha_registro_cliente = fecha_inicio + timedelta(days=random.randint(1, 360))

            # Crear el Cliente
            cliente = ClienteLead.objects.create(
                Nombre_Empresa=nombre_empresa,
                tipo_empresa=tipo,
                contacto_principal=fake.name(),
                email=fake.unique.company_email(),
                telefono=fake.phone_number(),
                origen_lead=origen, 
                RegistradoPor=admin_user
            )
            ClienteLead.objects.filter(id=cliente.id).update(Fecha_Registro = fecha_registro_cliente)
            clientes_creados += 1

            # Elegimos aleatoriamente entre 1 y 3 productos del catálogo
            productos_seleccionados = random.sample(catalogo_productos, random.randint(1, 3))

            # --- PASO 3.5: AGREGAR LOS SERVICIOS DE INTERÉS (Relación ManyToMany) ---
            # Se usa el método .set() o .add() porque es un campo ManyToMany
            cliente.servicios_interes.set(productos_seleccionados)

            fecha_cotizacion = fecha_registro_cliente + timedelta(days=random.randint(1, 5))

            # Crear la Cotización (El monto_estimado inicia en 0)
            cotizacion = SolicitudCotizacion.objects.create(
                folio=f"COT-{2025000 + i}",
                cliente=cliente,
                estado=est_aprobada,
                agente_asignado=admin_user,
                descripcion_requerimiento=fake.text(max_nb_chars=150),
                monto_estimado=0.00, # Tu función actualizar_total lo cambiará
            )
            #Forzar la fecha histórica
            SolicitudCotizacion.objects.filter(id=cotizacion.id).update(fecha_solicitud = fecha_cotizacion)

            # --- 4. AGREGAR DETALLES A LA COTIZACIÓN ---
            # Elegimos aleatoriamente entre 1 y 4 productos para esta cotización
            productos_seleccionados = random.sample(catalogo_productos, random.randint(1, 4))
            
            for producto in productos_seleccionados:
                cantidad = random.randint(1, 5)
                # Al crear el detalle, tu método save() calculará el subtotal y llamará a actualizar_total()
                DetalleCotizacion.objects.create(
                    cotizacion=cotizacion,
                    servicio=producto,
                    cantidad=cantidad
                    # No mandamos precio_unitario, tu modelo tomará el precio_base automáticamente
                )

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se crearon {clientes_creados} clientes, sus cotizaciones y el desglose de productos exacto.'))