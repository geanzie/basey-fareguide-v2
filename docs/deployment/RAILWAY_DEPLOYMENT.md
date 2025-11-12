# Railway Deployment Guide for Basey Fare Guide

This guide will walk you through deploying your Django backend to Railway.

## ✅ Preparation Complete

The following files have been created/updated for Railway:
- `Procfile` - Tells Railway how to run your app
- `runtime.txt` - Specifies Python version
- `railway.json` - Railway configuration
- `requirements.txt` - Updated with gunicorn and whitenoise
- `bfg/settings.py` - Updated for production deployment

## 🚀 Step-by-Step Deployment

### 1. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Login" and sign up with GitHub (recommended)
3. Verify your email

### 2. Create New Project
1. Click "New Project" button
2. Select "Deploy from GitHub repo"
3. If this is your first time:
   - Click "Configure GitHub App"
   - Give Railway access to your repository
4. Select the `basey-fareguide-v2` repository
5. Click "Deploy Now"

### 3. Add PostgreSQL Database
1. In your Railway project dashboard, click "New"
2. Select "Database"
3. Choose "PostgreSQL"
4. Railway will automatically create a database and set the `DATABASE_URL` environment variable

### 4. Configure Environment Variables
1. Click on your Django service (not the database)
2. Go to "Variables" tab
3. Add the following variables:

```
SECRET_KEY=your-production-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,basey-fareguide-v2.vercel.app
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
GOOGLE_MAPS_SERVER_API_KEY=your-server-side-google-maps-api-key
```

**Important Notes:**
- `SECRET_KEY`: Generate a new one (never use your development key)
  - You can generate one at: https://djecrety.ir/
- `ALLOWED_HOSTS`: Replace `your-app-name` with your actual Railway domain
- Railway automatically sets `DATABASE_URL` - don't add it manually

### 5. Generate Django Secret Key
Run this command locally to generate a secure secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as your `SECRET_KEY` in Railway.

### 6. Deploy and Monitor
1. Railway will automatically deploy your app
2. Watch the deployment logs in the "Deployments" tab
3. Wait for the build to complete (usually 3-5 minutes)
4. Look for messages like:
   - ✅ "Collecting static files"
   - ✅ "Running migrations"
   - ✅ "Starting gunicorn"

### 7. Get Your Backend URL
1. Go to "Settings" tab in your Django service
2. Scroll to "Domains" section
3. Click "Generate Domain"
4. Your URL will be something like: `https://basey-fare-guide-production.up.railway.app`
5. **Copy this URL** - you'll need it for Vercel!

### 8. Populate the Database
After deployment, you need to add the Basey locations to your production database.

**Option A: Using Railway CLI** (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run the populate script
railway run python populate_basey_locations.py
```

**Option B: Using Django Admin**
1. Create a superuser:
   ```bash
   railway run python manage.py createsuperuser
   ```
2. Go to `https://your-app.railway.app/admin`
3. Manually add locations (not recommended for 158 locations!)

**Option C: Upload via API**
- Export your local database and upload via the API
- See `populate_database.py` for reference

### 9. Verify Deployment
Test your backend API:
```
https://your-app.railway.app/v2/locations/
```

You should see a JSON response with locations.

### 10. Update Vercel Frontend
Now configure your Vercel frontend to use the Railway backend.

1. Go to [vercel.com](https://vercel.com)
2. Select your `basey-fareguide-v2` project
3. Go to "Settings" → "Environment Variables"
4. Add/Update:
   ```
   REACT_APP_API_URL = https://your-app.railway.app/v2
   ```
5. Go to "Deployments" tab
6. Click "Redeploy" on the latest deployment
7. Check "Use existing Build Cache" OFF
8. Click "Redeploy"

## 🎉 Success!

After Vercel redeploys (usually 1-2 minutes), your locations should load!

Visit: `https://basey-fareguide-v2.vercel.app`

## 🔧 Troubleshooting

### Locations still not loading?
1. Check Railway logs for errors: Dashboard → Deployments → View Logs
2. Verify the API works: `https://your-app.railway.app/v2/locations/`
3. Check browser console for CORS errors
4. Verify Vercel environment variable is set correctly

### Database issues?
```bash
# Check migrations
railway run python manage.py showmigrations

# Run migrations manually if needed
railway run python manage.py migrate
```

### Static files not loading?
```bash
# Collect static files
railway run python manage.py collectstatic --noinput
```

## 💰 Railway Costs

- **Free Tier**: $5 credit per month (usually enough for small projects)
- **Hobby Plan**: $5/month for more resources
- Monitor your usage in Railway dashboard

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- Railway Discord: Great community support

---

**Next Steps After Deployment:**
1. Set up automated backups for your database
2. Configure custom domain (optional)
3. Set up monitoring/error tracking (e.g., Sentry)
4. Enable HTTPS (Railway provides this automatically)
