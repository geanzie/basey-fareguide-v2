import React, { useState, useEffect } from 'react';
import './Routes.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://web-production-8fd2c.up.railway.app/v2'
    : 'http://localhost:8000/v2');

const Routes = () => {
  const [routes, setRoutes] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    origin: '',
    destination: '',
    transport_type: '',
    search: ''
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadLocations();
  }, []);

  useEffect(() => {
    loadRoutes();
  }, [page, filters]);

  const loadLocations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/locations/`);
      const data = await response.json();
      setLocations(data.results || data);
    } catch (err) {
      console.error('Failed to load locations:', err);
    }
  };

  const loadRoutes = async () => {
    setLoading(true);
    setError('');
    
    try {
      const params = new URLSearchParams();
      params.append('page', page);
      
      if (filters.origin) params.append('origin', filters.origin);
      if (filters.destination) params.append('destination', filters.destination);
      if (filters.transport_type) params.append('transport_type', filters.transport_type);
      if (filters.search) params.append('search', filters.search);

      const response = await fetch(`${API_BASE_URL}/routes/?${params.toString()}`);
      const data = await response.json();
      
      setRoutes(data.results || []);
      setTotalPages(Math.ceil((data.count || data.length) / 10));
    } catch (err) {
      setError('Failed to load routes. Please try again.');
      console.error('Error loading routes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
    setPage(1);
  };

  const clearFilters = () => {
    setFilters({
      origin: '',
      destination: '',
      transport_type: '',
      search: ''
    });
    setPage(1);
  };

  const getFareForRoute = async (routeId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/fares/?route=${routeId}`);
      const data = await response.json();
      return data.results || [];
    } catch (err) {
      console.error('Failed to load fares:', err);
      return [];
    }
  };

  const getTransportIcon = (type) => {
    const icons = {
      'TRICYCLE': '🛺',
      'JEEPNEY': '🚌',
      'MOTORCYCLE': '🏍️',
      'HABAL_HABAL': '🏍️',
      'VAN': '🚐',
      'BOAT': '⛵'
    };
    return icons[type] || '🚗';
  };

  return (
    <div className="routes-container">
      <div className="routes-header">
        <h1>Available Routes</h1>
        <p className="routes-subtitle">Browse all transportation routes in Basey, Samar</p>
      </div>

      <div className="routes-filters">
        <div className="filter-group">
          <input
            type="text"
            name="search"
            placeholder="Search locations..."
            value={filters.search}
            onChange={handleFilterChange}
            className="filter-input"
          />
        </div>

        <div className="filter-group">
          <select
            name="origin"
            value={filters.origin}
            onChange={handleFilterChange}
            className="filter-select"
          >
            <option value="">All Origins</option>
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>
                {loc.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <select
            name="destination"
            value={filters.destination}
            onChange={handleFilterChange}
            className="filter-select"
          >
            <option value="">All Destinations</option>
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>
                {loc.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <select
            name="transport_type"
            value={filters.transport_type}
            onChange={handleFilterChange}
            className="filter-select"
          >
            <option value="">All Transport Types</option>
            <option value="TRICYCLE">Tricycle</option>
            <option value="JEEPNEY">Jeepney</option>
            <option value="MOTORCYCLE">Motorcycle</option>
            <option value="HABAL_HABAL">Habal-Habal</option>
            <option value="VAN">Van</option>
            <option value="BOAT">Boat</option>
          </select>
        </div>

        <button onClick={clearFilters} className="btn-clear-filters">
          Clear Filters
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading-spinner">Loading routes...</div>
      ) : (
        <>
          <div className="routes-grid">
            {routes.length === 0 ? (
              <div className="no-routes">
                <p>No routes found matching your filters.</p>
              </div>
            ) : (
              routes.map((route) => (
                <RouteCard 
                  key={route.id} 
                  route={route} 
                  getTransportIcon={getTransportIcon}
                  getFareForRoute={getFareForRoute}
                />
              ))
            )}
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="btn-page"
              >
                Previous
              </button>
              <span className="page-info">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage(Math.min(totalPages, page + 1))}
                disabled={page === totalPages}
                className="btn-page"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

const RouteCard = ({ route, getTransportIcon, getFareForRoute }) => {
  const [showFares, setShowFares] = useState(false);
  const [fares, setFares] = useState([]);
  const [loadingFares, setLoadingFares] = useState(false);

  const handleShowFares = async () => {
    if (!showFares && fares.length === 0) {
      setLoadingFares(true);
      const routeFares = await getFareForRoute(route.id);
      setFares(routeFares);
      setLoadingFares(false);
    }
    setShowFares(!showFares);
  };

  return (
    <div className="route-card">
      <div className="route-header">
        <div className="transport-icon">
          {getTransportIcon(route.transport_type)}
        </div>
        <div className="route-title">
          <h3>{route.origin_name || route.origin}</h3>
          <span className="route-arrow">→</span>
          <h3>{route.destination_name || route.destination}</h3>
        </div>
      </div>

      <div className="route-details">
        <div className="detail-item">
          <span className="detail-label">Transport:</span>
          <span className="detail-value">{route.transport_type.replace('_', ' ')}</span>
        </div>
        
        {route.distance_km && (
          <div className="detail-item">
            <span className="detail-label">Distance:</span>
            <span className="detail-value">{route.distance_km} km</span>
          </div>
        )}
        
        {route.estimated_duration_minutes && (
          <div className="detail-item">
            <span className="detail-label">Duration:</span>
            <span className="detail-value">~{route.estimated_duration_minutes} mins</span>
          </div>
        )}
      </div>

      <button onClick={handleShowFares} className="btn-show-fares">
        {showFares ? 'Hide' : 'Show'} Fares
      </button>

      {showFares && (
        <div className="fares-section">
          {loadingFares ? (
            <p>Loading fares...</p>
          ) : fares.length === 0 ? (
            <p>No fare information available</p>
          ) : (
            <div className="fares-list">
              {fares.map((fare) => (
                <div key={fare.id} className="fare-item">
                  <span className="fare-type">{fare.passenger_type}</span>
                  <span className="fare-amount">₱{parseFloat(fare.amount).toFixed(2)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Routes;
