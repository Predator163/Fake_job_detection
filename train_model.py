"""
Job Fraud Detection - Model Training Script
This script loads the dataset, preprocesses it, trains a model, and saves it for deployment.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("JOB FRAUD DETECTION - MODEL TRAINING")
print("=" * 70)

# Step 1: Load the dataset
print("\n[1/6] Loading dataset...")
# Update this path to your Excel file location
df = pd.read_csv('fake_job_postings.csv')  # or .xlsx if Excel file

print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
print(f"Target distribution:\n{df['fraudulent'].value_counts()}")

# Step 2: Data Preprocessing
print("\n[2/6] Preprocessing data...")

# Fill missing values
text_columns = ['title', 'location', 'department', 'company_profile', 
                'description', 'requirements', 'benefits', 'employment_type',
                'required_experience', 'required_education', 'industry', 'function']

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna('')

# Binary columns
binary_columns = ['telecommuting', 'has_company_logo', 'has_questions']
for col in binary_columns:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Step 3: Feature Engineering
print("\n[3/6] Engineering features...")

# Combine text features
df['combined_text'] = (
    df['title'] + ' ' + 
    df['company_profile'] + ' ' + 
    df['description'] + ' ' + 
    df['requirements'] + ' ' + 
    df['benefits']
)

# Text length features
df['title_length'] = df['title'].apply(len)
df['description_length'] = df['description'].apply(len)
df['requirements_length'] = df['requirements'].apply(len)

# Salary range indicator
df['has_salary'] = df['salary_range'].notna().astype(int) if 'salary_range' in df.columns else 0

# Label encoding for categorical variables
categorical_features = ['employment_type', 'required_experience', 'required_education', 
                        'industry', 'function', 'location']

label_encoders = {}
for col in categorical_features:
    if col in df.columns:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# TF-IDF for text
print("   Creating TF-IDF features...")
tfidf = TfidfVectorizer(max_features=500, min_df=2, max_df=0.8, ngram_range=(1, 2))
tfidf_features = tfidf.fit_transform(df['combined_text'])
tfidf_df = pd.DataFrame(tfidf_features.toarray(), 
                        columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])])

# Step 4: Prepare features and target
print("\n[4/6] Preparing features and target...")

# Numerical and encoded features
feature_columns = (
    binary_columns + 
    ['title_length', 'description_length', 'requirements_length', 'has_salary'] +
    [col + '_encoded' for col in categorical_features if col in df.columns]
)

X_structured = df[feature_columns].values
X_text = tfidf_df.values
X = np.hstack([X_structured, X_text])
y = df['fraudulent'].values

print(f"Feature matrix shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Fraudulent jobs: {sum(y)} ({sum(y)/len(y)*100:.2f}%)")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Step 5: Train Model
print("\n[5/6] Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Model training complete!")

# Step 6: Evaluate Model
print("\n[6/6] Evaluating model...")

y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraudulent']))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save all models and encoders
print("\n[7/7] Saving model and preprocessors...")

os.makedirs('saved_models', exist_ok=True)

joblib.dump(model, 'saved_models/fraud_detection_model.pkl')
joblib.dump(tfidf, 'saved_models/tfidf_vectorizer.pkl')
joblib.dump(label_encoders, 'saved_models/label_encoders.pkl')
joblib.dump(feature_columns, 'saved_models/feature_columns.pkl')

print("\n✓ Model saved successfully!")
print("Files created:")
print("  - saved_models/fraud_detection_model.pkl")
print("  - saved_models/tfidf_vectorizer.pkl")
print("  - saved_models/label_encoders.pkl")
print("  - saved_models/feature_columns.pkl")

print("\n" + "=" * 70)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 70)