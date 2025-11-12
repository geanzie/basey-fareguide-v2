# Basey Fare Guide - React Frontend Integration Guide

## ✅ Setup Complete!

Your Django backend has been successfully integrated with a React frontend!

## 🎯 What's Been Set Up

### 1. **React Application** (`frontend/` directory)
   - Created with Create React App
   - Installed dependencies: React Router, Axios, Google Maps API loader
   - Modern component-based architecture

### 2. **Django Backend Configuration**
   - CORS configured for React development server (port 3000)
   - Static files configuration for production builds
   - URL routing to serve React app
   - Template directory configured

### 3. **API Integration Layer**
   - Axios HTTP client with interceptors
   - Automatic JWT token refresh
   - Service modules for all API endpoints
   - Error handling and request/response transformation

### 4. **React Components**
   - **Home**: Landing page with features
   - **Login/Register**: Authentication pages
   - **FareCalculator**: Main fare calculation interface
   - **Locations**: Browse and search locations
   - **Profile**: User profile and fare history
   - **Navbar**: Navigation component
   - **PrivateRoute**: Route protection

### 5. **State Management**
   - AuthContext for global authentication state
   - User session persistence with localStorage
   - Protected routes with role-based access

## 🚀 How to Run

### Option 1: Development Mode (Recommended for Development)

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

Access:
- **React App**: http://localhost:3000 (hot reload enabled)
- **Django API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

### Option 2: Production Mode

Build React and serve from Django:

```powershell
cd frontend
npm run build
cd ..
python manage.py runserver
```

Access everything at: http://localhost:8000

## 📋 Features Available

### Public Features (No Login Required)
- ✅ View home page
- ✅ Browse locations
- ✅ Calculate fares
- ✅ Register new account
- ✅ Login

### Authenticated Features
- ✅ User profile management
- ✅ Fare calculation history
- ✅ Edit profile information
- ✅ View past calculations

### Admin Features (via Django Admin)
- ✅ Manage users
- ✅ Manage locations
- ✅ Manage routes
- ✅ Manage fares
- ✅ Review discount cards
- ✅ Handle incident reports

## 🔑 Test Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test User:**
- Username: `testuser`
- Password: `test123`

## 📁 Directory Structure

```
Basey Fare Guide 2.0/
├── frontend/                    # React application
│   ├── public/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── context/            # React context (state)
│   │   ├── services/           # API service modules
│   │   ├── App.js
│   │   ├── config.js
│   │   └── index.js
│   ├── .env                    # Frontend environment variables
│   └── package.json
├── bfg/                        # Django project settings
├── users/                      # Users app
├── locations/                  # Locations app
├── routes/                     # Routes app
├── fares/                      # Fares app
├── manage.py
└── requirements.txt
```

## 🔧 Configuration Files

### Frontend Environment Variables (`.env`)
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_MAPS_API_KEY=
```

### Django Settings Updates
- ✅ CORS headers configured
- ✅ Static files for React build
- ✅ Template directory for React index.html
- ✅ Catch-all URL pattern for React routing

## 🎨 UI Features

- **Modern Design**: Purple gradient theme
- **Responsive**: Works on all devices
- **Smooth Animations**: Professional transitions
- **User Feedback**: Loading states and error messages
- **Intuitive Navigation**: Clear menu structure

## 🔐 Security Features

- JWT token-based authentication
- Automatic token refresh
- Protected routes
- CORS configuration
- Secure password handling

## 🛠️ Development Tips

### Hot Reload
- React: Automatic (development mode)
- Django: Automatic (when DEBUG=True)

### API Testing
- Use Django Browsable API: http://localhost:8000/api/
- Or use tools like Postman/Insomnia

### Database Management
```powershell
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
python manage.py shell          # Django shell
```

### React Development
```powershell
npm test                        # Run tests
npm run build                   # Build for production
npm install <package>           # Add new package
```

## 📡 API Endpoints Used by React

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/me/` - Get current user
- `PUT /api/auth/profile/` - Update profile

### Locations
- `GET /api/locations/` - List locations
- `GET /api/locations/{id}/` - Get location details

### Fare Calculation
- `POST /api/routes/calculate/` - Calculate fare
- `GET /api/fare-calculations/` - Fare history
- `GET /api/fare-calculations/my_history/` - User's history

## 🚀 Next Steps

1. **Add Google Maps API Key**:
   - Edit `frontend/.env`
   - Add your Google Maps API key
   - Enable Distance Matrix API in Google Cloud Console

2. **Customize Design**:
   - Edit CSS files in `frontend/src/components/`
   - Update colors, fonts, layouts as needed

3. **Add More Features**:
   - Discount card management UI
   - Incident reporting UI
   - Real-time updates with WebSockets
   - Map visualization with Google Maps

4. **Testing**:
   - Write unit tests for components
   - Write integration tests for API calls
   - Test on different devices

5. **Deployment**:
   - Build React app for production
   - Deploy Django with Gunicorn/uWSGI
   - Set up reverse proxy (Nginx)
   - Configure production database

## ❓ Troubleshooting

### CORS Errors
- Ensure Django server is running
- Check CORS settings in `bfg/settings.py`
- Verify API URL in `frontend/.env`

### 404 on React Routes
- Build React app: `npm run build`
- Restart Django server

### Token Errors
- Clear localStorage in browser DevTools
- Login again to get new tokens

### Port Conflicts
- Django: Change port with `python manage.py runserver 8001`
- React: Set PORT=3001 in `.env` before `npm start`

## 📚 Documentation

- [React Documentation](https://react.dev/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Router](https://reactrouter.com/)
- [Axios](https://axios-http.com/)

## ✨ Summary

You now have a fully integrated Django + React application for the Basey Fare Guide! The frontend provides a modern, responsive interface while the Django backend handles all business logic, authentication, and database operations.

Start both servers and begin testing the application. Happy coding! 🎉
