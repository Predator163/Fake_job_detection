import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import JobPostingForm from './components/JobPostingForm';
import PredictionResult from './components/PredictionResult';

// Add this at the top of your component
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Updated API call
      const response = await axios.post(`${API_BASE_URL}/api/predict/`, formData);
      
      if (response.data.success) {
        setPrediction(response.data.data);
      } else {
        setError('Prediction failed. Please try again.');
      }
    } catch (err) {
      console.error('Prediction error:', err);
      setError(
        err.response?.data?.details || 
        err.response?.data?.error || 
        'An error occurred while making the prediction. Please check if the backend server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Job Fraud Detection System</h1>
        <p className="subtitle">Detect fraudulent job postings using AI</p>
      </header>

      <main className="App-main">
        <div className="container">
          {!prediction && (
            <JobPostingForm 
              onSubmit={handlePredict} 
              loading={loading}
            />
          )}

          {error && (
            <div className="error-message">
              <h3>❌ Error</h3>
              <p>{error}</p>
              <button onClick={handleReset} className="btn-reset">
                Try Again
              </button>
            </div>
          )}

          {prediction && (
            <PredictionResult 
              prediction={prediction} 
              onReset={handleReset}
            />
          )}

          {loading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
              <p>Analyzing job posting...</p>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>© 2025 Job Fraud Detection System | Powered by Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;