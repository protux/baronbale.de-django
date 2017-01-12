"""
Django settings for baronbale_website project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

VERSION = '1.0.2'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n-w+15&03a8srymecq%i_1m&!#19_(qg5&ysezugj+7lm^p_wk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'baronbale.de']


# Application definition
SITE_ID = 1
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'request',
    'django_xmlrpc',
    'django_comments',
    'mptt',
    'tagging',
    'zinnia',
    
    'staticpages',
    'gc_toolbox',
    'toolbox',
    'homepage',
    'lab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'request.middleware.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'baronbale_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'zinnia.context_processors.version',
                
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'baronbale_website.wsgi.application'

from zinnia.xmlrpc import ZINNIA_XMLRPC_METHODS
XMLRPC_METHODS = ZINNIA_XMLRPC_METHODS

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
	# Development Database
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		}
	}
else:
    #   PRODUCTION DATABASE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'baronbale.de',
            'USER': 'baronbale.de',
            'PASSWORD': 'QRBgl7Yp4TnzK2DvXAFo',
            'HOST': '127.0.0.1',
            'PORT': '5432',
#            'OPTIONS': {
#                'client_encoding': 'UTF8',
#                'default_transaction_isolation': 'read committed',
#                'timezone': 'Europe/Berlin'
#            },
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
]

ZINNIA_MARKUP_LANGUAGE = 'markdown'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'templates/locale'),
]
LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
  ('de', 'Deutsch'),
  ('en', 'English'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = [
        '/home/nico/projekte/baronbale.de/static/',
    ]
else: 
    STATICFILES_DIRS = [
        '/home/nico/web/baronbale.de/static/',
    ]

if DEBUG:
    STATIC_ROOT = '/home/nico/projekte/baronbale.de/tmp/static/'
else:
    STATIC_ROOT = '/var/www/baronbale.de/static/'
STATIC_URL = '/static/'

if DEBUG:
    MEDIA_ROOT = '/home/nico/projekte/baronbale.de/tmp/media_root/'
else:
    MEDIA_ROOT = '/var/www/baronbale.de/media_root/'
MEDIA_URL = '/media/'

# Authentication settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_HTML = False
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# E-Mail
EMAIL_HOST = 'smtp.strato.de'
EMAIL_PORT = 465
EMAIL_HOST_PASSWORD = 'nFsCRWVBFxQPfzdHN4AC'
EMAIL_HOST_USER = 'webmaster@baronbale.de'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = ''
EMAIL_TIMEOUT = 60
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'bale@baronbale.de'
EMAIL_FROM_SERVICE = 'bale@baronbale.de'

