# 🔒 SECURITY FIX - QUICK REFERENCE CARD

## ⚡ CRITICAL - DO THIS FIRST

### 1. Update .env RIGHT NOW
```env
# Change this:
DEBUG=True

# To this:
DEBUG=False

# Replace your SECRET_KEY with this new one:
SECRET_KEY=d-ri&v*ow5u1e3!0&w@_(p%@t00)!_1^n^kj6nuhgkw&wzv^f4
```

### 2. Rotate Database Password
1. Go to: https://console.neon.tech
2. Select your project: `ep-fragrant-cake-a1l57i7a`
3. Go to Settings → Reset Password
4. Copy new password
5. Update in .env:
```env
DATABASE_URL=postgresql://neondb_owner:NEW_PASSWORD@ep-fragrant-cake-a1l57i7a-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
DB_PASSWORD=NEW_PASSWORD
```

### 3. Regenerate Google Maps Keys
1. Go to: https://console.cloud.google.com/apis/credentials
2. Delete old keys: `AIzaSyD5Y9oWfPh5DUVlLHneB0SUN6VOoOmqXEM` and `AIzaSyB3wLCd2CoZusuxmL-pHqVcX57wU6onls4`
3. Create new Client Key with restrictions:
   - Type: HTTP referrer
   - Restrictions: `http://localhost:3000/*` and `https://basey-fareguide-v2.vercel.app/*`
4. Create new Server Key with restrictions:
   - Type: IP addresses (or none if dynamic)
5. Update in .env:
```env
GOOGLE_MAPS_API_KEY=YOUR_NEW_CLIENT_KEY
GOOGLE_MAPS_SERVER_API_KEY=YOUR_NEW_SERVER_KEY
```

### 4. Get New Resend Key
1. Go to: https://resend.com/api-keys
2. Delete old key: `re_ScczQt6K_JkSjdhi8dGkCB7KA7bthrNSp`
3. Create new key
4. Update in .env:
```env
RESEND_API_KEY=YOUR_NEW_RESEND_KEY
```

---

## 🛠️ FIX SETTINGS.PY

### Add Rate Limiting
In `bfg/settings.py`, update `REST_FRAMEWORK` dict to include:

```python
REST_FRAMEWORK = {
    # ... existing settings ...
    
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
```

### Remove SECRET_KEY Default
Find this line in `settings.py`:
```python
SECRET_KEY = config('SECRET_KEY', default="django-insecure-n1lolh=...")
```

Change to:
```python
SECRET_KEY = config('SECRET_KEY')  # No default - will fail if missing
```

### Add Security Headers
Add these lines after `TIME_ZONE` in `settings.py`:

```python
# Security Settings (Production)
if not DEBUG:
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
```

### Fix CORS for Production
Update `CORS_ALLOWED_ORIGINS` in `settings.py`:

```python
# Production CORS
CORS_ALLOWED_ORIGINS = [
    "https://basey-fareguide-v2.vercel.app",
]

# Add localhost only in development
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
```

---

## ✅ TEST BEFORE DEPLOY

### 1. Test Locally with DEBUG=False
```bash
# Update .env
DEBUG=False

# Test the server
python manage.py runserver

# Try accessing:
# - http://127.0.0.1:8000/v2/locations/
# - Login functionality
# - API endpoints
```

### 2. Check for Errors
- Watch console for any errors
- Test all main features
- Verify authentication works
- Check API responses

### 3. Test Rate Limiting
```bash
# Make multiple rapid requests
for ($i=0; $i -lt 150; $i++) {
    Invoke-WebRequest -Uri "http://127.0.0.1:8000/v2/locations/" | Select-Object StatusCode
}
# Should see 429 (Too Many Requests) after 100 requests
```

---

## 🚀 DEPLOY

### Railway Deployment
1. Update environment variables in Railway dashboard
2. Deploy new version
3. Check Railway logs for errors
4. Test production URL

### Vercel Frontend
1. Update frontend .env in Vercel dashboard:
   ```env
   REACT_APP_API_URL=https://web-production-8fd2c.up.railway.app/v2
   REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_NEW_CLIENT_KEY
   ```
2. Redeploy frontend

---

## 📊 VERIFICATION CHECKLIST

After deploying, verify:

- [ ] Can access production URL
- [ ] No DEBUG information in errors
- [ ] Login works
- [ ] API endpoints respond
- [ ] HTTPS redirects work
- [ ] Rate limiting active
- [ ] Google Maps loads correctly
- [ ] Database connections work
- [ ] No 500 errors in logs

---

## 🆘 IF SOMETHING BREAKS

### Site won't load:
1. Check Railway logs: `railway logs`
2. Verify DATABASE_URL is correct
3. Check ALLOWED_HOSTS includes your domain

### 500 errors:
1. Check DEBUG is False
2. Review error logs
3. Verify all env variables set

### Database connection issues:
1. Verify new password is correct
2. Check DATABASE_URL format
3. Ensure `?sslmode=require` is in URL

### API not accessible:
1. Check CORS settings
2. Verify ALLOWED_HOSTS
3. Check frontend API_BASE_URL

---

## 📞 QUICK COMMANDS

```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Test database connection
python manage.py check --database default

# Run security check
python manage.py check --deploy

# View Railway logs
railway logs

# Test API endpoint
Invoke-WebRequest -Uri "https://web-production-8fd2c.up.railway.app/v2/locations/" -Method GET
```

---

## ⏱️ TIME ESTIMATE

- Credential rotation: 30-45 minutes
- Settings.py updates: 15-20 minutes  
- Testing: 20-30 minutes
- Deployment: 15-20 minutes

**Total: ~90 minutes**

---

## 📝 FILES TO REFERENCE

1. **SECURITY_AUDIT_REPORT.md** - Detailed findings
2. **production_settings.py** - Complete production config
3. **fix_security.py** - Security checker script

---

**Remember:** Do NOT deploy until ALL credentials are rotated!

**Status After Fixes:** Production Ready ✅

---

*Keep this card handy during deployment!*
