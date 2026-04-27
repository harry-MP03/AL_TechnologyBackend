from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import ServicioProducto
from .serializers import ServicioProductoSerializer

class CatalogoProductoServicioAPIView(APIView):
    """
    Endpoint público para listar todos los servicios y productos activos
    """

    @swagger_auto_schema(responses={200: ServicioProductoSerializer(many=True)})
    def get(self, request):
        #Consultando la base de datos donde solo se muestre aquellos registros activos
        servicios = ServicioProducto.objects.filter(activo_producto=True)

        #Pasar los datos por el serializador "many=True" porque es una lista
        serializer = ServicioProductoSerializer(servicios, many=True)

        #Retornar la respuesta en formato JSON
        return Response(serializer.data, status=status.HTTP_200_OK)