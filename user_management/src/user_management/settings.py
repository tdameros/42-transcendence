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

BASE_DIR = Path(__file__).resolve().parent.parent

CRON_SCRIPT_PATH = os.path.join(BASE_DIR, 'commands')
COMMANDS_LOG_PATH = os.path.join(CRON_SCRIPT_PATH, 'commands.log')

CRONJOBS = [
    ('0 0 * * *', 'myapp.commands.delete_inactive_users', f'>> {COMMANDS_LOG_PATH} 2>&1'),
]

MAX_INACTIVITY_DAYS_BEFORE_DELETION = 365

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_MAX_LENGTH = 60
EMAIL_LOCAL_PART_MIN_LENGTH = 1
EMAIL_VERIFICATION_TOKEN_MAX_LENGTH = 100
USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 2
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 100
ELO_DEFAULT = 500
TLD_MAX_LENGTH = 15
FORGOT_PASSWORD_CODE_MAX_LENGTH = 6
FORGOT_PASSWORD_CODE_EXPIRATION_MINUTES = 15
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
MAX_USERNAME_SEARCH_RESULTS = 10

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
GITHUB_REDIRECT_URI = 'https://localhost:6002/user/oauth/callback/github/'
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_USER_PROFILE_URL = 'https://api.github.com/user'
FT_API_CLIENT_ID = os.getenv('FT_API_CLIENT_ID')
FT_API_AUTHORIZE_URL = 'https:///api.intra.42.fr/oauth/authorize/'
FT_API_ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token/'
FT_API_REDIRECT_URI = 'https://localhost:6002/user/oauth/callback/42api/'
FT_API_CLIENT_SECRET = os.getenv('FT_API_CLIENT_SECRET')
FT_API_USER_PROFILE_URL = 'https://api.intra.42.fr/v2/me'

APPEND_SLASH = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&r*!icx1$(sv7f-sj&ezvjxw+pljt-yz(r6yowfg18ihdu@15k'  # TODO ask Tom if we can delete this
REFRESH_KEY = 'WE_SOULD_ALSO_CHANGE_THIS_KEY'  # TODO change this key
ACCESS_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCXzxVVqvlfqUCU
eOPijiuvdagBCWhI1vGODJR3p1TfPdrwlsuJuKHKX8uOt8AlcJPf0XMFuNxYfDt2
cOQF5TTFfyk80RKR8kjvDHORzVZw+TUozC/LV1NqgK5vt9nE2Xag45t3NMamJzxy
jtU5SprlwmSzcxMv/yKnFp/gdUniW69zJK89+UvXChY7dB9OiYv8H9ee71+aPbKe
fwOm19jAkR7h4UD+PH5M/dyg8GCz9dgbey13KKyWbnvhT7lC99GLW6KLyOQWCkjH
BSfFhvGZlb5fwh0aZpSe5w14XWktmMQhyvsyTM/fObVq5DDDvUM5sZM9ossk2NM9
0/etZgmZAgMBAAECggEAA7hZZ34HGmcFZB4KR5UAUQ5rDYtzeMV7qeV5Be2d0NKt
ONQZLMjPfiwWyuqJ1OELXqK9VNiQ3cI9msttaw+Q2X4iPpFJCTaMvv7pHhuQELiq
qtNGII+FRcjdfXNd7Mr/czXgq20pqQyxGIWTiBHh9dtrqFIbmEOCT+HoDRISu29G
EjBetmvVZFUOcnRsbleYC1SQkzSRQfF8r49EhKMUdjm4UqWoMXlZhyShS5skiTwx
1I12L52YkDLvzldUnFbB8FJwr7QaWO+WjhTCaIzWhTicL1SQKPY4OGvgc/MsgZg9
K6bLz5RDDeshP1sfPcXvX0i7IQyYFyXy3VI0XcRXWQKBgQDQTXLwqjahNQai39pS
Sv9WWlNcuOvyoLa1dd62jW3/yTBXsucolps5On5R1mz5gWgnzEqkC8RIR2jH8+qc
pKXo8SlVlPtIF2JX1/eU0W64IXOnP+GmpbhL+9J2wr9FJOH7g0krjJ3hiN2WIgU/
D89MNNHitIbcL5HrMNDE3mA1MwKBgQC6kgR9ajqRGiGc4VwhX/08f5bvnhmrD2f2
7z+w5ngEwNVfg3adKn4KpwkyIDOt6W5GqnsE8aTDBru9SarHO0W/8Stx7CgkRwjw
WVL+0cir6SDo6EkcoO8hpAV3LOj8stY5LLL+IgFmf3TNl+AfyWu1yeDmITkU79nf
jzutO/DuAwKBgGmEMgszTgUPRVNQLdmt3/YwPzYi/nKjcqotESpMLkJ5+aETIQFw
eSTeOoreIcmqAcbXN6AtzboHYk6XgmrjBKAhOZz+oON95PU2k1WxWXKwj1NTiszN
+bOT1qMON7Gg41ByyqfizT8oA4c/qISvT4T85K0AYag7+KC406hGNVn9AoGBAK0X
+chtvSaQSu0k/HgOeYEekud/FCtroLYuJDY4rNMkIRJ7gpmwKb4yWMrDq47HisNP
OdFNa+JxJc8pQKOVL1I0K22Hf3qg2P88sE6wTXCJWzobAHHqMdJRPazi4spIFY54
FRzIaeoxiCmSpaJ4GlFPmjOIUVBGcyoB1okTmqUHAoGAaZvBn10vGBRkK8G3wKYu
lfXCoz40jhE4N1kidOYBGwPPWyF5OYbhZjCWI2Pq8ldB4hU/bz8eLobrPs4i15Dz
mZpeFfyRNLuFLV4U8B9TKtLXKqM5ttR+T4qVu6emm9w7sk3XsFpUPHtl6Q8y90qe
i16cG6lJDF0tN7qwIIDcKYs=
-----END PRIVATE KEY-----"""
REFRESH_EXPIRATION_MINUTES = 60 * 24 * 30
ACCESS_EXPIRATION_MINUTES = 15

# avatar
MAX_IMAGE_SIZE = 1000000

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False

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
                'NAME': 'mydatabase',
                'USER': 'myuser',
                'PASSWORD': 'mypassword',
                'HOST': 'user-management-db',
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
STATIC_ROOT = BASE_DIR / 'user/static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USER_MANAGEMENT_SECRET_KEY = os.getenv('USER_MANAGEMENT_SECRET_KEY')
