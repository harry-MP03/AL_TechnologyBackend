from .settings import *
import os

# --- CONFIGURACIÓN DE PRODUCCIÓN ---__
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Para que Django sepa que está detrás de un proxy seguro (HTTPS en Azure)
# y genere las URLs correctamente.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME_NEON'),
            'USER': os.environ.get('USER_NEON'),
            'PASSWORD': os.environ.get('PASSWORD_NEON'),
            'HOST': os.environ.get('HOST_NEON'),
            'PORT': os.environ.get('PORT_NEON', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            }
        }
}
# config/prod.py
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')