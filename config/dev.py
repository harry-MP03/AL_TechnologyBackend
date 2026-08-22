from .settings import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SECRET_KEY = config('SECRET_KEY')

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