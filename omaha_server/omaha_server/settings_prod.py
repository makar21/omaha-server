# coding: utf8

import os

from django.utils import crypto

from furl import furl

from .settings import *

DEBUG = False

ALLOWED_HOSTS = (HOST_NAME,)
SECRET_KEY = os.environ.get('SECRET_KEY') or crypto.get_random_string(50)

STATICFILES_STORAGE = 'omaha_server.s3utils.StaticS3Storage'
DEFAULT_FILE_STORAGE = 'omaha_server.s3utils.S3Storage'
PUBLIC_READ_FILE_STORAGE = 'omaha_server.s3utils.PublicReadS3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME', 'us-east-1')
AWS_SES_REGION_ENDPOINT = os.environ.get(
    'AWS_SES_REGION_ENDPOINT', 'email.us-east-1.amazonaws.com'
)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_RECIPIENTS = os.environ.get('EMAIL_RECIPIENTS')

MEDIA_URL = ''.join([S3_URL, 'media/'])
STATIC_URL = ''.join([S3_URL, 'static/'])

AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_DEFAULT_ACL = 'private'

FILEBEAT_HOST = os.environ.get('FILEBEAT_HOST', 'localhost')
FILEBEAT_PORT = os.environ.get('FILEBEAT_PORT', 9021)
RSYSLOG_ENABLE = True if os.environ.get('RSYSLOG_ENABLE', '').title() == 'True' else False

CELERYD_HIJACK_ROOT_LOGGER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'filebeat_format': {
            'format': 'hostname={}|level=%(levelname)s|logger=%(name)s|timestamp=%(asctime)s|module=%(module)s|process=%(process)d|thread=%(thread)d|message=%(message)s'.format(HOST_NAME)
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'rsyslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'filebeat_format',
            'address': '/dev/log'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery.beat': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery.task': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'limitation': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}

if FILEBEAT_HOST and FILEBEAT_PORT:
    LOGGING['handlers']['filebeat'] = {
        'level': os.environ.get('FILEBEAT_LOGGING_LEVEL', 'INFO'),
        'class': 'logging.handlers.SysLogHandler',
        'formatter': 'filebeat_format',
        'address': (FILEBEAT_HOST, int(FILEBEAT_PORT))
    }
    LOGGING['root']['handlers'].append('filebeat')
    LOGGING['loggers']['django.request']['handlers'].append('filebeat')

if RSYSLOG_ENABLE:
    LOGGING['root']['handlers'].append('rsyslog')
    LOGGING['loggers']['django.request']['handlers'].append('rsyslog')
    LOGGING['loggers']['celery.beat']['handlers'].append('rsyslog')
    LOGGING['loggers']['celery.task']['handlers'].append('rsyslog')
    LOGGING['loggers']['limitation']['handlers'].append('rsyslog')

if os.environ.get('CDN_NAME'):
    CDN_NAME = os.environ.get('CDN_NAME')
