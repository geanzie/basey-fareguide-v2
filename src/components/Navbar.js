import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <img src="/logo.png" alt="Basey Fare Guide Logo" style={{width: '40px', height: '40px', marginRight: '10px'}} />
          Basey Fare Guide
        </Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">Home</Link>
          </li>
          <li className="navbar-item">
            <Link to="/fare-calculator" className="navbar-link">Calculate Fare</Link>
          </li>
          <li className="navbar-item">
            <Link to="/locations" className="navbar-link">Locations</Link>
          </li>
          {isAuthenticated ? (
            <>
              <li className="navbar-item">
                <Link to="/profile" className="navbar-link">
                  👤 {user?.username}
                </Link>
              </li>
              <li className="navbar-item">
                <button onClick={handleLogout} className="navbar-link btn-logout">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li className="navbar-item">
                <Link to="/login" className="navbar-link">Login</Link>
              </li>
              <li className="navbar-item">
                <Link to="/register" className="navbar-link btn-register">Register</Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
