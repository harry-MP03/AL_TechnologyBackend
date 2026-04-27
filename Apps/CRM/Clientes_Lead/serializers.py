from rest_framework import serializers
from .models import ClienteLead

class LeadRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        #Incluir solo los campos necesarios para que el cliente los rellene
        model = ClienteLead
        fields = [
            'Nombre_Empresa',
            'contacto_principal',
            'email',
            'telefono',
            'tipo_empresa',
            'servicios_interes'
        ]