from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# CSRF Trusted Origins (para producción con HTTPS)
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default=''
).split(',') if config('CSRF_TRUSTED_ORIGINS', default='') else []

TIME_ZONE = config('TIME_ZONE', default='UTC')
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',  # django-csp para Content-Security-Policy
    # Local apps
    'accounts',
    'services',
    'bookings',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir static files en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',  # Content-Security-Policy
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url

# SQLite para desarrollo, PostgreSQL para producción (Render)
if config('DATABASE_URL', default=None):
    # Producción: PostgreSQL desde DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = LANGUAGE_CODE

TIME_ZONE = TIME_ZONE

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise configuration (producción)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@spahotel.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='admin@spahotel.com')


# ========== SECURITY HEADERS ==========

# XSS Protection (Navegadores antiguos)
SECURE_BROWSER_XSS_FILTER = True

# Clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# Content-Type sniffing prevention
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer Policy (Privacidad)
REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Cookie Security (condicional por DEBUG)
if not DEBUG:
    # PRODUCCIÓN: Solo HTTPS
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    # DESARROLLO: HTTP local
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

# Always secure these (dev y prod)
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# Content-Security-Policy (compatible con Bootstrap + HTMX + Forms)
# Formato django-csp 4.0+
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': (
            "'self'",
            "'unsafe-inline'",  # Django admin forms
            'cdn.jsdelivr.net',  # Bootstrap JS
            'unpkg.com',  # HTMX
        ),
        'style-src': (
            "'self'",
            "'unsafe-inline'",  # Inline styles en templates
            'cdn.jsdelivr.net',  # Bootstrap CSS
        ),
        'img-src': ("'self'", 'data:'),
        'font-src': (
            "'self'",
            'cdn.jsdelivr.net',
            'data:',
        ),
        'connect-src': ("'self'",),
        'frame-ancestors': ("'none'",),  # Bloquea iframes
        'base-uri': ("'self'",),
        'form-action': ("'self'",),
    }
}

# Remover las configuraciones antiguas de django-csp < 4.0
# CSP_DEFAULT_SRC = ...
# CSP_SCRIPT_SRC = ...
# etc.

# HSTS (Solo producción, DESPUÉS de HTTPS comprobado)
# Descomenta cuando HTTPS esté comprobado en producción
# if not DEBUG:
#     SECURE_HSTS_SECONDS = 31536000  # 1 año
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True


# ========== LOGGING CONFIGURATION ==========

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'bookings': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'services': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'dashboard': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

