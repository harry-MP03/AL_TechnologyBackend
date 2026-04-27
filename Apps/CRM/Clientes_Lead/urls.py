from django.urls import path
from .views import CapturaLeadAPIView

urlpatterns = [

    path('nuevolead/', CapturaLeadAPIView.as_view(), name='api_nuevo_lead'),
]