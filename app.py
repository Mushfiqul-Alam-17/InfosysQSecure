import streamlit as st
from streamlit.components.v1 import html
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
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
        color: #0d47a1;
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
    ["Zero Trust Security", "User Behavior Analysis", 
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
        text_input, analyze_button = biometric_collector.capture_typing_data("_main")
        
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
                overall_verdict = results['overall_verdict']
                is_anomaly = overall_verdict.startswith("SUSPICIOUS")
                # Calculate combined confidence from both algorithms
                if_confidence = results['isolation_forest']['confidence']
                svm_confidence = results['one_class_svm']['confidence']
                confidence = (if_confidence + svm_confidence) / 2
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

# AI Threat Intelligence section completely removed from the interface
# Functionality is still available in the backend and used by other components

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
                <div>User: Mushfiqul.Alam</div>
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
        
        action_tabs = st.tabs(["View Accounts", "Make a Transfer", "Pay Bills", "View Statements"])
        
        with action_tabs[0]:  # View Accounts
            st.subheader("Account Overview")
            with st.spinner("Processing request and verifying user behavior..."):
                # Simulate behavior verification
                time.sleep(0.5)
                
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
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 8px;">Savings (****7890)</td>
                            <td style="text-align: right; padding: 8px;">$12,458.63</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">Investment (****1234)</td>
                            <td style="text-align: right; padding: 8px;">$87,652.44</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
        with action_tabs[1]:  # Make a Transfer
            st.subheader("Transfer Money")
            with st.spinner("Verifying user identity..."):
                time.sleep(0.5)
                
                # Display verification steps
                st.success("✓ Identity verified")
                st.markdown("""
                **Security Checks Passed:**
                - Behavioral biometrics match user profile
                - Action consistent with historical patterns
                - Multi-factor authentication successful
                - Transaction risk assessment: Low
                """)
                
                # Create a proper Streamlit form for transfers
                transfer_form = st.form(key="transfer_form")
                with transfer_form:
                    st.selectbox("From Account:", 
                                ["Checking (****4567) - $3,241.87", 
                                 "Savings (****7890) - $12,458.63",
                                 "Investment (****1234) - $87,652.44"])
                    
                    st.selectbox("To Account:", 
                                ["Savings (****7890)", 
                                 "Checking (****4567)",
                                 "Credit Card (****5623)",
                                 "External Account (Add New)"])
                    
                    st.text_input("Amount:", value="$0.00")
                    st.text_input("Memo (Optional):", placeholder="Enter note")
                    
                    submit_button = st.form_submit_button(label="Submit Transfer")
                
                if submit_button:
                    with st.spinner("Processing transfer..."):
                        time.sleep(1)
                        st.success("✅ Transfer completed successfully!")
                        st.markdown("""
                        **Transfer Details:**
                        - Transaction ID: TRX298753
                        - Date: March 16, 2025
                        - Time: 11:24 AM
                        - Status: Completed
                        """)
        
        with action_tabs[2]:  # Pay Bills
            st.subheader("Bill Payments")
            with st.spinner("Loading payment center..."):
                time.sleep(0.5)
                
                # Display security verification
                st.success("✓ Identity verified for bill payments")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("#### Upcoming Bills")
                    
                    bills_data = [
                        {"name": "City Electric Utility", "amount": "$142.87", "due": "March 19, 2025", "status": "Due Soon", "color": "#FFA500"},
                        {"name": "Mortgage Payment", "amount": "$1,876.50", "due": "March 28, 2025", "status": "Scheduled", "color": "#008000"},
                        {"name": "Internet Service", "amount": "$89.99", "due": "April 3, 2025", "status": "Upcoming", "color": "#0068C9"},
                        {"name": "Water Bill", "amount": "$78.32", "due": "April 5, 2025", "status": "Upcoming", "color": "#0068C9"}
                    ]
                    
                    for bill in bills_data:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: bold;">{bill['name']}</div>
                                <div style="color: #666; font-size: 14px;">Due: {bill['due']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: bold;">{bill['amount']}</div>
                                <div style="color: {bill['color']}; font-size: 14px;">{bill['status']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### Quick Pay")
                    st.selectbox("From Account:", ["Checking (****4567)"])
                    st.selectbox("Pay To:", ["City Electric Utility", "Mortgage Payment", "Internet Service", "Water Bill", "+ Add New Payee"])
                    
                    if st.button("Pay Selected Bill"):
                        with st.spinner("Processing payment..."):
                            time.sleep(1)
                            st.success("✅ Payment scheduled successfully!")
        
        with action_tabs[3]:  # View Statements
            st.subheader("Account Statements")
            with st.spinner("Retrieving statements..."):
                time.sleep(0.5)
                
                # Form for statement selection
                st.selectbox("Select Account:", ["Checking (****4567)", "Savings (****7890)", "Investment (****1234)"])
                
                # Create table for statements
                statements = [
                    {"period": "March 1 - March 31, 2025", "balance": "$3,241.87", "transactions": "24"},
                    {"period": "February 1 - February 29, 2025", "balance": "$2,856.32", "transactions": "31"},
                    {"period": "January 1 - January 31, 2025", "balance": "$3,102.54", "transactions": "28"},
                    {"period": "December 1 - December 31, 2024", "balance": "$2,785.41", "transactions": "35"}
                ]
                
                for statement in statements:
                    cols = st.columns([3, 2, 2, 1])
                    with cols[0]:
                        st.write(statement["period"])
                    with cols[1]:
                        st.write(f"Ending Balance: {statement['balance']}")
                    with cols[2]:
                        st.write(f"{statement['transactions']} transactions")
                    with cols[3]:
                        if st.button("View", key=f"view_{statement['period']}"):
                            with st.spinner("Loading statement..."):
                                time.sleep(1)
                                st.success("Statement loaded")
                                
                                st.markdown(f"""
                                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; background-color: white; margin-top: 15px;">
                                    <h4 style="margin-top: 0;">Statement for {statement['period']}</h4>
                                    <p>Checking Account (****4567)</p>
                                    <p><strong>Beginning Balance:</strong> $2,741.87</p>
                                    <p><strong>Ending Balance:</strong> {statement['balance']}</p>
                                    <p><strong>Transactions:</strong> {statement['transactions']}</p>
                                    
                                    <h5>Recent Transactions</h5>
                                    <table style="width: 100%; border-collapse: collapse;">
                                        <tr style="border-bottom: 1px solid #ddd;">
                                            <th style="text-align: left; padding: 8px;">Date</th>
                                            <th style="text-align: left; padding: 8px;">Description</th>
                                            <th style="text-align: right; padding: 8px;">Amount</th>
                                        </tr>
                                        <tr style="border-bottom: 1px solid #ddd;">
                                            <td style="padding: 8px;">Mar 15, 2025</td>
                                            <td style="padding: 8px;">DIRECT DEPOSIT - SALARY</td>
                                            <td style="text-align: right; padding: 8px; color: green;">+$2,450.00</td>
                                        </tr>
                                        <tr style="border-bottom: 1px solid #ddd;">
                                            <td style="padding: 8px;">Mar 12, 2025</td>
                                            <td style="padding: 8px;">MORTGAGE PAYMENT</td>
                                            <td style="text-align: right; padding: 8px; color: red;">-$1,876.50</td>
                                        </tr>
                                        <tr style="border-bottom: 1px solid #ddd;">
                                            <td style="padding: 8px;">Mar 10, 2025</td>
                                            <td style="padding: 8px;">GROCERY STORE</td>
                                            <td style="text-align: right; padding: 8px; color: red;">-$87.32</td>
                                        </tr>
                                    </table>
                                </div>
                                """, unsafe_allow_html=True)
        
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
                    # Create animated security score with lightning bolt effect
                    security_score = 96
                    
                    # Define the HTML without f-string for the CSS animations part
                    css_part = """
                    <style>
                        @keyframes lightning-flash {
                            0% { background: transparent; }
                            10% { background: rgba(255, 255, 255, 0.8); }
                            20% { background: transparent; }
                            30% { background: rgba(255, 255, 255, 0.6); }
                            40% { background: transparent; }
                            60% { background: rgba(255, 255, 255, 0.2); }
                            100% { background: transparent; }
                        }
                        
                        .lightning {
                            animation: lightning-flash 5s infinite;
                            clip-path: polygon(
                                50% 0%, 
                                65% 30%, 
                                100% 30%, 
                                60% 50%, 
                                75% 70%, 
                                40% 70%, 
                                40% 100%, 
                                25% 60%, 
                                0% 60%, 
                                35% 40%
                            );
                        }
                    </style>
                    """
                    
                    # Now create the HTML with the dynamic content separate from the CSS
                    security_score_html = f"""
                    <div style="background: linear-gradient(135deg, #051937, #004d7a, #008793); border-radius: 10px; padding: 15px; color: white; text-align: center; position: relative; overflow: hidden;">
                        <h3 style="margin-top: 0; margin-bottom: 5px; font-size: 18px;">Security Score</h3>
                        <div id="lightning-container" style="position: relative; height: 150px; width: 100%;">
                            <div class="lightning" style="position: absolute; top: 0; left: 40%; width: 20%; height: 100%; z-index: 10;"></div>
                            <div class="score-display" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 20;">
                                <div class="score-value" style="font-size: 48px; font-weight: bold;">{security_score}<span style="font-size: 28px;">%</span></div>
                                <div style="font-size: 16px; color: #4eff9f;">+2% from last week</div>
                            </div>
                        </div>
                        {css_part}
                    </div>
                    """
                    html(security_score_html, height=200)
    
    with tab2:
        st.subheader("Attacker Detection Simulation")
        st.markdown("Experience how the system detects and blocks malicious behavior in real-time.")
        
        # Enhanced banking portal interface
        banking_action = st.selectbox(
            "Choose Banking Action",
            ["Home", "View Accounts", "Make a Transfer", "Pay Bills", "View Statements"],
            key="banking_action"
        )
        
        # Simulate a realistic banking portal interface
        # Header section of the banking portal
        header_html = """
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
            <div style="background-color: #0068C9; color: white; padding: 12px; border-radius: 5px 5px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">🔒</div>
                    <div>secure.trust-ebanking.com</div>
                </div>
                <div>User: Mushfiqul.Alam</div>
            </div>
            <div style="padding: 15px; background-color: white; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="color: #333; margin: 0;">Welcome to TrustBank Online</h3>
                    <div style="color: #666; font-size: 14px;">Last login: Today, 10:42 AM</div>
                </div>
                
                <div style="display: flex; margin-bottom: 20px;">
                    <div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; width: 100%;">
                        <p style="margin: 0; color: #0068C9; font-weight: bold;">Good afternoon, Mushfiqul!</p>
                        <p style="margin: 5px 0 0 0; color: #555;">Your accounts are in good standing.</p>
                    </div>
                </div>
        """
        # Use the html component to render HTML properly
        html(header_html, height=220)
        
        # Display different content based on selected banking action
        if banking_action == "Home" or banking_action == "View Accounts":
            accounts_html = """
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #333;">Your Accounts</h4>
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">Primary Checking</div>
                        <div style="font-weight: bold; color: #333;">$12,857.42</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">Account #...4872</div>
                        <div style="color: #0a0; font-size: 14px;">+$1,250.00 today</div>
                    </div>
                </div>
                
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">Savings Account</div>
                        <div style="font-weight: bold; color: #333;">$34,928.10</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">Account #...2983</div>
                        <div style="color: #0a0; font-size: 14px;">+$87.66 interest this month</div>
                    </div>
                </div>
                
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">Investment Portfolio</div>
                        <div style="font-weight: bold; color: #333;">$128,530.76</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">14 holdings</div>
                        <div style="color: #0a0; font-size: 14px;">+2.4% this week</div>
                    </div>
                </div>
            </div>
            """
            html(accounts_html, height=300)
            
        elif banking_action == "Make a Transfer":
            transfer_html = """
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 15px 0; color: #333;">Make a Transfer</h4>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">From Account</label>
                    <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option>Primary Checking (...4872) - $12,857.42</option>
                        <option>Savings Account (...2983) - $34,928.10</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">To Account</label>
                    <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option>Savings Account (...2983) - $34,928.10</option>
                        <option>Primary Checking (...4872) - $12,857.42</option>
                        <option>Credit Card Payment (...5623)</option>
                        <option>External Account/Recipient</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Amount</label>
                    <input type="text" placeholder="$0.00" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">When</label>
                    <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option>Today</option>
                        <option>Tomorrow</option>
                        <option>Choose Date</option>
                        <option>Set up recurring transfer</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Memo (Optional)</label>
                    <input type="text" placeholder="Add a note" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
            </div>
            """
            html(transfer_html, height=350)
            
        elif banking_action == "Pay Bills":
            bills_html = """
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 15px 0; color: #333;">Pay Bills</h4>
                
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px; margin-bottom: 15px; background-color: #fff8e1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">City Electric Utility</div>
                        <div style="font-weight: bold; color: #1976D2;">$142.87</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">Due in 3 days</div>
                        <button style="background-color: #0068C9; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 14px;">Pay Now</button>
                    </div>
                </div>
                
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px; margin-bottom: 15px; background-color: #fff;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">Mortgage Payment</div>
                        <div style="font-weight: bold; color: #333;">$1,876.50</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">Due in 12 days</div>
                        <button style="background-color: #0068C9; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 14px;">Pay Now</button>
                    </div>
                </div>
                
                <div style="border: 1px solid #eee; border-radius: 5px; padding: 12px; margin-bottom: 15px; background-color: #fff;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="font-weight: bold; color: #333;">Internet Service</div>
                        <div style="font-weight: bold; color: #333;">$89.99</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="color: #666; font-size: 14px;">Due in 18 days</div>
                        <button style="background-color: #0068C9; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 14px;">Pay Now</button>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; margin-right: 10px;">Add New Payee</button>
                    <button style="background-color: white; color: #0068C9; border: 1px solid #0068C9; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 14px;">View Payment History</button>
                </div>
            </div>
            """
            html(bills_html, height=350)
            
        elif banking_action == "View Statements":
            statements_html = """
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 15px 0; color: #333;">Account Statements</h4>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Select Account</label>
                    <select style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 15px;">
                        <option>Primary Checking (...4872)</option>
                        <option>Savings Account (...2983)</option>
                        <option>Credit Card (...5623)</option>
                    </select>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
                    <thead>
                        <tr style="background-color: #f5f5f5; border-bottom: 2px solid #ddd;">
                            <th style="padding: 10px; text-align: left;">Statement Period</th>
                            <th style="padding: 10px; text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px;">March 1 - March 31, 2025</td>
                            <td style="padding: 10px; text-align: right;">
                                <a href="#" style="color: #0068C9; text-decoration: none; margin-right: 10px;">View</a>
                                <a href="#" style="color: #0068C9; text-decoration: none;">Download</a>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px;">February 1 - February 29, 2025</td>
                            <td style="padding: 10px; text-align: right;">
                                <a href="#" style="color: #0068C9; text-decoration: none; margin-right: 10px;">View</a>
                                <a href="#" style="color: #0068C9; text-decoration: none;">Download</a>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px;">January 1 - January 31, 2025</td>
                            <td style="padding: 10px; text-align: right;">
                                <a href="#" style="color: #0068C9; text-decoration: none; margin-right: 10px;">View</a>
                                <a href="#" style="color: #0068C9; text-decoration: none;">Download</a>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px;">December 1 - December 31, 2024</td>
                            <td style="padding: 10px; text-align: right;">
                                <a href="#" style="color: #0068C9; text-decoration: none; margin-right: 10px;">View</a>
                                <a href="#" style="color: #0068C9; text-decoration: none;">Download</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
                
                <div style="margin-top: 15px;">
                    <button style="background-color: white; color: #0068C9; border: 1px solid #0068C9; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 14px;">Request Paper Statement</button>
                </div>
            </div>
            """
            html(statements_html, height=400)
            
        # Footer buttons for the banking interface
        footer_html = """
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px;">
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Accounts</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Make a Transfer</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Pay Bills</button>
                    <button style="background-color: #0068C9; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Statements</button>
                    <button style="background-color: #2196F3; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; margin-left: auto;">Logout</button>
                </div>
            </div>
        </div>
        """
        html(footer_html, height=80)
        
        # Real attack demonstration
        st.markdown("### Real Attack Demonstration & Defense")
        
        # Create a more detailed attack selection with realistic descriptions
        attack_col1, attack_col2 = st.columns([1, 2])
        
        with attack_col1:
            attack_type = st.radio(
                "Attack Vector",
                [
                    "Credential Stuffing",
                    "Man-in-the-Browser",
                    "Keystroke Timing Attack",
                    "Advanced Persistent Threat"
                ]
            )
        
        with attack_col2:
            if attack_type == "Credential Stuffing":
                st.info("""
                **Attack Technique:** Attackers use stolen username/password combinations from data breaches to attempt access.
                
                **How it works:**
                1. Attacker obtains breached credentials from dark web
                2. Uses automated tools to try thousands of credentials rapidly
                3. Exploits password reuse across multiple sites
                
                **Why it's dangerous:** Around 65% of people reuse passwords across multiple sites.
                """)
            elif attack_type == "Man-in-the-Browser":
                st.info("""
                **Attack Technique:** Malware operates within the browser to modify web pages and transactions in real-time.
                
                **How it works:**
                1. Browser extension or malware infects user's system
                2. Malware activates when banking websites are visited
                3. Silently changes transaction details while showing user the expected information
                
                **Why it's dangerous:** Users see legitimate transaction details while different actions execute.
                """)
            elif attack_type == "Keystroke Timing Attack":
                st.info("""
                **Attack Technique:** Advanced attackers analyze timing patterns between keystrokes to identify imposters.
                
                **How it works:**
                1. Attackers record normal typing rhythm of legitimate users
                2. When attempting unauthorized access, they mimic typing patterns
                3. Statistical algorithms generate timing similar to legitimate users
                
                **Why it's dangerous:** Can bypass traditional behavioral monitoring systems.
                """)
            else:  # Advanced Persistent Threat
                st.info("""
                **Attack Technique:** Sophisticated attackers gain access and remain undetected for long periods.
                
                **How it works:**
                1. Initial compromise through targeted spear-phishing
                2. Establish persistent access with customized backdoors
                3. Slowly escalate privileges while avoiding detection
                4. Launch devastating attacks after mapping network
                
                **Why it's dangerous:** Average detection time is 280 days, allowing extensive data theft.
                """)
        
        # Attack execution interface
        st.markdown("### Live Attack Execution & Defense")
        
        attack_stages = [
            "Reconnaissance & Planning",
            "Initial Access Attempt",
            "Evasion Techniques Deployment",
            "Behavior Pattern Manipulation",
            "Data/Transaction Targeting"
        ]
        
        selected_stage = st.select_slider(
            "Attack Progress Stage:",
            options=attack_stages
        )
        
        # Stage indicator
        stage_index = attack_stages.index(selected_stage)
        progress_bar = st.progress((stage_index + 1) / len(attack_stages))
        
        # Execute attack button
        if st.button("Execute Attack & Observe Defense", type="primary"):
            with st.spinner(f"Executing {attack_type} attack at stage: {selected_stage}..."):
                # Real attack process simulation with actual timeline
                for i in range(10):
                    time.sleep(0.2)  # Speed up the demonstration
                
                # Attack is detected at different points based on the type and stage
                early_detection = stage_index < 2  # Detected early in the attack chain
                
                if early_detection:
                    detection_phase = "Pre-execution Prevention"
                    detection_message = "Attack prevented before execution!"
                else:
                    detection_phase = "Runtime Detection & Mitigation"
                    detection_message = "Attack detected during execution and mitigated!"
                
                # Show attack detection interface with realistic details
                st.error(f"⚠️ **ATTACK DETECTED: {attack_type} {detection_message}**")
                
                # Create detailed security alert with actual attack TTP (Tactics, Techniques, Procedures)
                st.markdown(f"""
                <div style="border: 2px solid #2196F3; border-radius: 5px; padding: 15px; background-color: #e3f2fd; margin-top: 15px;">
                    <h4 style="margin-top: 0; color: #0d47a1;">Real-Time Security Alert</h4>
                    <ul style="margin-bottom: 0;">
                        <li><strong>Detection Phase:</strong> {detection_phase}</li>
                        <li><strong>Attack Type:</strong> {attack_type}</li>
                        <li><strong>Threat Level:</strong> Critical</li>
                        <li><strong>Detection Method:</strong> RAIN™ Multi-layered Behavioral Analysis</li>
                        <li><strong>Response:</strong> Automated threat containment activated</li>
                        <li><strong>Time to Detection:</strong> {(2.3 if early_detection else 4.7):.1f} seconds</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Show the user blocking screen
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9; margin-top: 20px;">
                    <div style="background-color: #0d47a1; color: white; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
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
                
                # Display attack-specific detection metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if attack_type == "Credential Stuffing":
                        st.metric(
                            label="Login Attempt Rate", 
                            value="237/min", 
                            delta="235",
                            delta_color="inverse"
                        )
                    elif attack_type == "Man-in-the-Browser":
                        st.metric(
                            label="DOM Manipulation", 
                            value="Detected", 
                            delta="Critical",
                            delta_color="inverse"
                        )
                    elif attack_type == "Keystroke Timing Attack":
                        st.metric(
                            label="Timing Variance", 
                            value="2.3%", 
                            delta="-93.7%",
                            delta_color="inverse"
                        )
                    else:  # Advanced Persistent Threat
                        st.metric(
                            label="Lateral Movement", 
                            value="Detected", 
                            delta="7 systems",
                            delta_color="inverse"
                        )
                    
                with col2:
                    if attack_type == "Credential Stuffing":
                        st.metric(
                            label="IP Reputation", 
                            value="Malicious", 
                            delta="Known Bot",
                            delta_color="inverse"
                        )
                    elif attack_type == "Man-in-the-Browser":
                        st.metric(
                            label="Script Injection", 
                            value="17 events", 
                            delta="Critical",
                            delta_color="inverse"
                        )
                    elif attack_type == "Keystroke Timing Attack":
                        st.metric(
                            label="Rhythm Pattern", 
                            value="Synthetic", 
                            delta="AI Generated",
                            delta_color="inverse"
                        )
                    else:  # Advanced Persistent Threat
                        st.metric(
                            label="Privilege Escalation", 
                            value="Attempted", 
                            delta="3 attempts",
                            delta_color="inverse"
                        )
                    
                with col3:
                    if attack_type == "Credential Stuffing":
                        st.metric(
                            label="Success Probability", 
                            value="0%", 
                            delta="Blocked",
                            delta_color="normal"
                        )
                    elif attack_type == "Man-in-the-Browser":
                        st.metric(
                            label="Transaction Safety", 
                            value="Protected", 
                            delta="Secured",
                            delta_color="normal"
                        )
                    elif attack_type == "Keystroke Timing Attack":
                        st.metric(
                            label="Authentication", 
                            value="Challenged", 
                            delta="MFA Required",
                            delta_color="normal"
                        )
                    else:  # Advanced Persistent Threat
                        st.metric(
                            label="Containment", 
                            value="Active", 
                            delta="Isolated",
                            delta_color="normal"
                        )
                    
                # Show detailed attack detection information
                st.markdown("### Real-Time Detection Analysis")
                
                if attack_type == "Credential Stuffing":
                    detection_details = """
                    - **RAIN AI Detection**: Attack identified as automated credential stuffing with 99.2% confidence
                    - **Pattern Recognition**: 237 login attempts per minute from distributed IP addresses
                    - **Behavioral Analysis**: Uniform timing between attempts (bot signature)
                    - **Attack Source**: Botnet utilizing 172 different IP addresses across 14 countries
                    - **Bypassed Controls**: IP rate limiting, standard geographical blocks
                    - **Target Goal**: Account compromise through brute force of stolen credentials
                    """
                elif attack_type == "Man-in-the-Browser":
                    detection_details = """
                    - **RAIN AI Detection**: JavaScript injection and DOM manipulation detected with 97.5% confidence
                    - **Malicious Scripts**: 17 unauthorized DOM modifications identified targeting form fields
                    - **Attack Technique**: Browser extension with form field interception API access
                    - **Evasion Method**: Uses legitimate looking extension with obfuscated malicious code
                    - **Transaction Impact**: Attempted to modify transfer amount from $500 to $5,000
                    - **Goal**: Financial fraud through transaction modification
                    """
                elif attack_type == "Keystroke Timing Attack":
                    detection_details = """
                    - **RAIN AI Detection**: Synthetic keystroke pattern identified with 98.7% confidence
                    - **Pattern Analysis**: Typing rhythm patterns show unnatural consistency (2.3% variance vs normal 35-45%)
                    - **Attack Technique**: AI-generated keystroke sequences mimicking legitimate user patterns
                    - **Evasion Method**: Uses ML-based user behavior simulation to avoid traditional pattern detection
                    - **User Impact**: Attempted account access with synthetic biometrics profile
                    - **Sophistication Level**: Advanced - evidence of Neural Network character prediction
                    """
                else:  # Advanced Persistent Threat
                    detection_details = """
                    - **RAIN AI Detection**: Lateral movement and privilege escalation patterns identified with 96.4% confidence
                    - **Dwell Time**: Attack signature indicates presence in network for approximately 34 days
                    - **Attack Progress**: Compromised 7 systems with 3 privilege escalation attempts
                    - **Evasion Methods**: Timestomping, log clearing, fileless malware components
                    - **Data Access Patterns**: Unusual file access in customer records database with evidence of exfiltration staging
                    - **Attribution Indicators**: Attack patterns consistent with financially motivated nation-state group
                    """
                
                st.markdown(detection_details, unsafe_allow_html=True)
                
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
