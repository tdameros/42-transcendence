"""
Django settings for tournament project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from common.src import settings as common_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APPEND_SLASH = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    USER_MANAGEMENT_URL = 'http://localhost:8001/'
    USER_STATS_URL = 'http://localhost:8002/'
    NOTIFICATION_URL = 'http://localhost:8003/'
else:
    USER_MANAGEMENT_URL = common_settings.USER_MANAGEMENT_URL
    USER_STATS_URL = common_settings.USER_STATS_URL
    NOTIFICATION_URL = common_settings.NOTIFICATION_URL

USER_MANAGEMENT_USER_ENDPOINT = USER_MANAGEMENT_URL + 'user/id/'
USER_STATS_USER_ENDPOINT = USER_STATS_URL + 'statistics/user/'
USER_NOTIFICATION_ENDPOINT = NOTIFICATION_URL + 'notification/user/'

MIN_TOURNAMENT_NAME_LENGTH = 3
MAX_TOURNAMENT_NAME_LENGTH = 20
MAX_PLAYERS = 16
MIN_PLAYERS = 3

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50

MIN_NICKNAME_LENGTH = 3
MAX_NICKNAME_LENGTH = 14

HASH_PASSWORD_MAX_LENGTH = 128
PASSWORD_MIN_LENGTH = 4
PASSWORD_MAX_LENGTH = 30

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jyplfl_@yqc2@o&hh)b6s&c%b$&qna9mov4gi#%w3=z9c#8*=f'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['https://*']

ROOT_URLCONF = 'tournament.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tournament.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # PostgreSQL for GitHub Actions
    if 'GITHUB_ACTIONS' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',

                'NAME': os.environ.get('DB_NAME'),
                'USER': os.environ.get('DB_USER'),
                'PASSWORD': os.environ.get('DB_PASSWORD'),
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
    # PostgreSQL for production
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'mydatabase',
                'USER': 'myuser',
                'PASSWORD': 'mypassword',
                'HOST': 'tournament-db',
                'PORT': '5432',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
