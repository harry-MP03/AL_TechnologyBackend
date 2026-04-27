from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .serializers import SolicitudCotizacionSerializer

class CrearCotizacionAPIView(APIView):
    """
    Endpoint para crear una cotización completa junto con sus partidas (detalles)
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=SolicitudCotizacionSerializer,
        responses={201: 'Cotización generada exitosamente'}
    )
    def post(self, request):
        serializer = SolicitudCotizacionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Cotización estructurada con éxito."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
