"""
Django settings for omaha_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

import dotenv
import environ
from django.urls import reverse_lazy

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
environ.Env.read_env('.env')
env = environ.Env()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = BASE_DIR


IS_PRIVATE = env.bool('OMAHA_SERVER_PRIVATE', default=True)
SENTRY_DSN = env('RAVEN_DSN', default=None)

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN
}

if env.bool('OMAHA_ONLY_HTTPS', default=False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [
        r"^healthcheck/status/$"
    ]

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'absolute.context_processors.absolute',
            ],
        },
    },
]

APP_VERSION = "0.7.3"

SUIT_CONFIG = {
    'ADMIN_NAME': 'Omaha Server [{}]'.format(APP_VERSION),
    'MENU': tuple(filter(None, [
        # 'sites',
        {'app': 'omaha', 'label': 'Omaha', 'icon': 'icon-refresh'},
        {'app': 'sparkle', 'label': 'Sparkle', 'icon': 'icon-circle-arrow-down'},
        {'app': 'crash', 'label': 'Crash reports', 'icon': 'icon-fire'},
        {'app': 'feedback', 'label': 'Feedbacks', 'icon': 'icon-comment'},
        {'label': 'Statistics', 'url': 'omaha_statistics', 'icon': 'icon-star'},
        {'label': 'Preferences', 'url': reverse_lazy('set_preferences', args=['']), 'icon': 'icon-wrench'},
        {'label': 'Storage monitoring', 'url': 'monitoring', 'icon': 'icon-hdd'},
    ])),
    'CONFIRM_UNSAVED_CHANGES': False,
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='qicy(##kk%%2%#5zyoz)&0*@2wlfis+6s*al2q3t!+#++(0%23')

HOST_NAME = env('HOST_NAME', default='*')
OMAHA_URL_PREFIX = env('OMAHA_URL_PREFIX', default='')  # no trailing slash!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)
TEMPLATE_DEBUG = env('TEMPLATE_DEBUG', default=True)

ALLOWED_HOSTS = [HOST_NAME]


# Application definition

INSTALLED_APPS = (
    'cacheops',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'storages',
    'django_extensions',
    'versionfield',
    'absolute',
    'django_nvd3',
    'djangobower',
    'django_filters',
    'django_tables2',
    'django_ace',
    'rest_framework',
    'django_select2',
    'bootstrap3',
    'dynamic_preferences',

    'omaha',
    'crash',
    'feedback',
    'sparkle',
    'downloads',
    'healthcheck',
    'tinymce',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'omaha_server.middlewares.CUP2Middleware',
]

if IS_PRIVATE:
    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'omaha_server.middlewares.LoggingMiddleware',
        'omaha_server.middlewares.TimezoneMiddleware',
     ] + MIDDLEWARE

ROOT_URLCONF = 'omaha_server.urls'

WSGI_APPLICATION = 'omaha_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('POSTGRES_HOST', default='db'),
        'PORT': env('POSTGRES_PORT', default=5432),
        'NAME': env('POSTGRES_DB', default='db'),
        'USER': env('POSTGRES_USER', default='admin'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='admin'),
        'CONN_MAX_AGE': 0,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'assets'),
)


REDIS_HOST = env('REDIS_HOST', default='redis')
REDIS_PORT = env.int('REDIS_PORT', default=6379)

REDIS_PASSWORD = env('REDIS_PASSWORD', default=None)
REDIS_AUTH = 'redis://:{}@'.format(REDIS_PASSWORD) if REDIS_PASSWORD else ''

REDIS_STAT_HOST = env('REDIS_STAT_HOST', default=REDIS_HOST)
REDIS_STAT_PORT = env.int('REDIS_STAT_PORT', default=REDIS_PORT)

REDIS_STAT_DB = env.int('REDIS_STAT_DB', default=15)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'.format(
            REDIS_PORT=REDIS_PORT,
            REDIS_HOST=REDIS_HOST,
            REDIS_DB=env.int('REDIS_DB', default=1)),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'statistics': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'.format(
            REDIS_PORT=REDIS_STAT_PORT,
            REDIS_HOST=REDIS_STAT_HOST,
            REDIS_DB=REDIS_STAT_DB),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# TODO: see if possible to change session storage to local
SESSION_CACHE_ALIAS = 'default'

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder",
                       "djangobower.finders.BowerFinder",)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_DIR, 'assets', 'components')
BOWER_INSTALLED_APPS = (
    'd3#3.3.13',
    'nvd3#1.7.1',
    'bootstrap#3.3.5',
)


# Celery
from kombu import Queue

BROKER_URL = CELERY_RESULT_BACKEND = '{}{}:{}/{}'.format(REDIS_AUTH or 'redis://', REDIS_HOST, REDIS_PORT, 3)
CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_SERIALIZER = 'msgpack'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_MESSAGE_COMPRESSION = 'zlib'
CELERY_QUEUES = (
    Queue('transient', routing_key='transient', delivery_mode=1),
    Queue('default', routing_key='default'),
)
CELERY_ACCEPT_CONTENT = ['pickle', 'msgpack']

if IS_PRIVATE:
    CELERY_QUEUES += (
        Queue('limitation', routing_key='limitation'),
        Queue('private', routing_key='private'),
    )

    CELERYBEAT_SCHEDULE = {
        'auto_delete_older_then': {
            'task': 'tasks.auto_delete_older_then',
            'schedule': timedelta(hours=24),
            'options': {'queue': 'limitation'},
        },
        'auto_delete_size_is_exceed': {
            'task': 'tasks.auto_delete_size_is_exceeded',
            'schedule': timedelta(hours=1),
            'options': {'queue': 'limitation'},
        },
        'auto_delete_duplicate_crashes': {
            'task': 'tasks.auto_delete_duplicate_crashes',
            'schedule': timedelta(hours=24),
            'options': {'queue': 'limitation'},
        },
        'auto_monitoring_size': {
            'task': 'tasks.auto_monitoring_size',
            'schedule': timedelta(seconds=60),
            'options': {'queue': 'limitation'},
        },
        'auto_delete_dangling_files': {
            'task': 'tasks.auto_delete_dangling_files',
            'schedule': timedelta(hours=24),
            'options': {'queue': 'limitation'},
        },
    }

# TODO: see if this is needed
# Cache
CACHEOPS_REDIS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': 1,
    'socket_timeout': 3,
    'password': REDIS_PASSWORD or '',
}

CACHEOPS = {
    'omaha.*': {'ops': (), 'timeout': 10},
    'sparkle.*': {'ops': (), 'timeout': 10},
    'crash.*': {'ops': (), 'timeout': 10},
}

# Crash

CRASH_S3_MOUNT_PATH = env('CRASH_S3_MOUNT_PATH', default='/srv/omaha_s3')
CRASH_SYMBOLS_PATH = os.path.join(CRASH_S3_MOUNT_PATH, 'symbols')

# django-rest-framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

# django_select2

AUTO_RENDER_SELECT2_STATICS = False

# Client Update Protocol
CUP_REQUEST_VALIDATION = env.bool('CUP_REQUEST_VALIDATION', default=False)

CUP_PEM_KEYS = {}
if CUP_REQUEST_VALIDATION:
    CUP_PEM_KEYS['1'] = '/run/secrets/cup_key'

CRASH_TRACKER = env('CRASH_TRACKER', default='Sentry')

LOGSTASH_HOST = env('LOGSTASH_HOST', default=None)
LOGSTASH_PORT = env('LOGSTASH_PORT', default=None)

TINYMCE_BUTTONS = [
    'bold',
    'italic',
    'underline',
    'strikethrough',
    'separator',
    'bullist',
    'numlist',
    'outdent',
    'indent',
    'separator',
    'image',
    'media',
    'table',
    'link',
    'unlink',
    'separator',
    'forecolor',
    'backcolor',
    'separator',
    'hr',
]

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'theme_advanced_buttons1': TINYMCE_BUTTONS,
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'paste_text_sticky': True,
    'paste_text_sticky_default': True,
    'plugins': 'table,media'
}
