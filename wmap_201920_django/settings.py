"""
Django settings for wmap_201920_django project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket
from django.urls import path, include, reverse_lazy, reverse

if os.name == "nt":
    import fix_gdal
    fix_gdal.fix()

# Here we make sure that we don't commit private data such as db userids/passwords to a public GitHub repository.
# Also set up configuration files to ease deployment on Docker with SSL/TLS cert.
from . import secrets
SECRETS = secrets.get_secrets()
secrets.insert_domainname_in_conf(SECRETS["NGINX_CONF"], SECRETS["MY_DOMAIN_NAME"])
secrets.insert_imagename_in_compose(SECRETS["DOCKER_COMPOSE_FILE"], SECRETS["DOCKER_IMAGE"])

## Need to change '/' to '\\' for Windows. Double backslash is because \ normally denotes an escape character
if os.name == "nt":
    secrets.insert_projectname_in_uwsgi_ini(__file__.split("\\")[-2], "uwsgi.ini")
else:
    secrets.insert_projectname_in_uwsgi_ini(__file__.split("/")[-2], "uwsgi.ini")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS["SECRET_KEY"]

ALLOWED_HOSTS = ['*', ]
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'corsheaders',
    'crispy_forms',
    'bootstrap3',
    'leaflet',
    'jquery',
    'pwa',
    'App.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wmap_201920_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        },
    },
]

WSGI_APPLICATION = 'wmap_201920_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = SECRETS["DATABASES"]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

PWA_SERVICE_WORKER_PATH = f'{STATIC_ROOT}/App/js/serviceworker.js'
PWA_APP_NAME = "Wmap 2019/20"
PWA_APP_DESCRIPTION = "Sample app for Adv Web Mapping module"
PWA_APP_START_URL = reverse_lazy('app:default')
PWA_APP_DISPLAY = 'standalone'
PWA_APP_ORIENTATION = "portrait"
PWA_APP_BACKGROUND_COLOR = 'darkgreen'
PWA_APP_THEME_COLOR = 'brown'
PWA_APP_ICONS = [
    {
        'src': f'{STATIC_URL}App/images/tudublin_logo_192.png',
        'type': 'image/png',
        'sizes': '192x192'
    },
    {
        'src': f'{STATIC_URL}App/images/tudublin_logo_512.png',
        'type': 'image/png',
        'sizes': '512x512'
    }
]
PWA_APP_SPLASH_SCREEN = []

LOGIN_REDIRECT_URL = reverse_lazy('app:about')
LOGOUT_REDIRECT_URL = reverse_lazy('app:login')

LEAFLET_CONFIG = {
    'RESET_VIEW': False,
    'TILES': [('OSM','https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{"useCache": True, "crossOrigin": True})],
    'PLUGINS': {
        'PouchDBCached': {
            'js': 'https://unpkg.com/leaflet.tilelayer.pouchdbcached@latest/L.TileLayer.PouchDBCached.js',
            'auto-include': True,
        },
        'MarkerCluster': {
            'js': 'https://unpkg.com/leaflet.markercluster@latest/dist/leaflet.markercluster.js',
            'css': ['https://unpkg.com/leaflet.markercluster@latest/dist/MarkerCluster.css',
                    'https://unpkg.com/leaflet.markercluster@latest/dist/MarkerCluster.Default.css'],
            'auto-include': True,
        },
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
# Your computer hostname goes here
if socket.gethostname() in SECRETS["ALLOWED_HOSTNAMES"]:
    DEBUG = True
    TEMPLATES[0]["OPTIONS"]["debug"] = True
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    DEBUG = False
    TEMPLATES[0]["OPTIONS"]["debug"] = False


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}
