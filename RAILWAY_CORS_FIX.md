# Railway CORS Fix - Deployment Instructions

## Problem
Your Vercel frontend at `https://basey-fareguide-v2.vercel.app` is being blocked by CORS when trying to access your Railway backend at `https://web-production-8fd2c.up.railway.app`.

## Solution

### 1. Verify Environment Variables on Railway

Go to your Railway project dashboard and ensure these environment variables are set:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,web-production-8fd2c.up.railway.app,.railway.app
DATABASE_URL=your-postgres-url-here
```

**Important:** Make sure `DEBUG=False` in production!

### 2. Changes Made to Fix CORS

The following changes have been made to `bfg/settings.py`:

1. **Added explicit CORS headers:**
   - `CORS_EXPOSE_HEADERS` - Exposes headers to the browser
   - `CORS_PREFLIGHT_MAX_AGE` - Caches preflight requests for 1 hour

2. **Added environment variable support:**
   - You can now add extra CORS origins via the `CORS_EXTRA_ALLOWED_ORIGINS` environment variable

3. **Your Vercel frontend is already whitelisted:**
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://basey-fareguide-v2.vercel.app",
   ]
   ```

### 3. Deploy to Railway

You have two options:

#### Option A: Push to GitHub (Recommended)
```powershell
git add .
git commit -m "Fix CORS configuration for Vercel frontend"
git push origin main
```
Railway will automatically redeploy.

#### Option B: Manual Railway CLI Deploy
```powershell
railway up
```

### 4. Verify CORS is Working

After deployment, test the CORS endpoint:

```powershell
# Test from PowerShell
Invoke-WebRequest -Uri "https://web-production-8fd2c.up.railway.app/v2/cors-test/" -Method GET | Select-Object -ExpandProperty Headers
```

You should see CORS headers in the response:
- `Access-Control-Allow-Origin: https://basey-fareguide-v2.vercel.app`
- `Access-Control-Allow-Credentials: true`
- `Access-Control-Allow-Methods: DELETE, GET, OPTIONS, PATCH, POST, PUT`

### 5. Test from Your Frontend

Open your Vercel app (`https://basey-fareguide-v2.vercel.app`) and check the browser console. The CORS errors should be gone.

### 6. Debugging CORS Issues

If you still have issues, you can:

1. **Check Railway Logs:**
   ```powershell
   railway logs
   ```

2. **Run the CORS diagnostic script locally:**
   ```powershell
   python check_cors.py
   ```

3. **Temporarily enable all origins (ONLY FOR TESTING):**
   
   In Railway environment variables, add:
   ```
   CORS_ALLOW_ALL_ORIGINS=True
   ```
   
   **WARNING:** Remove this after testing! It's a security risk.

### 7. Common Issues

#### Issue: CORS headers still not showing
**Solution:** Make sure Railway has redeployed with the new code. Check the deployment logs.

#### Issue: "ALLOWED_HOSTS" error
**Solution:** Add your Railway domain to the `ALLOWED_HOSTS` environment variable:
```
ALLOWED_HOSTS=web-production-8fd2c.up.railway.app,.railway.app,localhost
```

#### Issue: Frontend still can't connect
**Solution:** Check if your frontend is using the correct backend URL. It should be:
```javascript
const API_URL = 'https://web-production-8fd2c.up.railway.app';
```

### 8. Security Checklist

Before going to production, ensure:

- [ ] `DEBUG=False` on Railway
- [ ] `SECRET_KEY` is set and unique (not the same as local)
- [ ] Only your Vercel domain is in `CORS_ALLOWED_ORIGINS`
- [ ] `CORS_ALLOW_ALL_ORIGINS` is NOT set or is `False`
- [ ] `ALLOWED_HOSTS` includes only your Railway and Vercel domains

### 9. Testing the Fix

1. Open browser console (F12)
2. Navigate to your Vercel frontend
3. You should see data loading without CORS errors
4. Check Network tab - you should see successful requests to Railway

## Need More Help?

If you're still seeing CORS issues after following these steps:

1. Check Railway deployment logs
2. Verify environment variables are set correctly
3. Make sure the code has been pushed and deployed
4. Test the `/v2/cors-test/` endpoint directly
5. Check browser console for specific error messages

## Files Modified

- `bfg/settings.py` - Added CORS headers and configuration
- `bfg/urls.py` - Added CORS test endpoint
- `check_cors.py` - New diagnostic script
