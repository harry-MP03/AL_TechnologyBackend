from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import LeadRegistroSerializer

class CapturaLeadAPIView(APIView):
    """
    Endpoint público para recibir los prospectos desde la página web de AL-Tech
    """
    @swagger_auto_schema(request_body=LeadRegistroSerializer,
                         responses={201:'Lead creado con éxito',400: 'Errores de validación'})
    def post(self, request):
        serializer = LeadRegistroSerializer(data=request.data)

        #Proceso de validación del email del cliente, campos obligatorios vacíos, etc.
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "¡Gracias! Hemos recibido tus datos. Un asesor de AL-TECH te contactará pronto."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    