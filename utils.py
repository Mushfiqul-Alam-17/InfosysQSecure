import streamlit as st

def load_logo():
    """
    Loads and displays a logo for the application.
    Since we can't generate image files, we'll create a text-based logo.
    """
    # Create a stylized text logo
    st.markdown("""
    <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #0068C9; letter-spacing: 2px;">🔒 Q-SECURE</h1>
        <p style="color: #555555; font-style: italic;">Quantum-Resistant Zero Trust Security</p>
    </div>
    """, unsafe_allow_html=True)

def display_security_metrics(detection_rate, false_positive_rate, response_time):
    """
    Display security metrics in a visually appealing way.
    
    Parameters:
    -----------
    detection_rate: float
        Rate of successful threat detection (0-100%)
    false_positive_rate: float
        Rate of false positive alerts (0-100%)
    response_time: float
        Average time to respond to threats (milliseconds)
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Threat Detection Rate",
            value=f"{detection_rate:.1f}%",
            delta="1.2%" if detection_rate > 95 else "-0.8%"
        )
        
    with col2:
        # For false positives, lower is better, so we invert the delta
        st.metric(
            label="False Positive Rate",
            value=f"{false_positive_rate:.1f}%",
            delta="-0.5%" if false_positive_rate < 5 else "0.7%",
            delta_color="inverse"  # Green when going down
        )
        
    with col3:
        st.metric(
            label="Response Time",
            value=f"{response_time:.0f}ms",
            delta="-15ms" if response_time < 100 else "10ms",
            delta_color="inverse"  # Green when going down
        )
