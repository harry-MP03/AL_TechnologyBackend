from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ClienteLead

#El decorador @receiver "conecta" esta función al evento post_save del modelo ClienteLead
@receiver(post_save, sender=ClienteLead)
def enviar_alerta_nuevo_lead(sender, instance, created, **kwargs):
    #el parámetro 'created' es un booleano que nos dice si es un registro nuevo (True) o si
    #solo se está actualizando uno existente (False)
    if created:
        asunto = f"🚀 ¡Nuevo Lead Capturado! - {instance.Nombre_Empresa}" 
        
        mensaje = f"""
        ¡Hola equipo de AL-Technology!
        
        El sistema ha capturado un nuevo Cliente potencial desde la página web:
        
        🏢 Empresa: {instance.Nombre_Empresa}
        👤 Contacto: {instance.contacto_principal}
        📧 Correo: {instance.email}
        📱 Teléfono: {instance.telefono}
        
        Por favor, ingresen al panel de administración de AL-Technology para revisar
        """

        #Función nativa de Django para enviar el correo
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email='notificaciones@altech.com',
            recipient_list=['ventas@altech.com'],
            fail_silently=False,
        )
        