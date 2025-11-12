import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="home-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Welcome to Basey Fare Guide</h1>
          <p className="hero-subtitle">
            Your reliable tricycle fare calculator for Basey, Samar
          </p>
          {isAuthenticated && user && (
            <p className="welcome-message">
              Hello, <strong>{user.first_name || user.username}</strong>!
            </p>
          )}
          <div className="hero-buttons">
            <Link to="/fare-calculator" className="btn btn-primary">
              Calculate Fare Now
            </Link>
            {!isAuthenticated && (
              <Link to="/register" className="btn btn-secondary">
                Get Started
              </Link>
            )}
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Fare Calculator</h3>
            <p>Calculate accurate tricycle fares based on distance and passenger type</p>
          </div>
          <div className="feature-card">
            <h3>Location Search</h3>
            <p>Find barangays, landmarks, and popular destinations in Basey</p>
          </div>
          <div className="feature-card">
            <h3>Discount System</h3>
            <p>20% discount for Senior Citizens, PWDs, and Students with valid IDs</p>
          </div>
          <div className="feature-card">
            <h3>Route Information</h3>
            <p>View established routes with distance and estimated travel time</p>
          </div>
          <div className="feature-card">
            <h3>Mobile Friendly</h3>
            <p>Access fare information on any device, anywhere</p>
          </div>
          <div className="feature-card">
            <h3>Secure & Private</h3>
            <p>Your data is protected with industry-standard security</p>
          </div>
        </div>
      </section>

      <section className="info-section">
        <h2>How It Works</h2>
        <div className="steps-grid">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Select Locations</h3>
            <p>Choose your pickup and destination points from our database</p>
          </div>
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Choose Passenger Type</h3>
            <p>Select regular or discounted passenger type</p>
          </div>
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Get Fare Estimate</h3>
            <p>Receive accurate fare calculation based on the formula</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to Calculate Your Fare?</h2>
        <p>Start using Basey Fare Guide today for accurate tricycle fare estimates</p>
        <Link to="/fare-calculator" className="btn btn-primary btn-large">
          Calculate Fare Now
        </Link>
      </section>
    </div>
  );
};

export default Home;
