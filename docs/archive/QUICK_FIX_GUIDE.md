# Quick Reference: Fixing "No Locations Loading" Issue

## Problem
Your Vercel frontend (https://basey-fareguide-v2.vercel.app) can't load locations because it's trying to connect to `http://localhost:8000/v2`, which only works on your local machine.

## Solution Overview
1. Deploy Django backend to Railway
2. Configure Vercel to use Railway backend URL

## Current Status ✅
Your project is now **ready for Railway deployment**!

Files created:
- ✅ `Procfile` - Railway startup command
- ✅ `railway.json` - Build configuration
- ✅ `runtime.txt` - Python version
- ✅ `.env.production.example` - Production environment template
- ✅ `RAILWAY_DEPLOYMENT.md` - Complete deployment guide

Files updated:
- ✅ `requirements.txt` - Added gunicorn and whitenoise
- ✅ `bfg/settings.py` - Production-ready configuration

## Next Steps

### 1. Deploy to Railway (10-15 minutes)
Follow the step-by-step guide in `RAILWAY_DEPLOYMENT.md`

**Quick Summary:**
1. Go to https://railway.app and sign up
2. Create new project from GitHub
3. Add PostgreSQL database
4. Set environment variables
5. Deploy automatically happens
6. Get your Railway URL (e.g., `https://your-app.railway.app`)

### 2. Populate Database
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link
railway login
railway link

# Populate locations
railway run python populate_basey_locations.py
```

### 3. Update Vercel (2 minutes)
1. Go to https://vercel.com
2. Open your project settings
3. Add environment variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-app.railway.app/v2` (use your actual Railway URL)
4. Redeploy

## Testing

After deployment, test:

1. **Backend API**:
   ```
   https://your-app.railway.app/v2/locations/
   ```
   Should return JSON with 158 locations

2. **Frontend**:
   ```
   https://basey-fareguide-v2.vercel.app
   ```
   Should now load locations in dropdowns

## Troubleshooting

### Locations still not showing?
1. Check Railway logs: Railway Dashboard → Deployments → Logs
2. Verify API endpoint works (visit the URL in browser)
3. Check Vercel deployment logs for errors
4. Open browser console (F12) to see API errors

### CORS errors?
Django settings already configured for your Vercel domain. If you see CORS errors:
- Verify `ALLOWED_HOSTS` in Railway includes your Vercel domain
- Check that Vercel environment variable is correct

### Database empty?
Run: `railway run python populate_basey_locations.py`

## Cost
- **Railway**: $5 free credits/month (sufficient for testing)
- **Vercel**: Free for hobby projects

## Need Help?
- Railway Docs: https://docs.railway.app
- Check RAILWAY_DEPLOYMENT.md for detailed instructions
- Railway Discord community is very helpful

---

**Estimated Time to Fix**: 15-20 minutes total
**Difficulty**: Beginner-friendly (just follow the steps!)
