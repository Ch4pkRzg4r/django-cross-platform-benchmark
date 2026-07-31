"""
Django settings for ecommerce project.

ئەم فایلە دەستکاری کراوە بۆ گواستنەوە لە SQLite بۆ PostgreSQL 17.
ئێستا هەموو زانیارییە هەستیارەکان لە environment variables خوێندەوە دەکرێن
لە ڕێگەی python-decouple. بۆ production، فایلێکی .env دروست بکە.
"""

import os
from pathlib import Path
from decouple import config, Csv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS (ئاسایش)
# =============================================================================

# SECRET_KEY ئێستا لە .env خوێندەوە دەکرێت نەک hardcoded
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-CHANGE-THIS-IN-PRODUCTION-a2ukv8zjuu'
)

# DEBUG لە بنەڕەتدا False بۆ ئاسایش، لە .env فایلدا چالاک دەکرێت بۆ پەرەپێدان
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*',
    cast=Csv()
)

# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'commerce',
    'colorfield',
    'django.contrib.sites',
    'silk',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    # silk middleware لە بارودۆخی benchmark ناچالاک کراوە بۆ پاراستنی ئەنجامە وردەکان
    # 'silk.middleware.SilkyMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'commerce', 'templates')],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION - PostgreSQL 17
# =============================================================================
# گۆڕانکاری سەرەکی: لە SQLite گواسترایەوە بۆ PostgreSQL 17
# پشتگیرییەکی ئەکادیمی: Saleor و Django Oscar، دوو پلاتفۆرمی سەرەکی
# e-commerce لەسەر Django، هەردووکیان PostgreSQL بە پێویست دەزانن.
#
# PgBouncer (پۆرتی 6432) بەکار دێت بۆ connection pooling — ئەم پۆرتە
# لە docker-compose.yml دا ڕێک دەخرێت. ئەگەر ڕاستەوخۆ بە PostgreSQL
# پەیوەندی دەکەیت، DB_PORT=5432 دابنێ لە .env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='ecommerce_benchmark'),
        'USER': config('DB_USER', default='benchuser'),
        'PASSWORD': config('DB_PASSWORD', default='changeme'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='6432'),  # PgBouncer port
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'connect_timeout': 10,
            'application_name': 'ecommerce_django',
        },
    }
}

# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FIELDS = ['username', 'email*', 'password1', 'password2']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise بۆ خزمەتکردنی static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 31536000

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD=[REDACTED]

# =============================================================================
# SECURITY (CSRF & SESSIONS)
# =============================================================================

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000,http://localhost:8081,http://127.0.0.1:8000',
    cast=Csv()
)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR"}},
}

# =============================================================================
# DEFAULTS
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
