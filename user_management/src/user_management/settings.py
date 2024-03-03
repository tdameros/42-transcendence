"""
Django settings for user_management project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

from common.src import settings as common_settings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CRON_SCRIPT_PATH = os.path.join(BASE_DIR, 'commands')
COMMANDS_LOG_PATH = os.path.join(CRON_SCRIPT_PATH, 'commands.log')

CRONJOBS = [
    ('0 0 * * *', 'myapp.commands.delete_inactive_users', f'>> {COMMANDS_LOG_PATH} 2>&1'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if os.getenv('DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False

if DEBUG:
    FRONT_URL = "https://localhost:6002/"
else:
    FRONT_URL = common_settings.FRONT_URL

if DEBUG:
    USER_MANAGEMENT_IP = 'http://localhost:8000/'
else:
    USER_MANAGEMENT_IP = 'https://localhost:6002/'

# FRONT_ACTIVE_ACCOUNT URL
if DEBUG:
    FRONT_ACTIVE_ACCOUNT_URL = 'http://localhost:8080/account/active/'
else:
    FRONT_ACTIVE_ACCOUNT_URL = common_settings.FRONT_ACTIVE_ACCOUNT_URL

# user management URL
if DEBUG:
    USER_MANAGEMENT_URL = 'http://localhost:8001/'
else:
    USER_MANAGEMENT_URL = common_settings.USER_MANAGEMENT_URL

# tournament URL
if DEBUG:
    TOURNAMENT_URL = 'http://localhost:8000/'
else:
    TOURNAMENT_URL = common_settings.TOURNAMENT_URL
ALLOWED_HOSTS = ['*']

# user stats URL
if DEBUG:
    USER_STATS_URL = 'http://localhost:8002/'
else:
    USER_STATS_URL = common_settings.USER_STATS_URL
ALLOWED_HOSTS = ['*']

# cron jobs variables
MAX_INACTIVITY_DAYS_BEFORE_DELETION = 365
MAX_DAYS_BEFORE_PENDING_ACCOUNTS_DELETION = 1

# account creation rules
EMAIL_MAX_LENGTH = 60
EMAIL_LOCAL_PART_MIN_LENGTH = 1
EMAIL_VERIFICATION_TOKEN_MAX_LENGTH = 100
TLD_MAX_LENGTH = 15  # TLD stands for Top level domain ( .fr, .com ...)
USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 2
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 100

ELO_DEFAULT = 500
MAX_USERNAME_SEARCH_RESULTS = 10
FORGOT_PASSWORD_CODE_MAX_LENGTH = 6
FORGOT_PASSWORD_CODE_EXPIRATION_MINUTES = 15

# to send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# 2fa
TOTP_SECRET_MAX_LENGTH = 32
TOTP_CONFIG_URL_MAX_LENGTH = 100

# OAuth
OAUTH_STATE_MAX_LENGTH = 256
OAUTH_STATE_RANDOM_STRING_LENGTH = 16
OAUTH_SOURCE_MAX_LENGTH = 100
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize/'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token/'
GITHUB_REDIRECT_URI = f'{USER_MANAGEMENT_IP}user/oauth/callback/github/'
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_USER_PROFILE_URL = 'https://api.github.com/user'
FT_API_CLIENT_ID = os.getenv('FT_API_CLIENT_ID')
FT_API_AUTHORIZE_URL = 'https:///api.intra.42.fr/oauth/authorize/'
FT_API_ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token/'
FT_API_REDIRECT_URI = f'{USER_MANAGEMENT_IP}user/oauth/callback/42api/'
FT_API_CLIENT_SECRET = os.getenv('FT_API_CLIENT_SECRET')
FT_API_USER_PROFILE_URL = 'https://api.intra.42.fr/v2/me'

APPEND_SLASH = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('USER_MANAGEMENT_SECRET_KEY')
USER_MANAGEMENT_SECRET_KEY = os.getenv('USER_MANAGEMENT_SECRET_KEY')

# Json Web Tokens
USER_MANAGEMENT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ACCESS_PRIVATE_KEY = open(f'{USER_MANAGEMENT_FOLDER}/src/private_access_jwt_key.pem').read()
ACCESS_PUBLIC_KEY = common_settings.ACCESS_PUBLIC_KEY
REFRESH_KEY = os.getenv('REFRESH_KEY')
REFRESH_EXPIRATION_MINUTES = 60 * 24 * 30
ACCESS_EXPIRATION_MINUTES = 15

# avatar
MAX_IMAGE_SIZE = 1000000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
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
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['https://*']

ROOT_URLCONF = 'user_management.urls'

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

WSGI_APPLICATION = 'user_management.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# #SQLite 3 for debugs and tests

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
                'NAME': os.environ.get('POSTGRES_DB'),
                'USER': os.environ.get('POSTGRES_USER'),
                'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
                'HOST': os.environ.get('POSTGRES_HOST'),
                'PORT': os.environ.get('POSTGRES_PORT'),
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
STATIC_ROOT = BASE_DIR / 'user/static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
