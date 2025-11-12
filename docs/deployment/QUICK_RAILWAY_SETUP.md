# Quick Railway Deployment - Using Your Existing Neon Database

Since you already have a Neon PostgreSQL database set up, deployment is even simpler!

## 🚀 Fast Track Deployment (10 minutes)

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Click "Login" → Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `basey-fareguide-v2` repository
6. Click "Deploy"

### Step 2: Set Environment Variables in Railway
Click on your service → "Variables" tab → Add these:

```bash
# Django Core
SECRET_KEY=<generate-new-production-secret-key>
DEBUG=False

# Database - Your Existing Neon Database
DATABASE_URL=<your-neon-database-url-from-env-file>

# Google Maps API
GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-google-maps-server-api-key>

# Email (optional)
RESEND_API_KEY=<your-resend-api-key>
EMAIL_FROM=onboarding@resend.dev
```

**IMPORTANT**: After Railway generates your domain, come back and update:
```bash
ALLOWED_HOSTS=your-app-name.up.railway.app,basey-fareguide-v2.vercel.app
```

### Step 3: Get Your Railway URL
1. Go to "Settings" tab
2. Scroll to "Domains"
3. Click "Generate Domain"
4. Copy the URL (e.g., `https://basey-fare-guide-production.up.railway.app`)

### Step 4: Test Your API
Visit: `https://your-railway-url.up.railway.app/v2/locations/`

You should see your 158 locations! (They're already in your Neon database)

### Step 5: Update Vercel
1. Go to [vercel.com](https://vercel.com)
2. Select your `basey-fareguide-v2` project
3. Go to "Settings" → "Environment Variables"
4. Add or update:
   ```
   REACT_APP_API_URL = https://your-railway-url.up.railway.app/v2
   ```
5. Go to "Deployments" → Click "..." on latest → "Redeploy"
6. Uncheck "Use existing Build Cache"
7. Click "Redeploy"

### Step 6: Test Your App! 🎉
Visit: `https://basey-fareguide-v2.vercel.app`

Locations should now load in the dropdowns!

## 🐛 Troubleshooting

### Railway build fails?
Check the logs. Common issues:
- Missing environment variables
- Need to update `ALLOWED_HOSTS`

### API works but frontend still shows no locations?
1. Check browser console (F12) for errors
2. Verify `REACT_APP_API_URL` is set correctly in Vercel
3. Make sure Vercel redeployed after changing env vars

### CORS errors?
Add to Railway variables:
```bash
ALLOWED_HOSTS=your-railway-domain.up.railway.app,basey-fareguide-v2.vercel.app
```

## 💡 Why This Works

You already have:
- ✅ Database set up (Neon)
- ✅ 158 locations populated
- ✅ All API keys configured

You just need to:
- Deploy the Django backend to Railway
- Point Vercel frontend to Railway backend

That's it!

---

**Estimated Time**: 10 minutes
**Cost**: Free (Railway $5 credits + Neon free tier)
