"""
Django settings for proxima_core_engine project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-pe=!pmu^!m6c-y=8z)w4dva&dhqi!%l##j11$za6o52=n6%$vt"
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True#os.getenv("DEBUG")

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'core.proximaai.co']


# Application definition

INSTALLED_APPS = [
    # 'daphne', # new
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Custom apps
    'core_engine_auth_app',
    'core_engine_descriptive_analytics_app',
    'core_engine_chat_app',
    'core_engine_tenant_management_app',
    'core_engine_tenant_users_app',
    'core_engine_users_profile_app',
    # 'core_engine_payments_app',
    'core_engine_community_app',
    'core_engine_survey_app',
    'core_engine_social_intergtaions',
    # Installed apps
    'django_celery_results',
    'django_celery_beat',
    'django_extensions',
    # 'cacheops',
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    # 'dj_rest_auth',
    'rest_framework.authtoken'
    
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
    'core_engine_utils_app.middleware.swagger_post.SwaggerMiddleware',

]

ROOT_URLCONF = 'proxima_core_engine.urls'
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',

]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],        'APP_DIRS': True,
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

WSGI_APPLICATION = 'proxima_core_engine.wsgi.application'
# ASGI_APPLICATION = 'proxima_core_engine.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", 'proximacoreenginedb'),
        "USER": os.getenv("POSTGRES_USER", 'proximaadmin'),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", 'aTgLpUfKGhu'),
        "HOST": 'localhost',#os.getenv("DB_HOST", 'core_engine_db'),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = "django_ses.SESBackend"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

ENV_TYPE = os.getenv("ENV_TYPE", "dev")
if ENV_TYPE == "dev":
    # DOMAIN_NAME = "localhost:8000"
    # SESSION_COOKIE_DOMAIN = "localhost:8000"

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
    STATIC_URL = "/static/"
elif ENV_TYPE == "prod":

    from .server_settings import *

# celery Tasks
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


# CACHING
REDIS_CACHE = os.getenv('REDIS_CACHE', 'redis://redis:6379/1')
CACHEOPS_REDIS = REDIS_CACHE
CACHEOPS = {
    'auth.*': {'ops': 'all', 'timeout': 60 * 60 * 2},
    'payments.*': {'ops': 'all', 'timeout': 60 * 60 * 2},
}

# CELERY
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/2')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/3')
CELERY_CACHE_BACKEND = REDIS_CACHE
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_EXTENDED = True
CELERY_DISABLE_RATE_LIMITS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_RESULT_PERSISTENT = True
CELERY_IGNORE_RESULT = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "console_debug_false": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "logfile": {
            "class": "logging.FileHandler",
            "filename": "server.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
                "console_debug_false",
                "logfile",
            ],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# APPLICATION_NAME = "bottlecrm"

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

SETTINGS_EXPORT = ["APPLICATION_NAME"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core_engine_tenant_users_app.backends.JWTClientAuthentication',
        'core_engine_tenant_users_app.backends.JWTAdminAuthentication',
        'core_engine_tenant_users_app.backends.JWTEmployeeAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ],
    # 'EXCEPTION_HANDLER': 'apps.utils.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}


SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "proxima_core_engine.urls.info",
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
}

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://google.com',
    'http://hostname.example.com',
    'http://localhost:8000',
    'http://127.0.0.1:9000',
    'https://app.proximaai.co',

]
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = 'core_engine_tenant_users_app.User'



DOMAIN_NAME = 'localhost'#os.environ["DOMAIN_NAME"]
SWAGGER_ROOT_URL = 'localhost'#os.environ["SWAGGER_ROOT_URL"]

# Flutterwave
FW_TEST_SK = 'FLWSECK_TEST-91f464015dfe26899980e5f2a5728b2a-X'
FW_LIVE_SK = 'FLWSECK_TEST-be89c731faf80af6443145d22cd5546d-X'
FW_SECRET_KEY = FW_TEST_SK if DEBUG else FW_LIVE_SK

REST_AUTH = {
    'LOGIN_SERIALIZER': 'core_engine_auth_app.serializers.UserLoginSerializer',
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',

    'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    'TOKEN_CREATOR': 'dj_rest_auth.utils.default_create_token',

    'PASSWORD_RESET_USE_SITES_DOMAIN': False,
    'OLD_PASSWORD_FIELD_ENABLED': False,
    'LOGOUT_ON_PASSWORD_CHANGE': False,
    'SESSION_LOGIN': True,
    'USE_JWT': False,

}


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = False
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = 'your@djangoapp.com'
# EMAIL_HOST_PASSWORD = 'your password'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'administrator@proximaai.co'
EMAIL_HOST_PASSWORD = '@PaulFrank45'
EMAIL_USE_TLS = True  # or False if not using TLS
EMAIL_USE_SSL = False
