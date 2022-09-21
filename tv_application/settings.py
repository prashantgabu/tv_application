"""
Django settings for tv_application project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from firebase_admin import initialize_app

load_dotenv()
env = os.environ.get

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+51h1+&i*z-u#myrr@vs4cw3)#(_i!37hu$u(3hw7)hsc^pmk)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core",
    "fcm_django",
]

X_FRAME_OPTIONS = 'SAMEORIGIN'  # only if django version >= 3.0

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tv_application.urls'

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

WSGI_APPLICATION = 'tv_application.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.getenv("DATABASE_HOST"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER", ""),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "PORT": "",
        "CONN_MAX_AGE": 500,
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# FCM_DJANGO_SETTINGS = {
#     # default: _('FCM Django')
#     "APP_VERBOSE_NAME": "Remote Box",
#     # Your firebase API KEY
#     "FCM_SERVER_KEY": "AAAA4bkV7pg:APA91bFIs40RjKjt5_M6VLZemwa69q90fsbP5iNT7yf5MJhP_P9-O-c8xVwqywk3Z-mu09Im6z2LdOGoecrd0hDN176cXpPMHuJyOrjj3L6ActT8F5llkFTvrc0TYGiYhKByxyGdHWDR",
#     # true if you want to have only one active device per registered user at a time
#     # default: False
#     "ONE_DEVICE_PER_USER": True,
#     # devices to which notifications cannot be sent,
#     # are deleted upon receiving error response from FCM
#     # default: False
#     "DELETE_INACTIVE_DEVICES": False,
# }

RAW_FILES_DIR = str(BASE_DIR) + '/raw'
LATEST_APK_INFO = {
    'checksum': '83ae46aa6ad49d22921dad0072d52349',
    'version': 3,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.TokenAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_PAGINATION_CLASS": None,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    # "APP_VERBOSE_NAME": "",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": False,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
