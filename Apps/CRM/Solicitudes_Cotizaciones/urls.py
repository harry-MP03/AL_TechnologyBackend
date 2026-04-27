from django.urls import path
from .views import CrearCotizacionAPIView

urlpatterns = [
    path('nueva/', CrearCotizacionAPIView.as_view(), name='api_nueva_cotizacion'),
]