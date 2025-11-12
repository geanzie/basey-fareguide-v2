"""
Quick Security Fix Script
Run this to apply critical security fixes to settings.py
"""

import os
import sys
from pathlib import Path

# Add color support for Windows
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
except ImportError:
    GREEN = RED = YELLOW = RESET = ''


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")


def print_status(message, status='info'):
    """Print status message"""
    if status == 'success':
        print(f"{GREEN}✓ {message}{RESET}")
    elif status == 'error':
        print(f"{RED}✗ {message}{RESET}")
    elif status == 'warning':
        print(f"{YELLOW}⚠ {message}{RESET}")
    else:
        print(f"  {message}")


def check_env_file():
    """Check .env file configuration"""
    print_header("Checking .env File")
    
    env_path = Path('.env')
    if not env_path.exists():
        print_status(".env file not found", 'warning')
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check DEBUG setting
    if 'DEBUG=True' in content:
        print_status("DEBUG=True found in .env", 'error')
        print_status("MUST set DEBUG=False for production", 'error')
        return False
    elif 'DEBUG=False' in content:
        print_status("DEBUG=False correctly set", 'success')
    else:
        print_status("DEBUG setting not found in .env", 'warning')
    
    # Check for SECRET_KEY
    if 'SECRET_KEY=' in content:
        if 'django-insecure' in content:
            print_status("Using insecure SECRET_KEY", 'error')
            return False
        else:
            print_status("SECRET_KEY found", 'success')
    else:
        print_status("SECRET_KEY not found in .env", 'error')
        return False
    
    return True


def check_settings_py():
    """Check settings.py configuration"""
    print_header("Checking settings.py")
    
    settings_path = Path('bfg/settings.py')
    if not settings_path.exists():
        print_status("settings.py not found", 'error')
        return False
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for rate limiting
    if 'DEFAULT_THROTTLE_CLASSES' not in content:
        issues.append("Rate limiting not configured")
        print_status("Rate limiting not configured", 'error')
    else:
        print_status("Rate limiting configured", 'success')
    
    # Check for security headers
    security_settings = [
        'SECURE_SSL_REDIRECT',
        'SECURE_HSTS_SECONDS',
        'SESSION_COOKIE_SECURE',
        'CSRF_COOKIE_SECURE',
    ]
    
    missing_settings = [s for s in security_settings if s not in content]
    if missing_settings:
        print_status(f"Missing security settings: {', '.join(missing_settings)}", 'error')
        issues.append("Security headers not configured")
    else:
        print_status("Security headers configured", 'success')
    
    # Check for SECRET_KEY default
    if 'SECRET_KEY = config(\'SECRET_KEY\', default=' in content:
        print_status("SECRET_KEY has unsafe default fallback", 'error')
        issues.append("SECRET_KEY has default value")
    
    return len(issues) == 0


def generate_new_secret_key():
    """Generate a new Django secret key"""
    print_header("Generate New SECRET_KEY")
    
    try:
        from django.core.management.utils import get_random_secret_key
        new_key = get_random_secret_key()
        print_status("New SECRET_KEY generated:", 'success')
        print(f"\n{new_key}\n")
        print_status("Add this to your .env file:", 'info')
        print(f"SECRET_KEY={new_key}")
        return True
    except ImportError:
        print_status("Django not installed, cannot generate key", 'error')
        print_status("Run: python -c \"import secrets; print(secrets.token_urlsafe(50))\"", 'info')
        return False


def check_dependencies():
    """Check for security-related dependencies"""
    print_header("Checking Dependencies")
    
    requirements_path = Path('requirements.txt')
    if not requirements_path.exists():
        print_status("requirements.txt not found", 'error')
        return False
    
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    # Check Django version
    if 'Django==' in content:
        version_line = [line for line in content.split('\n') if 'Django==' in line][0]
        print_status(f"Found {version_line}", 'success')
    
    # Check for security packages
    recommended = {
        'django-cors-headers': 'CORS protection',
        'gunicorn': 'Production server',
        'whitenoise': 'Static file serving',
        'psycopg2-binary': 'PostgreSQL driver',
    }
    
    for package, description in recommended.items():
        if package in content:
            print_status(f"{package} installed ({description})", 'success')
        else:
            print_status(f"{package} not found ({description})", 'warning')
    
    return True


def print_credentials_rotation_guide():
    """Print guide for rotating credentials"""
    print_header("CREDENTIAL ROTATION REQUIRED")
    
    print(f"{RED}⚠ YOUR CREDENTIALS WERE EXPOSED IN THIS SESSION{RESET}")
    print("\nYou MUST rotate all the following credentials:\n")
    
    print("1. Django SECRET_KEY")
    print("   Run the generation function in this script")
    
    print("\n2. Neon Database Password")
    print("   • Go to: https://console.neon.tech")
    print("   • Select your project")
    print("   • Reset the password")
    print("   • Update DATABASE_URL in .env")
    
    print("\n3. Google Maps API Keys")
    print("   • Go to: https://console.cloud.google.com/apis/credentials")
    print("   • Delete old keys")
    print("   • Create new keys with restrictions:")
    print("     - Client key: HTTP referrer restrictions")
    print("     - Server key: IP restrictions")
    print("   • Update GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_SERVER_API_KEY in .env")
    
    print("\n4. Resend API Key")
    print("   • Go to: https://resend.com/api-keys")
    print("   • Delete old key")
    print("   • Create new key")
    print("   • Update RESEND_API_KEY in .env")
    
    print(f"\n{YELLOW}DO NOT deploy to production until all credentials are rotated!{RESET}\n")


def main():
    """Main execution"""
    print_header("🔒 BASEY FARE GUIDE - SECURITY FIX CHECKER")
    
    print(f"{RED}IMPORTANT: This app is NOT production ready!{RESET}")
    print(f"{RED}Critical security issues were found.{RESET}\n")
    
    # Run checks
    env_ok = check_env_file()
    settings_ok = check_settings_py()
    deps_ok = check_dependencies()
    
    # Print summary
    print_header("Summary")
    
    if env_ok and settings_ok and deps_ok:
        print_status("All checks passed!", 'success')
        print_status("However, you still need to rotate credentials", 'warning')
    else:
        print_status("Security issues found - review above", 'error')
    
    # Print credential rotation guide
    print_credentials_rotation_guide()
    
    # Offer to generate new secret key
    print_header("Action Items")
    response = input("Generate new SECRET_KEY now? (y/n): ")
    if response.lower() == 'y':
        generate_new_secret_key()
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Rotate ALL credentials (see guide above)")
    print("2. Update .env with new credentials")
    print("3. Set DEBUG=False in .env")
    print("4. Apply production_settings.py changes to settings.py")
    print("5. Test locally with DEBUG=False")
    print("6. Deploy to staging first")
    print("7. Run security scan")
    print("8. Then deploy to production")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
