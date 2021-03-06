"""
Django settings for baronbale_website project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os


def comma_separated_string_to_list(string):
    return string.split(",")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "n-w+15&03a8srymecq%i_1m&!#19_(qg5&ysezugj+7lm^p_wk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "baronbale.de", "85.214.231.140"]

LOGFILE_DJANGO = os.environ.get(
    "LOGFILE_DJANGO", "/opt/baronbale.de/logs/baronbale.log"
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGFILE_DJANGO,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(funcName)s %(message)s"
        }
    },
}

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "request",
    "baronbale_website.staticpages",
    "baronbale_website.gc_toolbox",
    "baronbale_website.toolbox",
    "baronbale_website.homepage",
    "baronbale_website.checker",
    "baronbale_website.banner_parser",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "request.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "baronbale_website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "baronbale_website/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "baronbale_website.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
    # Development Database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    #   PRODUCTION DATABASE
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "baronbale.de",
            "USER": "baronbale.de",
            "PASSWORD": os.environ.get("BB_DB_PASSWORD"),
            "HOST": "127.0.0.1",
            "PORT": "5432",
            #            'OPTIONS': {
            #                'client_encoding': 'UTF8',
            #                'default_transaction_isolation': 'read committed',
            #                'timezone': 'Europe/Berlin'
            #            },
        }
    }
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "templates/locale"),
]
LANGUAGE_CODE = "de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_DIRS = os.environ.get("STATICFILES_DIRS", ["/opt/baronbale.de/static/"])
if not isinstance(STATICFILES_DIRS, list):
    STATICFILES_DIRS = comma_separated_string_to_list(STATICFILES_DIRS)
STATIC_ROOT = os.environ.get("STATIC_ROOT", "/var/www/baronbale.de/static/")
STATIC_URL = "/static/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "/var/www/baronbale.de/media_root/")
MEDIA_URL = "/media/"

# Authentication settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_HTML = False
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

# E-Mail
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_SUBJECT_PREFIX = ""
EMAIL_TIMEOUT = 60
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_FROM_SERVICE = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
ADMINS = [
    ("Nico", "protux@baronbale.de"),
]
MANAGERS = ADMINS
