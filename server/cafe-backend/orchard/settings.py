"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

AUTH_USER_MODEL = "cafe.User"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0%u5im)hfu55qv54d4f+$3@ijy+%gxq%49cm#b@-vq)z7g6y93'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['seal-epic-luckily.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://seal-epic-luckily.ngrok-free.app']

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',

    'rules.permissions.ObjectPermissionBackend',
]

LOGIN_REDIRECT_URL = "/"

# Application definition

INSTALLED_APPS = [
    'cafe',
    'django_bridge',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',

    'huey.contrib.djhuey',

    'rules',

    'hijack',
    'hijack.contrib.admin'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
    'django_bridge.middleware.DjangoBridgeMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_DISPLAY = lambda user: user.get_short_name()

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_ADAPTER = 'cafe.social_adapter.CafeSocialAccountAdapter'
SOCIALACCOUNT_ONLY = True
SOCIALACCOUNT_PROVIDERS = {
    'discord': {
        'EMAIL_AUTHENTICATION': True,
        'VERIFIED_EMAIL': True,
        'SCOPE': ['email', 'identify'],
        'APP': {
            'client_id': os.environ['DISCORD_CLIENT_ID'],
            'secret': os.environ['DISCORD_CLIENT_SECRET'],
            'key': ''
        }
    }
}

DISCORD_PUBLIC_KEY = os.environ['DISCORD_PUBLIC_KEY']
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
DOMAIN_URL = os.environ['DOMAIN_URL']

DJANGO_BRIDGE = {
    "CONTEXT_PROVIDERS": {
        "csrf_token": "cafe.contexts.csrf_token.csrf_token",
        "user": "cafe.contexts.user.user"
    },
    "VITE_DEVSERVER_URL": "http://localhost:5173/static",
}

ROOT_URLCONF = 'orchard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'cafe/templates/')
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

WSGI_APPLICATION = 'orchard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# https://gcollazo.com/optimal-sqlite-settings-for-django/
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "init_command": (
                "PRAGMA foreign_keys=ON;"
                "PRAGMA journal_mode = WAL;"
                "PRAGMA synchronous = NORMAL;"
                "PRAGMA busy_timeout = 5000;"
                "PRAGMA temp_store = MEMORY;"
                "PRAGMA mmap_size = 134217728;"
                "PRAGMA journal_size_limit = 67108864;"
                "PRAGMA cache_size = 2000;"
            ),
            "transaction_mode": "IMMEDIATE",
        },
    },
}

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

NUMBER_OF_WORKERS = int(os.environ['NUMBER_OF_WORKERS'])



# settings.py
HUEY = {
    'huey_class': 'huey.PriorityRedisExpireHuey',  # Huey implementation to use.
    'name': 'orchard',
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': False, 
    'utc': True,  # Use UTC for all times internally.
    'blocking': True,  # Perform blocking pop rather than poll Redis.
    'connection': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': 0,
        'max_connections': 10,
        'read_timeout': 2,  # If not polling (blocking pop), use timeout.
    },
    'consumer': {
        'workers': NUMBER_OF_WORKERS,
        'worker_type': 'process',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 1,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

S3_API_URL = os.environ["S3_API_URL"]
S3_ACCESS_KEY_ID = os.environ["S3_ACCESS_KEY_ID"]
S3_SECRET_ACCESS_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
S3_REGION = os.environ["S3_REGION"]
S3_PUBLIC_CDN_URL = os.environ["S3_PUBLIC_CDN_URL"]
