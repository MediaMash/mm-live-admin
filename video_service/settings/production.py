from .base import *
import os
from os.path import join, normpath

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'media-mash',
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'USER': 'media-mash',
        'HOST': os.environ.get("DATABASE_HOST"),
        'PORT': '25060',
    }
}

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

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = 'DO008NMYH26WBDFEQNJ3'
AWS_SECRET_ACCESS_KEY = os.environ.get("SPACES_SECRET")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN") + "/" + AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL  = os.environ.get("AWS_S3_ENDPOINT_URL")

MEDIA_URL = AWS_S3_CUSTOM_DOMAIN + "/" + AWS_STORAGE_BUCKET_NAME + "/"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_DEFAULT_ACL = 'public-read'

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = "123sdf45d2f234ggsdfg5gfewrvdfj345gfds9jdfg999fer"

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") 