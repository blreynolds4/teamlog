"""
Django settings for runchat project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import date

LOCAL_DEV = ''
ExecutionEnvironment = os.getenv("TL_ENV", LOCAL_DEV)
print("Exec Env is", ExecutionEnvironment)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_VERSION = "0.0.8"

DEFAULT_SEASON_START = date(2017, 6, 18)

ACHIEVEMENTS = [50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

DATE_FORMAT = "%m-%d-%Y"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mc26vzk$^1*v(yokgxz9sett8n4f6jf)&s9$52^g_1+73!f&g5'

# SECURITY WARNING: don't run with debug turned on in production!
if ExecutionEnvironment == LOCAL_DEV:
    DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    ALLOWED_HOSTS = ["45.76.13.111", "prideruns.com", "www.prideruns.com", "aemsxcruns.com", "www.aemsxcruns.com"]

# tagging settings
FORCE_LOWERCASE_TAGS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tagging',
    'home',
    'accounts',
    'posts',
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

ROOT_URLCONF = 'runchat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'runchat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
db_conf = dict(engine='django.db.backends.postgresql_psycopg2',
               name=os.getenv('TL_DB_NAME'),
               user=os.getenv('TL_DB_USER'),
               password=os.getenv('TL_DB_PASSWORD'),
               host=os.getenv('TL_DB_HOST'),
               port=int(os.getenv('TL_DB_PORT', 0)))

print("DB Conf", db_conf)

# use sqllite when running locally
if ExecutionEnvironment == LOCAL_DEV:
    print("Using sqlite3...")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    print("Using pg db...")
    DATABASES = {
        'default': {
            'ENGINE': db_conf['engine'],
            'NAME': db_conf['name'],
            'USER': db_conf['user'],
            'PASSWORD': db_conf['password'],
            'HOST': db_conf['host'],
            'PORT': db_conf['port'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
