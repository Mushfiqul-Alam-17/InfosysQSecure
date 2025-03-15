import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import time
import openai
from datetime import datetime

from zero_trust import generate_user_data, check_user_behavior
from quantum_visualization import create_quantum_animation
from presentation_guide import display_presentation_guide
from utils import load_logo
from biometric_collector import BiometricCollector
from ai_threat_analyzer import AIThreatAnalyzer

# Set page configuration
st.set_page_config(
    page_title="Quantum-Resistant Zero Trust AI Security System",
    page_icon="🔒",
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
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a component:",
    ["Zero Trust Security Prototype", "AI Threat Analysis", "Quantum Security Animation", "Threat Intelligence Dashboard", "Presentation Guide"]
)

# API Key Configuration in sidebar
with st.sidebar.expander("AI Integration Settings", expanded=False):
    if st.button("Configure OpenAI API Key"):
        toggle_api_key_input()
    
    if st.session_state.show_api_key_input:
        api_key = st.text_input("Enter OpenAI API Key", 
                               type="password", 
                               help="This is required for AI threat analysis. Your API key is stored only in this session.")
        if api_key:
            ai_threat_analyzer.set_api_key(api_key)
            st.success("API key configured successfully!")

# Display logo
load_logo()
st.title("Quantum-Resistant Zero Trust AI Security System")

if page == "Zero Trust Security Prototype":
    st.header("Zero Trust Security Prototype")
    
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
        st.subheader("Real-time Biometric Analysis")
        st.markdown("This mode analyzes your actual typing behavior in real-time to detect potential security threats.")
        
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
            
            # Compare with anomaly detection algorithms
            if st.button("Analyze My Behavior", type="primary"):
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
                        else:
                            st.info("Configure an OpenAI API key in the sidebar to enable AI threat analysis.")
                    
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
                    normal_users, suspicious_users = generate_user_data(
                        normal_count=100, 
                        suspicious_count=10,
                        normal_typing_speed_mean=5.0,
                        normal_mouse_speed_mean=300.0,
                        suspicious_typing_speed_mean=2.0,
                        suspicious_mouse_speed_mean=600.0
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
                
                # Run analysis
                is_anomaly, confidence, predicted_label = check_user_behavior(
                    current_user, 
                    st.session_state.model
                )
                
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
                
                # Plot normal users
                ax.scatter(
                    st.session_state.normal_users['typing_speed'],
                    st.session_state.normal_users['mouse_movement_speed'],
                    color='blue', alpha=0.5, label='Normal Users'
                )
                
                # Plot suspicious users
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
                st.metric("Normal Users", len(st.session_state.normal_users))
            with col3:
                st.metric("Suspicious Users", len(st.session_state.suspicious_users))
                
            # Display data distributions
            st.subheader("User Behavior Distribution")
            dist_col1, dist_col2 = st.columns(2)
            
            with dist_col1:
                # Typing speed histogram
                fig, ax = plt.subplots()
                ax.hist(st.session_state.normal_users['typing_speed'], alpha=0.5, bins=15, label='Normal Users')
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
                ax.hist(st.session_state.normal_users['mouse_movement_speed'], alpha=0.5, bins=15, label='Normal Users')
                ax.hist(st.session_state.suspicious_users['mouse_movement_speed'], alpha=0.5, bins=15, label='Suspicious Users')
                ax.set_xlabel('Mouse Movement Speed (pixels/sec)')
                ax.set_ylabel('Count')
                ax.set_title('Mouse Movement Distribution')
                ax.axvline(x=current_user['mouse_movement_speed'], color='green', linestyle='--', linewidth=2)
                ax.legend()
                st.pyplot(fig)
        
        else:
            st.info("Please initialize the system by clicking the button above.")

elif page == "AI Threat Analysis":
    st.header("AI-Powered Threat Analysis")
    
    if ai_threat_analyzer.has_api_key():
        st.markdown("""
        This component uses OpenAI's language models to provide expert analysis of security threats
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
                        <div style="font-size: 0.8em; color: #666;">Timestamp: {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</div>
                        <div>Typing: {threat['typing_speed']:.2f} k/s | Mouse: {threat['mouse_speed']:.2f} px/s</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show a button to view full threat history
                if st.button("View Full Threat Dashboard"):
                    st.session_state.last_page = page
                    st.rerun()  # This will rerun the app and go to Threat Dashboard
            else:
                st.info("No threat assessments yet. Run the AI Threat Analysis to build a history.")
    else:
        st.warning("OpenAI API key is required for AI Threat Analysis. Please configure it in the sidebar.")
        
        st.markdown("""
        ### Why AI Threat Analysis?
        
        The AI component enhances the Zero Trust system by:
        
        1. **Providing expert context** to machine learning anomaly detection
        2. **Explaining the security implications** of unusual behavior patterns
        3. **Recommending specific security responses** based on threat assessment
        4. **Creating an audit trail** of security events and decisions
        
        To enable this feature, provide your OpenAI API key in the sidebar settings.
        """)

elif page == "Quantum Security Animation":
    st.header("Quantum Security Animation")
    
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
        
        **The Animation Below:**
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
        if st.button("Generate Enhanced Animation", type="primary", use_container_width=True):
            with st.spinner("Creating quantum security animation with advanced visual effects..."):
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
            st.video(animation_bytes)
            
            # Option to download the animation
            st.download_button(
                label="Download Animation",
                data=animation_bytes,
                file_name="quantum_security_animation.mp4",
                mime="video/mp4"
            )
        
        # Display explanation of the animation
        st.markdown("""
        ### Animation Explanation
        
        The visualization illustrates the effectiveness of different encryption methods under quantum computing attacks:
        
        - **Red Line (RSA)**: Shows how traditional RSA encryption strength rapidly decreases as quantum computing power increases, eventually providing no security.
        
        - **Green Line (Lattice-based)**: Demonstrates how lattice-based cryptography maintains its security strength even as quantum computing advances.
        
        ### Key Events in the Animation
        
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

elif page == "Threat Intelligence Dashboard":
    st.header("Threat Intelligence Dashboard")
    
    # Check if there's any threat history data
    if hasattr(st.session_state, 'threat_history') and st.session_state.threat_history:
        # Display the threat dashboard
        ai_threat_analyzer.show_threat_dashboard()
        
        # Add quantum computing threat timeline
        st.subheader("Quantum Computing Threat Timeline")
        
        # Create a visually appealing timeline
        years = np.array([2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        qubits = np.array([127, 300, 650, 1200, 2000, 3000, 4500, 7000])
        
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1f1f2e')
        ax.set_facecolor('#1f1f2e')
        
        # Plot the timeline with glowing effect
        ax.plot(years, qubits, '-', color='#69f0ae', linewidth=3, marker='o', markersize=10)
        
        # Add glow effect
        for width, alpha in [(5, 0.1), (8, 0.05), (11, 0.02)]:
            ax.plot(years, qubits, '-', color='#69f0ae', linewidth=width, alpha=alpha)
        
        # Add critical threshold line
        ax.axhline(y=4000, color='#ff5252', linestyle='--', linewidth=2, label='Critical Threshold (4000+ qubits)')
        ax.fill_between(years, 4000, 8000, alpha=0.2, color='#ff5252')
        
        # Add current state marker
        ax.scatter(2023, 127, color='white', s=150, zorder=5, marker='o', edgecolors='#69f0ae', linewidth=2)
        ax.annotate("Current State: 127 qubits (IBM)", 
                    xy=(2023, 127), xytext=(2023.2, 300),
                    color='white', fontweight='bold',
                    arrowprops=dict(arrowstyle="->", color='white'))
        
        # Add years to breakthrough
        breakthrough_year = 2028  # When qubits exceed 4000
        ax.annotate("Estimated RSA-2048 Breakdown: 2028", 
                    xy=(breakthrough_year, 4000), xytext=(breakthrough_year-1, 5000),
                    color='#ff5252', fontweight='bold', fontsize=12,
                    arrowprops=dict(arrowstyle="->", color='#ff5252'))
        
        # Style the chart
        ax.set_xlabel('Year', color='white', fontsize=12)
        ax.set_ylabel('Estimated Qubits', color='white', fontsize=12)
        ax.set_title('Quantum Computing Progress Timeline', color='white', fontsize=16, fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='gray')
        
        # Add explanatory text
        ax.text(2024, 6500, 'DANGER ZONE: RSA encryption vulnerable', 
                color='#ff5252', fontsize=12, fontweight='bold')
        ax.text(2024, 2000, 'SAFE ZONE: With quantum-resistant cryptography', 
                color='#69f0ae', fontsize=12, fontweight='bold')
        
        st.pyplot(fig)
        
        # Add global cyber threat statistics
        st.subheader("Global Cyber Threat Statistics")
        
        # Create realistic threat statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Global Cyber Attacks", 
                "11.6M per day", 
                "+8.3%",
                help="Average number of daily cyber attacks globally"
            )
        
        with col2:
            st.metric(
                "Quantum-Ready Organizations", 
                "8.4%", 
                "+2.1%",
                help="Percentage of organizations prepared for quantum computing threats"
            )
        
        with col3:
            st.metric(
                "Average Attack Cost", 
                "$4.35M", 
                "+12.7%",
                help="Average cost of a data breach in 2023"
            )
        
        # Add a section on organization readiness
        st.subheader("Quantum Security Readiness Assessment")
        
        # Create a gauge chart showing readiness levels
        readiness_categories = ['Financial Services', 'Healthcare', 'Government', 
                                'Technology', 'Manufacturing', 'Retail']
        readiness_values = [42, 23, 38, 67, 18, 12]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(readiness_categories, readiness_values, 
                       color=['#69f0ae' if x > 50 else '#ff9e80' if x > 30 else '#ff5252' for x in readiness_values])
        
        # Add percentage labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{readiness_values[i]}%', 
                    va='center', fontweight='bold')
        
        ax.set_xlim(0, 100)
        ax.set_xlabel('Readiness Level (%)')
        ax.set_title('Quantum Security Readiness by Industry')
        ax.grid(axis='x', alpha=0.3)
        
        st.pyplot(fig)
        
    else:
        st.info("No threat data available yet. Run the AI Threat Analysis to build threat intelligence data.")
        
        # Display placeholder content
        st.subheader("Sample Threat Intelligence Dashboard")
        st.markdown("""
        The Threat Intelligence Dashboard will display:
        
        1. History of detected security threats
        2. Distribution of threat severity levels
        3. Timeline of security events
        4. Quantum computing progress timeline
        5. Global cyber threat statistics
        6. Organization readiness assessments
        
        Start using the AI Threat Analysis feature to populate this dashboard with real data.
        """)

elif page == "Presentation Guide":
    # Display the presentation guide
    display_presentation_guide()

# Footer
st.markdown("---")
st.markdown("Quantum-Resistant Zero Trust AI Security System - Created for Infosys")
