import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import fareService from '../services/fareService';
import authService from '../services/authService';
import './Profile.css';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [fareHistory, setFareHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
  });
  const [message, setMessage] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  useEffect(() => {
    loadFareHistory();
  }, []);

  const loadFareHistory = async () => {
    try {
      const data = await fareService.getUserFareHistory();
      setFareHistory(data.results || data);
    } catch (err) {
      console.error('Failed to load fare history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    
    try {
      const updatedUser = await authService.updateProfile(formData);
      updateUser(updatedUser);
      setEditMode(false);
      setMessage('Profile updated successfully!');
    } catch (err) {
      setMessage('Failed to update profile. Please try again.');
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'ADMIN':
        return '#f44336';
      case 'MODERATOR':
        return '#ff9800';
      case 'DRIVER':
        return '#2196f3';
      default:
        return '#4caf50';
    }
  };

  // Pagination calculations
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = fareHistory.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(fareHistory.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    
    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      if (currentPage <= 3) {
        for (let i = 1; i <= 4; i++) pages.push(i);
        pages.push('...');
        pages.push(totalPages);
      } else if (currentPage >= totalPages - 2) {
        pages.push(1);
        pages.push('...');
        for (let i = totalPages - 3; i <= totalPages; i++) pages.push(i);
      } else {
        pages.push(1);
        pages.push('...');
        pages.push(currentPage - 1);
        pages.push(currentPage);
        pages.push(currentPage + 1);
        pages.push('...');
        pages.push(totalPages);
      }
    }
    return pages;
  };

  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            {user?.first_name?.charAt(0) || user?.username?.charAt(0) || '?'}
          </div>
          <h2>{user?.first_name && user?.last_name 
            ? `${user.first_name} ${user.last_name}` 
            : user?.username}
          </h2>
          <span 
            className="role-badge" 
            style={{ backgroundColor: getRoleBadgeColor(user?.role) }}
          >
            {user?.role?.replace('_', ' ')}
          </span>
        </div>

        {message && (
          <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        {editMode ? (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            <div className="form-buttons">
              <button type="submit" className="btn-save">Save Changes</button>
              <button 
                type="button" 
                onClick={() => setEditMode(false)} 
                className="btn-cancel"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="profile-info">
            <div className="info-item">
              <span className="info-label">Username:</span>
              <span className="info-value">{user?.username}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Email:</span>
              <span className="info-value">{user?.email || 'Not provided'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Member Since:</span>
              <span className="info-value">
                {new Date(user?.created_at).toLocaleDateString()}
              </span>
            </div>
            <button onClick={() => setEditMode(true)} className="btn-edit">
              Edit Profile
            </button>
          </div>
        )}
      </div>

      <div className="fare-history-card">
        <h3>Fare Calculation History</h3>
        {loading ? (
          <p className="loading">Loading history...</p>
        ) : fareHistory.length === 0 ? (
          <p className="no-history">No fare calculations yet. Start calculating fares!</p>
        ) : (
          <>
            <div className="table-info">
              Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, fareHistory.length)} of {fareHistory.length} calculations
            </div>
            <div className="history-table-container">
              <table className="history-table">
                <thead>
                  <tr>
                    <th>Origin</th>
                    <th>Destination</th>
                    <th>Distance</th>
                    <th>Passenger Type</th>
                    <th>Fare</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {currentItems.map((calculation) => (
                    <tr key={calculation.id}>
                      <td>{calculation.origin_name}</td>
                      <td>{calculation.destination_name}</td>
                      <td>{calculation.distance_km.toFixed(2)} km</td>
                      <td>{calculation.passenger_type}</td>
                      <td className="fare-amount">₱{calculation.final_fare.toFixed(2)}</td>
                      <td>{new Date(calculation.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {totalPages > 1 && (
              <div className="pagination">
                <button
                  className="pagination-btn"
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                {getPageNumbers().map((page, index) => (
                  page === '...' ? (
                    <span key={`ellipsis-${index}`} className="pagination-ellipsis">...</span>
                  ) : (
                    <button
                      key={page}
                      className={`pagination-btn ${currentPage === page ? 'active' : ''}`}
                      onClick={() => handlePageChange(page)}
                    >
                      {page}
                    </button>
                  )
                ))}
                <button
                  className="pagination-btn"
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Profile;
