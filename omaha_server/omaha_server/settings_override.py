from .settings_prod import *

# TODO: should work by default
STATIC_URL = 'https://{}.s3.amazonaws.com/'.format(os.environ.get('AWS_STORAGE_BUCKET_NAME'))
MEDIA_URL = 'https://{}.s3.amazonaws.com/'.format(os.environ.get('AWS_STORAGE_BUCKET_NAME'))

if os.environ.get('CDN_NAME'):
    CDN_NAME = os.environ.get('CDN_NAME')

CUP_PEM_KEYS = {
    '1': '/run/secrets/cup_key'
}
