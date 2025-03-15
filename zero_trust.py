import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st

def generate_user_data(normal_count=100, suspicious_count=10, 
                      normal_typing_speed_mean=5.0, normal_mouse_speed_mean=300.0,
                      suspicious_typing_speed_mean=2.0, suspicious_mouse_speed_mean=600.0):
    """
    Generate simulated user behavior data for normal and suspicious users.
    
    Parameters:
    -----------
    normal_count: int
        Number of normal users to simulate
    suspicious_count: int
        Number of suspicious users to simulate
    normal_typing_speed_mean: float
        Mean typing speed for normal users (keystrokes/sec)
    normal_mouse_speed_mean: float
        Mean mouse movement speed for normal users (pixels/sec)
    suspicious_typing_speed_mean: float
        Mean typing speed for suspicious users (keystrokes/sec)
    suspicious_mouse_speed_mean: float
        Mean mouse movement speed for suspicious users (pixels/sec)
    
    Returns:
    --------
    normal_users_df: pandas DataFrame
        DataFrame containing normal user behavior data
    suspicious_users_df: pandas DataFrame
        DataFrame containing suspicious user behavior data
    """
    try:
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate normal user data
        normal_typing_speeds = np.random.normal(normal_typing_speed_mean, 1.0, normal_count)
        normal_mouse_speeds = np.random.normal(normal_mouse_speed_mean, 50.0, normal_count)
        
        # Ensure all values are positive
        normal_typing_speeds = np.maximum(normal_typing_speeds, 0.5)
        normal_mouse_speeds = np.maximum(normal_mouse_speeds, 50.0)
        
        normal_users_df = pd.DataFrame({
            'user_id': [f'normal_user_{i}' for i in range(normal_count)],
            'typing_speed': normal_typing_speeds,
            'mouse_movement_speed': normal_mouse_speeds,
            'is_suspicious': False
        })
        
        # Generate suspicious user data
        suspicious_typing_speeds = np.random.normal(suspicious_typing_speed_mean, 0.5, suspicious_count)
        suspicious_mouse_speeds = np.random.normal(suspicious_mouse_speed_mean, 100.0, suspicious_count)
        
        # Ensure all values are positive
        suspicious_typing_speeds = np.maximum(suspicious_typing_speeds, 0.1)
        suspicious_mouse_speeds = np.maximum(suspicious_mouse_speeds, 100.0)
        
        suspicious_users_df = pd.DataFrame({
            'user_id': [f'suspicious_user_{i}' for i in range(suspicious_count)],
            'typing_speed': suspicious_typing_speeds,
            'mouse_movement_speed': suspicious_mouse_speeds,
            'is_suspicious': True
        })
        
        return normal_users_df, suspicious_users_df
        
    except Exception as e:
        st.error(f"Error generating user data: {str(e)}")
        # Return empty DataFrames if there's an error
        return pd.DataFrame(), pd.DataFrame()

def check_user_behavior(user_data, model):
    """
    Check if a user's behavior is anomalous using the Isolation Forest model.
    
    Parameters:
    -----------
    user_data: pandas Series or DataFrame
        Data containing user behavior metrics (typing_speed, mouse_movement_speed)
    model: sklearn.ensemble.IsolationForest
        Trained Isolation Forest model for anomaly detection
    
    Returns:
    --------
    is_anomaly: bool
        True if user behavior is anomalous, False otherwise
    confidence: float
        Confidence score (0-100) of the prediction
    predicted_label: str
        Predicted label ("Normal" or "Suspicious")
    """
    try:
        # Extract features
        if isinstance(user_data, pd.DataFrame):
            features = user_data[['typing_speed', 'mouse_movement_speed']]
        else:  # Assuming it's a Series
            features = pd.DataFrame({
                'typing_speed': [user_data['typing_speed']],
                'mouse_movement_speed': [user_data['mouse_movement_speed']]
            })
            
        # Get anomaly score (-1 for anomalies, 1 for normal)
        score = model.decision_function(features)
        
        # Convert to a more intuitive scale (higher = more normal)
        normalized_score = (score + 1) / 2  # Convert from [-1, 1] to [0, 1]
        
        # Determine if anomalous
        prediction = model.predict(features)
        is_anomaly = prediction[0] == -1  # -1 means anomaly in Isolation Forest
        
        # Calculate confidence (0-100%)
        if is_anomaly:
            confidence = (1 - normalized_score[0]) * 100  # Confidence in anomaly prediction
        else:
            confidence = normalized_score[0] * 100  # Confidence in normal prediction
            
        # Get label
        predicted_label = "Suspicious" if is_anomaly else "Normal"
        
        return is_anomaly, confidence, predicted_label
        
    except Exception as e:
        st.error(f"Error analyzing user behavior: {str(e)}")
        # Return default values if there's an error
        return True, 0.0, "Error"
