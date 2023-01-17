from .base import *

# CORS to allow external apps auth through OAuth 2
# https://github.com/ottoyiu/django-cors-headers

INSTALLED_APPS += (
    'corsheaders',
)

MIDDLEWARE_CORS = [
    'corsheaders.middleware.CorsMiddleware',
]

MIDDLEWARE = MIDDLEWARE_CORS + MIDDLEWARE

CORS_ORIGIN_WHITELIST = os.environ['CORS_ORIGIN_WHITELIST'].split(',')

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(os.environ['DATABASE_ENGINE']),
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.environ['DATABASE_PORT'],
    }
}



# Security
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts

try:
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')
except KeyError:
    ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/2.0/ref/settings/#secure-proxy-ssl-header

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# NGINX and HTTPS
# https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-USE_X_FORWARDED_HOST

USE_X_FORWARDED_HOST = True if os.getenv('USE_X_FORWARDED_HOST') == 'True' \
    else False

# https://docs.djangoproject.com/en/2.0/ref/settings/#secure-proxy-ssl-header

if os.getenv('USE_HTTPS') == 'True':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

try:
    from .local import *
except ImportError:
    pass

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # new
DEFAULT_FROM_EMAIL = "help@buildly.io"
EMAIL_HOST = "smtp.sendgrid.net"  # new
EMAIL_HOST_USER = "apikey"  # new
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD")  # new
EMAIL_PORT = 587  # new
EMAIL_USE_TLS = True  # new

AWS_STORAGE_BUCKET_NAME = 'mediamash'
AWS_ACCESS_KEY_ID = 'DO00MW9V6QPPJKVCGHYA'
AWS_SECRET_ACCESS_KEY = os.environ.get("SPACES_SECRET")
AWS_S3_CUSTOM_DOMAIN = 'cms-static.nyc3.digitaloceanspaces.com' + "/" + AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL  = 'https://cms-static.nyc3.digitaloceanspaces.com'


MEDIA_URL = AWS_S3_CUSTOM_DOMAIN + "/" + AWS_STORAGE_BUCKET_NAME + "/"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_DEFAULT_ACL = 'public-read'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False