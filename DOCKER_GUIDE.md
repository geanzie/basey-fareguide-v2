# 🐳 Docker Deployment Guide

## Quick Start - Local Development

### 1. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Your app will be available at: `http://localhost:8000`

### 2. Run Migrations and Create Superuser

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Populate locations
docker-compose exec backend python populate_basey_locations.py
```

---

## 🚂 Railway Deployment with Docker

Railway will automatically detect and use the Dockerfile!

### Step 1: Push to GitHub

```bash
git add Dockerfile .dockerignore docker-compose.yml railway.json
git commit -m "Add Docker configuration for easy deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `basey-fareguide-v2`
6. Railway will automatically detect the Dockerfile and build it!

### Step 3: Add Environment Variables

In Railway dashboard → Your service → Variables:

```bash
SECRET_KEY=ydlv#)*rs$sds)o!y!51ba7_*_s_hi!%*@c58l3!=za##u13z3
DEBUG=False
DATABASE_URL=<your-neon-database-url>
GOOGLE_MAPS_API_KEY=<your-key>
GOOGLE_MAPS_SERVER_API_KEY=<your-key>
RESEND_API_KEY=<your-key>
```

### Step 4: Generate Domain

1. Go to Settings → Domains
2. Click "Generate Domain"
3. Get your URL: `https://your-app.up.railway.app`
4. Add to environment variables:
   ```
   ALLOWED_HOSTS=your-app.up.railway.app
   ```

### Step 5: Run Database Setup

Using Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link to project
railway login
railway link

# Run migrations
railway run python manage.py migrate

# Populate locations
railway run python populate_basey_locations.py

# Create superuser
railway run python manage.py createsuperuser
```

---

## 🎯 Benefits of Docker

✅ **Consistent Environment** - Same behavior in dev, staging, and production
✅ **Easy Deployment** - Single command to deploy anywhere
✅ **Isolated Dependencies** - No conflicts with system packages
✅ **Portable** - Deploy to Railway, AWS, GCP, Azure, or any Docker host
✅ **Fast Builds** - Docker layer caching speeds up rebuilds

---

## 📦 Docker Commands Reference

### Local Development

```bash
# Build image
docker build -t basey-fare-guide .

# Run container
docker run -p 8000:8000 --env-file .env basey-fare-guide

# View running containers
docker ps

# Stop container
docker stop <container-id>

# View logs
docker logs <container-id>

# Access container shell
docker exec -it <container-id> bash
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# Rebuild and restart
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Execute commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py shell
```

---

## 🔧 Troubleshooting

### Build fails?
```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Can't connect to database?
- Check DATABASE_URL is set correctly
- Ensure Neon database allows connections
- Verify SSL mode: `?sslmode=require`

### Static files not loading?
```bash
# Collect static files manually
docker-compose exec backend python manage.py collectstatic --noinput
```

---

## 🌐 Deploy to Other Platforms

### Deploy to any Docker host:

```bash
# Build and tag
docker build -t basey-fare-guide:latest .

# Push to Docker Hub
docker tag basey-fare-guide:latest yourusername/basey-fare-guide:latest
docker push yourusername/basey-fare-guide:latest

# Pull and run on any server
docker pull yourusername/basey-fare-guide:latest
docker run -p 8000:8000 --env-file .env yourusername/basey-fare-guide:latest
```

---

**Last Updated**: November 12, 2025
