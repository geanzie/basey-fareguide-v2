# 🚀 Quick Start Guide

## Prerequisites

- Python 3.11+
- PostgreSQL (or use Neon cloud)
- Node.js 18+ (for React frontend)
- Google Maps API key

## 1. Clone & Setup

```bash
git clone https://github.com/geanzie/basey-fareguide-v2.git
cd basey-fareguide-v2
```

## 2. Backend Setup

### Create Virtual Environment
```bash
python -m venv BFG-env
BFG-env\Scripts\activate  # Windows
source BFG-env/bin/activate  # Mac/Linux
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
Copy `.env.example` to `.env` and fill in:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=your-database-url
GOOGLE_MAPS_API_KEY=your-maps-key
GOOGLE_MAPS_SERVER_API_KEY=your-server-key
```

### Initialize Database
```bash
python manage.py migrate
python populate_database.py  # Creates sample data + admin user
```

### Run Backend
```bash
python manage.py runserver
```

Backend runs at: http://localhost:8000

## 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at: http://localhost:3000

## 4. Default Credentials

**Important:** Change these after first login!

- **Admin:** username: `admin`, password: (set in populate_database.py)
- **Test User:** username: `testuser`, password: (set in populate_database.py)

## 5. Verify Installation

Test the API:
```bash
curl http://localhost:8000/api/locations/
```

Access admin panel: http://localhost:8000/admin/

## Next Steps

- Review API documentation: `docs/API.md`
- Deploy to production: `docs/DEPLOYMENT.md`
- Customize fare calculations in `fares/fare_calculator.py`

## Troubleshooting

**Database connection errors:**
- Verify DATABASE_URL in .env
- Check PostgreSQL is running

**CORS errors:**
- Ensure frontend URL is in CORS_ALLOWED_ORIGINS (settings.py)

**Import errors:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

## Project Structure

```
basey-fareguide-v2/
├── manage.py              # Django management
├── populate_database.py   # Setup script
├── bfg/                   # Django settings
├── fares/                 # Fare calculation app
├── locations/             # Locations app
├── routes/                # Routes app
├── users/                 # Users & auth app
└── frontend/              # React app
```
