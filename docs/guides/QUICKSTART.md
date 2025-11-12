# 🚀 Quick Start Guide - Basey Fare Guide with React

## Start the Application

### Development Mode (2 Terminals)

**Terminal 1 - Django Backend:**
```powershell
cd "C:\Users\OCENA\OneDrive\Documents\Python Projects late 2024\Basey Fare Guide 2.0"
.\BFG-env\Scripts\Activate.ps1
python manage.py runserver
```

**Terminal 2 - React Frontend:**
```powershell
cd "C:\Users\OCENA\OneDrive\Documents\Python Projects late 2024\Basey Fare Guide 2.0\frontend"
npm start
```

✅ **Access**: http://localhost:3000

---

### Production Mode (1 Terminal)

```powershell
cd "C:\Users\OCENA\OneDrive\Documents\Python Projects late 2024\Basey Fare Guide 2.0"
cd frontend
npm run build
cd ..
.\BFG-env\Scripts\Activate.ps1
python manage.py runserver
```

✅ **Access**: http://localhost:8000

---

## Test Accounts

**Admin:**
- Username: `admin`
- Password: `admin123`

**Regular User:**
- Username: `testuser`
- Password: `test123`

---

## Key URLs

- **React App**: http://localhost:3000 (dev mode)
- **Django Admin**: http://localhost:8000/admin
- **API Root**: http://localhost:8000/api
- **API Docs**: http://localhost:8000/api (browsable)

---

## Features to Try

1. ✅ **Register** a new account
2. ✅ **Login** with credentials
3. ✅ **Browse Locations** - search and filter
4. ✅ **Calculate Fare** - select origin, destination, passenger type
5. ✅ **View Profile** - see fare history
6. ✅ **Edit Profile** - update information

---

## Troubleshooting

### Port Already in Use
```powershell
# Django on different port
python manage.py runserver 8001

# React on different port (add to frontend/.env)
PORT=3001
```

### CORS Errors
- Make sure Django is running on port 8000
- Check `bfg/settings.py` CORS_ALLOWED_ORIGINS

### API Not Found
- Verify Django server is running
- Check API URL in `frontend/.env`

### Build Errors
```powershell
cd frontend
npm install  # Reinstall dependencies
npm start
```

---

## Development Tips

### Add Google Maps API Key
Edit `frontend/.env`:
```env
REACT_APP_GOOGLE_MAPS_API_KEY=your_key_here
```

### Database Commands
```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

### Clear Browser Data
If you have login issues:
1. Open Browser DevTools (F12)
2. Application → Local Storage
3. Clear `access_token` and `refresh_token`

---

## Project Structure

```
Basey Fare Guide 2.0/
├── frontend/           # React application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── context/
│   └── build/         # Production build (after npm run build)
├── bfg/               # Django settings
├── users/             # User management
├── locations/         # Location data
├── routes/            # Route data
├── fares/             # Fare calculations
└── manage.py
```

---

## 📚 Documentation

- `README.md` - Main project documentation
- `API_GUIDE.md` - API endpoints reference
- `REACT_INTEGRATION.md` - Detailed React setup guide
- `frontend/README.md` - Frontend-specific docs

---

## Need Help?

Check the logs:
- Django: Terminal output
- React: Browser console (F12)
- Network: Browser DevTools → Network tab

Happy coding! 🎉
