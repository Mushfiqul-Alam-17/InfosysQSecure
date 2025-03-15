import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

class BiometricCollector:
    """Class for collecting real biometric data (typing speed) from user interactions"""
    
    def __init__(self):
        """Initialize the biometric collector with session state variables"""
        # Initialize session state variables if they don't exist
        if 'keypress_times' not in st.session_state:
            st.session_state.keypress_times = []
        if 'typing_speeds' not in st.session_state:
            st.session_state.typing_speeds = []
        if 'last_typing_speed' not in st.session_state:
            st.session_state.last_typing_speed = 0.0
        if 'mouse_positions' not in st.session_state:
            st.session_state.mouse_positions = []
        if 'mouse_speeds' not in st.session_state:
            st.session_state.mouse_speeds = []
        if 'last_mouse_speed' not in st.session_state:
            st.session_state.last_mouse_speed = 0.0
        if 'last_mouse_record_time' not in st.session_state:
            st.session_state.last_mouse_record_time = time.time()
    
    def track_keystroke(self):
        """Record a keystroke event and calculate typing speed"""
        current_time = time.time()
        st.session_state.keypress_times.append(current_time)
        
        # Keep only the last 10 seconds of keystrokes
        cutoff_time = current_time - 10
        st.session_state.keypress_times = [t for t in st.session_state.keypress_times if t > cutoff_time]
        
        # Calculate typing speed (keystrokes per second) over the last time window
        if len(st.session_state.keypress_times) > 1:
            time_window = current_time - st.session_state.keypress_times[0]
            if time_window > 0:
                typing_speed = (len(st.session_state.keypress_times) - 1) / time_window
                st.session_state.last_typing_speed = typing_speed
                st.session_state.typing_speeds.append(typing_speed)
                
                # Keep only the last 20 speed measurements
                if len(st.session_state.typing_speeds) > 20:
                    st.session_state.typing_speeds.pop(0)
    
    def capture_typing_data(self):
        """Capture typing data using a Streamlit text area with JavaScript callback"""
        st.markdown("""
        <style>
        .typing-area {
            border: 2px solid #0068C9;
            border-radius: 10px;
            padding: 15px;
            background-color: #f0f8ff;
            font-size: 16px;
            height: 120px;
            transition: all 0.3s;
        }
        .typing-area:focus {
            border-color: #00C853;
            box-shadow: 0 0 10px rgba(0, 200, 83, 0.3);
        }
        /* Enterprise styling enhancements */
        .enterprise-section {
            border-left: 4px solid #0068C9;
            padding-left: 15px;
            margin: 15px 0;
        }
        .security-status {
            font-weight: bold;
            padding: 8px 15px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 10px;
        }
        .security-status.normal {
            background-color: #e8f5e9;
            color: #2e7d32;
            border: 1px solid #2e7d32;
        }
        .security-status.warning {
            background-color: #fff8e1;
            color: #f57c00;
            border: 1px solid #f57c00;
        }
        .security-status.alert {
            background-color: #ffebee;
            color: #c62828;
            border: 1px solid #c62828;
        }
        /* Button styling */
        .analyze-button {
            background-color: #0068C9;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 15px;
            width: 100%;
        }
        .analyze-button:hover {
            background-color: #004c94;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create a text area for typing with custom styling
        st.markdown("### Type here to measure your typing speed")
        st.markdown("Type naturally as you would in a regular document, then press **Analyze Now** to evaluate your biometric security profile.")
        
        # Custom text area with keystroke tracking
        text_input = st.text_area(
            "Your typing will be analyzed for security verification:",
            height=150,
            key="typing_input",
            help="Type normally to generate biometric security data",
            on_change=self.track_keystroke
        )
        
        # Add a manual analysis button (this will be used in app.py)
        analyze_button = st.button("🔒 Analyze Security Biometrics", type="primary", key="analyze_typing")
        
        # Display current typing speed if we have data AND the button was pressed
        if st.session_state.typing_speeds:
            avg_speed = sum(st.session_state.typing_speeds) / len(st.session_state.typing_speeds)
            
            # Add an indicator for the security status
            security_status = "normal"
            security_message = "Normal Human Pattern"
            
            if avg_speed > 8.0:
                security_status = "alert"
                security_message = "Suspicious: Abnormally Fast Typing"
            elif avg_speed < 2.0:
                security_status = "warning"
                security_message = "Caution: Unusually Slow Typing"
            
            st.markdown(f"""
            <div class="enterprise-section">
                <h3>RAIN™ Biometric Security Analysis</h3>
                <div class="security-status {security_status}">
                    {security_message}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Current Typing Speed", 
                    f"{st.session_state.last_typing_speed:.2f} keystrokes/sec",
                    delta=f"{st.session_state.last_typing_speed - avg_speed:.2f}" if len(st.session_state.typing_speeds) > 1 else None
                )
            with col2:
                st.metric(
                    "Average Typing Speed", 
                    f"{avg_speed:.2f} keystrokes/sec"
                )
                
            # Create a nice visualization of typing speed over time
            if len(st.session_state.typing_speeds) > 1:
                fig, ax = plt.subplots(figsize=(10, 3))
                ax.plot(st.session_state.typing_speeds, color='#0068C9', linewidth=2)
                ax.set_ylabel('Keystrokes/sec')
                ax.set_xlabel('Time (most recent measurements)')
                ax.set_title('RAIN™ Biometric Typing Pattern Analysis')
                ax.grid(True, alpha=0.3)
                
                # Add horizontal line for average
                ax.axhline(y=avg_speed, color='#FF5252', linestyle='--', alpha=0.7, label=f'Average: {avg_speed:.2f}')
                
                # Add shaded areas for normal vs. suspicious zones
                ax.axhspan(avg_speed * 0.7, avg_speed * 1.3, alpha=0.2, color='green', label='Normal Range')
                if avg_speed * 1.3 < 10:  # Don't shade too high
                    ax.axhspan(avg_speed * 1.3, 10, alpha=0.2, color='red', label='Suspicious (Too Fast)')
                ax.axhspan(0, avg_speed * 0.7, alpha=0.2, color='orange', label='Suspicious (Too Slow)')
                
                ax.legend()
                st.pyplot(fig)
                
                # Add enterprise-level explanation
                st.markdown("""
                ### RAIN™ AI-Driven Biometric Analysis
                
                This system is analyzing your typing patterns using:
                
                1. **Temporal Keystroke Dynamics**: Timing between keypresses creates a unique behavioral fingerprint
                2. **Pattern Consistency Analysis**: AI models detect deviations from your established baseline
                3. **Anomaly Detection Algorithms**: Isolation Forest and One-Class SVM machine learning algorithms
                4. **Gemini-Powered Threat Intelligence**: Advanced AI interprets behavioral patterns
                
                The RAIN™ system provides continuous security verification without requiring passwords or tokens.
                """)
        else:
            st.info("Start typing and press 'Analyze Security Biometrics' to generate your security profile...")
        
        return text_input, analyze_button
    
    def simulate_mouse_data(self, normal_count=100, suspicious_count=10):
        """
        Simulate mouse movement data for comparison with real typing data.
        This will generate realistic mouse movement patterns based on common human behavior.
        
        Parameters:
        -----------
        normal_count: int
            Number of normal users to simulate
        suspicious_count: int
            Number of suspicious users to simulate
        
        Returns:
        --------
        normal_users_df: pandas DataFrame
            DataFrame containing normal user behavior data
        suspicious_users_df: pandas DataFrame
            DataFrame containing suspicious user behavior data
        """
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate normal user data with realistic distributions
        normal_typing_speeds = np.random.normal(4.5, 0.8, normal_count)
        normal_mouse_speeds = np.random.normal(320.0, 50.0, normal_count)
        
        # Different patterns for suspicious users
        suspicious_types = np.random.choice(['bot_fast', 'bot_slow', 'erratic'], suspicious_count)
        suspicious_typing_speeds = []
        suspicious_mouse_speeds = []
        
        for suspicious_type in suspicious_types:
            if suspicious_type == 'bot_fast':
                # Bots type unnaturally fast and move mouse quickly
                suspicious_typing_speeds.append(np.random.uniform(7.0, 12.0))
                suspicious_mouse_speeds.append(np.random.uniform(500.0, 700.0))
            elif suspicious_type == 'bot_slow':
                # Bots that move very methodically (too consistent)
                suspicious_typing_speeds.append(np.random.uniform(1.0, 2.0))
                suspicious_mouse_speeds.append(np.random.uniform(100.0, 150.0))
            else:  # erratic
                # Erratic behavior - unusual combinations
                suspicious_typing_speeds.append(np.random.uniform(0.5, 1.5))
                suspicious_mouse_speeds.append(np.random.uniform(600.0, 800.0))
        
        # Create DataFrames
        normal_users_df = pd.DataFrame({
            'user_id': [f'normal_user_{i}' for i in range(normal_count)],
            'typing_speed': normal_typing_speeds,
            'mouse_movement_speed': normal_mouse_speeds,
            'is_suspicious': False
        })
        
        suspicious_users_df = pd.DataFrame({
            'user_id': [f'suspicious_user_{i}' for i in range(suspicious_count)],
            'typing_speed': suspicious_typing_speeds,
            'mouse_movement_speed': suspicious_mouse_speeds,
            'is_suspicious': True
        })
        
        return normal_users_df, suspicious_users_df
    
    def compare_algorithms(self, user_typing_speed, normal_users_df, suspicious_users_df):
        """
        Compare Isolation Forest and One-Class SVM on the user's typing speed
        and simulated mouse data.
        
        Parameters:
        -----------
        user_typing_speed: float
            The user's current typing speed
        normal_users_df: pandas DataFrame
            DataFrame containing normal user behavior data
        suspicious_users_df: pandas DataFrame
            DataFrame containing suspicious user behavior data
            
        Returns:
        --------
        results_dict: dict
            Dictionary containing anomaly detection results from both algorithms
        """
        # Simulate a reasonable mouse speed for the user based on their typing speed
        # This creates a more realistic correlation between typing and mouse behavior
        user_mouse_speed = user_typing_speed * 70 + np.random.normal(0, 20)
        if user_mouse_speed < 50:
            user_mouse_speed = 50
        
        # Combine normal and suspicious data
        training_df = pd.concat([normal_users_df, suspicious_users_df])
        X_train = training_df[['typing_speed', 'mouse_movement_speed']]
        
        # Create user data point
        user_data = pd.DataFrame({
            'typing_speed': [user_typing_speed],
            'mouse_movement_speed': [user_mouse_speed]
        })
        
        # Train Isolation Forest model
        isolation_forest = IsolationForest(
            contamination=0.1,  # Expect about 10% anomalies
            random_state=42,
            n_estimators=100,  # More trees for better accuracy
            max_samples='auto'
        )
        isolation_forest.fit(X_train)
        
        # Get Isolation Forest prediction
        if_score = isolation_forest.decision_function(user_data)[0]
        if_normalized_score = (if_score + 0.5) / 1.5  # Convert to 0-1 scale
        if_prediction = isolation_forest.predict(user_data)[0]
        if_is_anomaly = if_prediction == -1
        if_confidence = max(0, min(100, if_normalized_score * 100 if not if_is_anomaly else (1 - if_normalized_score) * 100))
        
        # Train One-Class SVM model
        one_class_svm = OneClassSVM(
            nu=0.1,  # Similar to contamination
            kernel='rbf',
            gamma='scale'
        )
        # Train only on normal data for One-Class SVM (more common approach)
        one_class_svm.fit(normal_users_df[['typing_speed', 'mouse_movement_speed']])
        
        # Get One-Class SVM prediction
        svm_prediction = one_class_svm.predict(user_data)[0]
        svm_score = one_class_svm.decision_function(user_data)[0]
        svm_normalized_score = 1 / (1 + np.exp(-svm_score))  # Sigmoid to get 0-1 scale
        svm_is_anomaly = svm_prediction == -1
        svm_confidence = max(0, min(100, svm_normalized_score * 100 if not svm_is_anomaly else (1 - svm_normalized_score) * 100))
        
        # Create visualization comparing the two algorithms
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot normal users
        ax.scatter(
            normal_users_df['typing_speed'],
            normal_users_df['mouse_movement_speed'],
            color='blue', alpha=0.6, s=50, label='Normal Users'
        )
        
        # Plot suspicious users
        ax.scatter(
            suspicious_users_df['typing_speed'],
            suspicious_users_df['mouse_movement_speed'],
            color='red', alpha=0.6, s=50, label='Suspicious Users'
        )
        
        # Plot user with appropriate color
        if if_is_anomaly and svm_is_anomaly:
            # Both algorithms flag as anomaly - strong red
            user_color = '#ff0000'
            marker = 'X'
            verdict = "SUSPICIOUS (Both Algorithms)"
        elif if_is_anomaly or svm_is_anomaly:
            # One algorithm flags - orange
            user_color = '#ff9800'
            marker = '*'
            verdict = "SUSPICIOUS (Single Algorithm)"
        else:
            # No flags - green
            user_color = '#4caf50'
            marker = 'o'
            verdict = "NORMAL"
        
        # Plot user data point with bigger marker
        ax.scatter(
            user_typing_speed, user_mouse_speed,
            color=user_color, s=200, marker=marker, 
            edgecolors='black', linewidths=2,
            label=f'Your Behavior ({verdict})'
        )
        
        # Add decision boundaries using contours (simplification for visualization)
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, 100),
            np.linspace(y_min, y_max, 100)
        )
        grid = np.c_[xx.ravel(), yy.ravel()]
        
        # Isolation Forest boundary
        Z_if = isolation_forest.decision_function(grid)
        Z_if = Z_if.reshape(xx.shape)
        contour_if = ax.contour(xx, yy, Z_if, levels=[0], colors=['green'], linestyles=['-'], alpha=0.7)
        plt.clabel(contour_if, inline=True, fontsize=8, fmt='Isolation Forest')
        
        # One-Class SVM boundary
        Z_svm = one_class_svm.decision_function(grid)
        Z_svm = Z_svm.reshape(xx.shape)
        contour_svm = ax.contour(xx, yy, Z_svm, levels=[0], colors=['purple'], linestyles=['--'], alpha=0.7)
        plt.clabel(contour_svm, inline=True, fontsize=8, fmt='One-Class SVM')
        
        # Add labels and title
        ax.set_xlabel('Typing Speed (keystrokes/sec)')
        ax.set_ylabel('Mouse Movement Speed (pixels/sec)')
        ax.set_title('Anomaly Detection: Isolation Forest vs. One-Class SVM')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Return results
        results_dict = {
            'isolation_forest': {
                'is_anomaly': if_is_anomaly,
                'confidence': if_confidence,
                'verdict': 'Suspicious' if if_is_anomaly else 'Normal'
            },
            'one_class_svm': {
                'is_anomaly': svm_is_anomaly,
                'confidence': svm_confidence,
                'verdict': 'Suspicious' if svm_is_anomaly else 'Normal'
            },
            'user_data': {
                'typing_speed': user_typing_speed,
                'mouse_speed': user_mouse_speed
            },
            'plot': fig,
            'overall_verdict': verdict
        }
        
        return results_dict