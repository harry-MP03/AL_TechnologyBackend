from .settings import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'AL_TECH_DB',
            'USER': 'altech_admin',
            'PASSWORD': 'admin123',
            'HOST': 'localhost',  
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',  
                'extra_params': 'TrustServerCertificate=yes', 
            },
        }
    }