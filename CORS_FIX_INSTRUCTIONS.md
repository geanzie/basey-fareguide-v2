# CORS Fix - Instructions

## Problem Fixed
Your frontend was trying to access a placeholder URL (`https://your-railway-app.up.railway.app`) instead of your actual Railway backend URL. This has been corrected.

## Changes Made

### 1. Updated `frontend/.env.production`
- Changed API URL from placeholder to actual Railway URL: `https://web-production-8fd2c.up.railway.app/v2`

### 2. Updated `vercel.json`
- Updated the proxy rewrite rule to point to your actual Railway backend

### 3. Enhanced `bfg/settings.py`
- Added explicit `CORS_ALLOW_METHODS` to handle preflight requests properly
- Verified `https://basey-fareguide-v2.vercel.app` is in `CORS_ALLOWED_ORIGINS`

## Next Steps - Deploy Updates

### Step 1: Push Changes to GitHub
```powershell
git add .
git commit -m "Fix: Update Railway URL and improve CORS configuration"
git push origin main
```

### Step 2: Update Vercel Environment Variables
1. Go to https://vercel.com/dashboard
2. Select your project: **basey-fareguide-v2**
3. Go to **Settings** → **Environment Variables**
4. Add or update:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://web-production-8fd2c.up.railway.app/v2`
   - **Environment**: Select `Production`

### Step 3: Redeploy on Vercel
Option A - Automatic (when you push to GitHub):
- Vercel will automatically redeploy when it detects the push

Option B - Manual:
1. Go to your Vercel dashboard
2. Click on your project
3. Go to **Deployments** tab
4. Click **Redeploy** on the latest deployment

### Step 4: Redeploy Backend on Railway
1. Go to https://railway.app/dashboard
2. Select your project: **web-production-8fd2c**
3. Click **Deploy** or push the changes to trigger a redeploy

### Step 5: Test
After both deployments complete:
1. Visit https://basey-fareguide-v2.vercel.app
2. Try to register a new user
3. Try to load locations
4. Check browser console for CORS errors (should be gone)

## Verification
After deployment, open browser DevTools and check:
- Network tab should show requests to `https://web-production-8fd2c.up.railway.app/v2/*`
- Response headers should include:
  - `Access-Control-Allow-Origin: https://basey-fareguide-v2.vercel.app`
  - `Access-Control-Allow-Credentials: true`

## If Issues Persist
1. Clear browser cache and cookies
2. Check Railway logs for any backend errors
3. Verify Railway environment variables are set correctly
4. Ensure Django DEBUG=False in production
