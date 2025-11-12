# Basey Fare Guide 2.0 - Django REST API + React Frontend

Full-stack tricycle fare calculation system with Django REST API backend and React frontend.

## ⚠️ SECURITY NOTICE - READ BEFORE CLONING

**IMPORTANT:** This repository does NOT include `.env` files with API keys and secrets.

Before running this project:
1. **Copy `.env.example` to `.env`** in both root and frontend directories
2. **Fill in your own API keys and secrets** (see [docs/guides/SECURITY.md](docs/guides/SECURITY.md))
3. **NEVER commit `.env` files** - they are gitignored for security
4. See the [Security Guidelines](docs/guides/SECURITY.md) for detailed setup instructions

## 📚 Documentation

All documentation has been organized in the `docs/` directory. See **[docs/INDEX.md](docs/INDEX.md)** for a complete guide to all available documentation.

## 🎯 Tech Stack

- **Backend**: Django 5.2 + Django REST Framework
- **Frontend**: React 18 with React Router
- **Database**: PostgreSQL 12+
- **Authentication**: JWT (Simple JWT)
- **APIs**: Google Maps Distance Matrix & Directions API
- **Styling**: Modern CSS3 with gradients and animations

## 🚀 Features Implemented

### Frontend (React)
- ✅ **Modern UI/UX** - Responsive design with smooth animations
- ✅ **User Authentication** - Login, register, and profile management
- ✅ **Fare Calculator** - Interactive fare calculation interface
- ✅ **Location Browser** - Search and filter locations
- ✅ **User Dashboard** - Profile and fare calculation history
- ✅ **Protected Routes** - Role-based access control
- ✅ **Auto Token Refresh** - Seamless authentication experience

### Backend (Django REST API)

#### Core Functionality
- ✅ **Fare Calculation System** - Based on Municipal Ordinance 105 Series of 2023
  - Base fare: ₱15.00 (first 3km)
  - Additional rate: ₱3.00/km beyond 3km
  - Automatic rounding to nearest ₱0.50
  - 20% discount for Senior Citizens, PWDs, and Students

- ✅ **Google Maps Integration**
  - Distance Matrix API for accurate route distances
  - Directions API for detailed polylines
  - GPS fallback using Haversine formula

- ✅ **Discount Card Management**
  - Card application with ID upload
  - Admin verification workflow
  - Automatic discount application
  - Usage tracking and logging

- ✅ **Incident Reporting System**
  - Multiple incident types (overcharging, reckless driving, etc.)
  - Evidence file uploads
  - GPS coordinates capture
  - Admin review and resolution

- ✅ **JWT Authentication**
  - Secure token-based authentication
  - Token refresh mechanism
  - Role-based access control (Admin, Moderator, Driver, Public User)

### Models (Complete Database Schema)
- **User** - Custom user model with roles
- **Vehicle** - Driver vehicle registration
- **DiscountCard** - Discount eligibility cards
- **DiscountUsageLog** - Track discount usage
- **Incident** - Incident reports
- **FareCalculation** - Historical fare calculations
- **Location** - Barangay and landmark locations
- **Route** - Transportation routes
- **Fare** - Fare pricing by route and passenger type

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Google Maps API Key (with Distance Matrix & Directions APIs enabled)

### 1. Database Setup

Create PostgreSQL database:
```sql
CREATE DATABASE basey_fare_guide;
```

Or using PowerShell:
```powershell
psql -U postgres -c "CREATE DATABASE basey_fare_guide;"
```

### 2. Environment Configuration

**⚠️ CRITICAL: Follow these steps exactly to avoid exposing secrets**

#### Backend Environment Setup
```powershell
# In the project root directory
cp .env.example .env
```

Then edit `.env` and replace all placeholder values with your actual credentials. See [SECURITY.md](SECURITY.md) for detailed instructions on:
- Generating secure SECRET_KEY and JWT_SECRET
- Setting up Google Maps API keys with proper restrictions
- Configuring database credentials
- Setting up Resend API for emails

#### Frontend Environment Setup
```powershell
# In the frontend directory
cd frontend
cp .env.example .env
```

Edit `frontend/.env` and add your API URL and Google Maps key.

**Never commit `.env` files!** They are excluded via `.gitignore`.

### 3. Install Dependencies

Activate virtual environment and install packages:
```powershell
.\BFG-env\Scripts\Activate.ps1
pip install -r requirements.txt
```

Required packages:
- Django 5.2+
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- python-decouple
- django-cors-headers
- django-filter
- googlemaps
- Pillow

### 4. Run Migrations

```powershell
python manage.py migrate
```

### 5. Create Superuser

```powershell
python manage.py createsuperuser
```

### 6. Set Up React Frontend

```powershell
cd frontend
npm install
```

### 7. Run Development Servers

**Option 1: Automatic (Recommended)**
```powershell
.\start-dev.ps1
```

**Option 2: Manual**

Terminal 1 - Django:
```powershell
.\BFG-env\Scripts\Activate.ps1
python manage.py runserver
```

Terminal 2 - React:
```powershell
cd frontend
npm start
```

**URLs:**
- React Frontend: `http://localhost:3000`
- Django API: `http://localhost:8000/api/`
- Admin interface: `http://localhost:8000/admin/`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `POST /api/auth/logout/` - Logout (blacklist token)
- `GET /api/auth/me/` - Get current user
- `PUT/PATCH /api/auth/profile/` - Update profile
- `POST /api/auth/token/refresh/` - Refresh access token

### Route Calculation
- `POST /api/routes/calculate/` - Calculate fare and route
  ```json
  {
    "origin": [11.28026, 125.06909],
    "destination": [11.2768363, 125.0114879],
    "user_id": 1,
    "use_google_maps": true
  }
  ```

### Resource Endpoints (REST CRUD)
- `/api/users/` - User management
- `/api/vehicles/` - Vehicle management
- `/api/discount-cards/` - Discount card management
  - `POST /api/discount-cards/{id}/verify/` - Verify card (admin only)
  - `GET /api/discount-cards/pending/` - Get pending cards (admin only)
- `/api/discount-usage-logs/` - Discount usage logs (read-only)
- `/api/incidents/` - Incident management
  - `PATCH /api/incidents/{id}/update_status/` - Update status (admin only)
- `/api/fare-calculations/` - Fare calculation history
- `/api/locations/` - Location management
- `/api/routes/` - Route management
- `/api/fares/` - Fare pricing management

### Query Parameters
Most list endpoints support:
- `?search=keyword` - Search functionality
- `?ordering=field` - Sort by field
- `?page=1&page_size=20` - Pagination
- `?status=PENDING` - Filter by status
- `?type=BARANGAY` - Filter by type

## 🔐 Authentication

Include JWT token in requests:
```http
Authorization: Bearer <your_access_token>
```

Example using fetch:
```javascript
fetch('http://localhost:8000/api/fare-calculations/', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

## 🧮 Fare Calculation Logic

### Server-Side Calculation
```python
from fares.fare_calculator import FareCalculator

# Basic calculation
result = FareCalculator.calculate_fare(
    distance_km=5.5,
    discount_rate=0.20  # 20% discount
)

# With Google Maps
from fares.fare_calculator import calculate_route_with_fare

result = calculate_route_with_fare(
    origin=(11.28026, 125.06909),
    destination=(11.2768363, 125.0114879),
    discount_card=discount_card_instance,
    use_google_maps=True
)
```

### Response Format
```json
{
  "success": true,
  "method": "google_maps",
  "distance": {
    "kilometers": 5.5,
    "meters": 5500
  },
  "fare": {
    "fare": 18.0,
    "original_fare": 24.0,
    "discount_applied": 6.0,
    "breakdown": {
      "base_fare": 15.0,
      "base_distance_km": 3.0,
      "additional_distance_km": 2.5,
      "additional_fare": 9.0,
      "distance_km": 5.5
    }
  },
  "discount_card": {
    "card_id": 1,
    "discount_type": "SENIOR_CITIZEN",
    "discount_rate": 0.2
  }
}
```

## 👨‍💼 Admin Interface Features

Access at `/admin/` with superuser credentials.

### Discount Card Management
- Bulk approve/reject actions
- Color-coded verification status badges
- Usage statistics tracking
- ID image preview

### Incident Management
- Color-coded status and priority badges
- Filter by type, status, priority
- Quick status updates
- Evidence file management

### User Management
- Role-based filtering
- Activity tracking
- Vehicle associations

## 🔧 Development Notes

### Adding Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable APIs:
   - Distance Matrix API
   - Directions API
   - Maps JavaScript API (for frontend)
3. Create API key
4. Add to `.env` file

### Database Migrations
After model changes:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Testing API Endpoints
Use tools like:
- Postman
- Thunder Client (VS Code)
- Django REST Framework Browsable API

### CORS Configuration
Frontend origins configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## 📊 Key Differences from Next.js Version

| Feature | Next.js | Django |
|---------|---------|--------|
| **ORM** | Prisma | Django ORM |
| **Auth** | Custom JWT | djangorestframework-simplejwt |
| **File Uploads** | Multer | Django FileField/ImageField |
| **API Pattern** | Next.js API Routes | Django REST Framework ViewSets |
| **Admin** | Custom React UI | Django Admin (built-in) |
| **Validation** | Zod/Custom | DRF Serializers |

## 🚀 Production Deployment

### Environment Variables
Set all production values in `.env`:
- `DEBUG=False`
- `SECRET_KEY=<strong-random-key>`
- `ALLOWED_HOSTS=yourdomain.com`
- Database credentials
- Google Maps API key

### Static Files
```powershell
python manage.py collectstatic
```

### Database
Run migrations on production database:
```powershell
python manage.py migrate --settings=bfg.settings
```

### Web Server
Use:
- **Gunicorn** (recommended): `gunicorn bfg.wsgi:application`
- **uWSGI**: `uwsgi --http :8000 --module bfg.wsgi`

### Nginx Configuration (example)
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /media/ {
    alias /path/to/media/;
}
```

## � Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide for running the application
- **[REACT_INTEGRATION.md](REACT_INTEGRATION.md)** - Detailed React setup and architecture
- **[API_GUIDE.md](API_GUIDE.md)** - Complete API endpoint documentation
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation
- **[MIGRATION_LOG.md](MIGRATION_LOG.md)** - Database migration history

## �📝 Next Steps

1. ✅ Core models and API implemented
2. ✅ React frontend with modern UI
3. ✅ Authentication and protected routes
4. ⏳ Add GeoJSON barangay boundary processing
5. ⏳ Implement batch location import from allLocations.ts
6. ⏳ Add analytics and reporting endpoints
7. ⏳ Implement rate limiting
8. ⏳ Add comprehensive test suite
9. ⏳ Set up Celery for async tasks
10. ⏳ Add caching (Redis)
11. ⏳ Add real-time features with WebSockets

## 🐛 Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U postgres -l`

### Google Maps API Error
- Verify API key is correct
- Check APIs are enabled in Google Cloud Console
- Ensure billing is enabled

### Import Errors
- Activate virtual environment: `.\BFG-env\Scripts\Activate.ps1`
- Reinstall packages: `pip install -r requirements.txt`

### React Build Errors
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Clear npm cache: `npm cache clean --force`

### CORS Issues
- Ensure Django is running on port 8000
- Check CORS settings in `bfg/settings.py`
- Verify React .env has correct API_URL

## 📄 License

Same as original project - for Basey Municipality use.

## 👥 Credits

Django replication by: Assistant
Original Next.js project by: OCENA
Based on: Municipal Ordinance 105 Series of 2023
