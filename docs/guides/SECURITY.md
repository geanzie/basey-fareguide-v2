# Security Guidelines

## Environment Variables Setup

This project uses environment variables to manage sensitive configuration. **NEVER commit `.env` files to Git.**

### Initial Setup

1. **Backend Setup (.env in root directory)**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and fill in your actual values:
   - `SECRET_KEY`: Generate a strong random string (50+ characters)
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `DB_PASSWORD`: Your database password
   - `JWT_SECRET`: Generate a strong random string (different from SECRET_KEY)
   - `GOOGLE_MAPS_API_KEY`: Your Google Maps API key (client-side)
   - `GOOGLE_MAPS_SERVER_API_KEY`: Your Google Maps API key (server-side)
   - `RESEND_API_KEY`: Your Resend API key for email services

2. **Frontend Setup (.env in frontend directory)**
   ```bash
   cd frontend
   cp .env.example .env
   ```
   
   Then edit `frontend/.env` and fill in:
   - `REACT_APP_API_URL`: Your API endpoint (default: http://localhost:8000/api)
   - `REACT_APP_GOOGLE_MAPS_API_KEY`: Your Google Maps API key

### Generating Secret Keys

**For Django SECRET_KEY and JWT_SECRET:**
```python
# In Python shell
import secrets
print(secrets.token_urlsafe(50))
```

Or use online generators (ensure they're from trusted sources).

### API Keys Required

1. **Google Maps API Keys** (https://console.cloud.google.com/)
   - Client-side key: Restrict to HTTP referrers (your domain)
   - Server-side key: Restrict to IP addresses or use separate key
   - Enable APIs: Maps JavaScript API, Geocoding API, Directions API, Distance Matrix API

2. **Resend API Key** (https://resend.com/api-keys)
   - Used for sending password reset emails
   - Free tier available for testing

3. **PostgreSQL Database**
   - You can use Neon (https://neon.tech) for free PostgreSQL hosting
   - Or run PostgreSQL locally

## What's Protected

The `.gitignore` file ensures these sensitive files are never committed:
- `.env` files (all variants)
- Virtual environments (`BFG-env/`, `venv/`, etc.)
- Database files
- Python cache files
- Node modules
- Build directories

## Before Committing

Always check what you're about to commit:
```bash
git status
git diff
```

If you accidentally committed sensitive data:
1. **Immediately** rotate all exposed credentials
2. Remove from Git history (contact your team lead)
3. Update `.env` with new credentials

## Production Deployment

For production environments:
- Set `DEBUG=False` in `.env`
- Use strong, unique passwords for each service
- Enable API key restrictions (referrers, IPs)
- Use environment variables provided by your hosting platform
- Never use the example values in production

## Need Help?

If you believe credentials have been exposed:
1. Rotate the credentials immediately
2. Document what was exposed and when
3. Notify the project maintainers

## Checklist Before First Commit

- [ ] `.env` files are listed in `.gitignore`
- [ ] `.env` files are created from `.env.example` with real values
- [ ] No API keys or passwords in source code
- [ ] No `.env` files staged for commit (`git status` should not show them)
- [ ] All secrets use environment variables via `config()` or `process.env`
