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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

EMAIL_MAX_LENGTH = 60
EMAIL_LOCAL_PART_MIN_LENGTH = 1
USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 2
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 30
ELO_DEFAULT = 500
TLD_MAX_LENGTH = 15

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&r*!icx1$(sv7f-sj&ezvjxw+pljt-yz(r6yowfg18ihdu@15k'
ACCESS_KEY = 'django-insecure-&r*!icx1$(sv7f-sj&ezvjxw+pljt-yz(r6yowfg18ihdu@15k'
REFRESH_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl88VVar5X6lAlHjj4o4r
r3WoAQloSNbxjgyUd6dU3z3a8JbLibihyl/LjrfAJXCT39FzBbjcWHw7dnDkBeU0
xX8pPNESkfJI7wxzkc1WcPk1KMwvy1dTaoCub7fZxNl2oOObdzTGpic8co7VOUqa
5cJks3MTL/8ipxaf4HVJ4luvcySvPflL1woWO3QfTomL/B/Xnu9fmj2ynn8DptfY
wJEe4eFA/jx+TP3coPBgs/XYG3stdyislm574U+5QvfRi1uii8jkFgpIxwUnxYbx
mZW+X8IdGmaUnucNeF1pLZjEIcr7MkzP3zm1auQww71DObGTPaLLJNjTPdP3rWYJ
mQIDAQAB
-----END PUBLIC KEY-----"""
REFRESH_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]

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

# #SQLite 3 for local development
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# PostgreSQL for production

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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
