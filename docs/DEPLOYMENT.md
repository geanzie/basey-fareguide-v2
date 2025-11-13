# 🚀 Production Deployment Guide

## Pre-Deployment Checklist

### 1. Generate New SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Set Environment Variables
Never use development credentials in production!

```env
SECRET_KEY=<new-generated-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
GOOGLE_MAPS_API_KEY=<your-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-key>
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 3. Security Settings
Verify in `bfg/settings.py`:
- `DEBUG = False`
- `SECURE_SSL_REDIRECT = True`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`

## Deploy to Railway

### 1. Setup Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `basey-fareguide-v2`

### 2. Configure Environment Variables
In Railway dashboard → Variables:

```
SECRET_KEY=<your-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-app>.up.railway.app
DATABASE_URL=<your-database-url>
GOOGLE_MAPS_API_KEY=<your-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-key>
CORS_ALLOWED_ORIGINS=https://<frontend-url>
```

### 3. Add PostgreSQL Database
1. Click "New" → "Database" → "PostgreSQL"
2. Railway auto-generates DATABASE_URL
3. Copy and add to environment variables

### 4. Deploy
```bash
git push origin main
```

Railway automatically detects and builds from Dockerfile.

### 5. Run Migrations
In Railway terminal:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python populate_database.py  # Initial data
```

### 6. Create Admin User
```bash
python manage.py createsuperuser
```

## Deploy Frontend (Vercel)

### 1. Setup Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import `basey-fareguide-v2` repo
3. Root directory: `frontend`

### 2. Environment Variables
```
REACT_APP_API_URL=https://<your-railway-app>.up.railway.app
REACT_APP_GOOGLE_MAPS_API_KEY=<your-key>
```

### 3. Deploy
```bash
cd frontend
npm run build
```

Vercel auto-deploys on push to main.

## Alternative: Deploy with Docker

### Build Image
```bash
docker build -t basey-fareguide .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=<your-key> \
  -e DEBUG=False \
  -e DATABASE_URL=<your-db-url> \
  basey-fareguide
```

## Post-Deployment

### 1. Verify Endpoints
```bash
curl https://your-domain.com/api/locations/
```

### 2. Test Authentication
```bash
curl -X POST https://your-domain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

### 3. Check Admin Panel
Visit: `https://your-domain.com/admin/`

### 4. Monitor Logs
Railway Dashboard → Deployments → Logs

## Database Backup

### Create Backup
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restore Backup
```bash
psql $DATABASE_URL < backup.sql
```

## Custom Domain

### Railway
1. Railway Dashboard → Settings → Domains
2. Add custom domain
3. Update DNS records (CNAME)

### Vercel
1. Vercel Dashboard → Domains
2. Add domain
3. Update DNS records

## Troubleshooting

### 502 Bad Gateway
- Check Railway logs
- Verify PORT environment variable
- Ensure Dockerfile CMD is correct

### CORS Errors
- Update CORS_ALLOWED_ORIGINS
- Include frontend URL
- Redeploy backend

### Database Connection Failed
- Verify DATABASE_URL
- Check database is running
- Confirm SSL mode (sslmode=require)

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## Security Best Practices

1. **Never commit .env files**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS only (SSL redirect)**
4. **Set restrictive CORS origins**
5. **Use environment variables for all secrets**
6. **Enable database backups**
7. **Monitor logs regularly**
8. **Keep dependencies updated**

## Rollback

If deployment fails:

```bash
# Railway
railway rollback

# Git
git revert HEAD
git push origin main
```

## Monitoring

- **Railway**: Built-in metrics & logs
- **Sentry**: Error tracking (optional)
- **Uptime monitoring**: UptimeRobot, Pingdom

## Scaling

### Increase Railway Resources
Dashboard → Settings → Resources

### Database Scaling
- Upgrade Neon tier
- Enable connection pooling
- Add read replicas

## Support

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Issues: GitHub repository issues

---

**🎉 Your app is now live in production!**
