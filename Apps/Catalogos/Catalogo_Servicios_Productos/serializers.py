from rest_framework import serializers
from .models import ServicioProducto

class ServicioProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria_producto.NombreCategoria', read_only=True)

    class Meta:
        model=ServicioProducto
        fields=['id','NombreProducto','categoria_nombre','precio_base','descripcionProducto']