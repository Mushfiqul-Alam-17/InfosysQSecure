import streamlit as st
from openai import OpenAI
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime

class AIThreatAnalyzer:
    """
    Class for analyzing security threats using OpenAI's GPT model.
    This provides real intelligence and recommendations based on detected anomalies.
    """
    
    def __init__(self):
        """Initialize the AI threat analyzer"""
        if 'openai_api_key' not in st.session_state:
            st.session_state.openai_api_key = None
        if 'threat_history' not in st.session_state:
            st.session_state.threat_history = []
    
    def set_api_key(self, api_key):
        """Set the OpenAI API key"""
        st.session_state.openai_api_key = api_key
    
    def has_api_key(self):
        """Check if an API key has been provided"""
        return st.session_state.openai_api_key is not None and st.session_state.openai_api_key.strip() != ""
    
    def analyze_threat(self, user_data, detection_results):
        """
        Analyze the threat using OpenAI GPT and provide an expert assessment
        
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
        if not self.has_api_key():
            return {
                'error': 'No API key provided',
                'recommendation': 'Please provide an OpenAI API key to enable AI threat analysis.',
                'threat_level': 'Unknown'
            }
        
        # Create a prompt for the AI
        typing_speed = user_data['typing_speed']
        mouse_speed = user_data['mouse_speed']
        
        isolation_forest_result = detection_results['isolation_forest']
        one_class_svm_result = detection_results['one_class_svm']
        
        # Build a detailed context for the AI
        prompt = f"""You are CyberGuardian, an advanced AI security analyst specializing in Zero Trust security and behavioral biometrics.

USER BEHAVIOR DATA:
- Typing Speed: {typing_speed:.2f} keystrokes/second
- Mouse Movement Speed: {mouse_speed:.2f} pixels/second

ANOMALY DETECTION RESULTS:
1. Isolation Forest Algorithm:
   - Verdict: {isolation_forest_result['verdict']}
   - Confidence: {isolation_forest_result['confidence']:.2f}%

2. One-Class SVM Algorithm:
   - Verdict: {one_class_svm_result['verdict']}
   - Confidence: {one_class_svm_result['confidence']:.2f}%

TASK:
Based on this behavioral biometric data and machine learning results, provide a security threat assessment with the following:

1. Threat Level (Critical, High, Medium, Low, or None)
2. Detailed Analysis (3-4 sentences explaining the reasoning behind your assessment)
3. Recommended Actions (2-3 specific security measures to take)

Use a professional cybersecurity tone and focus on behavioral biometrics in a Zero Trust security framework.
"""
        
        try:
            client = OpenAI(api_key=st.session_state.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are CyberGuardian, an advanced AI security analyst specializing in Zero Trust security and behavioral biometrics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract the response content
            analysis = response.choices[0].message.content
            
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
            st.error(f"Error analyzing threat: {str(e)}")
            return {
                'error': str(e),
                'recommendation': 'An error occurred while analyzing the threat. Please check your API key and try again.',
                'threat_level': 'Error'
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