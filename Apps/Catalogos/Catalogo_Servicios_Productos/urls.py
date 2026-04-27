from django.urls import path
from .views import CatalogoProductoServicioAPIView

urlpatterns = [
    path('servicios/', CatalogoProductoServicioAPIView.as_view(), name='api_catalogo_servicios'),
]