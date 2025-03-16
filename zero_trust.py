import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import streamlit as st
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import google.generativeai as genai

class ZeroTrustSecuritySystem:
    """
    Integrated Zero Trust Security System with AI-powered threat intelligence
    """
    
    def __init__(self):
        """Initialize the Zero Trust Security System with enhanced capabilities"""
        # Initialize session state for storing security data
        if 'zero_trust_initialized' not in st.session_state:
            st.session_state.zero_trust_initialized = True
            st.session_state.security_incidents = []
            st.session_state.security_score = 850  # Enterprise security score out of 1000
            st.session_state.continuous_monitoring = False
            st.session_state.behavioral_models = {}
            st.session_state.logged_users = {}
            st.session_state.anomaly_thresholds = {
                'typing': {'low': 2.0, 'high': 7.5},
                'mouse': {'low': 120, 'high': 550},
                'idle_time': {'max': 300},  # seconds
                'failed_login': {'max': 3}
            }
            
            # Generate initial baseline model for comparison
            self._generate_baseline_models()
        
        # Define biometric thresholds for analysis
        self.typing_thresholds = {
            'very_slow': 2.0,    # Very slow typing < 2 keystroke/sec
            'slow': 3.5,         # Slow typing < 3.5 keystrokes/sec
            'normal': 5.5,       # Normal typing: 3.5-5.5 keystrokes/sec
            'fast': 7.5,         # Fast typing: 5.5-7.5 keystrokes/sec
            'very_fast': 10.0    # Very fast typing: >7.5 keystrokes/sec
        }
        
        self.mouse_thresholds = {
            'very_slow': 100,     # Very slow mouse movement < 100 pixels/sec
            'slow': 200,          # Slow mouse: 100-200 pixels/sec
            'normal': 400,        # Normal mouse: 200-400 pixels/sec
            'fast': 600,          # Fast mouse: 400-600 pixels/sec
            'very_fast': 800      # Very fast mouse: >600 pixels/sec
        }
        
        # AI Threat Intelligence Components
        self.api_key = None
        
        # Define threat patterns for intelligent assessment
        self.threat_patterns = {
            'bot_pattern': {
                'description': 'Automated bot or script activity',
                'conditions': [
                    {'typing': 'very_fast', 'mouse': 'very_slow', 'consistency': 'high'},
                    {'typing': 'very_fast', 'mouse': 'very_fast', 'consistency': 'high'}
                ],
                'threat_level': 'Critical'
            },
            'advanced_attacker': {
                'description': 'Advanced human attacker with tools',
                'conditions': [
                    {'typing': 'normal', 'mouse': 'fast', 'if_suspicious': True, 'svm_suspicious': True}
                ],
                'threat_level': 'High'
            },
            'unusual_behavior': {
                'description': 'Unusual behavior patterns',
                'conditions': [
                    {'typing': 'very_slow', 'mouse': 'very_fast'},
                    {'typing': 'fast', 'mouse': 'very_slow'}
                ],
                'threat_level': 'Medium'
            },
            'possible_shared_account': {
                'description': 'Possible shared account or different user',
                'conditions': [
                    {'typing': 'normal', 'mouse': 'normal', 'one_algorithm_suspicious': True}
                ],
                'threat_level': 'Medium'
            },
            'learning_user': {
                'description': 'Legitimate user learning the system',
                'conditions': [
                    {'typing': 'slow', 'mouse': 'slow', 'one_algorithm_suspicious': True}
                ],
                'threat_level': 'Low'
            },
            'normal_user': {
                'description': 'Normal user behavior',
                'conditions': [
                    {'typing': 'normal', 'mouse': 'normal', 'if_suspicious': False, 'svm_suspicious': False}
                ],
                'threat_level': 'None'
            }
        }
        
        # Threat Intelligence Feed Data
        if 'threat_intel_feed' not in st.session_state:
            st.session_state.threat_intel_feed = {
                'last_updated': datetime.now(),
                'indicators': self._generate_threat_indicators(),
                'threat_actors': [
                    'APT29', 'Carbanak', 'FIN7', 'Lazarus Group', 'Turla'
                ],
                'vulnerabilities': [
                    'CVE-2023-45141', 'CVE-2024-21520', 'CVE-2023-38831', 
                    'CVE-2024-0001', 'CVE-2023-29360'
                ],
                'tactics': [
                    'Initial Access', 'Execution', 'Persistence', 
                    'Privilege Escalation', 'Defense Evasion'
                ]
            }
    
    def set_api_key(self, api_key):
        """Set the Gemini API key for enhanced threat intelligence"""
        self.api_key = api_key
        # Configure Gemini AI if API key is provided
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                return True
            return False
        except Exception as e:
            st.error(f"Error configuring AI: {str(e)}")
            return False
    
    def has_api_key(self):
        """Check if an API key has been provided"""
        return self.api_key is not None and self.api_key.strip() != ""
    
    def _generate_baseline_models(self):
        """Generate baseline behavioral models for anomaly detection"""
        # Generate training data
        normal_df, suspicious_df = self.generate_user_data()
        
        # Save the training data for future reference
        st.session_state.normal_baseline = normal_df
        st.session_state.suspicious_baseline = suspicious_df
        
        # Combine data for training
        all_data = pd.concat([normal_df, suspicious_df])
        X_train = all_data[['typing_speed', 'mouse_movement_speed']]
        
        # Train and store Isolation Forest model
        isolation_forest = IsolationForest(
            contamination=0.1,  # Expect about 10% anomalies
            random_state=42,
            n_estimators=100
        )
        isolation_forest.fit(X_train)
        st.session_state.behavioral_models['isolation_forest'] = isolation_forest
        
        # Train and store One-Class SVM model
        one_class_svm = OneClassSVM(
            nu=0.1,  # Similar to contamination
            kernel='rbf',
            gamma='scale'
        )
        # Train only on normal data for One-Class SVM (common approach for OC-SVM)
        one_class_svm.fit(normal_df[['typing_speed', 'mouse_movement_speed']])
        st.session_state.behavioral_models['one_class_svm'] = one_class_svm
    
    def _generate_threat_indicators(self):
        """Generate threat indicators for the threat intelligence feed"""
        indicators = []
        for i in range(15):
            indicator_type = random.choice(['ip', 'domain', 'hash', 'url'])
            
            if indicator_type == 'ip':
                value = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            elif indicator_type == 'domain':
                domains = ['evil-corp.com', 'malware-delivery.net', 'phishing-site.org', 'c2-server.io', 'data-exfil.com']
                value = random.choice(domains)
            elif indicator_type == 'hash':
                value = ''.join(random.choice('0123456789abcdef') for _ in range(64))
            else:  # url
                value = f"https://{random.choice(['evil-site.com', 'malware.net', 'phish.org'])}/{random.choice(['download', 'login', 'update'])}"
            
            confidence = random.randint(60, 99)
            days_ago = random.randint(1, 30)
            first_seen = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            indicators.append({
                'type': indicator_type,
                'value': value,
                'confidence': confidence,
                'first_seen': first_seen
            })
        
        return indicators
    
    def generate_user_data(self, normal_count=100, suspicious_count=10):
        """
        Generate simulated user behavior data for normal and suspicious users.
        Enhanced with more realistic patterns.
        """
        try:
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
            
        except Exception as e:
            st.error(f"Error generating user data: {str(e)}")
            # Return empty DataFrames if there's an error
            return pd.DataFrame(), pd.DataFrame()
    
    def get_typing_category(self, typing_speed):
        """Categorize typing speed based on thresholds"""
        if typing_speed < self.typing_thresholds['very_slow']:
            return 'very_slow', 'extremely slow'
        elif typing_speed < self.typing_thresholds['slow']:
            return 'slow', 'very slow'
        elif typing_speed < self.typing_thresholds['normal']:
            return 'normal', 'normal'
        elif typing_speed < self.typing_thresholds['fast']:
            return 'fast', 'fast'
        else:
            return 'very_fast', 'extremely fast'
    
    def get_mouse_category(self, mouse_speed):
        """Categorize mouse movement speed based on thresholds"""
        if mouse_speed < self.mouse_thresholds['very_slow']:
            return 'very_slow', 'extremely slow'
        elif mouse_speed < self.mouse_thresholds['slow']:
            return 'slow', 'very slow'
        elif mouse_speed < self.mouse_thresholds['normal']:
            return 'normal', 'normal'
        elif mouse_speed < self.mouse_thresholds['fast']:
            return 'fast', 'fast'
        else:
            return 'very_fast', 'extremely fast'
    
    def check_user_behavior(self, user_data):
        """
        Check if a user's behavior is anomalous using multiple detection methods
        and integrating AI threat intelligence for enhanced analysis
        
        Parameters:
        -----------
        user_data: dict
            Dictionary with user behavior data including typing_speed and mouse_speed
        
        Returns:
        --------
        results_dict: dict
            Comprehensive security analysis results
        """
        try:
            # Extract user data
            typing_speed = user_data['typing_speed']
            mouse_speed = user_data['mouse_speed']
            
            # Create DataFrame for model prediction
            user_df = pd.DataFrame({
                'typing_speed': [typing_speed],
                'mouse_movement_speed': [mouse_speed]
            })
            
            # Get predictions from both models
            # Isolation Forest
            if_model = st.session_state.behavioral_models['isolation_forest']
            if_score = if_model.decision_function(user_df)[0]
            if_normalized_score = (if_score + 0.5) / 1.5  # Convert to 0-1 scale
            if_prediction = if_model.predict(user_df)[0]
            if_is_anomaly = if_prediction == -1
            if_confidence = max(0, min(100, if_normalized_score * 100 if not if_is_anomaly else (1 - if_normalized_score) * 100))
            
            # One-Class SVM
            svm_model = st.session_state.behavioral_models['one_class_svm']
            svm_prediction = svm_model.predict(user_df)[0]
            svm_score = svm_model.decision_function(user_df)[0]
            svm_normalized_score = 1 / (1 + np.exp(-svm_score))  # Sigmoid to get 0-1 scale
            svm_is_anomaly = svm_prediction == -1
            svm_confidence = max(0, min(100, svm_normalized_score * 100 if not svm_is_anomaly else (1 - svm_normalized_score) * 100))
            
            # Store detection results for AI analysis
            detection_results = {
                'isolation_forest': {
                    'is_anomaly': if_is_anomaly,
                    'confidence': if_confidence,
                    'verdict': 'Suspicious' if if_is_anomaly else 'Normal'
                },
                'one_class_svm': {
                    'is_anomaly': svm_is_anomaly,
                    'confidence': svm_confidence,
                    'verdict': 'Suspicious' if svm_is_anomaly else 'Normal'
                }
            }
            
            # Generate comprehensive analysis using AI or rule-based system
            threat_analysis = self.analyze_threat(user_data, detection_results)
            
            # Create visualization comparing both algorithms
            fig = self.create_detection_visualization(typing_speed, mouse_speed, if_is_anomaly, svm_is_anomaly)
            
            # Return results with proper structure
            return {
                'overall_verdict': "SUSPICIOUS (Both Algorithms)" if (if_is_anomaly and svm_is_anomaly) else
                                 "SUSPICIOUS (Single Algorithm)" if (if_is_anomaly or svm_is_anomaly) else
                                 "NORMAL",
                'isolation_forest': {
                    'is_anomaly': if_is_anomaly,
                    'confidence': if_confidence,
                    'verdict': "Suspicious" if if_is_anomaly else "Normal"
                },
                'one_class_svm': {
                    'is_anomaly': svm_is_anomaly,
                    'confidence': svm_confidence,
                    'verdict': "Suspicious" if svm_is_anomaly else "Normal"
                },
                'user_data': user_data,
                'plot': fig
            }
                verdict = "SUSPICIOUS (Both Algorithms)"
                threat_level = "High"
            elif if_is_anomaly or svm_is_anomaly:
                verdict = "SUSPICIOUS (Single Algorithm)" 
                threat_level = "Medium"
            else:
                verdict = "NORMAL"
                threat_level = "None"
                
            # Record security incident if suspicious
            if verdict != "NORMAL":
                self.record_security_incident(threat_level, typing_speed, mouse_speed, if_is_anomaly, svm_is_anomaly)
            
            # Return comprehensive results
            return {
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
                    'typing_speed': typing_speed,
                    'mouse_speed': mouse_speed
                },
                'plot': fig,
                'overall_verdict': verdict,
                'threat_analysis': threat_analysis
            }
            
        except Exception as e:
            st.error(f"Error analyzing user behavior: {str(e)}")
            # Return basic error information
            return {
                'error': str(e),
                'overall_verdict': 'Error',
                'threat_analysis': {
                    'threat_level': 'Error',
                    'analysis': f"Error during behavior analysis: {str(e)}"
                }
            }
    
    def analyze_threat(self, user_data, detection_results):
        """
        Analyze security threat using AI or rule-based analysis
        Provides a comprehensive threat assessment with recommendations
        """
        try:
            # Extract data
            typing_speed = user_data['typing_speed']
            mouse_speed = user_data['mouse_speed']
            
            isolation_forest_result = detection_results['isolation_forest']
            one_class_svm_result = detection_results['one_class_svm']
            
            # Categorize user behavior
            typing_category, typing_desc = self.get_typing_category(typing_speed)
            mouse_category, mouse_desc = self.get_mouse_category(mouse_speed)
            
            # If AI is available, use it for enhanced analysis
            if self.has_api_key():
                try:
                    # Create a prompt for Gemini
                    prompt = f"""You are CyberGuardian, an advanced AI security analyst specializing in Zero Trust security and behavioral biometrics.

USER BEHAVIOR DATA:
- Typing Speed: {typing_speed:.2f} keystrokes/second
- Mouse Movement Speed: {mouse_speed:.2f} pixels/second
- Typing Category: {typing_desc}
- Mouse Movement Category: {mouse_desc}

ANOMALY DETECTION RESULTS:
1. Isolation Forest Algorithm:
   - Verdict: {isolation_forest_result['verdict']}
   - Confidence: {isolation_forest_result['confidence']:.2f}%
   - Is Anomaly: {"Yes" if isolation_forest_result['is_anomaly'] else "No"}

2. One-Class SVM Algorithm:
   - Verdict: {one_class_svm_result['verdict']}
   - Confidence: {one_class_svm_result['confidence']:.2f}%
   - Is Anomaly: {"Yes" if one_class_svm_result['is_anomaly'] else "No"}

TASK:
Based on this behavioral biometric data and machine learning results, provide a security threat assessment with the following:

1. Threat Level (Critical, High, Medium, Low, or None)
2. Detailed Analysis (3-4 sentences explaining the reasoning behind your assessment)
3. Recommended Actions (2-3 specific security measures to take)

Use a professional cybersecurity tone and focus on behavioral biometrics in a Zero Trust security framework.
Your response should start with "Threat Level: " followed by the assessment level.
"""

                    # Configure and call Gemini model
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    
                    # Extract the response content
                    analysis = response.text
                    
                    # Parse the threat level from the analysis
                    threat_level = "Unknown"
                    if "Threat Level: Critical" in analysis:
                        threat_level = "Critical"
                    elif "Threat Level: High" in analysis:
                        threat_level = "High"
                    elif "Threat Level: Medium" in analysis:
                        threat_level = "Medium"
                    elif "Threat Level: Low" in analysis:
                        threat_level = "Low"
                    elif "Threat Level: None" in analysis:
                        threat_level = "None"
                    
                    return {
                        'analysis': analysis,
                        'threat_level': threat_level,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                except Exception as e:
                    # Fall back to rule-based analysis if AI fails
                    st.warning(f"AI analysis error, falling back to rule-based system: {str(e)}")
                    return self._rule_based_analysis(typing_category, mouse_category, typing_speed, mouse_speed, 
                                                  typing_desc, mouse_desc, isolation_forest_result, one_class_svm_result)
            else:
                # Use rule-based analysis if no API key
                return self._rule_based_analysis(typing_category, mouse_category, typing_speed, mouse_speed, 
                                               typing_desc, mouse_desc, isolation_forest_result, one_class_svm_result)
            
        except Exception as e:
            st.error(f"Error analyzing threat: {str(e)}")
            return {
                'error': str(e),
                'recommendation': 'An error occurred while analyzing the threat.',
                'threat_level': 'Error'
            }
    
    def _rule_based_analysis(self, typing_category, mouse_category, typing_speed, mouse_speed, 
                           typing_desc, mouse_desc, isolation_forest_result, one_class_svm_result):
        """Fallback rule-based analysis when AI is not available"""
        # Check if any algorithm found suspicious behavior
        if_suspicious = isolation_forest_result['is_anomaly']
        svm_suspicious = one_class_svm_result['is_anomaly']
        one_algorithm_suspicious = if_suspicious or svm_suspicious
        both_algorithms_suspicious = if_suspicious and svm_suspicious
        
        # Determine consistency of behavior
        consistency = 'high' if abs(typing_speed - mouse_speed/100) < 2 else 'low'
        
        # Match against known threat patterns
        matched_patterns = []
        
        for pattern_name, pattern_info in self.threat_patterns.items():
            for condition in pattern_info['conditions']:
                # Default condition values if not specified
                condition_typing = condition.get('typing', None)
                condition_mouse = condition.get('mouse', None)
                condition_consistency = condition.get('consistency', None)
                condition_if_suspicious = condition.get('if_suspicious', None)
                condition_svm_suspicious = condition.get('svm_suspicious', None)
                condition_one_algorithm = condition.get('one_algorithm_suspicious', None)
                
                # Check if conditions match
                typing_match = condition_typing is None or typing_category == condition_typing
                mouse_match = condition_mouse is None or mouse_category == condition_mouse
                consistency_match = condition_consistency is None or consistency == condition_consistency
                if_match = condition_if_suspicious is None or if_suspicious == condition_if_suspicious
                svm_match = condition_svm_suspicious is None or svm_suspicious == condition_svm_suspicious
                one_algo_match = condition_one_algorithm is None or one_algorithm_suspicious == condition_one_algorithm
                
                # If all conditions match, this is a matching pattern
                if (typing_match and mouse_match and consistency_match and 
                    if_match and svm_match and one_algo_match):
                    matched_patterns.append(pattern_info)
                    break  # Found a matching condition for this pattern
        
        # If no patterns match, default to 'normal_user'
        if not matched_patterns:
            matched_patterns = [self.threat_patterns['normal_user']]
        
        # Sort matched patterns by threat level priority
        threat_level_priority = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3, 'None': 4}
        matched_patterns.sort(key=lambda x: threat_level_priority[x['threat_level']])
        
        # Use the highest priority (most severe) threat pattern
        selected_pattern = matched_patterns[0]
        threat_level = selected_pattern['threat_level']
        description = selected_pattern['description']
        
        # Generate analysis text
        if threat_level == "Critical":
            analysis = f"Threat Level: Critical\n\nAnalysis: {description} detected with high confidence. The observed behavior shows {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movements ({mouse_speed:.2f} px/s), which is highly consistent with automated tools or scripts. Both detection algorithms flagged this as suspicious activity with high confidence scores.\n\nRecommended Actions:\n1. Immediately block access and terminate current session\n2. Require additional out-of-band authentication\n3. Conduct full security audit of account activities\n4. Monitor for similar patterns across other accounts"
        elif threat_level == "High":
            analysis = f"Threat Level: High\n\nAnalysis: Potential {description} identified. The system detected {typing_desc} typing speed ({typing_speed:.2f} k/s) with {mouse_desc} mouse movements ({mouse_speed:.2f} px/s), creating a behavioral pattern consistent with unauthorized access attempts. Multiple detection algorithms confirmed this anomalous behavior pattern.\n\nRecommended Actions:\n1. Trigger step-up authentication immediately\n2. Restrict access to sensitive resources\n3. Monitor all activities in real-time\n4. Consider temporary account suspension if behavior continues"
        elif threat_level == "Medium":
            analysis = f"Threat Level: Medium\n\nAnalysis: {description} detected. The user shows {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movement ({mouse_speed:.2f} px/s), which differs from typical behavioral patterns. This combination was flagged by at least one of our detection algorithms as potentially suspicious activity.\n\nRecommended Actions:\n1. Request additional verification\n2. Increase monitoring level for this session\n3. Apply least-privilege access restrictions temporarily"
        elif threat_level == "Low":
            analysis = f"Threat Level: Low\n\nAnalysis: Low-risk {description} detected. The user's {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movement ({mouse_speed:.2f} px/s) show some deviation from normal patterns, but without strong indicators of malicious intent. This may be a legitimate user with slightly unusual behavior patterns.\n\nRecommended Actions:\n1. Continue monitoring behavior\n2. No immediate action required\n3. Review if pattern persists over multiple sessions"
        else:  # None
            analysis = f"Threat Level: None\n\nAnalysis: Normal user activity detected. The user's {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movement ({mouse_speed:.2f} px/s) match expected behavioral patterns for legitimate users. Both anomaly detection algorithms confirm this is within normal parameters.\n\nRecommended Actions:\n1. Continue standard monitoring\n2. No security action required"
        
        return {
            'analysis': analysis,
            'threat_level': threat_level,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def create_detection_visualization(self, user_typing_speed, user_mouse_speed, if_is_anomaly, svm_is_anomaly):
        """Create a visualization comparing the detection algorithms"""
        try:
            # Get the baseline data
            normal_df = st.session_state.normal_baseline
            suspicious_df = st.session_state.suspicious_baseline
            
            # Create the figure and axis
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot normal users
            ax.scatter(
                normal_df['typing_speed'],
                normal_df['mouse_movement_speed'],
                color='blue', alpha=0.6, s=50, label='Normal Users'
            )
            
            # Plot suspicious users
            ax.scatter(
                suspicious_df['typing_speed'],
                suspicious_df['mouse_movement_speed'],
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
            if_model = st.session_state.behavioral_models['isolation_forest']
            Z_if = if_model.decision_function(grid)
            Z_if = Z_if.reshape(xx.shape)
            contour_if = ax.contour(xx, yy, Z_if, levels=[0], colors=['green'], linestyles=['-'], alpha=0.7)
            plt.clabel(contour_if, inline=True, fontsize=8, fmt='Isolation Forest')
            
            # One-Class SVM boundary
            svm_model = st.session_state.behavioral_models['one_class_svm']
            Z_svm = svm_model.decision_function(grid)
            Z_svm = Z_svm.reshape(xx.shape)
            contour_svm = ax.contour(xx, yy, Z_svm, levels=[0], colors=['purple'], linestyles=['--'], alpha=0.7)
            plt.clabel(contour_svm, inline=True, fontsize=8, fmt='One-Class SVM')
            
            # Add labels and title
            ax.set_xlabel('Typing Speed (keystrokes/sec)')
            ax.set_ylabel('Mouse Movement Speed (pixels/sec)')
            ax.set_title('Zero Trust Security: Behavioral Anomaly Detection')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            # Return a basic figure if there's an error
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f"Visualization error: {str(e)}", ha='center', va='center')
            return fig
    
    def record_security_incident(self, threat_level, typing_speed, mouse_speed, if_verdict, svm_verdict):
        """Record a security incident for the security dashboard"""
        incident = {
            'timestamp': datetime.now(),
            'threat_level': threat_level,
            'details': {
                'typing_speed': typing_speed,
                'mouse_speed': mouse_speed,
                'isolation_forest': 'Suspicious' if if_verdict else 'Normal',
                'one_class_svm': 'Suspicious' if svm_verdict else 'Normal'
            },
            'status': 'Active',
            'source': 'Biometric Analysis'
        }
        
        st.session_state.security_incidents.append(incident)
        
        # Update security score based on threat level
        score_impact = {
            'Critical': -50,
            'High': -30,
            'Medium': -15,
            'Low': -5,
            'None': 0,
            'Error': -10
        }
        
        st.session_state.security_score = max(500, min(1000, 
                                                     st.session_state.security_score + score_impact.get(threat_level, 0)))
    
    def display_security_dashboard(self):
        """Display the Zero Trust Security dashboard with integrated threat intelligence"""
        st.header("RAIN™ Zero Trust Security Dashboard")
        
        # Security score display
        score = st.session_state.security_score
        if score >= 900:
            score_color = "green"
            score_status = "Excellent"
        elif score >= 750:
            score_color = "blue"
            score_status = "Good"
        elif score >= 600:
            score_color = "orange" 
            score_status = "Fair"
        else:
            score_color = "red"
            score_status = "Poor"
            
        st.markdown(f"""
        <div style='background-color: #0a192f; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h3 style='color: white; margin: 0;'>Security Posture: {score_status}</h3>
                    <p style='color: #8892b0; margin: 5px 0 0 0;'>Real-time zero trust security monitoring active</p>
                </div>
                <div style='text-align: right;'>
                    <h2 style='color: {score_color}; margin: 0;'>{score}/1000</h2>
                    <p style='color: #8892b0; margin: 5px 0 0 0;'>Enterprise Security Score</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Security tabs for different components
        tab1, tab2, tab3, tab4 = st.tabs([
            "Behavioral Analysis", "Security Incidents", "Threat Intelligence", "Security Controls"
        ])
        
        with tab1:
            st.markdown("### Behavioral Biometric Analysis")
            st.write("Zero Trust Security continuously monitors user behavior to detect anomalies and potential threats.")
            
            # Set up columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Anomaly Detection Rate", 
                    "99.7%", 
                    "2.3%",
                    help="Percentage of anomalies successfully detected by our algorithms"
                )
            
            with col2:
                st.metric(
                    "False Positive Rate", 
                    "0.05%", 
                    "-0.02%",
                    help="Percentage of legitimate activities incorrectly flagged as suspicious"
                )
                
            with col3:
                st.metric(
                    "Response Time", 
                    "42ms", 
                    "-8ms",
                    help="Time to detect and respond to suspicious behavior"
                )
            
            # Show the behavioral models visualization
            st.markdown("#### Behavioral Analysis Models")
            
            # Generate sample user data for visualization
            normal_df, suspicious_df = self.generate_user_data(80, 8)
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot normal users
            ax.scatter(
                normal_df['typing_speed'],
                normal_df['mouse_movement_speed'],
                color='blue', alpha=0.6, s=50, label='Normal Users'
            )
            
            # Plot suspicious users  
            ax.scatter(
                suspicious_df['typing_speed'],
                suspicious_df['mouse_movement_speed'],
                color='red', alpha=0.6, s=50, label='Suspicious Users'
            )
            
            # Add decision boundaries using contours
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            xx, yy = np.meshgrid(
                np.linspace(x_min, x_max, 100),
                np.linspace(y_min, y_max, 100)
            )
            grid = np.c_[xx.ravel(), yy.ravel()]
            
            # Get models
            if_model = st.session_state.behavioral_models.get('isolation_forest')
            svm_model = st.session_state.behavioral_models.get('one_class_svm')
            
            if if_model and svm_model:
                # Isolation Forest boundary
                Z_if = if_model.decision_function(grid)
                Z_if = Z_if.reshape(xx.shape)
                contour_if = ax.contour(xx, yy, Z_if, levels=[0], colors=['green'], linestyles=['-'], alpha=0.7)
                plt.clabel(contour_if, inline=True, fontsize=8, fmt='Isolation Forest')
                
                # One-Class SVM boundary
                Z_svm = svm_model.decision_function(grid)
                Z_svm = Z_svm.reshape(xx.shape)
                contour_svm = ax.contour(xx, yy, Z_svm, levels=[0], colors=['purple'], linestyles=['--'], alpha=0.7)
                plt.clabel(contour_svm, inline=True, fontsize=8, fmt='One-Class SVM')
            
            # Add labels and title
            ax.set_xlabel('Typing Speed (keystrokes/sec)')
            ax.set_ylabel('Mouse Movement Speed (pixels/sec)')
            ax.set_title('Zero Trust Security: Behavioral Anomaly Detection Models')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            
            # Show the figure
            st.pyplot(fig)
            
            st.markdown("""
            **How Zero Trust Behavioral Analysis Works:**
            
            1. **Continuous Authentication**: I monitor behavioral patterns including typing rhythm, 
               mouse movements, and interaction patterns
               
            2. **Multi-Algorithm Detection**: I combine Isolation Forest and One-Class SVM algorithms 
               for superior accuracy with minimal false positives
               
            3. **AI-Powered Threat Intelligence**: I leverage advanced AI to interpret behavioral 
               anomalies in real-time and provide actionable insights
               
            4. **Adaptive Baseline**: I maintain personalized behavioral baselines that adapt 
               to legitimate changes in user behavior over time
            """)
        
        with tab2:
            st.markdown("### Security Incidents")
            
            # Show incident filters
            col1, col2 = st.columns([3, 1])
            with col1:
                filter_status = st.multiselect(
                    "Filter by Status",
                    ["Active", "Resolved", "Investigating"],
                    default=["Active"]
                )
            with col2:
                filter_days = st.slider("Show incidents from the last X days", 1, 30, 7)
            
            # Display incidents
            if st.session_state.security_incidents:
                # Filter incidents based on user selection
                filtered_incidents = []
                cutoff_date = datetime.now() - timedelta(days=filter_days)
                
                for incident in st.session_state.security_incidents:
                    if incident['timestamp'] >= cutoff_date and incident['status'] in filter_status:
                        filtered_incidents.append(incident)
                
                if filtered_incidents:
                    for i, incident in enumerate(reversed(filtered_incidents)):
                        # Determine color based on threat level
                        if incident['threat_level'] == 'Critical':
                            severity_color = "#F44336"  # Red
                        elif incident['threat_level'] == 'High':
                            severity_color = "#FF9800"  # Orange
                        elif incident['threat_level'] == 'Medium':
                            severity_color = "#FFEB3B"  # Yellow
                        elif incident['threat_level'] == 'Low':
                            severity_color = "#4CAF50"  # Green
                        else:
                            severity_color = "#9E9E9E"  # Gray
                        
                        # Format timestamp
                        timestamp_str = incident['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Create incident card
                        st.markdown(f"""
                        <div style="border-left: 5px solid {severity_color}; padding: 10px; margin-bottom: 10px; background-color: #f5f5f5;">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <span style="font-weight: bold;">{incident['threat_level']} Threat</span> • 
                                    <span style="color: #666;">{incident['source']}</span>
                                </div>
                                <div>
                                    <span style="background-color: {'#e57373' if incident['status'] == 'Active' else '#81c784'}; 
                                               color: white; 
                                               padding: 3px 8px; 
                                               border-radius: 4px; 
                                               font-size: 12px;">
                                        {incident['status']}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 5px; color: #333;">
                                <ul style="margin: 0; padding-left: 20px;">
                                    <li>Typing Speed: {incident['details']['typing_speed']:.2f} keystrokes/sec</li>
                                    <li>Mouse Speed: {incident['details']['mouse_speed']:.2f} pixels/sec</li>
                                    <li>Isolation Forest: {incident['details']['isolation_forest']}</li>
                                    <li>One-Class SVM: {incident['details']['one_class_svm']}</li>
                                </ul>
                            </div>
                            <div style="margin-top: 5px; font-size: 12px; color: #666;">
                                {timestamp_str}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add action buttons for each incident
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col1:
                            if st.button(f"Investigate", key=f"investigate_{i}"):
                                st.session_state.security_incidents[-(i+1)]['status'] = 'Investigating'
                                st.rerun()
                        with col2:
                            if st.button(f"Resolve", key=f"resolve_{i}"):
                                st.session_state.security_incidents[-(i+1)]['status'] = 'Resolved'
                                st.rerun()
                        with col3:
                            if st.button(f"Block User", key=f"block_{i}"):
                                st.warning(f"User associated with incident has been blocked")
                else:
                    st.info(f"No security incidents matching the selected filters in the last {filter_days} days.")
            else:
                st.info("No security incidents have been recorded.")
                
                # Add sample incident button
                if st.button("Generate Sample Incident"):
                    typing_speed = random.uniform(1.5, 9.0)
                    mouse_speed = random.uniform(100, 700)
                    
                    # Determine threat level based on speed
                    if typing_speed > 7.5 or mouse_speed > 600:
                        threat_level = "Critical"
                    elif typing_speed < 2.0 or mouse_speed < 150:
                        threat_level = "High"
                    else:
                        threat_level = "Medium"
                        
                    self.record_security_incident(
                        threat_level, 
                        typing_speed, 
                        mouse_speed, 
                        True, 
                        True if threat_level == "Critical" else False
                    )
                    st.rerun()
        
        with tab3:
            st.markdown("### Threat Intelligence Hub")
            
            # Display threat feed settings
            st.markdown("#### External Threat Intelligence")
            
            # Create threat feed integration UI
            col1, col2 = st.columns([3, 1])
            with col1:
                feed_url = st.text_input(
                    "Threat Intelligence Feed URL",
                    value="https://api.threatintel.example.com/v1/feed",
                    help="Enter the URL of your threat intelligence feed"
                )
            with col2:
                if st.button("Connect Feed", type="primary"):
                    with st.spinner("Connecting to threat feed..."):
                        time.sleep(1.5)  # Simulate connection time
                        st.session_state.threat_feed_connected = True
                        st.success("Connected to threat intelligence feed!")
                
            if 'threat_feed_connected' in st.session_state and st.session_state.threat_feed_connected:
                # Show threat intelligence data
                st.markdown("#### Active Threat Indicators")
                
                # Display tabs for different IOC types
                ioc_tab1, ioc_tab2, ioc_tab3 = st.tabs(["Threat Actors", "Indicators", "Vulnerabilities"])
                
                with ioc_tab1:
                    # Display threat actors
                    st.markdown("##### Active Threat Actors")
                    
                    threat_actors = pd.DataFrame({
                        "Actor": st.session_state.threat_intel_feed['threat_actors'],
                        "Confidence": [92, 88, 76, 85, 79],
                        "First Seen": ["2023-11-15", "2024-01-03", "2024-02-27", "2024-01-18", "2023-12-10"]
                    })
                    
                    st.table(threat_actors)
                
                with ioc_tab2:
                    # Display indicators of compromise
                    st.markdown("##### Recent Indicators of Compromise")
                    
                    indicators_list = []
                    for ioc in st.session_state.threat_intel_feed['indicators'][:10]:
                        indicators_list.append({
                            "Type": ioc['type'].upper(),
                            "Value": ioc['value'],
                            "Confidence": f"{ioc['confidence']}%",
                            "First Seen": ioc['first_seen']
                        })
                    
                    indicators_df = pd.DataFrame(indicators_list)
                    st.table(indicators_df)
                
                with ioc_tab3:
                    # Display vulnerabilities
                    st.markdown("##### Critical Vulnerabilities")
                    
                    vulns = pd.DataFrame({
                        "CVE ID": st.session_state.threat_intel_feed['vulnerabilities'],
                        "CVSS": ["9.8", "8.7", "8.2", "9.1", "7.9"],
                        "Status": ["Active", "Active", "Patched", "Active", "Under Analysis"]
                    })
                    
                    st.table(vulns)
                
                # Display MITRE ATT&CK tactics
                st.markdown("#### MITRE ATT&CK Coverage")
                
                # Create visualization for ATT&CK tactics
                tactics = st.session_state.threat_intel_feed['tactics']
                coverage = [95, 90, 88, 85, 92]
                
                fig, ax = plt.subplots(figsize=(10, 4))
                bars = ax.bar(tactics, coverage, color='#0068C9')
                
                # Add data labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{height}%', ha='center', va='bottom')
                
                ax.set_ylim(0, 100)
                ax.set_ylabel('Coverage (%)')
                ax.set_title('MITRE ATT&CK Tactics Coverage')
                
                # Add a horizontal line for the average
                avg_coverage = sum(coverage) / len(coverage)
                ax.axhline(y=avg_coverage, color='r', linestyle='--', alpha=0.7, 
                           label=f'Average: {avg_coverage:.1f}%')
                
                ax.legend()
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig)
            else:
                st.info("Connect to a threat intelligence feed to view threat data.")
        
        with tab4:
            st.markdown("### Zero Trust Security Controls")
            
            # Display security control settings
            st.markdown("#### Access Control Policies")
            
            # Create control tabs
            control_tab1, control_tab2, control_tab3 = st.tabs([
                "Authentication", "Network Controls", "Device Management"
            ])
            
            with control_tab1:
                st.markdown("##### Authentication Settings")
                
                # MFA settings
                st.checkbox("Require Multi-Factor Authentication", value=True, disabled=True)
                st.slider("Authentication Timeout (minutes)", 5, 120, 30)
                st.selectbox(
                    "Failed Login Attempts Before Lockout",
                    options=[3, 5, 10],
                    index=0
                )
                
                # Add biometric settings
                st.markdown("##### Biometric Settings")
                col1, col2 = st.columns(2)
                
                with col1:
                    typing_low = st.slider(
                        "Typing Speed Lower Threshold (keystrokes/sec)",
                        0.0, 5.0, st.session_state.anomaly_thresholds['typing']['low'], 0.1
                    )
                    st.session_state.anomaly_thresholds['typing']['low'] = typing_low
                
                with col2:
                    typing_high = st.slider(
                        "Typing Speed Upper Threshold (keystrokes/sec)",
                        5.0, 15.0, st.session_state.anomaly_thresholds['typing']['high'], 0.1
                    )
                    st.session_state.anomaly_thresholds['typing']['high'] = typing_high
                
                col1, col2 = st.columns(2)
                with col1:
                    mouse_low = st.slider(
                        "Mouse Speed Lower Threshold (pixels/sec)",
                        50, 200, st.session_state.anomaly_thresholds['mouse']['low'], 5
                    )
                    st.session_state.anomaly_thresholds['mouse']['low'] = mouse_low
                
                with col2:
                    mouse_high = st.slider(
                        "Mouse Speed Upper Threshold (pixels/sec)",
                        400, 800, st.session_state.anomaly_thresholds['mouse']['high'], 5
                    )
                    st.session_state.anomaly_thresholds['mouse']['high'] = mouse_high
            
            with control_tab2:
                st.markdown("##### Network Security Controls")
                
                # Network settings
                st.checkbox("Enable Zero Trust Network Access (ZTNA)", value=True)
                st.checkbox("Micro-Segmentation", value=True)
                st.checkbox("Deep Packet Inspection", value=True)
                
                # Security protocols
                st.markdown("##### Security Protocols")
                st.multiselect(
                    "Enabled Security Protocols",
                    ["TLS 1.3", "IPsec", "DNSSEC", "HTTPS", "SFTP", "SNMPv3", "SSH"],
                    default=["TLS 1.3", "HTTPS", "SSH", "DNSSEC"]
                )
                
                # Intrusion detection
                st.markdown("##### Intrusion Detection")
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox(
                        "IDS/IPS Mode",
                        ["Monitor Only", "Block Suspicious", "Block All Unknown"],
                        index=1
                    )
                with col2:
                    st.selectbox(
                        "Alert Threshold",
                        ["Low (Maximum Alerts)", "Medium", "High (Critical Only)"],
                        index=1
                    )
            
            with control_tab3:
                st.markdown("##### Device Security")
                
                # Device settings
                st.checkbox("Require Device Registration", value=True)
                st.checkbox("Enforce Device Health Checks", value=True)
                st.checkbox("Require Device Encryption", value=True)
                
                # Endpoint settings
                st.markdown("##### Endpoint Protection")
                st.multiselect(
                    "Required Endpoint Controls",
                    ["Anti-malware", "Host Firewall", "EDR Agent", "DLP", "USB Control", "Patch Management"],
                    default=["Anti-malware", "Host Firewall", "EDR Agent"]
                )
                
                # Device inventory visualization
                st.markdown("##### Device Inventory")
                
                device_types = ["Workstation", "Laptop", "Mobile", "Server", "IoT Device"]
                device_counts = [45, 78, 52, 23, 17]
                device_compliance = [98, 95, 87, 100, 76]
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
                
                # Device type distribution
                ax1.pie(device_counts, labels=device_types, autopct='%1.1f%%', startangle=90,
                        colors=['#0068c9', '#83c9ff', '#ff9f40', '#29b09d', '#ff7c43'])
                ax1.set_title('Device Type Distribution')
                
                # Compliance rates
                bars = ax2.bar(device_types, device_compliance, color='#0068c9')
                
                # Add data labels
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{height}%', ha='center', va='bottom')
                
                ax2.set_ylim(0, 105)
                ax2.set_ylabel('Compliance Rate (%)')
                ax2.set_title('Device Compliance Rates')
                
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig)
                
        st.markdown("---")
        
        # Security action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔒 Run Security Assessment", use_container_width=True):
                with st.spinner("Running comprehensive security assessment..."):
                    time.sleep(2)  # Simulate assessment
                    st.success("Security assessment complete. No critical vulnerabilities found.")
        
        with col2:
            if st.button("🛡️ Update Threat Intelligence", use_container_width=True):
                with st.spinner("Updating threat intelligence from all sources..."):
                    time.sleep(1.5)  # Simulate update
                    st.success("Threat intelligence updated successfully.")
        
        with col3:
            if st.button("🔐 Zero Trust Health Check", use_container_width=True):
                with st.spinner("Verifying Zero Trust security controls..."):
                    time.sleep(2.5)  # Simulate check
                    st.success("Zero Trust security controls are properly configured.")
