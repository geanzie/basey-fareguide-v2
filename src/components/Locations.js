import React, { useState, useEffect } from 'react';
import locationService from '../services/locationService';
import './Locations.css';

const Locations = () => {
  const [locations, setLocations] = useState([]);
  const [filteredLocations, setFilteredLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);

  useEffect(() => {
    loadLocations();
  }, []);

  useEffect(() => {
    filterLocations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm, filterType, locations]);

  const loadLocations = async () => {
    try {
      const data = await locationService.getLocations();
      setLocations(data.results || data);
    } catch (err) {
      console.error('Failed to load locations:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterLocations = () => {
    let filtered = locations;

    // Filter by type
    if (filterType !== 'ALL') {
      filtered = filtered.filter((loc) => loc.type === filterType);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter((loc) =>
        loc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (loc.description && loc.description.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    setFilteredLocations(filtered);
    setCurrentPage(1); // Reset to first page when filters change
  };

  // Pagination calculations
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredLocations.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredLocations.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: 'smooth' });
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

  if (loading) {
    return (
      <div className="locations-container">
        <div className="loading">Loading locations...</div>
      </div>
    );
  }

  return (
    <div className="locations-container">
      <div className="locations-header">
        <h1>Locations in Basey, Samar</h1>
        <p>Browse barangays, landmarks, and sitios</p>
      </div>

      <div className="locations-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search locations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filterType === 'ALL' ? 'active' : ''}`}
            onClick={() => setFilterType('ALL')}
          >
            All ({locations.length})
          </button>
          <button
            className={`filter-btn ${filterType === 'BARANGAY' ? 'active' : ''}`}
            onClick={() => setFilterType('BARANGAY')}
          >
            Barangays ({locations.filter((l) => l.type === 'BARANGAY').length})
          </button>
          <button
            className={`filter-btn ${filterType === 'LANDMARK' ? 'active' : ''}`}
            onClick={() => setFilterType('LANDMARK')}
          >
            Landmarks ({locations.filter((l) => l.type === 'LANDMARK').length})
          </button>
          <button
            className={`filter-btn ${filterType === 'SITIO' ? 'active' : ''}`}
            onClick={() => setFilterType('SITIO')}
          >
            Sitios ({locations.filter((l) => l.type === 'SITIO').length})
          </button>
        </div>
      </div>

      <div className="locations-table-container">
        {filteredLocations.length === 0 ? (
          <div className="no-results">
            <p>No locations found matching your criteria.</p>
          </div>
        ) : (
          <>
            <div className="table-info">
              Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredLocations.length)} of {filteredLocations.length} locations
            </div>
            <table className="locations-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Barangay</th>
                  <th>Coordinates</th>
                </tr>
              </thead>
              <tbody>
                {currentItems.map((location) => (
                  <tr key={location.id}>
                    <td className="location-name">{location.name}</td>
                    <td className="location-type">{location.type}</td>
                    <td className="location-barangay">{location.barangay || '-'}</td>
                    <td className="location-coordinates">
                      {location.latitude != null && location.longitude != null
                        ? `${Number(location.latitude).toFixed(6)}, ${Number(location.longitude).toFixed(6)}`
                        : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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

export default Locations;
