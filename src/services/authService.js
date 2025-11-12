import api from './api';
import { API_ENDPOINTS, ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from '../config';

const authService = {
  // Register new user
  register: async (userData) => {
    const response = await api.post(API_ENDPOINTS.AUTH_REGISTER, userData);
    if (response.data.tokens) {
      localStorage.setItem(ACCESS_TOKEN_KEY, response.data.tokens.access);
      localStorage.setItem(REFRESH_TOKEN_KEY, response.data.tokens.refresh);
    }
    return response.data;
  },

  // Login user
  login: async (credentials) => {
    const response = await api.post(API_ENDPOINTS.AUTH_LOGIN, credentials);
    if (response.data.tokens) {
      localStorage.setItem(ACCESS_TOKEN_KEY, response.data.tokens.access);
      localStorage.setItem(REFRESH_TOKEN_KEY, response.data.tokens.refresh);
    }
    return response.data;
  },

  // Logout user
  logout: async () => {
    try {
      const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
      if (refreshToken) {
        await api.post(API_ENDPOINTS.AUTH_LOGOUT, { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    }
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get(API_ENDPOINTS.AUTH_ME);
    return response.data;
  },

  // Update user profile
  updateProfile: async (profileData) => {
    const response = await api.put(API_ENDPOINTS.AUTH_PROFILE, profileData);
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  // Get access token
  getAccessToken: () => {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },
};

export default authService;
