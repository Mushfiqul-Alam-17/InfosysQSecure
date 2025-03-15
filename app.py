import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import time
from zero_trust import generate_user_data, check_user_behavior
from quantum_visualization import create_quantum_animation
from presentation_guide import display_presentation_guide
from utils import load_logo

# Set page configuration
st.set_page_config(
    page_title="Quantum-Resistant Zero Trust AI Security System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def increment_user():
    """Function to increment the current user index when the button is clicked"""
    # Increment the user index and wrap around if needed
    st.session_state.current_user_index = (st.session_state.current_user_index + 1) % (len(st.session_state.normal_users) + len(st.session_state.suspicious_users))
    st.rerun()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a component:",
    ["Zero Trust Security Prototype", "Quantum Security Animation", "Presentation Guide"]
)

# Display logo (using a placeholder since we can't generate image files)
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
        2. Anomaly detection using machine learning
        3. Real-time security alerts when suspicious activity is detected
        
        **How it works:**
        - We simulate 100 "normal" users with typical behavior patterns
        - We simulate 10 "suspicious" users with abnormal behavior patterns
        - The system uses Isolation Forest algorithm to detect anomalies
        - When you click "Check Next User", the system will analyze a random user and show if they're suspicious
        """)
    
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
    
    # Animation section
    st.subheader("RSA vs. Lattice-Based Cryptography Under Quantum Attack")
    
    # Button to generate animation
    if st.button("Generate Animation", type="primary"):
        with st.spinner("Creating quantum security animation..."):
            # Create animation
            animation_data = create_quantum_animation()
            st.session_state.animation_data = animation_data
            st.session_state.animation_created = True
            
    # Display animation if it's been created
    if st.session_state.animation_created and st.session_state.animation_data:
        animation_bytes = st.session_state.animation_data
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
        **Animation Explanation:**
        
        The animation illustrates the effectiveness of different encryption methods under quantum computing attacks:
        
        - **Red Line (RSA)**: Shows how traditional RSA encryption strength rapidly decreases as quantum computing power increases, eventually providing no security.
        
        - **Green Line (Lattice-based)**: Demonstrates how lattice-based cryptography maintains its security strength even as quantum computing advances.
        
        This visualization highlights why organizations need to start transitioning to quantum-resistant encryption methods now, before practical quantum computers become available.
        """)

elif page == "Presentation Guide":
    # Display the presentation guide
    display_presentation_guide()

# Footer
st.markdown("---")
st.markdown("Quantum-Resistant Zero Trust AI Security System - Created for Infosys")
