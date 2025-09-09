import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#Confiuracion de variables de entorno
#Usa la libreria django-environ para leer el archivo .env
env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

#Aplicamos ENV
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

#For security
VALID_API_KEYS = env.str("VALID_API_KEYS").split(",")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#Aplicamos ENV
#Host que permiten conectarse a la aplicacion
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#Aplicaciones NUESTRAS 
PROJECTS_APPS = [
    'apps.blog',
]

#Aplicaciones de TERCEROS
THIRD_PARTY_APPS = [
    'rest_framework',
    'channels',
    'django_ckeditor_5',
    'django_celery_results',
    'django_celery_beat',
]

INSTALLED_APPS = DJANGO_APPS + PROJECTS_APPS + THIRD_PARTY_APPS

#Config para usar poe default o exntends etc, es el nombre que aplicamos lo que queremois usar con CKEditor
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
        "autoParagraph": False
    }
}




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Middleware for serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ASGI application for Channels
ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

#Conexion a la base de datos PostgreSQL, con los datos de la creacion del contenedor con la db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"), #NOmbre de la database dentro del contendor
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),  # Container name of the service in docker-compose
        'PORT': 5432  # Default port PostgreSQL 
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

#Configurando archivos estaticos
#Usa WhiteNoise para servir archivos estaticos en produccion
STATIC_LOCATION = "static"

STATIC_URL = 'static/'
STATIC_ROOT= os.path.join(BASE_DIR, "static")

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.AllowAny"
    ],
}

# Channels settings
#WebSockets + Redis
#Usa Redis para gestionar mensajes entre WebSockets
CHANNELS_LAYERS = {
    "default": {
        #Redis backend para manejar los canales de comunicación de WebSocket en Django Channels
        "BACKEND" : "channels_redis.core.RedisChannelLayer",
        #Configuración nombre del servicio Redis dentro de Docker, junto a su puerto
        "CONFIG": {
            "hosts": [env("REDIS_URL")],  # URL del servicio Redis
        }
    }
}


REDIS_HOST = env("REDIS_HOST")

"""
CLIENT_CLASS = Define el tipo de cliente de Redis que Django usa como cache
"django_redis.client.DefaultClient"	Usa el cliente por defecto provisto por django-redis
"""
# Caching settings
#Usa Redis como sistema de cache para acelerar respuestas
#Configurar la cache de Django para usar tambien Redis- 
CACHES = {
    "default": {
        #Usando Redis como backend de cache
        "BACKEND": "django_redis.cache.RedisCache",
        #usamos reddis: usando con TLS, configuracion con nombre de docker y puerto por defecto
        #"LOCATION": "rediss://django_redis:6379",

        #Redis normal sin TLS
        "LOCATION": env("REDIS_URL"),

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Channels allowed origins 
#Permite quienes se conecten por WebSocket
CHANNELS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

#Usamos json comoi serialziador de mensaje predeterimando
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Bogota"

#Celery necesita el brokerm usamos redis para este 
#COnfiguramos el broker con redis
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,
    'socket_timeout': 5,
    'retry_timeout': True
}

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

CELERY_IMPORTS = (
    'core.tasks',
    'apps.blog.tasks'
)

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {}