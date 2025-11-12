# ⚡ Quick Reference - Production Setup

## 🎯 TL;DR - What You Need to Know

### Your Current Setup ✅
- **Database:** Neon PostgreSQL (Singapore) - KEEP IT!
- **Backend:** Deploy to Railway
- **Frontend:** Deploy to Vercel

### Total Cost
- **Now:** $0-5/mo (free tiers)
- **After growth:** $19-39/mo

---

## 📋 Deployment Commands Cheat Sheet

### 1. Generate New Secret Key
```powershell
& "C:/Users/OCENA/OneDrive/Documents/Python Projects late 2024/Basey Fare Guide 2.0/BFG-env/Scripts/python.exe" -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Test Database Connection Locally
```powershell
& "C:/Users/OCENA/OneDrive/Documents/Python Projects late 2024/Basey Fare Guide 2.0/BFG-env/Scripts/python.exe" manage.py check --database default
```

### 3. Install Railway CLI
```powershell
npm i -g @railway/cli
railway login
railway link
```

### 4. Populate Production Database
```bash
railway run python populate_basey_locations.py
```

### 5. Create Superuser
```bash
railway run python manage.py createsuperuser
```

### 6. Check Logs
```bash
railway logs
```

---

## 🔑 Environment Variables for Railway

Copy these to Railway → Variables tab:

```bash
SECRET_KEY=<generate-new-one-dont-use-dev-key>
DEBUG=False
ALLOWED_HOSTS=<your-railway-domain>.up.railway.app,basey-fareguide-v2.vercel.app
DATABASE_URL=<your-neon-database-url-from-env-file>
GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-google-maps-server-api-key>
RESEND_API_KEY=<your-resend-api-key>
EMAIL_FROM=onboarding@resend.dev
JWT_SECRET=<generate-new-one-or-reuse-secret-key>
```

---

## 🔗 Important URLs

### Development
- **Local Backend:** http://127.0.0.1:8000
- **Local Frontend:** http://localhost:3000

### Production (Fill in after deployment)
- **Railway Backend:** https://________________.up.railway.app
- **Vercel Frontend:** https://basey-fareguide-v2.vercel.app
- **Neon Dashboard:** https://console.neon.tech

---

## ✅ Quick Testing Checklist

### After Railway Deployment:
1. ✅ Visit: `https://<railway-domain>/v2/locations/`
2. ✅ Should see JSON with 158 locations
3. ✅ Check Railway logs for errors

### After Vercel Deployment:
1. ✅ Visit: `https://basey-fareguide-v2.vercel.app`
2. ✅ Locations should load in dropdowns
3. ✅ No errors in browser console (F12)

---

## 🐛 Common Issues & Quick Fixes

### Issue: "DisallowedHost" Error
**Fix:** Update `ALLOWED_HOSTS` in Railway variables to include your Railway domain

### Issue: CORS Error
**Fix:** Make sure `ALLOWED_HOSTS` includes both Railway and Vercel domains

### Issue: Locations Not Showing
**Fix:** 
1. Verify DATABASE_URL is correct
2. Run `railway run python populate_basey_locations.py`
3. Check: `https://<railway-domain>/v2/locations/`

### Issue: 500 Internal Server Error
**Fix:** 
1. Check Railway logs: `railway logs`
2. Verify all env variables are set
3. Check SECRET_KEY is set correctly

---

## 📊 Database Info

### Current Capacity
- **Storage:** 512 MB (free tier)
- **Your Usage:** ~2-5 MB (plenty of room!)
- **Can Handle:** 50,000+ users

### Connection String
```
postgresql://neondb_owner:npg_Dkhqz6sVt7Wf@ep-fragrant-cake-a1l57i7a-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

### Key Features You Have
- ✅ Connection pooling (-pooler)
- ✅ SSL encryption (sslmode=require)
- ✅ Auto backups (7 days)
- ✅ Can create branches for testing

---

## 📚 Documentation Files

1. **PRODUCTION_SETUP.md** - Full production guide with database comparison
2. **DEPLOYMENT_CHECKLIST.md** - Step-by-step deployment checklist
3. **DATABASE_COMPARISON.md** - Detailed comparison of database options
4. **QUICK_RAILWAY_SETUP.md** - Fast Railway deployment guide
5. **QUICK_REFERENCE.md** - This file (commands & quick help)

---

## 💡 Pro Tips

1. **Always test in staging first**
   - Create Neon branch for testing
   - Deploy to Railway staging environment

2. **Monitor your usage**
   - Check Neon dashboard weekly
   - Watch Railway metrics daily (first week)

3. **Secure your API keys**
   - Never commit to GitHub
   - Use Railway variables, not .env files
   - Rotate keys every 90 days

4. **Keep backups**
   - Neon auto-backs up daily
   - Create manual branch monthly: `backup-2025-11`

5. **Performance optimization**
   - Use Neon connection pooler (already doing this!)
   - Monitor slow queries in Neon dashboard
   - Add database indexes as needed

---

## 🚨 Emergency Contacts

### If Production Goes Down:
1. Check Railway status: https://status.railway.app
2. Check Neon status: https://status.neon.tech
3. Check Vercel status: https://www.vercel-status.com

### Support Channels:
- **Railway:** Discord or support@railway.app
- **Neon:** Discord or support@neon.tech  
- **Vercel:** vercel.com/support

---

## 🎯 Next Actions

### Right Now:
1. [ ] Generate production SECRET_KEY
2. [ ] Deploy to Railway
3. [ ] Get Railway domain
4. [ ] Update ALLOWED_HOSTS
5. [ ] Test backend API

### This Week:
1. [ ] Deploy frontend to Vercel
2. [ ] Test full app functionality
3. [ ] Create superuser account
4. [ ] Share with beta users

### Ongoing:
1. [ ] Monitor logs daily (first week)
2. [ ] Check Neon storage weekly
3. [ ] Gather user feedback
4. [ ] Plan feature updates

---

## 🎉 You're Ready!

Everything is set up. Just follow:
1. **DEPLOYMENT_CHECKLIST.md** for step-by-step guide
2. **PRODUCTION_SETUP.md** for detailed information
3. This file for quick commands

**Good luck with your launch! 🚀**

---

## 📞 Questions?

- Check the documentation files first
- Search Railway/Neon docs
- Ask in Discord communities
- Review logs for error messages

**Most issues are solved by:**
1. Checking environment variables
2. Reading error logs carefully
3. Verifying URLs and domains
4. Testing API endpoints directly
