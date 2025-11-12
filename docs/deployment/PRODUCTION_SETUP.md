# 🚀 Production Setup Guide - Basey Fare Guide

## PostgreSQL Database: Neon (Your Current Setup) ✅

You're already using **Neon PostgreSQL** - an excellent choice! Keep it.

### Current Database Info:
- **Provider:** Neon
- **Region:** Singapore (ap-southeast-1)
- **Database:** neondb
- **Connection:** Pooled (optimized for serverless)
- **URL:** `postgresql://neondb_owner:npg_...@ep-fragrant-cake-a1l57i7a-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`

---

## 🏗️ Production Architecture

```
┌─────────────────┐
│   Vercel        │ ← React Frontend (Static)
│   (Frontend)    │   - Next.js/React hosting
└────────┬────────┘   - Edge network (fast globally)
         │ HTTPS
         ▼
┌─────────────────┐
│   Railway       │ ← Django API Backend
│   (Backend)     │   - Gunicorn + Django
└────────┬────────┘   - Auto-scaling
         │
         ▼
┌─────────────────┐
│   Neon          │ ← PostgreSQL Database
│   (Database)    │   - Serverless PostgreSQL
└─────────────────┘   - Auto-scaling & branching
```

---

## 📊 Database Comparison (For Your Reference)

### **Neon PostgreSQL** (Your Current - RECOMMENDED) ⭐
**Best for:** Modern serverless apps, automatic scaling, branching

| Feature | Free Tier | Launch ($19/mo) | Scale ($69/mo) |
|---------|-----------|-----------------|----------------|
| Storage | 512 MB | 10 GB | 50 GB |
| Compute | 0.25 vCPU | 1 vCPU | 4 vCPU |
| Connections | 100 | 1000 | Unlimited |
| Branches | 10 | Unlimited | Unlimited |
| Auto-suspend | ✅ Yes | ✅ Yes | ✅ Yes |
| Region | Singapore | All regions | All regions |

**Pros:**
- ✅ Serverless (auto-scale, auto-suspend)
- ✅ Database branching (like Git for your DB)
- ✅ Modern dashboard and excellent DX
- ✅ Free tier is generous
- ✅ No cold starts (connection pooling)

**Cons:**
- ❌ Free tier storage limit (512MB)
- ❌ Relatively new (less battle-tested)

### **Railway PostgreSQL**
**Best for:** All-in-one deployment (backend + database together)

| Feature | Free Trial | Hobby ($5/mo) | Pro ($20/mo) |
|---------|------------|---------------|--------------|
| Storage | 1 GB | 5 GB | 100 GB |
| RAM | 512 MB | 512 MB | 8 GB |
| Resources | $5 credit | $5 credit | $20 credit |

**Pros:**
- ✅ Integrated with Railway (same platform as backend)
- ✅ Simple billing (everything in one place)
- ✅ Good for monolithic apps

**Cons:**
- ❌ Usage-based pricing (can be unpredictable)
- ❌ No branching feature
- ❌ Less specialized than Neon

### **Supabase**
**Best for:** Backend-as-a-Service with real-time features

| Feature | Free | Pro ($25/mo) |
|---------|------|--------------|
| Storage | 500 MB | 8 GB |
| Bandwidth | 2 GB | 50 GB |
| Auth Users | Unlimited | Unlimited |
| Realtime | Limited | Unlimited |

**Pros:**
- ✅ Built-in auth, storage, real-time
- ✅ Good free tier
- ✅ Postgres + Firebase-like features

**Cons:**
- ❌ Overkill for your use case (you have Django)
- ❌ More expensive than Neon
- ❌ Extra features you won't use

### **Render PostgreSQL**
**Best for:** Simple deployments, similar to Heroku

| Feature | Free | Starter ($7/mo) |
|---------|------|-----------------|
| Storage | 1 GB | 10 GB |
| Connections | 50 | 500 |
| Expires | 90 days | Never |

**Pros:**
- ✅ Simple setup
- ✅ Good documentation
- ✅ Heroku-like experience

**Cons:**
- ❌ Free tier expires after 90 days
- ❌ Limited free connections
- ❌ More expensive than Neon at scale

---

## 🎯 My Recommendation: Keep Neon + Use These Settings

### 1. Optimize Your Neon Database

#### Enable Connection Pooling (Already Done! ✅)
Your connection string already uses `-pooler`, which is perfect for Railway/serverless.

#### Create Database Branch for Testing
```bash
# In Neon dashboard:
1. Go to your project
2. Click "Branches" tab
3. Click "New Branch"
4. Name it "development" or "staging"
5. Use the branch URL for testing migrations
```

This way you can test database changes without affecting production!

### 2. Monitoring & Maintenance

#### Set Up Alerts in Neon:
1. Go to Neon dashboard
2. Settings → Notifications
3. Enable alerts for:
   - Storage usage (set at 80%)
   - Connection limits
   - Compute time

#### Regular Maintenance (Monthly):
```sql
-- Run this via Neon SQL Editor
VACUUM ANALYZE;  -- Optimize database
REINDEX DATABASE neondb;  -- Rebuild indexes
```

### 3. Backup Strategy

Neon automatically backs up your data, but for extra safety:

#### Option A: Regular Exports (Recommended)
```bash
# From Railway or local with Neon credentials:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Upload to cloud storage (Google Drive, Dropbox, etc.)
```

#### Option B: Use Neon Branching
- Create monthly branches as "snapshots"
- Keep last 3-6 months of branches
- Branch name: `backup-2025-11-12`

### 4. Security Checklist

- [x] SSL/TLS enabled (sslmode=require) ✅
- [x] Connection pooling enabled ✅
- [ ] Rotate database password every 90 days
- [ ] Use separate database users for different services
- [ ] Enable IP allowlist (if available in your Neon plan)

---

## 💰 Cost Projection

### Current Setup (Free Tier):
- **Neon:** $0/mo (Free tier)
- **Railway:** $5 credit/mo (should cover low traffic)
- **Vercel:** $0/mo (Free hobby tier)
- **Total:** ~$5-10/mo after free credits

### When You Grow (100+ daily users):
- **Neon Launch:** $19/mo (10GB storage)
- **Railway Hobby:** $20/mo usage (estimated)
- **Vercel Pro:** $20/mo (if you need custom domain features)
- **Total:** ~$59/mo

### At Scale (1000+ daily users):
- **Neon Scale:** $69/mo
- **Railway Pro:** $50/mo usage
- **Vercel Pro:** $20/mo
- **Total:** ~$139/mo

---

## 🚀 Deployment Steps (Using Your Current Neon DB)

### Step 1: Verify Database Access
```bash
# Test connection from Railway
railway run python manage.py check --database default
railway run python manage.py migrate --check
```

### Step 2: Deploy to Railway
See `QUICK_RAILWAY_SETUP.md` for detailed steps.

Environment variables for Railway:
```bash
DATABASE_URL=<your-neon-database-url-from-env-file>
SECRET_KEY=<generate-new-one-for-production>
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.up.railway.app,basey-fareguide-v2.vercel.app
```

### Step 3: Populate Production Database
```bash
# Via Railway CLI
railway run python populate_basey_locations.py

# Or via Railway web interface: Settings → Variables → Add
# Then deploy and check logs
```

### Step 4: Create Superuser
```bash
railway run python manage.py createsuperuser
```

---

## 📊 Database Capacity Planning

Your current data:
- **Locations:** 158 records (~50KB)
- **Users:** Estimate 100-500 users (~100KB)
- **Routes:** Estimate 1000 routes (~500KB)
- **Fares:** Estimate 5000 calculations (~1MB)
- **Total:** ~2-5 MB of data

**Neon Free Tier (512MB)** can handle:
- ~50,000 users
- ~100,000 routes
- ~500,000 fare calculations

**You're WELL within limits!** 🎉

---

## 🔄 Migration Path (If Needed Later)

If you ever outgrow Neon free tier:

### Option 1: Upgrade Neon (Easiest)
- Click "Upgrade" in dashboard
- Choose Launch plan ($19/mo)
- Zero downtime upgrade

### Option 2: Migrate to Railway PostgreSQL
```bash
# 1. Create Railway PostgreSQL
railway add

# 2. Dump from Neon
pg_dump $NEON_DATABASE_URL > backup.sql

# 3. Restore to Railway
psql $RAILWAY_DATABASE_URL < backup.sql

# 4. Update environment variable
# 5. Redeploy
```

### Option 3: Self-hosted (Advanced)
- DigitalOcean Managed PostgreSQL: $15/mo
- AWS RDS: ~$20/mo
- Google Cloud SQL: ~$25/mo

---

## 🎯 Bottom Line

**Keep your Neon database!** It's:
- ✅ Already set up and working
- ✅ Perfect for your scale
- ✅ Free (for now)
- ✅ Modern and developer-friendly
- ✅ Can scale when you need it

**Next steps:**
1. Deploy backend to Railway (use existing Neon database)
2. Deploy frontend to Vercel
3. Monitor usage in Neon dashboard
4. Upgrade when you hit 400MB storage or 5000+ users

You're all set! 🚀
