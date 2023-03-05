"""
Django settings for video_service project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, normpath

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG') == 'False' else True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS_DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_THIRD_PARTIES = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
    'material',
    'storages',
    'django_social_share',

    # Health check
    'health_check',
        'health_check.db',

    # openapi
    'drf_yasg',
]

INSTALLED_APPS_LOCAL = [
    'video',
    'login',
    'shop',
]

INSTALLED_APPS = INSTALLED_APPS_DJANGO + INSTALLED_APPS_THIRD_PARTIES + \
    INSTALLED_APPS_LOCAL

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'video_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'video_service.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# change URL for login redirect
LOGIN_REDIRECT_URL = '/video'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'video_service.permissions.AllowOptionsAuthentication',
    )
}

# JWT Configuration

JWT_AUTH_DISABLED = True
JWT_ALLOWED_ISSUER = 'bifrost'
JWT_PUBLIC_KEY_RSA_BIFROST = os.getenv('JWT_PUBLIC_KEY_RSA_BIFROST')

CLOUDFLARE_API_URL = os.getenv('CLOUDFLARE_API_URL')
CLOUDFLARE_ACCOUNT = os.getenv('CLOUDFLARE_ACCOUNT')
CLOUDFLARE_TOKEN = os.getenv('CLOUDFLARE_TOKEN')
CLOUDFLARE_AUTH_EMAIL = os.getenv('CLOUDFLARE_AUTH_EMAIL')

YOUTUBE_API_URL = os.getenv('YOUTUBE_API_URL')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

SECRET_KEY = "12345d2f2345gfewrvdfj3459jddddfg999fer"

SITE_ID = 1

GOOGLE_APPLICATION_CREDENTIALS = "dev-buildly-e1ddcc965746.json"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://stingray-app-4wzxb.ondigitalocean.app/'