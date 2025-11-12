"""
Production Security Settings for Basey Fare Guide
Add these settings to your settings.py when deploying to production
"""

from decouple import config

# =============================================================================
# CRITICAL PRODUCTION SETTINGS
# =============================================================================

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = False  # MUST be False in production

# SECURITY WARNING: keep the secret key used in production secret!
# Remove any default value - force environment variable
SECRET_KEY = config('SECRET_KEY')  # No default - will fail if missing

# =============================================================================
# SECURITY HEADERS & HTTPS
# =============================================================================

# Redirect all HTTP traffic to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
# Tells browsers to only use HTTPS for your site
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies security
SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True     # Only send CSRF cookie over HTTPS
SESSION_COOKIE_HTTPONLY = True # Prevent JavaScript access to session cookie
CSRF_COOKIE_HTTPONLY = True    # Prevent JavaScript access to CSRF cookie

# Security headers
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking

# =============================================================================
# RATE LIMITING & THROTTLING
# =============================================================================

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
        # Remove BrowsableAPIRenderer in production for security
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # Add rate limiting
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',    # Anonymous users: 100 requests per hour
        'user': '1000/hour',   # Authenticated users: 1000 requests per hour
        'login': '5/minute',   # Login attempts: 5 per minute (add custom throttle)
    }
}

# =============================================================================
# CORS CONFIGURATION (Production)
# =============================================================================

# Only allow requests from your production frontend
CORS_ALLOWED_ORIGINS = [
    "https://basey-fareguide-v2.vercel.app",
    # Add your Railway backend domain if serving API separately
    # "https://your-backend.railway.app",
]

# Don't allow all origins in production
# CORS_ALLOW_ALL_ORIGINS = False  # NEVER set to True in production

CORS_ALLOW_CREDENTIALS = True

# Restrict allowed methods if needed
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# =============================================================================
# ALLOWED HOSTS (Production)
# =============================================================================

# Only allow requests from these domains
ALLOWED_HOSTS = [
    'web-production-8fd2c.up.railway.app',
    '.railway.app',
    'basey-fareguide-v2.vercel.app',
]

# Add Railway public domain dynamically
railway_domain = config('RAILWAY_PUBLIC_DOMAIN', default='')
if railway_domain and railway_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_domain)

# =============================================================================
# LOGGING & MONITORING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
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
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# =============================================================================
# CONTENT SECURITY POLICY (Optional but Recommended)
# =============================================================================

# Install: pip install django-csp
# Then add to MIDDLEWARE: 'csp.middleware.CSPMiddleware'

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://maps.googleapis.com",
    "https://www.googletagmanager.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",  # Required for some inline styles
    "https://fonts.googleapis.com",
)
CSP_IMG_SRC = (
    "'self'",
    "data:",
    "https://maps.googleapis.com",
    "https://maps.gstatic.com",
)
CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://maps.googleapis.com",
)

# =============================================================================
# DATABASE CONFIGURATION (Production)
# =============================================================================

# Ensure SSL mode is required for database connections
DATABASES = {
    "default": {
        # ... your database config ...
        "OPTIONS": {
            "sslmode": "require",  # Force SSL
        }
    }
}

# =============================================================================
# ADMIN SECURITY
# =============================================================================

# Consider changing admin URL from /admin/ to something obscure
# In urls.py: path("secret-admin-url/", admin.site.urls)

# Restrict admin access to specific IPs (optional)
ADMIN_ALLOWED_IPS = config('ADMIN_ALLOWED_IPS', default='').split(',')

# =============================================================================
# SESSION SECURITY
# =============================================================================

SESSION_COOKIE_AGE = 3600  # 1 hour (adjust as needed)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# =============================================================================
# PASSWORD VALIDATION (Enhanced)
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Increased from 8
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# FILE UPLOAD SECURITY
# =============================================================================

# Restrict file upload size
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Allowed file types (already in your settings, but verify)
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

# =============================================================================
# GOOGLE MAPS API SECURITY
# =============================================================================

# Ensure your Google Maps API keys have proper restrictions:
# Client Key: HTTP referrer restrictions (your frontend domains)
# Server Key: IP restrictions (your server IPs) or no restrictions

# Never expose server key to frontend
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')  # Client-side key
GOOGLE_MAPS_SERVER_API_KEY = config('GOOGLE_MAPS_SERVER_API_KEY')  # Server-side only

# =============================================================================
# ERROR REPORTING (Optional - Sentry Integration)
# =============================================================================

# Install: pip install sentry-sdk
# Uncomment and configure:

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# sentry_sdk.init(
#     dsn=config('SENTRY_DSN', default=''),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=0.1,
#     send_default_pii=False,  # Don't send user data to Sentry
#     environment='production',
# )

# =============================================================================
# ADDITIONAL SECURITY MIDDLEWARE (Optional)
# =============================================================================

# Install django-axes for brute force protection
# pip install django-axes
# Add to INSTALLED_APPS: 'axes'
# Add to MIDDLEWARE: 'axes.middleware.AxesMiddleware'

# Configuration for django-axes
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # Lock for 1 hour
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True

# =============================================================================
# CHECKLIST BEFORE DEPLOYING
# =============================================================================

"""
CRITICAL CHECKLIST:
[ ] Set DEBUG = False
[ ] Rotate SECRET_KEY (generate new one)
[ ] Rotate database password
[ ] Regenerate Google Maps API keys with restrictions
[ ] Get new Resend API key
[ ] Update ALLOWED_HOSTS with production domains
[ ] Update CORS_ALLOWED_ORIGINS with production domains
[ ] Test with DEBUG=False locally
[ ] Enable HTTPS redirect
[ ] Verify SSL certificates
[ ] Set up error monitoring (Sentry)
[ ] Configure logging
[ ] Test rate limiting
[ ] Review admin security
[ ] Set up automated backups
[ ] Run security scan (OWASP ZAP)
[ ] Load test the application
[ ] Set up monitoring and alerts
"""
