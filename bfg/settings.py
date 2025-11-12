"""
Django settings for bfg project.
"""

from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

# Parse ALLOWED_HOSTS from environment variable or use defaults
allowed_hosts_str = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,web-production-8fd2c.up.railway.app,.railway.app')
ALLOWED_HOSTS = [s.strip() for s in allowed_hosts_str.split(',') if s.strip()]

# Add Railway public domain if available
railway_domain = config('RAILWAY_PUBLIC_DOMAIN', default='')
if railway_domain and railway_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_domain)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    
    # Local apps
    "users",
    "locations",
    "routes",
    "fares",
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise for static files
    "corsheaders.middleware.CorsMiddleware",  # Add CORS
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bfg.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "build"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bfg.wsgi.application"

# Database - PostgreSQL
# Support both DATABASE_URL (Railway/production) and individual parameters (local)
# SECURITY: No default value - must be set in .env file
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Production: Use DATABASE_URL from Railway/Heroku/etc
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local development: Use individual parameters
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config('DB_NAME', default='basey_fare_guide'),
            "USER": config('DB_USER', default='postgres'),
            "PASSWORD": config('DB_PASSWORD', default=''),
            "HOST": config('DB_HOST', default='localhost'),
            "PORT": config('DB_PORT', default='5432'),
        }
    }

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"  # Philippine timezone
USE_I18N = True
USE_TZ = True

if not DEBUG:
    # Proxy configuration for Railway
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Security settings
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# React static files
STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "build" / "static",
] if (BASE_DIR / "frontend" / "build").exists() else []

# WhiteNoise configuration for production static file serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (uploads)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
     # Add these:
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}

# Simple JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings
# Allow requests from Vercel frontend and local development
CORS_ALLOWED_ORIGINS = [
    "https://basey-fareguide-v2.vercel.app",
]

# Add localhost only in development
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

# In production, you may want to use CORS_ALLOW_ALL_ORIGINS = True for testing
# but it's better to specify exact origins for security

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Google Maps API Keys
# Client-side key (with HTTP referrer restrictions)
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
# Server-side key (for Distance Matrix, Directions APIs - no referrer restrictions)
GOOGLE_MAPS_SERVER_API_KEY = config('GOOGLE_MAPS_SERVER_API_KEY', default='')

# File Upload Settings
MAX_UPLOAD_SIZE = 5242880  # 5MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
