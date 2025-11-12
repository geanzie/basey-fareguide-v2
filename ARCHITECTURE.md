# Basey Fare Guide - System Architecture

## 🏗️ Full Stack Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / BROWSERS                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTP/HTTPS Requests
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND (Port 3000)                  │
├─────────────────────────────────────────────────────────────────┤
│  Components:                                                     │
│  • Home - Landing page with features                            │
│  • Login/Register - Authentication                              │
│  • FareCalculator - Main fare calculation interface            │
│  • Locations - Browse and search locations                     │
│  • Profile - User dashboard and history                        │
│  • Navbar - Navigation                                         │
│                                                                 │
│  State Management:                                              │
│  • AuthContext - Global authentication state                   │
│  • localStorage - Token persistence                            │
│                                                                 │
│  Services (API Integration):                                    │
│  • authService - Authentication API calls                      │
│  • fareService - Fare calculations                             │
│  • locationService - Location management                       │
│  • routeService - Route management                             │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ REST API Calls
                 │ (Axios with JWT tokens)
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DJANGO BACKEND (Port 8000)                     │
├─────────────────────────────────────────────────────────────────┤
│  Django REST Framework:                                          │
│                                                                  │
│  Authentication:                                                 │
│  • JWT Token Authentication (Simple JWT)                        │
│  • Token Refresh & Blacklist                                    │
│  • Role-based Permissions                                       │
│                                                                  │
│  API Endpoints:                                                  │
│  • /api/auth/*        - Authentication endpoints               │
│  • /api/users/        - User management                        │
│  • /api/locations/    - Location CRUD                          │
│  • /api/routes/       - Route management                       │
│  • /api/fares/        - Fare management                        │
│  • /api/fare-calculations/ - Fare history                      │
│  • /api/vehicles/     - Vehicle management                     │
│  • /api/discount-cards/ - Discount cards                       │
│  • /api/incidents/    - Incident reports                       │
│                                                                  │
│  Apps:                                                           │
│  • users - User & authentication                                │
│  • locations - Location data                                    │
│  • routes - Route data                                          │
│  • fares - Fare calculations                                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Database Queries (ORM)
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                           │
├─────────────────────────────────────────────────────────────────┤
│  Tables:                                                         │
│  • users_user             - User accounts & roles               │
│  • locations_location     - Barangays, landmarks, sitios        │
│  • routes_route          - Transportation routes                │
│  • fares_fare            - Fare pricing                         │
│  • fares_farecalculation - Calculation history                  │
│  • users_vehicle         - Driver vehicles                      │
│  • users_discountcard    - Discount eligibility                 │
│  • users_discountusagelog - Discount tracking                   │
│  • users_incident        - Incident reports                     │
└─────────────────────────────────────────────────────────────────┘

                        ┌────────────────┐
                        │ External APIs  │
                        ├────────────────┤
                        │ Google Maps    │
                        │ Distance Matrix│
                        │ Directions API │
                        └────────────────┘
                                ▲
                                │
                        Django Backend
                        (API Calls)

## 🔄 Authentication Flow

┌──────────┐         ┌──────────┐         ┌──────────┐
│  React   │         │  Django  │         │   JWT    │
│  Client  │         │  Backend │         │  Tokens  │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                    │                     │
     │ 1. Login Request   │                     │
     │ (username/password)│                     │
     ├───────────────────>│                     │
     │                    │                     │
     │                    │ 2. Verify Credentials
     │                    │                     │
     │                    │ 3. Generate Tokens  │
     │                    ├────────────────────>│
     │                    │                     │
     │ 4. Return Tokens   │                     │
     │ (access + refresh) │                     │
     │<───────────────────┤                     │
     │                    │                     │
     │ 5. Store in        │                     │
     │    localStorage    │                     │
     │                    │                     │
     │ 6. API Request     │                     │
     │    + Bearer Token  │                     │
     ├───────────────────>│                     │
     │                    │                     │
     │                    │ 7. Verify Token     │
     │                    ├────────────────────>│
     │                    │                     │
     │                    │ 8. Token Valid      │
     │                    │<────────────────────┤
     │                    │                     │
     │ 9. Return Data     │                     │
     │<───────────────────┤                     │
     │                    │                     │

## 🧮 Fare Calculation Flow

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  React   │    │  Django  │    │ Google   │    │  Haversine│
│  Form    │    │  Backend │    │  Maps    │    │  Formula │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │
     │ 1. Submit     │               │               │
     │    Origin +   │               │               │
     │    Destination│               │               │
     ├──────────────>│               │               │
     │               │               │               │
     │               │ 2. Try Google │               │
     │               │    Maps API   │               │
     │               ├──────────────>│               │
     │               │               │               │
     │               │ 3. Distance + │               │
     │               │    Duration   │               │
     │               │<──────────────┤               │
     │               │               │               │
     │               │ (If API fails)                │
     │               │ 4. Fallback   │               │
     │               │    to GPS     │               │
     │               ├──────────────────────────────>│
     │               │               │               │
     │               │ 5. Distance   │               │
     │               │<──────────────────────────────┤
     │               │               │               │
     │               │ 6. Calculate Fare:            │
     │               │    • Base: ₱15 (first 3km)   │
     │               │    • Additional: ₱3/km        │
     │               │    • Round to ₱0.50           │
     │               │    • Apply discount (20%)     │
     │               │                               │
     │ 7. Return     │                               │
     │    Fare Data  │                               │
     │<──────────────┤                               │
     │               │                               │
     │ 8. Display    │                               │
     │    Results    │                               │
     │               │                               │

## 📁 File Structure

```
Basey Fare Guide 2.0/
│
├── frontend/                  # React Application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # State management
│   │   ├── services/         # API integration
│   │   ├── App.js           # Main app
│   │   └── config.js        # Configuration
│   ├── .env                 # Environment variables
│   └── package.json         # Dependencies
│
├── bfg/                      # Django Project Settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
│
├── users/                    # Users Django App
│   ├── models.py            # User, Vehicle, DiscountCard, Incident
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   └── auth_views.py        # Auth endpoints
│
├── locations/                # Locations Django App
│   ├── models.py            # Location model
│   ├── views.py             # CRUD views
│   └── serializers.py       # Serializers
│
├── routes/                   # Routes Django App
│   ├── models.py            # Route model
│   ├── views.py             # Route calculation
│   └── serializers.py       # Serializers
│
├── fares/                    # Fares Django App
│   ├── models.py            # Fare, FareCalculation
│   ├── views.py             # Fare views
│   ├── fare_calculator.py   # Fare logic
│   └── serializers.py       # Serializers
│
├── manage.py                 # Django management
├── requirements.txt          # Python dependencies
├── start-dev.ps1            # Start script
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
└── REACT_INTEGRATION.md     # Integration guide

```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Frontend Security:                                      │
│     • Protected Routes (PrivateRoute component)            │
│     • Token storage in localStorage                        │
│     • Automatic token refresh                              │
│     • HTTPS (production)                                   │
│                                                             │
│  2. API Security:                                           │
│     • JWT Token Authentication                             │
│     • Token expiration (7 days access, 30 days refresh)   │
│     • Token blacklist on logout                            │
│     • CORS configuration                                   │
│     • Role-based permissions                               │
│                                                             │
│  3. Backend Security:                                       │
│     • Django security middleware                           │
│     • CSRF protection                                      │
│     • SQL injection prevention (ORM)                       │
│     • XSS prevention                                       │
│     • Password hashing (bcrypt)                            │
│                                                             │
│  4. Database Security:                                      │
│     • Encrypted connections                                │
│     • User permissions                                     │
│     • Prepared statements                                  │
│     • Regular backups                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │   Domain     │
                    │ (HTTPS/SSL)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Nginx      │
                    │ (Reverse     │
                    │  Proxy)      │
                    └──┬─────────┬─┘
                       │         │
         ┌─────────────┘         └─────────────┐
         │                                      │
    ┌────▼────┐                          ┌─────▼────┐
    │ Static  │                          │ Gunicorn │
    │ Files   │                          │ Django   │
    │ (React  │                          │ Backend  │
    │  Build) │                          └─────┬────┘
    └─────────┘                                │
                                        ┌──────▼──────┐
                                        │ PostgreSQL  │
                                        │  Database   │
                                        └─────────────┘
```

This architecture provides a solid foundation for the Basey Fare Guide system!
