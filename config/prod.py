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
# Leemos la cadena de texto de Azure
cors_origins_env = os.environ.get('CORS_ALLOWED_ORIGINS_STR', '')

# Si la variable existe, la dividimos por comas; si no, dejamos una lista vacía
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',')]
else:
    CORS_ALLOWED_ORIGINS = []