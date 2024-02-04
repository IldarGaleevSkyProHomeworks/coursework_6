"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import json
import locale
import logging.config
from pathlib import Path

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)
DEBUG_MAIL = env.bool('DEBUG_MAIL', False)
DISABLE_PASSWORD_VALIDATION = env.bool('DISABLE_PASSWORD_VALIDATION', False)

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])
SITE_ID = env.int('SITE_ID', 1)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "django_crontab",
    "django_bootstrap5",
    "captcha",

    "app_accounts",
    "app_mailing",
    "app_logging",
    "app_blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
if DEBUG and DISABLE_PASSWORD_VALIDATION:
    AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'en-us')

TIME_ZONE = env.str('TIME_ZONE', 'UTC')
# DATE_INPUT_FORMATS = [
#     '%d/%m/%Y',
#     '%d.%m.%Y'
# ]

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

BOOTSTRAP5 = {
    "css_url": {
        "url": f'/{STATIC_URL}css/bootstrap.min.css'
    },

    "javascript_url": {
        "url": f'/{STATIC_URL}js/bootstrap.bundle.min.js'
    },

}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'app_accounts.User'
LOGOUT_REDIRECT_URL = reverse_lazy('app_accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('app_accounts:user_detail')

CAPTCHA_BACKGROUND_COLOR = '#212529'
CAPTCHA_FOREGROUND_COLOR = '#dee2e6'
CAPTCHA_FONT_SIZE = 26

POPULAR_ARTICLES_COUNT = env.int('POPULAR_ARTICLES_COUNT', 5)

log_config_file = env.str('LOGGING_CONFIG_FILE', None)
if log_config_file:
    try:
        with open(log_config_file, encoding='utf-8') as f:
            log_config = json.load(f)
            LOGGING_CONFIG = None
            logging.config.dictConfig(log_config)
    except Exception as e:
        print(f'Log file open error: {e}')

if DEBUG_MAIL:
    EMAIL_BACKEND = env.str('EMAIL_BACKEND', 'django.core.mail.backends.filebased.EmailBackend')
    EMAIL_FILE_PATH = BASE_DIR / 'tmp/email'
else:
    EMAIL_BACKEND = env.str('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_FILE_PATH = env.str('EMAIL_FILE_PATH', None)
    EMAIL_HOST = env.str('EMAIL_HOST')
    EMAIL_PORT = env.int('EMAIL_PORT', 465)
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', False)
    EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', True)
    DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

ACCOUNT_SERVICE_MAIL_RETRY_COUNT = env.int('ACCOUNT_SERVICE_MAIL_RETRY_COUNT', 3)
ACCOUNT_SERVICE_MAIL_TASK_TTL = env.int('ACCOUNT_SERVICE_MAIL_TASK_TTL', 30 * 60)

BACKGROUND_TASK_MANAGER = {
    "redis": {
        "hostname": env.str('BG_TASK__REDIS_HOSTNAME', 'localhost'),
        "port": env.int('BG_TASK__REDIS_PORT', 6379),
        "db_id": env.int('BG_TASK__REDIS_DB', 1)
    }
}

CRONJOBS = [
    # Каждый день, неделю и месяц
    ('1 0 * * *', 'app_mailing.cronjobs.schedule_daily'),
    ('1 0 * * 0', 'app_mailing.cronjobs.schedule_weekly'),
    ('0 0 1 * *', 'app_mailing.cronjobs.schedule_monthly'),

    # Попытка повторной отправки в 6 и 12 часов каждый день
    ('0 6 * * *', 'app_mailing.cronjobs.schedule_resend'),
    ('0 12 * * *', 'app_mailing.cronjobs.schedule_resend'),

    # Фоновые задачи каждую минуту
    ('* * * * *', 'app_accounts.cronjobs.run_scheduled'),
]
