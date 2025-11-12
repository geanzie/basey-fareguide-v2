import api from './api';
import { API_ENDPOINTS } from '../config';

const routeService = {
  // Get all routes
  getRoutes: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.ROUTES, { params });
    return response.data;
  },

  // Get route by ID
  getRouteById: async (id) => {
    const response = await api.get(`${API_ENDPOINTS.ROUTES}${id}/`);
    return response.data;
  },

  // Create route (admin only)
  createRoute: async (routeData) => {
    const response = await api.post(API_ENDPOINTS.ROUTES, routeData);
    return response.data;
  },

  // Update route (admin only)
  updateRoute: async (id, routeData) => {
    const response = await api.put(`${API_ENDPOINTS.ROUTES}${id}/`, routeData);
    return response.data;
  },

  // Delete route (admin only)
  deleteRoute: async (id) => {
    const response = await api.delete(`${API_ENDPOINTS.ROUTES}${id}/`);
    return response.data;
  },
};

export default routeService;
