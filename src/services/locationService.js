import api from './api';
import { API_ENDPOINTS } from '../config';

const locationService = {
  // Get all locations
  getLocations: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.LOCATIONS, { params });
    return response.data;
  },

  // Get location by ID
  getLocationById: async (id) => {
    const response = await api.get(`${API_ENDPOINTS.LOCATIONS}${id}/`);
    return response.data;
  },

  // Create location (admin only)
  createLocation: async (locationData) => {
    const response = await api.post(API_ENDPOINTS.LOCATIONS, locationData);
    return response.data;
  },

  // Update location (admin only)
  updateLocation: async (id, locationData) => {
    const response = await api.put(`${API_ENDPOINTS.LOCATIONS}${id}/`, locationData);
    return response.data;
  },

  // Delete location (admin only)
  deleteLocation: async (id) => {
    const response = await api.delete(`${API_ENDPOINTS.LOCATIONS}${id}/`);
    return response.data;
  },

  // Search locations
  searchLocations: async (searchTerm) => {
    const response = await api.get(API_ENDPOINTS.LOCATIONS, {
      params: { search: searchTerm },
    });
    return response.data;
  },
};

export default locationService;
