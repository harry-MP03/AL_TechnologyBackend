from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi



# Configuración del panel de Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API de AL-TECH",
      default_version='v1',
      description="Documentación oficial de los endpoints del sistema",
      contact=openapi.Contact(email="contacto@altech.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    #Rutas de las APIs
    path('api/catalogos/', include('Apps.Catalogos.Catalogo_Servicios_Productos.urls')),
    path('api/leads/', include('Apps.CRM.Clientes_Lead.urls')),
    path('api/cotizaciones/', include('Apps.CRM.Solicitudes_Cotizaciones.urls')),

    
]