# 🚀 Production Deployment Checklist

## ✅ Database Setup (Neon PostgreSQL)

- [x] **Neon account created** - ✅ Done
- [x] **Database created** - ✅ neondb
- [x] **Connection string obtained** - ✅ In .env
- [x] **Connection pooling enabled** - ✅ Using -pooler endpoint
- [x] **SSL enabled** - ✅ sslmode=require
- [ ] **Create database branch for staging** (Optional)
  ```
  1. Go to Neon dashboard → Branches
  2. Click "New Branch" → Name: "staging"
  3. Use staging branch URL for testing
  ```

---

## 🔐 Security Setup

### 1. Generate New Production Secret Key
```powershell
# Run this locally to generate a new secret key:
& "C:/Users/OCENA/OneDrive/Documents/Python Projects late 2024/Basey Fare Guide 2.0/BFG-env/Scripts/python.exe" -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- [ ] **Copy the generated key** (save it somewhere safe!)
- [ ] **Add to Railway environment variables** as `SECRET_KEY`

### 2. API Keys Review
- [x] **Google Maps API Key** - ✅ Have it
- [x] **Google Maps Server API Key** - ✅ Have it
- [x] **Resend API Key** - ✅ Have it
- [ ] **Restrict API keys** to production domains:
  - Add your Railway domain to Google Cloud Console
  - Add your Vercel domain to Google Cloud Console

---

## 🚂 Railway Backend Deployment

### 1. Create Railway Account
- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up with GitHub
- [ ] Verify email

### 2. Deploy Project
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose `basey-fareguide-v2`
- [ ] Click "Deploy"

### 3. Configure Environment Variables
Click on your service → "Variables" tab → Add these:

```bash
# Django Core
SECRET_KEY=<paste-the-generated-secret-key-here>
DEBUG=False

# Database (Your Neon Database)
DATABASE_URL=<your-neon-database-url-from-env-file>

# Google Maps API
GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-google-maps-server-api-key>

# Email
RESEND_API_KEY=<your-resend-api-key>
EMAIL_FROM=onboarding@resend.dev

# JWT
JWT_SECRET=<paste-the-generated-secret-key-here-or-use-a-different-one>
```

**Note:** Don't add `ALLOWED_HOSTS` yet - do it in Step 4!

### 4. Generate Railway Domain
- [ ] Go to "Settings" tab
- [ ] Scroll to "Domains" section
- [ ] Click "Generate Domain"
- [ ] **Copy the domain** (e.g., `basey-fare-guide-production.up.railway.app`)

### 5. Update ALLOWED_HOSTS
- [ ] Go back to "Variables" tab
- [ ] Add new variable:
  ```
  ALLOWED_HOSTS=<your-railway-domain>.up.railway.app,basey-fareguide-v2.vercel.app
  ```
- [ ] Railway will auto-redeploy

### 6. Wait for Deployment
- [ ] Click "Deployments" tab
- [ ] Watch the logs
- [ ] Wait for "Deployment successful" ✅
- [ ] Look for these in logs:
  - ✅ "Collecting static files"
  - ✅ "Running migrations"
  - ✅ "Starting gunicorn"

### 7. Test Your Backend API
Open in browser: `https://<your-railway-domain>.up.railway.app/v2/locations/`

- [ ] **Does it return JSON with locations?** ✅
- [ ] **Shows 158 locations?** ✅

If you see locations, backend is working! 🎉

---

## 🌐 Vercel Frontend Setup

### 1. Update Frontend API URL
- [ ] Go to [vercel.com](https://vercel.com)
- [ ] Select `basey-fareguide-v2` project
- [ ] Go to "Settings" → "Environment Variables"
- [ ] Add or update:
  ```
  REACT_APP_API_URL=https://<your-railway-domain>.up.railway.app/v2
  ```

### 2. Update Frontend Config File (if needed)
Check if you have a config file that needs updating:

```bash
# In frontend/src/config.js or similar
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/v2';
```

- [ ] **Config file exists and uses env variable?** ✅

### 3. Redeploy Vercel
- [ ] Go to "Deployments" tab
- [ ] Click "..." on latest deployment
- [ ] Click "Redeploy"
- [ ] **Uncheck** "Use existing Build Cache"
- [ ] Click "Redeploy"
- [ ] Wait for deployment to complete

### 4. Test Your Live App
Visit: `https://basey-fareguide-v2.vercel.app`

- [ ] **App loads?** ✅
- [ ] **Locations dropdown shows 158 locations?** ✅
- [ ] **Can select origin and destination?** ✅
- [ ] **Fare calculation works?** ✅

---

## 🗃️ Database Population

### Option A: Via Railway CLI (Recommended)
```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Populate locations
railway run python populate_basey_locations.py
```

- [ ] **Railway CLI installed**
- [ ] **Logged in**
- [ ] **Project linked**
- [ ] **Locations populated**

### Option B: Via Django Admin
- [ ] Run: `railway run python manage.py createsuperuser`
- [ ] Go to: `https://<railway-domain>/admin/`
- [ ] Login with superuser credentials
- [ ] Manually add locations (tedious!)

---

## 🧪 Testing Checklist

### Backend Tests
- [ ] `/v2/locations/` returns 158 locations
- [ ] `/v2/routes/` returns empty list (or routes if you created any)
- [ ] `/v2/fares/` returns empty list (or fares if calculated any)
- [ ] `/admin/` login page works
- [ ] No CORS errors in browser console

### Frontend Tests
- [ ] Homepage loads
- [ ] Locations load in dropdowns
- [ ] Can select origin/destination
- [ ] Map displays (if implemented)
- [ ] Fare calculation works (if implemented)
- [ ] No console errors (F12 → Console)

### Performance Tests
- [ ] Page loads in < 3 seconds
- [ ] API responses in < 500ms
- [ ] No 500 errors in Railway logs

---

## 📊 Monitoring Setup

### 1. Railway Monitoring
- [ ] Go to Railway dashboard
- [ ] Check "Metrics" tab regularly:
  - CPU usage
  - Memory usage
  - Network bandwidth
  - Response times

### 2. Neon Monitoring
- [ ] Go to Neon dashboard
- [ ] Check:
  - Storage usage (stay under 512MB for free tier)
  - Active connections
  - Query performance

### 3. Set Up Alerts
- [ ] **Neon alerts:**
  - Settings → Notifications
  - Enable "Storage threshold" at 80%
- [ ] **Railway alerts:**
  - Not available on free tier, monitor manually

---

## 🐛 Troubleshooting

### Backend not deploying?
1. Check Railway logs for errors
2. Verify all environment variables are set
3. Check if `requirements.txt` is complete
4. Verify `Procfile` exists

### CORS errors?
1. Verify `ALLOWED_HOSTS` includes both Railway and Vercel domains
2. Check `CORS_ALLOWED_ORIGINS` in settings.py
3. Make sure `corsheaders` middleware is enabled

### Locations not showing?
1. Check browser console for errors
2. Verify `REACT_APP_API_URL` is correct in Vercel
3. Test backend API directly in browser
4. Check if database is populated

### Database connection errors?
1. Verify `DATABASE_URL` is correct
2. Check Neon dashboard for connection issues
3. Verify SSL is enabled (`sslmode=require`)
4. Check connection pooler is being used

---

## ✅ Final Verification

Once everything is deployed and working:

- [ ] **Backend URL:** https://________________.up.railway.app
- [ ] **Frontend URL:** https://basey-fareguide-v2.vercel.app
- [ ] **Database:** Neon PostgreSQL (Singapore region)
- [ ] **All locations loaded** (158 total)
- [ ] **No errors in logs**
- [ ] **App is live and functional** 🎉

---

## 📝 Post-Deployment Notes

### Save These URLs:
```
Backend API: https://________________.up.railway.app
Frontend: https://basey-fareguide-v2.vercel.app
Database Dashboard: https://console.neon.tech
Railway Dashboard: https://railway.app/project/
Vercel Dashboard: https://vercel.com/dashboard
```

### Credentials to Save Securely:
- [ ] Railway account email
- [ ] Production SECRET_KEY
- [ ] Database credentials (in Neon dashboard)
- [ ] Django superuser credentials

### Next Steps After Launch:
1. Monitor logs daily for first week
2. Check Neon storage usage weekly
3. Test all features thoroughly
4. Get user feedback
5. Set up regular database backups

---

## 🎉 You're Done!

Your Basey Fare Guide app is now live in production!

- ✅ Django backend on Railway
- ✅ React frontend on Vercel
- ✅ PostgreSQL database on Neon
- ✅ All properly connected and secured

**Next:** Share your app link and gather user feedback! 🚀
