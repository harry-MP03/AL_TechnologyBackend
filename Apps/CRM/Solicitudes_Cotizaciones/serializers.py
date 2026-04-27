from rest_framework import serializers
from .models import SolicitudCotizacion, DetalleCotizacion

#Serializador de Hijo
class DetalleCotizacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = DetalleCotizacion
        #Solo se pide el servicio y la cantidad
        fields = ['servicio','cantidad']

#Serializador del Padre
class SolicitudCotizacionSerializer(serializers.ModelSerializer):
    #Se incrusta al hijo dentro del padre indicando que son muchos (un formato lista)
    detalles = DetalleCotizacionSerializador(many=True)

    class Meta: 
        model = SolicitudCotizacion
        fields = ['cliente','estado','descripcion_requerimiento','detalles']

    def create(self, validated_data):
        #1) Extrae la lista de detalles del diccionario principal
        detalles_data = validated_data.pop('detalles')

        #2) Crea la cotización Maestra en la base de datos
        cotizacion = SolicitudCotizacion.objects.create(**validated_data)

        #3) Recorre la lista de detalles y se crea uno por uno,
        #asignando la cotización que se acaba de crear en la linea 24
        for detalle_data in detalles_data:
            DetalleCotizacion.objects.create(cotizacion=cotizacion, **detalle_data)

        #4) Se forza la actualización del total general
        cotizacion.actualizar_total()
        
        return cotizacion
    