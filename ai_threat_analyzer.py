import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime
import random
import google.generativeai as genai

class AIThreatAnalyzer:
    """
    Class for analyzing security threats using Google's Gemini AI model.
    This provides real intelligence and recommendations based on detected anomalies.
    """
    
    def __init__(self):
        """Initialize the AI threat analyzer"""
        if 'threat_history' not in st.session_state:
            st.session_state.threat_history = []
            
        # Set default API key for demo purposes
        # In a real production environment, this would be securely stored
        self.api_key = "AIzaSyBX-IsY-_uOUEWV2_-r3k0xzCWFQim9rqA"  # Demo API key for presentation purposes
        
        # Configure Gemini AI with the demo API key
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            st.warning(f"Demo API configuration issue: {str(e)}")
            
        # Define expert knowledge base for threat analysis
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
        
        # Fallback threat patterns if AI is not available
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
        
        # Store API key
        self.api_key = None
        
    def set_api_key(self, api_key):
        """Set the Gemini API key"""
        self.api_key = api_key
        # Configure Gemini AI if API key is provided
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
        except Exception as e:
            st.error(f"Error configuring Gemini AI: {str(e)}")
    
    def has_api_key(self):
        """Check if an API key has been provided"""
        return self.api_key is not None and self.api_key.strip() != ""
    
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
    
    def analyze_threat(self, user_data, detection_results):
        """
        Analyze the threat using Google's Gemini AI model and provide an expert assessment
        
        Parameters:
        -----------
        user_data: dict
            Dictionary containing user behavior data
        detection_results: dict
            Dictionary containing anomaly detection results
            
        Returns:
        --------
        threat_analysis: dict
            Dictionary containing threat analysis results
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
            
            # Build a detailed context for the AI
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
                    
                    # Record the threat in history
                    self.record_threat(threat_level, typing_speed, mouse_speed, 
                                    isolation_forest_result['verdict'], 
                                    one_class_svm_result['verdict'])
                    
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
            analysis = f"Threat Level: Low\n\nAnalysis: Low-risk {description} detected. The user exhibits {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movement ({mouse_speed:.2f} px/s), which shows minor deviations from normal patterns. This created a low-confidence alert in one detection algorithm but is likely benign activity.\n\nRecommended Actions:\n1. Continue normal monitoring protocols\n2. No immediate action required\n3. Include data point in behavioral baseline updates"
        else:  # None
            analysis = f"Threat Level: None\n\nAnalysis: Normal user behavior confirmed. The user demonstrates {typing_desc} typing speed ({typing_speed:.2f} k/s) and {mouse_desc} mouse movement ({mouse_speed:.2f} px/s), which aligns with expected behavioral patterns. No anomalies were detected by either algorithm, indicating legitimate user activity.\n\nRecommended Actions:\n1. Continue standard Zero Trust verification\n2. Maintain regular authentication renewal cycle\n3. Update behavioral baseline with this interaction data"
        
        # Record the threat in history
        self.record_threat(threat_level, typing_speed, mouse_speed, 
                          isolation_forest_result['verdict'], 
                          one_class_svm_result['verdict'])
        
        return {
            'analysis': analysis,
            'threat_level': threat_level,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def record_threat(self, threat_level, typing_speed, mouse_speed, if_verdict, svm_verdict):
        """
        Record a threat in the threat history
        
        Parameters:
        -----------
        threat_level: str
            The threat level (Critical, High, Medium, Low, None, Error)
        typing_speed: float
            The user's typing speed
        mouse_speed: float
            The user's mouse speed
        if_verdict: str
            The Isolation Forest verdict
        svm_verdict: str
            The One-Class SVM verdict
        """
        threat = {
            'timestamp': datetime.now(),
            'threat_level': threat_level,
            'typing_speed': typing_speed,
            'mouse_speed': mouse_speed,
            'isolation_forest_verdict': if_verdict,
            'one_class_svm_verdict': svm_verdict
        }
        
        st.session_state.threat_history.append(threat)
        
        # Keep only the last 50 threats
        if len(st.session_state.threat_history) > 50:
            st.session_state.threat_history.pop(0)
    
    def show_threat_dashboard(self):
        """Display a dashboard of threat history"""
        if not st.session_state.threat_history:
            st.info("No threat history available. Start analyzing threats to build a history.")
            return
        
        st.subheader("Threat Intelligence Dashboard")
        
        # Convert threat history to DataFrame
        df = pd.DataFrame(st.session_state.threat_history)
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        
        # Total threats analyzed
        with col1:
            st.metric("Total Threats Analyzed", len(df))
            
        # Suspicious activities detected
        suspicious_count = sum((df['threat_level'] == 'Critical') | 
                              (df['threat_level'] == 'High') | 
                              (df['threat_level'] == 'Medium'))
        with col2:
            st.metric("Suspicious Activities", suspicious_count,
                     delta=f"{suspicious_count/len(df)*100:.1f}%" if len(df) > 0 else None)
            
        # Latest threat level
        with col3:
            latest_threat = df.iloc[-1]['threat_level'] if not df.empty else "None"
            st.metric("Latest Threat Level", latest_threat)
        
        # Create threat level distribution chart
        if len(df) > 0:
            threat_counts = df['threat_level'].value_counts()
            
            # Create a colorful pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = {
                'Critical': '#ff1744',
                'High': '#ff5252',
                'Medium': '#ff9100',
                'Low': '#ffeb3b',
                'None': '#4caf50',
                'Error': '#9e9e9e',
                'Unknown': '#9e9e9e'
            }
            
            # Extract colors for the actual threat levels present
            pie_colors = [colors.get(level, '#9e9e9e') for level in threat_counts.index]
            
            wedges, texts, autotexts = ax.pie(
                threat_counts, 
                labels=threat_counts.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=pie_colors,
                explode=[0.05] * len(threat_counts),
                shadow=True
            )
            
            # Style the text elements
            plt.setp(autotexts, size=10, weight="bold", color="white")
            plt.setp(texts, size=12)
            
            ax.set_title('Threat Level Distribution', size=14)
            plt.tight_layout()
            
            # Display the pie chart
            st.pyplot(fig)
            
            # Show timeline of threats
            st.subheader("Threat Timeline")
            
            # Create a timeline visualization
            fig, ax = plt.subplots(figsize=(12, 4))
            
            # Map threat levels to numeric values for plotting
            threat_level_map = {
                'Critical': 5,
                'High': 4,
                'Medium': 3,
                'Low': 2,
                'None': 1,
                'Error': 0,
                'Unknown': 0
            }
            
            df['threat_value'] = df['threat_level'].map(threat_level_map)
            
            # Create a colorful timeline
            scatter = ax.scatter(
                range(len(df)),
                df['threat_value'],
                c=[colors.get(level, '#9e9e9e') for level in df['threat_level']],
                s=100,
                alpha=0.7
            )
            
            # Connect points with a line
            ax.plot(range(len(df)), df['threat_value'], 'k--', alpha=0.3)
            
            # Set y-axis tick labels
            ax.set_yticks(list(threat_level_map.values()))
            ax.set_yticklabels(list(threat_level_map.keys()))
            
            # Set x-axis labels
            if len(df) > 10:
                # If many points, show only some x-labels
                x_ticks = np.linspace(0, len(df)-1, 10, dtype=int)
                ax.set_xticks(x_ticks)
                ax.set_xticklabels([f"Event {i+1}" for i in x_ticks], rotation=45)
            else:
                ax.set_xticks(range(len(df)))
                ax.set_xticklabels([f"Event {i+1}" for i in range(len(df))], rotation=45)
            
            ax.set_title('Threat Level Timeline')
            ax.set_xlabel('Events (Recent →)')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Show latest threat details
            st.subheader("Latest Threat Details")
            latest = df.iloc[-1]
            
            st.markdown(f"""
            **Time:** {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}  
            **Threat Level:** {latest['threat_level']}  
            **Typing Speed:** {latest['typing_speed']:.2f} keystrokes/sec  
            **Mouse Speed:** {latest['mouse_speed']:.2f} pixels/sec  
            **Isolation Forest:** {latest['isolation_forest_verdict']}  
            **One-Class SVM:** {latest['one_class_svm_verdict']}  
            """)
        
        # Provide a download option for the threat history
        if len(df) > 0:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Threat History",
                data=csv,
                file_name="threat_history.csv",
                mime="text/csv"
            )