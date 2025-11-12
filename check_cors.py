"""
Quick CORS Diagnostic Script
Checks if CORS headers are properly configured
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfg.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("CORS Configuration Diagnostic")
print("=" * 60)

print(f"\nDEBUG mode: {settings.DEBUG}")
print(f"\nALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

print(f"\nCORS_ALLOWED_ORIGINS:")
for origin in settings.CORS_ALLOWED_ORIGINS:
    print(f"  - {origin}")

print(f"\nCORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")

print(f"\nCORS_ALLOW_METHODS:")
for method in settings.CORS_ALLOW_METHODS:
    print(f"  - {method}")

print(f"\nCORS_ALLOW_HEADERS:")
for header in settings.CORS_ALLOW_HEADERS:
    print(f"  - {header}")

if hasattr(settings, 'CORS_EXPOSE_HEADERS'):
    print(f"\nCORS_EXPOSE_HEADERS:")
    for header in settings.CORS_EXPOSE_HEADERS:
        print(f"  - {header}")

if hasattr(settings, 'CORS_PREFLIGHT_MAX_AGE'):
    print(f"\nCORS_PREFLIGHT_MAX_AGE: {settings.CORS_PREFLIGHT_MAX_AGE}")

print("\n" + "=" * 60)

# Check if corsheaders is in INSTALLED_APPS
if 'corsheaders' in settings.INSTALLED_APPS:
    print("✓ corsheaders is in INSTALLED_APPS")
else:
    print("✗ ERROR: corsheaders is NOT in INSTALLED_APPS")
    sys.exit(1)

# Check if CorsMiddleware is in MIDDLEWARE
cors_middleware_found = False
for middleware in settings.MIDDLEWARE:
    if 'cors' in middleware.lower():
        print(f"✓ CORS middleware found: {middleware}")
        cors_middleware_found = True
        break

if not cors_middleware_found:
    print("✗ ERROR: CORS middleware NOT found in MIDDLEWARE")
    sys.exit(1)

print("\n" + "=" * 60)
print("Configuration looks good!")
print("=" * 60)
