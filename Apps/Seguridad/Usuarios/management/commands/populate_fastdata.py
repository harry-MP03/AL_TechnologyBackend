import random
import sys
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from django.conf import settings

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
    help = 'Crear 10,000 datos (con errores para limpieza en KNIME) usando BULK CREATE'

    @transaction.atomic
    def handle(self, *args, **options):
        # se apagará los correos para máxima velocidad y no consumir mucho recursos
        settings.EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

        #se borrarán los registros viejos
        self.stdout.write('Eliminando datos antiguos (Limpiando BD)...')
        DetalleCotizacion.objects.all().delete()
        SolicitudCotizacion.objects.all().delete()
        ClienteLead.objects.all().delete()
        ServicioProducto.objects.all().delete()
        categoria_producto.objects.all().delete()
        
        fake = Faker('es_ES')

        # --- 1. PREPARAR CATÁLOGOS BÁSICOS ---
        admin_user, _ = User.objects.get_or_create(username='admin_ventas', email='admin@altech.com')
        t_salud, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Salud')
        t_comercio, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Comercio')
        t_servicios, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Servicios Profesionales')
        t_educacion, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Educación')
        t_manufactura, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Manufactura')
        t_finanzas, _ = TipoEmpresa.objects.get_or_create(nombre_TipoEmpresa='Finanzas')

        est_aprobada, _ = EstadoCotizacion.objects.get_or_create(NombreEstado='Aprobada')
        est_rechazada, _ = EstadoCotizacion.objects.get_or_create(NombreEstado='Rechazada')
        est_pendiente, _ = EstadoCotizacion.objects.get_or_create(NombreEstado='Pendiente')

        cat_software, _ = categoria_producto.objects.get_or_create(NombreCategoria='Licencias de Software')
        cat_hardware, _ = categoria_producto.objects.get_or_create(NombreCategoria='Hardware y Equipos')
        cat_servicios, _ = categoria_producto.objects.get_or_create(NombreCategoria='Servicios TI')

        productos_info = [
            ('Licencia FactuSoft ERP (Anual)', cat_software, 1200.00),
            ('Módulo de Facturación Electrónica', cat_software, 350.00),
            ('Software POS para Retail', cat_software, 800.00),
            ('Servidor Dedicado Cloud', cat_hardware, 2500.00),
            ('Terminal Punto de Venta (Pantalla Táctil)', cat_hardware, 950.00),
            ('Lector de Código de Barras Industrial', cat_hardware, 150.00),
            ('Mantenimiento Preventivo de Equipos', cat_servicios, 120.00),
            ('Bolsa de 10 Horas de Soporte Técnico', cat_servicios, 400.00),
            ('Auditoría de Redes y Seguridad', cat_servicios, 850.00),
        ]

        catalogo_productos = []
        for nombre, cat, precio in productos_info:
            prod, _ = ServicioProducto.objects.get_or_create(
                NombreProducto=nombre, defaults={'categoria': cat, 'precio_base': precio}
            )
            catalogo_productos.append(prod)

        fecha_inicio = timezone.now() - timedelta(days=365)
        
        # --- LISTAS PARA BULK CREATE ---
        clientes_batch = []
        estados_precalculados = [] # Guardaremos el estado para usarlo en la cotización
        
        self.stdout.write('Fase 1/4: Construyendo Clientes en memoria (con errores y duplicados)...')
        
        # Generar los clientes en memoria
        for i in range(1, 10501):
            modulo = i % 5
            
           # ERRORES INYECTADOS: Formatos inconsistentes y más varianza de sectores
            if modulo == 0:
                # Búsquedas orgánicas: Salud o Educación
                tipo = random.choice([t_salud, t_educacion])
                origen = random.choice(['Google Search', 'google search', 'GOOGLE', 'Google'])
                prefijo = "Hospital/Clínica" if tipo == t_salud else "Instituto/Colegio"
                nombre_empresa = f"{prefijo} {fake.company()}"
                
            elif modulo == 1:
                # Facebook Ads: Comercio o Manufactura
                tipo = random.choice([t_comercio, t_manufactura])
                origen = random.choice(['Facebook Ads', 'Facebook', 'fb', 'facebook ads'])
                prefijo = "Comercializadora" if tipo == t_comercio else "Industrias"
                nombre_empresa = f"{prefijo} {fake.company()}"
                
            elif modulo == 2:
                # LinkedIn: Servicios o Finanzas (Canal corporativo)
                tipo = random.choice([t_servicios, t_finanzas])
                origen = random.choice(['LinkedIn', 'linkedin', 'Linked In'])
                prefijo = "Agencia" if tipo == t_servicios else "Financiera"
                nombre_empresa = f"{prefijo} {fake.company()}"
                
            elif modulo == 3:
                # TikTok: Mezcla de todos los sectores, pero más informales
                tipo = random.choice([t_comercio, t_servicios, t_educacion]) 
                origen = random.choice(['TikTok', 'tiktok', 'Tik Tok', 'tk'])
                nombre_empresa = f"Emprendimiento {fake.company()}"
                
            else:
                # Instagram: Enfoque visual (Comercio, Salud, Servicios)
                tipo = random.choice([t_salud, t_comercio, t_servicios]) 
                origen = random.choice(['Instagram', 'IG', 'insta', 'instagram'])
                nombre_empresa = f"Tienda/Consultorio {fake.company()}"

            # ERRORES INYECTADOS: Valores Faltantes (Nulls/Vacíos)
            if random.random() < 0.05: origen = "" 
            
            telefono_cliente = fake.phone_number()
            if random.random() < 0.05: telefono_cliente = ""

            # Precalcular el estado para saber si es cliente activo
            estado_random = random.choices([est_aprobada, est_rechazada, est_pendiente], weights=[50,30,20], k=1)[0]
            estados_precalculados.append(estado_random)

            cliente = ClienteLead(
                Nombre_Empresa=nombre_empresa,
                tipo_empresa=tipo,
                contacto_principal=fake.name(),
                email=fake.unique.company_email(),
                telefono=telefono_cliente,
                origen_lead=origen, 
                RegistradoPor=admin_user,
                Fecha_Registro=fecha_inicio + timedelta(days=random.randint(1, 360)),
                es_cliente_activo=(estado_random == est_aprobada)
            )
            clientes_batch.append(cliente)

            # ERRORES INYECTADOS: Registros duplicados (3%)
            if random.random() < 0.03:
                cliente_clon = ClienteLead(
                    Nombre_Empresa=nombre_empresa,
                    tipo_empresa=tipo,
                    contacto_principal=cliente.contacto_principal,
                    email=f"clon_{cliente.email}", # Leve cambio para que BD no colapse si es unique
                    telefono=cliente.telefono,
                    origen_lead=origen,
                    RegistradoPor=admin_user,
                    Fecha_Registro=cliente.Fecha_Registro,
                    es_cliente_activo=cliente.es_cliente_activo
                )
                clientes_batch.append(cliente_clon)
                estados_precalculados.append(estado_random)

        # UN SOLO VIAJE A LA BD PARA CLIENTES
        clientes_guardados = ClienteLead.objects.bulk_create(clientes_batch)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(clientes_guardados)} Clientes guardados.'))


        # --- FASE 2: RELACIÓN MUCHOS A MUCHOS Y COTIZACIONES ---
        self.stdout.write('Fase 2/4 y 3/4: Construyendo relaciones M2M y Cotizaciones...')
        
        m2m_batch = []
        cotizaciones_batch = []
        detalles_generados = [] # Guardaremos (producto, cantidad) para la Fase 4
        
        # Modelo intermedio oculto de Django para el ManyToMany
        ClienteServicioThrough = ClienteLead.servicios_interes.through

        for idx, cliente in enumerate(clientes_guardados):
            # 1. Preparar ManyToMany (servicios_interes)
            productos_m2m = random.sample(catalogo_productos, random.randint(1, 3))
            for prod in productos_m2m:
                m2m_batch.append(ClienteServicioThrough(clientelead_id=cliente.id, servicioproducto_id=prod.id))

            # 2. Calcular montos manualmente en Python
            productos_cotizacion = random.sample(catalogo_productos, random.randint(1, 4))
            total_calculado = 0
            detalles_temp = []
            
            for prod in productos_cotizacion:
                cantidad = random.randint(1, 5)
                total_calculado += float(prod.precio_base) * cantidad
                detalles_temp.append((prod, cantidad))

            # ERRORES INYECTADOS: Valores atípicos/Outliers (2%)
            if random.random() < 0.02:
                total_calculado = random.choice([-500.00, -150.50, 9999999.99, 5000000.00])

            # 3. Preparar Cotización
            cotizacion = SolicitudCotizacion(
                folio=f"COT-BULK-{cliente.id}",
                cliente=cliente,
                estado=estados_precalculados[idx],
                agente_asignado=admin_user,
                descripcion_requerimiento="Generado por Bulk Create",
                monto_estimado=total_calculado,
                fecha_solicitud=cliente.Fecha_Registro + timedelta(days=random.randint(1, 5))
            )
            cotizaciones_batch.append(cotizacion)
            detalles_generados.append(detalles_temp)

        # UN SOLO VIAJE PARA M2M
        ClienteServicioThrough.objects.bulk_create(m2m_batch)
        # UN SOLO VIAJE PARA COTIZACIONES
        cotizaciones_guardadas = SolicitudCotizacion.objects.bulk_create(cotizaciones_batch)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(cotizaciones_guardadas)} Cotizaciones guardadas.'))


        # --- FASE 4: DETALLES DE COTIZACIÓN ---
        self.stdout.write('Fase 4/4: Construyendo Detalles de Cotización...')
        detalles_batch = []
        
        for cotizacion, lista_detalles in zip(cotizaciones_guardadas, detalles_generados):
            for prod, cantidad in lista_detalles:
                detalles_batch.append(DetalleCotizacion(
                    cotizacion=cotizacion,
                    servicio=prod,
                    cantidad=cantidad,
                    precio_unitario=prod.precio_base,
                    subtotal=float(prod.precio_base) * cantidad
                ))

        # UN SOLO VIAJE PARA DETALLES
        DetalleCotizacion.objects.bulk_create(detalles_batch)
        self.stdout.write(self.style.SUCCESS('✓ Todos los detalles guardados.'))

        self.stdout.write(self.style.SUCCESS('\n¡ÉXITO TOTAL! BD generada con CAOS CONTROLADO en tiempo récord.'))