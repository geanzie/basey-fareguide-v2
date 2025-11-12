// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/v2';
export const GOOGLE_MAPS_API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '';

// Token storage keys
export const ACCESS_TOKEN_KEY = 'access_token';
export const REFRESH_TOKEN_KEY = 'refresh_token';

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  AUTH_REGISTER: '/auth/register/',
  AUTH_LOGIN: '/auth/login/',
  AUTH_LOGOUT: '/auth/logout/',
  AUTH_ME: '/auth/me/',
  AUTH_PROFILE: '/auth/profile/',
  AUTH_TOKEN_REFRESH: '/auth/token/refresh/',
  
  // Users
  USERS: '/users/',
  
  // Locations
  LOCATIONS: '/locations/',
  
  // Routes
  ROUTES: '/routes/',
  ROUTE_CALCULATE: '/routes/calculate/',
  
  // Fares
  FARES: '/fares/',
  FARE_CALCULATIONS: '/fare-calculations/',
  
  // Vehicles
  VEHICLES: '/vehicles/',
  
  // Discount Cards
  DISCOUNT_CARDS: '/discount-cards/',
  DISCOUNT_USAGE_LOGS: '/discount-usage-logs/',
  
  // Incidents
  INCIDENTS: '/incidents/',
};
