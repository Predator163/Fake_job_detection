"""
Utility functions for job fraud prediction
"""
import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings


class JobFraudPredictor:
    """
    Class to handle job fraud prediction using the trained model
    """
    
    def __init__(self):
        self.model = None
        self.tfidf = None
        self.label_encoders = None
        self.feature_columns = None
        self.load_models()
    
    def load_models(self):
        """Load all saved models and preprocessors"""
        try:
            model_dir = settings.MODEL_DIR
            
            self.model = joblib.load(os.path.join(model_dir, 'fraud_detection_model.pkl'))
            self.tfidf = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
            self.label_encoders = joblib.load(os.path.join(model_dir, 'label_encoders.pkl'))
            self.feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))
            
            print("✓ Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            raise
    
    def preprocess_input(self, data):
        """
        Preprocess input data to match training format
        
        Args:
            data (dict): Input job posting data
            
        Returns:
            np.array: Preprocessed feature array
        """
        # Fill missing values
        defaults = {
            'title': '',
            'location': '',
            'department': '',
            'company_profile': '',
            'description': '',
            'requirements': '',
            'benefits': '',
            'employment_type': '',
            'required_experience': '',
            'required_education': '',
            'industry': '',
            'function': '',
            'salary_range': '',
            'telecommuting': 0,
            'has_company_logo': 0,
            'has_questions': 0
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        # Create combined text
        combined_text = (
            str(data['title']) + ' ' +
            str(data['company_profile']) + ' ' +
            str(data['description']) + ' ' +
            str(data['requirements']) + ' ' +
            str(data['benefits'])
        )
        
        # Text length features
        title_length = len(str(data['title']))
        description_length = len(str(data['description']))
        requirements_length = len(str(data['requirements']))
        has_salary = 1 if data['salary_range'] else 0
        
        # Binary features
        telecommuting = int(data['telecommuting'])
        has_company_logo = int(data['has_company_logo'])
        has_questions = int(data['has_questions'])
        
        # Encode categorical variables
        categorical_features = ['employment_type', 'required_experience', 'required_education',
                               'industry', 'function', 'location']
        
        encoded_features = []
        for col in categorical_features:
            value = str(data.get(col, ''))
            if col in self.label_encoders:
                le = self.label_encoders[col]
                try:
                    encoded_value = le.transform([value])[0]
                except:
                    # If value not seen during training, use 0
                    encoded_value = 0
                encoded_features.append(encoded_value)
        
        # TF-IDF features
        tfidf_features = self.tfidf.transform([combined_text]).toarray()[0]
        
        # Combine all features
        structured_features = [
            telecommuting, has_company_logo, has_questions,
            title_length, description_length, requirements_length, has_salary
        ] + encoded_features
        
        all_features = np.concatenate([structured_features, tfidf_features])
        
        return all_features.reshape(1, -1)
    
    def predict(self, data):
        """
        Make prediction on input data
        
        Args:
            data (dict): Input job posting data
            
        Returns:
            dict: Prediction results
        """
        try:
            # Preprocess input
            features = self.preprocess_input(data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0]
            
            # Determine risk level
            fraud_prob = probability[1] * 100
            
            if fraud_prob >= 70:
                risk_level = "High Risk"
            elif fraud_prob >= 40:
                risk_level = "Medium Risk"
            else:
                risk_level = "Low Risk"
            
            result = {
                'prediction': 'Fraudulent' if prediction == 1 else 'Legitimate',
                'fraud_probability': round(fraud_prob, 2),
                'legitimate_probability': round(probability[0] * 100, 2),
                'risk_level': risk_level,
                'is_fraudulent': bool(prediction == 1)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")


# Create a global predictor instance
predictor = JobFraudPredictor()