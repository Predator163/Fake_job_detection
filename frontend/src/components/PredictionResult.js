import React from 'react';
import './PredictionResult.css';

const PredictionResult = ({ prediction, onReset }) => {
  const { 
    prediction: result, 
    fraud_probability, 
    legitimate_probability, 
    risk_level,
    is_fraudulent 
  } = prediction;

  const getRiskColor = () => {
    if (risk_level === 'High Risk') return '#dc3545';
    if (risk_level === 'Medium Risk') return '#ffc107';
    return '#28a745';
  };

  const getResultIcon = () => {
    if (is_fraudulent) return '⚠️';
    return '✅';
  };

  return (
    <div className="prediction-result">
      <div className="result-card">
        <div className="result-header" style={{ borderColor: getRiskColor() }}>
          <span className="result-icon">{getResultIcon()}</span>
          <h2>{result}</h2>
        </div>

        <div className="result-body">
          <div className="risk-badge" style={{ backgroundColor: getRiskColor() }}>
            {risk_level}
          </div>

          <div className="probability-section">
            <h3>Prediction Confidence</h3>
            
            <div className="probability-item">
              <div className="probability-label">
                <span className="label-text">Fraudulent</span>
                <span className="label-value">{fraud_probability.toFixed(2)}%</span>
              </div>
              <div className="probability-bar">
                <div 
                  className="probability-fill fraud"
                  style={{ width: `${fraud_probability}%` }}
                />
              </div>
            </div>

            <div className="probability-item">
              <div className="probability-label">
                <span className="label-text">Legitimate</span>
                <span className="label-value">{legitimate_probability.toFixed(2)}%</span>
              </div>
              <div className="probability-bar">
                <div 
                  className="probability-fill legitimate"
                  style={{ width: `${legitimate_probability}%` }}
                />
              </div>
            </div>
          </div>

          {is_fraudulent && (
            <div className="warning-box">
              <h4>⚠️ Warning Signs</h4>
              <ul>
                <li>This job posting shows characteristics commonly found in fraudulent listings</li>
                <li>Exercise extreme caution before providing personal information</li>
                <li>Verify the company through official channels</li>
                <li>Never pay money upfront for a job opportunity</li>
                <li>Be wary of unrealistic salary offers or vague job descriptions</li>
              </ul>
            </div>
          )}

          {!is_fraudulent && (
            <div className="success-box">
              <h4>✅ Appears Legitimate</h4>
              <p>
                This job posting appears to be legitimate based on our analysis. 
                However, always verify company details and be cautious when sharing 
                personal information.
              </p>
            </div>
          )}
        </div>

        <div className="result-footer">
          <button onClick={onReset} className="btn-analyze-another">
            Analyze Another Job Posting
          </button>
        </div>
      </div>

      <div className="disclaimer">
        <p>
          <strong>Disclaimer:</strong> This prediction is based on machine learning analysis 
          and should be used as a guide only. Always perform your own due diligence when 
          evaluating job opportunities.
        </p>
      </div>
    </div>
  );
};

export default PredictionResult;