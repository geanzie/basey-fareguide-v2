import api from './api';
import { API_ENDPOINTS } from '../config';
import locationService from './locationService';

const fareService = {
  // Calculate fare
  calculateFare: async (fareData) => {
    // Get location details to extract coordinates
    const [originLocation, destinationLocation] = await Promise.all([
      locationService.getLocationById(fareData.origin_location),
      locationService.getLocationById(fareData.destination_location)
    ]);

    // Transform the data to match backend expectations
    const requestData = {
      origin: [originLocation.latitude, originLocation.longitude],
      destination: [destinationLocation.latitude, destinationLocation.longitude],
      use_google_maps: fareData.calculation_method === 'GOOGLE_MAPS',
      passenger_type: fareData.passenger_type || 'REGULAR',
    };

    // Add user_id if authenticated
    if (fareData.user_id) {
      requestData.user_id = fareData.user_id;
    }

    const response = await api.post(API_ENDPOINTS.ROUTE_CALCULATE, requestData);
    
    // Add additional context to the response
    return {
      ...response.data,
      origin_location: originLocation,
      destination_location: destinationLocation,
      passenger_type: fareData.passenger_type,
    };
  },

  // Get all fares
  getFares: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.FARES, { params });
    return response.data;
  },

  // Get fare by ID
  getFareById: async (id) => {
    const response = await api.get(`${API_ENDPOINTS.FARES}${id}/`);
    return response.data;
  },

  // Get fare calculations history
  getFareCalculations: async (params = {}) => {
    const response = await api.get(API_ENDPOINTS.FARE_CALCULATIONS, { params });
    return response.data;
  },

  // Get user's fare calculation history
  getUserFareHistory: async () => {
    const response = await api.get(`${API_ENDPOINTS.FARE_CALCULATIONS}my_history/`);
    return response.data;
  },
};

export default fareService;
