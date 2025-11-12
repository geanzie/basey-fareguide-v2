import React, { useState, useEffect } from 'react';
import fareService from '../services/fareService';
import locationService from '../services/locationService';
import { useAuth } from '../context/AuthContext';
import './FareCalculator.css';

const FareCalculator = () => {
  const { isAuthenticated, user } = useAuth();
  const [locations, setLocations] = useState([]);
  const [formData, setFormData] = useState({
    origin_location: '',
    destination_location: '',
    passenger_type: 'REGULAR',
    calculation_method: 'GOOGLE_MAPS',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const data = await locationService.getLocations();
      setLocations(data.results || data);
    } catch (err) {
      console.error('Failed to load locations:', err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    if (formData.origin_location === formData.destination_location) {
      setError('Origin and destination must be different locations');
      setLoading(false);
      return;
    }

    try {
      // Add user_id if authenticated
      const requestData = {
        ...formData,
        ...(isAuthenticated && user?.id && { user_id: user.id })
      };
      
      const data = await fareService.calculateFare(requestData);
      setResult(data);
    } catch (err) {
      console.error('Fare calculation error:', err);
      setError(err.response?.data?.error || err.response?.data?.detail || 'Failed to calculate fare. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fare-calculator-container">
      <div className="calculator-card">
        <h1>Tricycle Fare Calculator</h1>
        <p className="calculator-subtitle">Calculate your fare for tricycle rides in Basey, Samar</p>

        <form onSubmit={handleSubmit} className="calculator-form">
          <div className="form-group">
            <label htmlFor="origin_location">Pickup Location</label>
            <select
              id="origin_location"
              name="origin_location"
              value={formData.origin_location}
              onChange={handleChange}
              required
            >
              <option value="">Select pickup location</option>
              {locations.map((location) => (
                <option key={location.id} value={location.id}>
                  {location.name} ({location.type})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="destination_location">Destination</label>
            <select
              id="destination_location"
              name="destination_location"
              value={formData.destination_location}
              onChange={handleChange}
              required
            >
              <option value="">Select destination</option>
              {locations.map((location) => (
                <option key={location.id} value={location.id}>
                  {location.name} ({location.type})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="passenger_type">Passenger Type</label>
            <select
              id="passenger_type"
              name="passenger_type"
              value={formData.passenger_type}
              onChange={handleChange}
              required
            >
              <option value="REGULAR">Regular (Full Fare)</option>
              <option value="SENIOR">Senior Citizen (20% Discount)</option>
              <option value="PWD">PWD (20% Discount)</option>
              <option value="STUDENT">Student (20% Discount)</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="calculation_method">Calculation Method</label>
            <select
              id="calculation_method"
              name="calculation_method"
              value={formData.calculation_method}
              onChange={handleChange}
            >
              <option value="GOOGLE_MAPS">Google Maps (Recommended)</option>
              <option value="HAVERSINE">GPS Distance</option>
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="btn-calculate">
            {loading ? 'Calculating...' : 'Calculate Fare'}
          </button>
        </form>

        {result && result.success && (
          <div className="result-card">
            <h2>Fare Calculation Result</h2>
            <div className="result-details">
              <div className="result-item">
                <span className="result-label">Distance:</span>
                <span className="result-value">
                  {result.distance?.kilometers?.toFixed(2) || '0.00'} km
                </span>
              </div>
              {result.route?.duration?.text && (
                <div className="result-item">
                  <span className="result-label">Estimated Time:</span>
                  <span className="result-value">{result.route.duration.text}</span>
                </div>
              )}
              <div className="result-item">
                <span className="result-label">Base Fare:</span>
                <span className="result-value">
                  ₱{result.fare?.breakdown?.base_fare?.toFixed(2) || '0.00'}
                </span>
              </div>
              {result.fare?.discount_applied > 0 && (
                <div className="result-item discount">
                  <span className="result-label">Discount (20%):</span>
                  <span className="result-value">
                    -₱{result.fare.discount_applied.toFixed(2)}
                  </span>
                </div>
              )}
              <div className="result-item total">
                <span className="result-label">Total Fare:</span>
                <span className="result-value fare-amount">
                  ₱{result.fare?.fare?.toFixed(2) || '0.00'}
                </span>
              </div>
            </div>
            <div className="result-info">
              <p><strong>Method:</strong> {result.method === 'google_maps' ? 'Google Maps' : 'GPS Distance (Haversine Formula)'}</p>
              {result.method !== 'google_maps' && formData.calculation_method === 'GOOGLE_MAPS' && (
                <p className="info-text" style={{ color: '#ff9800', fontSize: '0.9em' }}>
                  ℹ️ Using GPS calculation as fallback. Distance estimated using road network multiplier.
                </p>
              )}
              <p className="fare-formula">
                <strong>Formula:</strong> ₱15.00 for first 3km, then ₱3.00/km additional
                {result.fare?.discount_applied > 0 && ' (20% discount applied)'}
              </p>
              {result.origin_location && (
                <p><strong>From:</strong> {result.origin_location.name}</p>
              )}
              {result.destination_location && (
                <p><strong>To:</strong> {result.destination_location.name}</p>
              )}
            </div>
          </div>
        )}

        {result && !result.success && (
          <div className="error-message">
            {result.error || 'Failed to calculate fare. Please try again.'}
          </div>
        )}

        {!isAuthenticated && (
          <div className="info-box">
            <p>💡 <strong>Tip:</strong> Register an account to save your fare calculation history!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FareCalculator;
