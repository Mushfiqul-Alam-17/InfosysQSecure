import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import time
from datetime import datetime

from zero_trust import ZeroTrustSecuritySystem
from quantum_visualization import create_quantum_animation, get_next_animation_frame
from presentation_guide import display_presentation_guide
from utils import load_logo
from biometric_collector import BiometricCollector
from ai_threat_analyzer import AIThreatAnalyzer
from enterprise_threat_dashboard import EnterpriseThreatDashboard

# Set page configuration
st.set_page_config(
    page_title="RAIN™ Enterprise Security Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0068C9;
        --background-color: #f5f7fa;
        --secondary-background-color: #ffffff;
        --text-color: #262730;
        --font: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Enhance buttons */
    .stButton > button {
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Card-like containers */
    .css-1r6slb0, .css-12oz5g7 {
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 1rem;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #0068C9;
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .alert-box.success {
        background-color: #e3f9e5;
        border-left: 5px solid #4CAF50;
        color: #1b5e20;
    }
    .alert-box.warning {
        background-color: #fff8e1;
        border-left: 5px solid #FFC107;
        color: #b76e00;
    }
    .alert-box.error {
        background-color: #ffebee;
        border-left: 5px solid #F44336;
        color: #c62828;
    }
    
    /* Data visualization containers */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Security metrics styling */
    .metrics-container {
        background: linear-gradient(to right, #f5f7fa, #e4e8f0);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Animation container */
    .animation-container {
        background: #1f1f2e;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Enhance sidebar */
    .css-6qob1r {
        background-image: linear-gradient(to bottom, #0068C9, #003366);
    }
    .css-6qob1r .css-10oheav {
        color: white !important;
    }
    .css-6qob1r label {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize key classes
biometric_collector = BiometricCollector()
ai_threat_analyzer = AIThreatAnalyzer()

# Create session state variables if they don't exist
if 'current_user_index' not in st.session_state:
    st.session_state.current_user_index = 0
if 'normal_users' not in st.session_state:
    st.session_state.normal_users = None
if 'suspicious_users' not in st.session_state:
    st.session_state.suspicious_users = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'animation_created' not in st.session_state:
    st.session_state.animation_created = False
if 'animation_data' not in st.session_state:
    st.session_state.animation_data = None
if 'show_api_key_input' not in st.session_state:
    st.session_state.show_api_key_input = False
if 'real_time_monitoring' not in st.session_state:
    st.session_state.real_time_monitoring = False
    
# Initialize the enterprise threat dashboard
enterprise_dashboard = EnterpriseThreatDashboard()

def increment_user():
    """Function to increment the current user index when the button is clicked"""
    # Increment the user index and wrap around if needed
    st.session_state.current_user_index = (st.session_state.current_user_index + 1) % (len(st.session_state.normal_users) + len(st.session_state.suspicious_users))
    st.rerun()

def toggle_api_key_input():
    """Toggle the visibility of the API key input field"""
    st.session_state.show_api_key_input = not st.session_state.show_api_key_input

def toggle_real_time_monitoring():
    """Toggle real-time monitoring mode"""
    st.session_state.real_time_monitoring = not st.session_state.real_time_monitoring

# Sidebar for navigation
st.sidebar.title("RAIN™ Platform")
page = st.sidebar.radio(
    "Select a component:",
    ["Zero Trust Security", "User Behavior Analysis", "AI Threat Intelligence", 
     "Quantum Security Visualization", "Enterprise Security Dashboard", "Executive Presentation", 
     "Enterprise Website"]
)

# Set the Gemini API key for background threat analysis (not shown to users)
if 'gemini_api_key' not in st.session_state:
    # Use the provided Gemini API key silently in the background
    st.session_state.gemini_api_key = "AIzaSyBWQ2WIgMd0O-ccgW-O7xgLet-dx5uIA4Y"
    ai_threat_analyzer.set_api_key(st.session_state.gemini_api_key)

# Display logo
load_logo()
st.markdown("""
<h1 style="text-align: center; color: #0068C9;">RAIN™ Enterprise Security Platform</h1>
<h3 style="text-align: center; color: #666; margin-top: 0;">Real-Time AI-Driven Threat Interceptor and Neutralizer</h3>
""", unsafe_allow_html=True)

if page == "Zero Trust Security":
    st.header("RAIN™ Zero Trust Security")
    
    # Description of the Zero Trust model
    with st.expander("What is Zero Trust Security?", expanded=False):
        st.markdown("""
        **Zero Trust Security** is a cybersecurity framework that requires all users, whether inside or outside the organization's network, to be authenticated, authorized, and continuously validated before being granted access to applications and data. 
        
        This prototype demonstrates:
        1. Continuous monitoring of user behavior (typing speed, mouse movement)
        2. Anomaly detection using multiple machine learning algorithms
        3. Real-time security alerts when suspicious activity is detected
        
        **How it works:**
        - We collect real biometric data from your typing behavior
        - We compare it against known patterns of normal and suspicious users
        - The system uses multiple algorithms to detect anomalies
        - When anomalies are detected, the system raises security alerts
        """)
    
    # Tabs for different modes
    tab1, tab2 = st.tabs(["Real-time Biometric Analysis", "Simulated User Analysis"])
    
    with tab1:
        st.subheader("RAIN™ Biometric Security Analysis")
        st.markdown("This enterprise-grade solution analyzes typing behavior to identify and block unauthorized access attempts.")
        
        # Capture real typing data with analyze button
        text_input, analyze_button = biometric_collector.capture_typing_data()
        
        if len(st.session_state.typing_speeds) > 0:
            # We have some typing data, so we can analyze it
            
            # Generate comparison data (if needed)
            if st.session_state.normal_users is None or st.session_state.suspicious_users is None:
                normal_users, suspicious_users = biometric_collector.simulate_mouse_data(100, 10)
                st.session_state.normal_users = normal_users
                st.session_state.suspicious_users = suspicious_users
            
            # Get current typing speed
            current_typing_speed = st.session_state.last_typing_speed
            
            # Compare with anomaly detection algorithms
            if analyze_button:
                with st.spinner("Analyzing your behavior patterns..."):
                    # Run comparison of algorithms
                    results = biometric_collector.compare_algorithms(
                        current_typing_speed,
                        st.session_state.normal_users,
                        st.session_state.suspicious_users
                    )
                    
                    # Display results
                    st.subheader("Security Analysis Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Display verdict
                        if results['overall_verdict'] == "SUSPICIOUS (Both Algorithms)":
                            st.error("⚠️ HIGH ALERT: Suspicious behavior detected by both algorithms!")
                        elif results['overall_verdict'] == "SUSPICIOUS (Single Algorithm)":
                            st.warning("⚠️ CAUTION: Potential suspicious behavior detected!")
                        else:
                            st.success("✓ Normal behavior pattern confirmed")
                        
                        # Display detailed metrics
                        st.markdown("### Behavior Metrics")
                        st.markdown(f"""
                        - **Your typing speed:** {results['user_data']['typing_speed']:.2f} keystrokes/sec
                        - **Estimated mouse speed:** {results['user_data']['mouse_speed']:.2f} pixels/sec
                        """)
                        
                        # Display algorithm results
                        st.markdown("### Algorithm Verdicts")
                        
                        # Isolation Forest results
                        if_result = results['isolation_forest']
                        if if_result['is_anomaly']:
                            st.markdown(f"🔍 **Isolation Forest:** Suspicious (Confidence: {if_result['confidence']:.2f}%)")
                        else:
                            st.markdown(f"🔍 **Isolation Forest:** Normal (Confidence: {if_result['confidence']:.2f}%)")
                        
                        # One-Class SVM results
                        svm_result = results['one_class_svm']
                        if svm_result['is_anomaly']:
                            st.markdown(f"🔍 **One-Class SVM:** Suspicious (Confidence: {svm_result['confidence']:.2f}%)")
                        else:
                            st.markdown(f"🔍 **One-Class SVM:** Normal (Confidence: {svm_result['confidence']:.2f}%)")
                        
                        # AI Threat Analysis if API key is provided
                        if ai_threat_analyzer.has_api_key():
                            st.markdown("### AI Threat Analysis")
                            with st.spinner("Analyzing threat with advanced AI..."):
                                threat_analysis = ai_threat_analyzer.analyze_threat(
                                    results['user_data'], 
                                    {
                                        'isolation_forest': if_result,
                                        'one_class_svm': svm_result
                                    }
                                )
                                
                                if 'error' in threat_analysis:
                                    st.error(f"Error in AI analysis: {threat_analysis['error']}")
                                else:
                                    # Record the threat in the enterprise dashboard system
                                    if 'threat_level' in threat_analysis:
                                        enterprise_dashboard.add_threat_event(
                                            threat_analysis['threat_level'],
                                            f"RAIN™ AI detected {threat_analysis['threat_level'].lower()} risk behavior pattern",
                                            "Real-Time Monitoring System"
                                        )
                                    
                                    # Display threat level with appropriate styling
                                    threat_level = threat_analysis['threat_level']
                                    if threat_level in ["Critical", "High"]:
                                        st.markdown(f"""
                                        <div class="alert-box error">
                                        <strong>Threat Level: {threat_level}</strong>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    elif threat_level == "Medium":
                                        st.markdown(f"""
                                        <div class="alert-box warning">
                                        <strong>Threat Level: {threat_level}</strong>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"""
                                        <div class="alert-box success">
                                        <strong>Threat Level: {threat_level}</strong>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    # Display the full analysis
                                    st.markdown(threat_analysis['analysis'])
                        # AI threat analysis is already enabled with Gemini API
                        # The empty else block is intentional - no message needed since API key is provided automatically
                    
                    with col2:
                        # Display the comparison plot
                        st.pyplot(results['plot'])
                        
                        # Display recommended actions
                        st.markdown("### Recommended Actions")
                        
                        if results['overall_verdict'] == "SUSPICIOUS (Both Algorithms)":
                            st.markdown("""
                            🚨 **High Priority Actions:**
                            1. Immediately require additional authentication factors
                            2. Temporarily restrict access to sensitive systems
                            3. Initiate security team investigation
                            4. Begin session recording for forensic analysis
                            5. Monitor all system commands and data access
                            """)
                        elif results['overall_verdict'] == "SUSPICIOUS (Single Algorithm)":
                            st.markdown("""
                            ⚠️ **Recommended Actions:**
                            1. Request additional authentication factor
                            2. Increase monitoring level for this session
                            3. Apply least-privilege access temporarily
                            4. Log this event for security review
                            """)
                        else:
                            st.markdown("""
                            ✓ **Standard Actions:**
                            1. Continue normal session monitoring
                            2. Apply standard Zero Trust verification at privilege escalation points
                            3. Maintain regular authentication renewal cycle
                            """)
                
    with tab2:
        st.subheader("Simulated User Analysis")
        st.markdown("This mode demonstrates the system using simulated user behavior patterns.")
        
        # Initialize or load the data and model
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("Initialize/Reset System", type="primary"):
                with st.spinner("Generating user data and training model..."):
                    # Generate simulated user data
                    # Initialize ZeroTrustSecuritySystem
                    zero_trust_system = ZeroTrustSecuritySystem()
                    
                    # Generate user data using the ZeroTrustSecuritySystem
                    normal_users, suspicious_users = zero_trust_system.generate_user_data(
                        normal_count=100, 
                        suspicious_count=10
                    )
                    
                    # Save data to session state
                    st.session_state.normal_users = normal_users
                    st.session_state.suspicious_users = suspicious_users
                    
                    # Combine data for model training
                    all_users = pd.concat([normal_users, suspicious_users])
                    X = all_users[['typing_speed', 'mouse_movement_speed']]
                    
                    # Train Isolation Forest model
                    model = IsolationForest(contamination=0.1, random_state=42)
                    model.fit(X)
                    st.session_state.model = model
                    
                    st.session_state.current_user_index = 0
                    
                    st.success("System initialized! Click 'Check Next User' to start analyzing user behavior.")

        # Display the current user and analysis results if data is loaded
        if st.session_state.normal_users is not None and st.session_state.model is not None:
            # Prepare data for current user
            all_users = pd.concat([st.session_state.normal_users, st.session_state.suspicious_users])
            current_user = all_users.iloc[st.session_state.current_user_index]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"Analyzing User #{st.session_state.current_user_index + 1}")
                
                # Initialize ZeroTrustSecuritySystem if needed
                if 'zero_trust_system' not in st.session_state:
                    st.session_state.zero_trust_system = ZeroTrustSecuritySystem()
                
                # Run analysis using ZeroTrustSecuritySystem
                results = st.session_state.zero_trust_system.check_user_behavior({
                    'typing_speed': current_user['typing_speed'],
                    'mouse_speed': current_user['mouse_movement_speed']
                })
                
                # Extract result values
                is_anomaly = results['overall_is_anomaly']
                confidence = results['overall_confidence']
                predicted_label = "Suspicious" if is_anomaly else "Normal"
                
                # Display user metrics
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    st.metric("Typing Speed", f"{current_user['typing_speed']:.2f} keystrokes/sec")
                with metrics_col2:
                    st.metric("Mouse Movement Speed", f"{current_user['mouse_movement_speed']:.2f} pixels/sec")
                
                # Display animation of typing and mouse movement (simulated)
                progress_placeholder = st.empty()
                
                if not st.session_state.get('animation_running', False):
                    st.session_state.animation_running = True
                    
                    # Simulate typing and mouse movement with progress bars
                    progress_typing = st.progress(0)
                    progress_mouse = st.progress(0)
                    
                    st.markdown("**Typing Activity:**")
                    progress_typing_placeholder = st.empty()
                    
                    st.markdown("**Mouse Movement:**")
                    progress_mouse_placeholder = st.empty()
                    
                    # Animate for 3 seconds
                    for i in range(100):
                        # Typing animation
                        typing_progress = min(100, int(i * (current_user['typing_speed'] / 7) * 100))
                        progress_typing.progress(typing_progress / 100)
                        
                        # Mouse animation
                        mouse_progress = min(100, int(i * (current_user['mouse_movement_speed'] / 700) * 100))
                        progress_mouse.progress(mouse_progress / 100)
                        
                        time.sleep(0.03)
                    
                    st.session_state.animation_running = False
                
                # Display analysis results
                st.subheader("Security Analysis")
                
                if is_anomaly:
                    st.error(f"⚠️ SECURITY ALERT: Suspicious behavior detected! (Confidence: {confidence:.2f}%)")
                    st.markdown("""
                    **Potential security threats:**
                    - Possible unauthorized user
                    - Potential automated attack
                    - Unusual user behavior pattern
                    
                    **Recommended actions:**
                    - Trigger additional authentication
                    - Temporarily restrict access
                    - Log event for further investigation
                    """)
                else:
                    st.success(f"✓ Normal user behavior confirmed (Confidence: {confidence:.2f}%)")
                
            with col2:
                # User behavior visualization
                st.subheader("Behavior Analysis")
                
                # Create scatter plot of all users with current user highlighted
                fig, ax = plt.subplots(figsize=(5, 5))
                
                # Plot normal users if data exists
                if st.session_state.normal_users is not None and not st.session_state.normal_users.empty:
                    ax.scatter(
                        st.session_state.normal_users['typing_speed'],
                        st.session_state.normal_users['mouse_movement_speed'],
                        color='blue', alpha=0.5, label='Normal Users'
                    )
                
                # Plot suspicious users if data exists
                if st.session_state.suspicious_users is not None and not st.session_state.suspicious_users.empty:
                    ax.scatter(
                        st.session_state.suspicious_users['typing_speed'],
                        st.session_state.suspicious_users['mouse_movement_speed'],
                        color='red', alpha=0.5, label='Suspicious Users'
                    )
                
                # Highlight current user
                ax.scatter(
                    current_user['typing_speed'], 
                    current_user['mouse_movement_speed'],
                    color='green', s=200, marker='*', label='Current User'
                )
                
                ax.set_xlabel('Typing Speed (keystrokes/sec)')
                ax.set_ylabel('Mouse Movement (pixels/sec)')
                ax.set_title('User Behavior Patterns')
                ax.legend()
                
                st.pyplot(fig)
                
                # Add a button to check the next user
                if st.button("Check Next User", key="check_next", on_click=increment_user):
                    pass  # The on_click handler will handle this

            # Show the overall user population statistics
            st.subheader("System Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Users Monitored", len(all_users))
            with col2:
                st.metric("Normal Users", len(st.session_state.normal_users) if st.session_state.normal_users is not None else 0)
            with col3:
                st.metric("Suspicious Users", len(st.session_state.suspicious_users) if st.session_state.suspicious_users is not None else 0)
                
            # Display data distributions
            st.subheader("User Behavior Distribution")
            dist_col1, dist_col2 = st.columns(2)
            
            with dist_col1:
                # Typing speed histogram
                fig, ax = plt.subplots()
                if st.session_state.normal_users is not None and not st.session_state.normal_users.empty:
                    ax.hist(st.session_state.normal_users['typing_speed'], alpha=0.5, bins=15, label='Normal Users')
                if st.session_state.suspicious_users is not None and not st.session_state.suspicious_users.empty:
                    ax.hist(st.session_state.suspicious_users['typing_speed'], alpha=0.5, bins=15, label='Suspicious Users')
                ax.set_xlabel('Typing Speed (keystrokes/sec)')
                ax.set_ylabel('Count')
                ax.set_title('Typing Speed Distribution')
                ax.axvline(x=current_user['typing_speed'], color='green', linestyle='--', linewidth=2)
                ax.legend()
                st.pyplot(fig)
                
            with dist_col2:
                # Mouse movement histogram
                fig, ax = plt.subplots()
                if st.session_state.normal_users is not None and not st.session_state.normal_users.empty:
                    ax.hist(st.session_state.normal_users['mouse_movement_speed'], alpha=0.5, bins=15, label='Normal Users')
                if st.session_state.suspicious_users is not None and not st.session_state.suspicious_users.empty:
                    ax.hist(st.session_state.suspicious_users['mouse_movement_speed'], alpha=0.5, bins=15, label='Suspicious Users')
                ax.set_xlabel('Mouse Movement Speed (pixels/sec)')
                ax.set_ylabel('Count')
                ax.set_title('Mouse Movement Distribution')
                ax.axvline(x=current_user['mouse_movement_speed'], color='green', linestyle='--', linewidth=2)
                ax.legend()
                st.pyplot(fig)
        
        else:
            st.info("Please initialize the system by clicking the button above.")

elif page == "AI Threat Intelligence":
    st.header("RAIN™ AI-Powered Threat Intelligence")
    
    # We're using Gemini API in the background with the key already configured
    st.markdown("""
    This component uses Google's Gemini AI to provide expert analysis of security threats
    detected by the Zero Trust system. It combines the machine learning detection results with
    AI-powered threat intelligence to deliver:
    
    1. Detailed threat assessment
    2. Threat level classification 
    3. Specific recommendations for security response
    """)
    
    # Create columns for the main components
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Real-time Typing Analysis for Threat Detection")
        
        # Capture real typing data
        text_input = biometric_collector.capture_typing_data()
        
        if len(st.session_state.typing_speeds) > 0:
            # We have some typing data, so we can analyze it
            
            # Generate comparison data (if needed)
            if st.session_state.normal_users is None or st.session_state.suspicious_users is None:
                normal_users, suspicious_users = biometric_collector.simulate_mouse_data(100, 10)
                st.session_state.normal_users = normal_users
                st.session_state.suspicious_users = suspicious_users
            
            # Get current typing speed
            current_typing_speed = st.session_state.last_typing_speed
            
            if st.button("Run AI Threat Analysis", type="primary"):
                with st.spinner("Running comprehensive AI threat assessment..."):
                    # Run comparison of algorithms
                    results = biometric_collector.compare_algorithms(
                        current_typing_speed,
                        st.session_state.normal_users,
                        st.session_state.suspicious_users
                    )
                    
                    # Get AI analysis
                    threat_analysis = ai_threat_analyzer.analyze_threat(
                        results['user_data'], 
                        {
                            'isolation_forest': results['isolation_forest'],
                            'one_class_svm': results['one_class_svm']
                        }
                    )
                    
                    if 'error' in threat_analysis:
                        st.error(f"AI analysis error: {threat_analysis['error']}")
                    else:
                        # Display threat assessment
                        st.subheader("AI Security Assessment")
                        
                        # Record the threat in the enterprise dashboard system
                        if 'threat_level' in threat_analysis:
                            enterprise_dashboard.add_threat_event(
                                threat_analysis['threat_level'],
                                f"RAIN™ AI detected {threat_analysis['threat_level'].lower()} risk behavior pattern",
                                "Biometric Analysis Engine"
                            )
                        
                        # Display threat level with appropriate styling
                        threat_level = threat_analysis['threat_level']
                        if threat_level in ["Critical", "High"]:
                            st.markdown(f"""
                            <div class="alert-box error">
                            <h3>⚠️ Threat Level: {threat_level}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        elif threat_level == "Medium":
                            st.markdown(f"""
                            <div class="alert-box warning">
                            <h3>⚠️ Threat Level: {threat_level}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="alert-box success">
                            <h3>✓ Threat Level: {threat_level}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Display the full analysis
                        st.markdown("### Expert Analysis")
                        st.markdown(threat_analysis['analysis'])
                        
                        # Display comparison chart
                        st.subheader("Behavior Analysis Visualization")
                        st.pyplot(results['plot'])
        else:
            st.info("Start typing in the box above to generate behavior patterns for analysis.")
    
    with col2:
        st.subheader("AI Security Feed")
        
        # Display threat history if available
        if st.session_state.threat_history:
            st.markdown("### Recent Threat Assessments")
            
            for i, threat in enumerate(reversed(st.session_state.threat_history[:5])):
                # Create styled threat cards
                threat_color = {
                    "Critical": "#ff1744",
                    "High": "#ff5252",
                    "Medium": "#ff9100",
                    "Low": "#ffeb3b",
                    "None": "#4caf50",
                }.get(threat['threat_level'], "#9e9e9e")
                
                st.markdown(f"""
                <div style="border-left: 5px solid {threat_color}; padding: 10px; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 5px;">
                    <div style="color: {threat_color}; font-weight: bold;">Threat Level: {threat['threat_level']}</div>
                    <div style="font-size: 0.8em; color: #666;">Timestamp: {threat['timestamp'] if isinstance(threat['timestamp'], str) else threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</div>
                    <div>User Activity: {threat.get('typing_speed', 0):.2f} k/s | {threat.get('mouse_speed', 0):.2f} px/s</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Show a button to view full threat history
            if st.button("View Full Threat Dashboard"):
                st.session_state.last_page = page
                st.rerun()  # This will rerun the app and go to Threat Dashboard
        else:
            st.info("No threat assessments yet. Run the AI Threat Analysis to build a history.")
    # We have already enabled AI threat analysis with Gemini API in the background
    # This else block shouldn't be reached, but keeping it for completeness

elif page == "User Behavior Analysis":
    st.header("RAIN™ User Behavior Analysis")
    
    with st.expander("How does the Web Surfing Security System work?", expanded=False):
        st.markdown("""
        ### Real-time Web Activity Security Monitoring
        
        This system combines multiple security layers to detect and block malicious behavior while allowing legitimate users to browse:
        
        1. **Behavioral Biometrics**: Analyzes typing patterns and mouse movements to establish a user baseline
        2. **Anomaly Detection**: Uses machine learning to identify deviations from normal browsing patterns
        3. **Zero Trust Security**: Continuously verifies user identity through their behavior, not just initial login
        4. **Real-time Blocking**: Immediately restricts access when suspicious patterns are detected
        
        The simulator below lets you experience how the system works from both perspectives:
        - As a legitimate user browsing normally
        - As an attacker attempting to compromise the system
        """)
    
    # Create tabs for different simulation modes
    tab1, tab2 = st.tabs(["Normal User Experience", "Attacker Detection"])
    
    with tab1:
        st.subheader("Normal User Web Browsing Experience")
        st.markdown("Experience how a legitimate user can browse normally while being protected by the system.")
        
        # Simulated website interface
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
            <div style="background-color: #0068C9; color: white; padding: 10px; border-radius: 5px 5px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <div>🔒 secure.banking-portal.com</div>
                <div>User: John.Smith</div>
            </div>
            <div style="padding: 15px; background-color: white; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px;">
                <h3 style="color: #333;">Welcome to SecureBank Online</h3>
                <p>Select an action below:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Accounts</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Make a Transfer</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Pay Bills</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Statements</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulated user actions
        st.markdown("### Simulate Normal User Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Account Balance", key="view_balance"):
                with st.spinner("Processing request and verifying user behavior..."):
                    # Simulate behavior verification
                    time.sleep(1)
                    
                    # Display verification steps
                    st.success("✓ User behavior verified")
                    st.markdown("""
                    **Security Checks Passed:**
                    - Typing pattern matches user profile
                    - Mouse movement consistent with previous sessions
                    - Action timing aligns with normal usage
                    - Location verification successful
                    """)
                    
                    # Show account information
                    st.markdown("""
                    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; background-color: white; margin-top: 15px;">
                        <h4 style="margin-top: 0;">Account Summary</h4>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid #ddd;">
                                <th style="text-align: left; padding: 8px;">Account</th>
                                <th style="text-align: right; padding: 8px;">Balance</th>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 8px;">Checking (****4567)</td>
                                <td style="text-align: right; padding: 8px;">$3,241.87</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px;">Savings (****7890)</td>
                                <td style="text-align: right; padding: 8px;">$12,458.63</td>
                            </tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
            
        with col2:
            if st.button("Make a Transfer", key="make_transfer"):
                with st.spinner("Processing request and verifying user behavior..."):
                    # Simulate behavior verification
                    time.sleep(1)
                    
                    # Display verification steps
                    st.success("✓ User behavior verified")
                    st.markdown("""
                    **Security Checks Passed:**
                    - Behavioral biometrics match user profile
                    - Action consistent with historical patterns
                    - Multi-factor authentication successful
                    - Transaction risk assessment: Low
                    """)
                    
                    # Show transfer form
                    st.markdown("""
                    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; background-color: white; margin-top: 15px;">
                        <h4 style="margin-top: 0;">New Transfer</h4>
                        <form>
                            <div style="margin-bottom: 10px;">
                                <label style="display: block; margin-bottom: 5px;">From Account:</label>
                                <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                                    <option>Checking (****4567) - $3,241.87</option>
                                    <option>Savings (****7890) - $12,458.63</option>
                                </select>
                            </div>
                            <div style="margin-bottom: 10px;">
                                <label style="display: block; margin-bottom: 5px;">To Account:</label>
                                <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                                    <option>Savings (****7890)</option>
                                    <option>External Account (Add New)</option>
                                </select>
                            </div>
                            <div style="margin-bottom: 10px;">
                                <label style="display: block; margin-bottom: 5px;">Amount:</label>
                                <input type="text" value="$0.00" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" />
                            </div>
                        </form>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a Streamlit button separate from HTML form to handle transaction submission properly
                    if st.button("Submit Transfer", key="submit_transfer_button"):
                        # Simulate processing the transfer
                        with st.spinner("Processing transfer..."):
                            time.sleep(1.5)
                            st.success("✅ Transfer completed successfully!")
                            # This won't redirect because it's a proper Streamlit button, not an HTML form submit
        
        # Real-time security monitoring visualization
        st.markdown("### Real-time Security Monitoring")
        
        # Create a visualization of security checks happening in real-time
        placeholder = st.empty()
        
        if st.button("Show Security Monitoring Visualization", key="show_monitoring"):
            with placeholder.container():
                # Create security monitoring visualization
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate real-time security monitoring
                for i in range(101):
                    # Update progress bar
                    progress_bar.progress(i)
                    
                    # Update status text based on progress
                    if i < 25:
                        status_text.markdown("🔍 **Analyzing typing patterns...**")
                    elif i < 50:
                        status_text.markdown("🔍 **Analyzing mouse movement patterns...**")
                    elif i < 75:
                        status_text.markdown("🔍 **Comparing with user behavioral baseline...**")
                    else:
                        status_text.markdown("🔍 **Calculating anomaly scores...**")
                    
                    # Slow down the animation
                    time.sleep(0.05)
                
                # Final security assessment
                st.success("✅ User behavior verified as legitimate")
                
                # Display security confidence scores
                st.markdown("### Security Confidence Scores")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Typing Pattern Match", 
                        value="98%", 
                        delta="3%",
                        delta_color="normal"
                    )
                
                with col2:
                    st.metric(
                        label="Mouse Pattern Match", 
                        value="95%", 
                        delta="2%",
                        delta_color="normal"
                    )
                
                with col3:
                    st.metric(
                        label="Overall Security Score", 
                        value="96%", 
                        delta="2%",
                        delta_color="normal"
                    )
    
    with tab2:
        st.subheader("Attacker Detection Simulation")
        st.markdown("Experience how the system detects and blocks malicious behavior in real-time.")
        
        # Simulated attacker interface
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
            <div style="background-color: #0068C9; color: white; padding: 10px; border-radius: 5px 5px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <div>🔒 secure.banking-portal.com</div>
                <div>User: John.Smith</div>
            </div>
            <div style="padding: 15px; background-color: white; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px;">
                <h3 style="color: #333;">Welcome to SecureBank Online</h3>
                <p>Select an action below:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Accounts</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Make a Transfer</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Pay Bills</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Statements</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Attacker simulation options
        st.markdown("### Simulate Attack Scenarios")
        
        attack_type = st.selectbox(
            "Select Attack Type",
            [
                "Automated Bot Attack",
                "Account Takeover Attempt",
                "Data Exfiltration Attempt",
                "Unusually Fast Navigation"
            ]
        )
        
        if st.button("Simulate Attack", type="primary"):
            with st.spinner("Simulating attack scenario..."):
                # Simulate detection process
                time.sleep(1.5)
                
                attack_detected = True
                
                if attack_detected:
                    # Show attack detection interface
                    st.error("⚠️ **ATTACK DETECTED: Suspicious Behavior Blocked**")
                    
                    # Show security alert details
                    st.markdown("""
                    <div style="border: 2px solid #ff5252; border-radius: 5px; padding: 15px; background-color: #ffebee; margin-top: 15px;">
                        <h4 style="margin-top: 0; color: #c62828;">Security Alert Details</h4>
                        <ul style="margin-bottom: 0;">
                            <li><strong>Alert Type:</strong> Behavioral Anomaly Detection</li>
                            <li><strong>Threat Level:</strong> Critical</li>
                            <li><strong>Trigger:</strong> Abnormal interaction patterns inconsistent with user profile</li>
                            <li><strong>Action Taken:</strong> Session blocked, additional authentication required</li>
                            <li><strong>Time:</strong> Just now</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show the user blocking screen
                    st.markdown("""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; margin-top: 20px;">
                        <div style="background-color: #c62828; color: white; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
                            <h3 style="margin: 0;">⚠️ Security Alert: Suspicious Activity Detected</h3>
                        </div>
                        <div style="padding: 15px; background-color: white; border: 1px solid #ddd; border-radius: 5px; text-align: center;">
                            <p style="font-size: 16px;">For your security, we've detected unusual activity on this account.</p>
                            <p style="font-size: 16px; margin-bottom: 20px;">Additional verification is required to continue.</p>
                            <button style="background-color: #0068C9; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px;">Verify Identity</button>
                            <p style="font-size: 14px; margin-top: 20px; color: #666;">If you believe this is an error, please contact customer support at 1-800-555-0123.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show real-time detection details
                    st.subheader("Threat Detection Details")
                    
                    # Display detection metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if attack_type == "Automated Bot Attack":
                            st.metric(
                                label="Bot Probability", 
                                value="94%", 
                                delta="92%",
                                delta_color="inverse"
                            )
                        elif attack_type == "Account Takeover Attempt":
                            st.metric(
                                label="User Match Score", 
                                value="12%", 
                                delta="-83%",
                                delta_color="inverse"
                            )
                        elif attack_type == "Data Exfiltration Attempt":
                            st.metric(
                                label="Data Access Pattern", 
                                value="Anomalous", 
                                delta="Unusual",
                                delta_color="inverse"
                            )
                        else:
                            st.metric(
                                label="Navigation Speed", 
                                value="14x Normal", 
                                delta="13x",
                                delta_color="inverse"
                            )
                    
                    with col2:
                        st.metric(
                            label="Behavioral Match", 
                            value="8%", 
                            delta="-87%",
                            delta_color="inverse"
                        )
                    
                    with col3:
                        st.metric(
                            label="Security Score", 
                            value="3%", 
                            delta="-93%",
                            delta_color="inverse"
                        )
                    
                    # Show detection algorithm results
                    st.markdown("### Algorithm Detection Results")
                    
                    if attack_type == "Automated Bot Attack":
                        detection_details = """
                        - **Isolation Forest**: Anomaly detected with 98% confidence
                        - **One-Class SVM**: Anomaly detected with 96% confidence
                        - **Typing Pattern Analysis**: Indicates automated input (perfect consistency)
                        - **Navigation Timing**: Abnormally rapid and consistent timing between actions
                        """
                    elif attack_type == "Account Takeover Attempt":
                        detection_details = """
                        - **Isolation Forest**: Anomaly detected with 92% confidence
                        - **One-Class SVM**: Anomaly detected with 88% confidence
                        - **Typing Pattern Analysis**: Completely different from account owner's pattern
                        - **Behavioral Biometrics**: Mouse movement patterns inconsistent with baseline
                        """
                    elif attack_type == "Data Exfiltration Attempt":
                        detection_details = """
                        - **Isolation Forest**: Anomaly detected with 94% confidence
                        - **One-Class SVM**: Anomaly detected with 91% confidence
                        - **Access Pattern Analysis**: Attempting to access unusual amount of records
                        - **Data Flow Analysis**: Suspicious attempt to download entire database
                        """
                    else:
                        detection_details = """
                        - **Isolation Forest**: Anomaly detected with 95% confidence
                        - **One-Class SVM**: Anomaly detected with 92% confidence
                        - **Navigation Analysis**: Extremely rapid page transitions (14x normal speed)
                        - **Session Behavior**: Non-human interaction patterns detected
                        """
                    
                    st.markdown(detection_details)
                    
                    # Automated response taken
                    st.markdown("### Automated Security Response")
                    st.markdown("""
                    **Actions Taken:**
                    - ✅ User session immediately suspended
                    - ✅ All pending transactions canceled
                    - ✅ Security alert sent to account owner
                    - ✅ Additional authentication challenge triggered
                    - ✅ Security team notified for investigation
                    - ✅ IP address added to monitoring list
                    """)

elif page == "Quantum Security Visualization":
    st.header("RAIN™ Quantum-Resistant Security")
    
    with st.expander("What is Quantum-Resistant Cryptography?", expanded=False):
        st.markdown("""
        **Quantum Computing Threat:**
        Quantum computers use quantum bits (qubits) that can represent multiple states simultaneously,
        making them exponentially more powerful than classical computers for certain computations.
        
        **Why Current Encryption Is Vulnerable:**
        Many current encryption methods (like RSA) rely on the difficulty of factoring large numbers,
        which quantum computers could solve efficiently using Shor's algorithm.
        
        **Lattice-Based Cryptography:**
        This is a quantum-resistant approach based on mathematical lattices - complex mathematical
        structures that present problems even quantum computers can't easily solve.
        
        **The Visualization Below:**
        Shows how traditional RSA encryption security drops to zero under quantum attack (red line),
        while lattice-based cryptography remains secure (green line).
        """)
    
    # Create a visually appealing animation container
    st.markdown("""
    <div class="animation-container">
        <h3 style="color: white; text-align: center; margin-bottom: 20px;">
            RSA vs. Lattice-Based Cryptography Under Quantum Attack
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Button to generate animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Enhanced Visualization", type="primary", use_container_width=True):
            with st.spinner("Creating quantum security visualization with advanced visual effects..."):
                # Create animation
                animation_data = create_quantum_animation()
                st.session_state.animation_data = animation_data
                st.session_state.animation_created = True
            
    # Display animation if it's been created
    if st.session_state.animation_created and st.session_state.animation_data:
        animation_bytes = st.session_state.animation_data
        
        # Display the animation in a centered column
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.image(animation_bytes)
            
            # Show sequential frames as a "slideshow"
            if st.button("Show Next Frame"):
                next_frame = get_next_animation_frame()
                if next_frame:
                    st.image(next_frame)
            
            # Option to download the visualization
            st.download_button(
                label="Download Visualization",
                data=animation_bytes,
                file_name="quantum_security_visualization.png",
                mime="image/png"
            )
        
        # Display explanation of the animation
        st.markdown("""
        ### Visualization Explanation
        
        The visualization illustrates the effectiveness of different encryption methods under quantum computing attacks:
        
        - **Red Line (RSA)**: Shows how traditional RSA encryption strength rapidly decreases as quantum computing power increases, eventually providing no security.
        
        - **Green Line (Lattice-based)**: Demonstrates how lattice-based cryptography maintains its security strength even as quantum computing advances.
        
        ### Key Events in the Visualization
        
        1. **At 20% Progress**: Quantum computers reach 1000 qubits, becoming powerful enough to start weakening RSA encryption.
        
        2. **At 50% Progress**: RSA-2048 encryption is completely broken, marked by a critical security breach.
        
        3. **At 75% Progress**: A global encryption crisis occurs, but systems using lattice-based cryptography remain secure.
        
        This visualization highlights why organizations need to start transitioning to quantum-resistant encryption methods now, before practical quantum computers become available.
        """)
        
        # Add an informative section on lattice-based cryptography implementation
        with st.expander("Technical Implementation of Lattice-Based Cryptography", expanded=False):
            st.markdown("""
            ### Implementing Lattice-Based Cryptography
            
            Lattice-based cryptography uses mathematical structures called lattices to create encryption that's resistant to quantum attacks. Here's a simplified overview of how it works:
            
            1. **Mathematical Foundation**: Lattices are regular arrangements of points in n-dimensional space. The security relies on the hardness of certain lattice problems, like the Shortest Vector Problem (SVP) and Learning With Errors (LWE).
            
            2. **Key Generation**:
               - Generate a random matrix A
               - Generate a short secret vector s
               - Compute b = As + e (where e is a small error term)
               - Public key is (A, b), private key is s
            
            3. **Encryption**:
               - To encrypt a message m, represent it as a binary vector
               - Generate a random vector r
               - Compute ciphertext c = (rA, rb + m⌊q/2⌋)
            
            4. **Decryption**:
               - Using private key s, compute rb - rAs = re
               - If error e is small enough, recover m
            
            Modern post-quantum cryptographic libraries implementing these techniques include:
            
            - **CRYSTALS-Kyber**: A module lattice-based key encapsulation mechanism
            - **NTRU**: One of the oldest lattice-based encryption systems
            - **Falcon**: A lattice-based signature scheme
            
            These algorithms are being standardized by NIST as part of their Post-Quantum Cryptography standardization process.
            """)

elif page == "Enterprise Security Dashboard":
    st.header("RAIN™ Enterprise Security Dashboard")
    
    # Use the enterprise dashboard class to display comprehensive security information
    enterprise_dashboard.display_enterprise_dashboard()

elif page == "Executive Presentation":
    # Display the presentation guide
    display_presentation_guide()

elif page == "Enterprise Website":
    # Import the Enterprise Website redirect module
    from ai_video_presentation import display_ai_video_presentation
    
    # Display the Enterprise Website redirect interface
    display_ai_video_presentation()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
<p>RAIN™ Enterprise Security Platform - Real-Time AI-Driven Threat Interceptor and Neutralizer</p>
<p>© 2025 • Created for Infosys</p>
</div>
""", unsafe_allow_html=True)
