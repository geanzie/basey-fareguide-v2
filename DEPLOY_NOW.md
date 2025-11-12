# 🚀 Railway Deployment - Ready to Deploy!

## ✅ Pre-Deployment Complete

All security checks passed and code is now on GitHub!

### What We've Done:
1. ✅ **Removed all exposed secrets** from documentation files
2. ✅ **Organized documentation** into `docs/` directory structure
3. ✅ **Verified .env is gitignored** 
4. ✅ **Created .env.example** templates for others
5. ✅ **Pushed clean code** to GitHub: `geanzie/basey-fareguide-v2`
6. ✅ **Generated production SECRET_KEY**: `ydlv#)*rs$sds)o!y!51ba7_*_s_hi!%*@c58l3!=za##u13z3`

---

## 🚂 Next Steps: Deploy to Railway

### Step 1: Create Railway Account & Project
1. Go to [railway.app](https://railway.app)
2. Click "Login" → Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `basey-fareguide-v2` repository
6. Click "Deploy"

### Step 2: Configure Environment Variables

Click on your service → "Variables" tab → Add these:

```bash
# Django Core
SECRET_KEY=ydlv#)*rs$sds)o!y!51ba7_*_s_hi!%*@c58l3!=za##u13z3
DEBUG=False

# Database (Your Neon Database)
DATABASE_URL=<copy-from-your-.env-file>

# Google Maps API
GOOGLE_MAPS_API_KEY=<copy-from-your-.env-file>
GOOGLE_MAPS_SERVER_API_KEY=<copy-from-your-.env-file>

# Email Service (Optional)
RESEND_API_KEY=<copy-from-your-.env-file>
EMAIL_FROM=onboarding@resend.dev
```

**IMPORTANT:** After Railway generates your domain (Step 3), come back and add:
```bash
ALLOWED_HOSTS=<your-app-name>.up.railway.app
```

### Step 3: Get Your Railway URL
1. Go to "Settings" tab
2. Scroll to "Domains" section
3. Click "Generate Domain"
4. Your URL will be something like: `https://basey-fare-guide-production.up.railway.app`
5. **Copy this URL** and add it to `ALLOWED_HOSTS` in Railway variables

### Step 4: Monitor Deployment
Watch the "Deployments" tab for:
- ✅ "Collecting static files"
- ✅ "Running migrations"
- ✅ "Starting gunicorn"

This usually takes 3-5 minutes.

### Step 5: Populate Production Database

Use Railway CLI (recommended):
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Populate database
railway run python populate_basey_locations.py
```

### Step 6: Test Your Backend
Visit your Railway URL:
- `https://your-app.up.railway.app/admin/` - Django admin
- `https://your-app.up.railway.app/api/v2/locations/` - API test

---

## 🔗 Important URLs

- **GitHub Repository**: https://github.com/geanzie/basey-fareguide-v2
- **Railway Dashboard**: https://railway.app/dashboard
- **Neon Database**: https://console.neon.tech
- **Your Railway URL**: `<will be generated in Step 3>`

---

## 📚 Documentation

All guides are now in the `docs/` folder:
- **[docs/deployment/QUICK_RAILWAY_SETUP.md](docs/deployment/QUICK_RAILWAY_SETUP.md)** - Quick deployment guide
- **[docs/deployment/DEPLOYMENT_CHECKLIST.md](docs/deployment/DEPLOYMENT_CHECKLIST.md)** - Complete checklist
- **[docs/INDEX.md](docs/INDEX.md)** - Full documentation index

---

## 🆘 Troubleshooting

### Deployment fails?
1. Check Railway logs in "Deployments" tab
2. Verify all environment variables are set
3. Ensure `DATABASE_URL` is correct

### Can't access admin?
```bash
# Create superuser via Railway CLI
railway run python manage.py createsuperuser
```

### API returns 500 error?
1. Check `ALLOWED_HOSTS` includes your Railway domain
2. Verify `DEBUG=False` is set
3. Check Railway logs for errors

---

**Last Updated**: November 12, 2025
**Status**: Ready for Railway Deployment! 🚀
