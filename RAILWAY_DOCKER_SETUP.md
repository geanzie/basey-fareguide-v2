# Railway Docker Deployment - Quick Reference

## ✅ What Was Fixed

1. **Dockerfile Updated** - Now installs Node.js 20 and builds React frontend inside Docker
2. **Frontend Fixed** - Removed as gitlink, added as regular directory
3. **package-lock.json** - Regenerated to fix sync issues
4. **dockerignore** - Updated to include frontend source but exclude build artifacts

## 🚀 Deployment Steps

### 1. Railway Will Auto-Deploy
Since you pushed to GitHub, Railway will automatically:
- Detect the `railway.json` file
- Use the `Dockerfile` to build
- Install Node.js 20 inside the container
- Build your React app
- Serve everything with Django + Gunicorn

### 2. Set Environment Variables in Railway

Go to Railway Dashboard → Your Service → **Variables**:

```env
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=your-postgresql-url
GOOGLE_MAPS_API_KEY=your-key
GOOGLE_MAPS_SERVER_API_KEY=your-key
RESEND_API_KEY=your-key
ALLOWED_HOSTS=.railway.app
```

### 3. Generate Domain

1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Get your URL: `https://your-app.up.railway.app`
4. Update `ALLOWED_HOSTS` to include your domain

### 4. Run Database Migrations

```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login and link
railway login
railway link

# Run migrations
railway run python manage.py migrate

# Populate locations
railway run python populate_basey_locations.py

# Create superuser (optional)
railway run python manage.py createsuperuser
```

## 🐳 How Docker Build Works

```
1. Starts with Python 3.11
2. Installs PostgreSQL client + Node.js 20
3. Installs Python dependencies (Django, etc.)
4. Copies frontend code
5. Runs `npm ci` to install React dependencies
6. Runs `npm run build` to build React
7. Runs `collectstatic` to collect all static files
8. Serves with Gunicorn on port 8000
```

## 📝 Key Files

- **Dockerfile** - Builds both backend and frontend
- **railway.json** - Tells Railway to use Docker
- **.dockerignore** - Excludes unnecessary files
- **docker-compose.yml** - For local development

## 🔍 Monitoring Deployment

Watch your Railway deployment:
1. Go to Railway Dashboard
2. Click on your service
3. View **"Deployments"** tab
4. Check build logs in real-time

## ✨ Benefits of This Setup

✅ Single Docker container for both frontend and backend  
✅ No separate frontend deployment needed  
✅ Django serves React as static files  
✅ Consistent builds across environments  
✅ Easy to scale and maintain  

## 🆘 Troubleshooting

**Build fails at npm ci?**
- Make sure `package-lock.json` is committed
- Run `npm install` locally and commit changes

**Frontend not loading?**
- Check that `ALLOWED_HOSTS` includes your Railway domain
- Verify `STATIC_ROOT` in Django settings
- Check Railway logs for errors

**Database errors?**
- Ensure `DATABASE_URL` is set in Railway
- Run migrations using `railway run python manage.py migrate`
