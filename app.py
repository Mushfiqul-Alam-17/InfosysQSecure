import streamlit as st
from ai_video_presentation import display_ai_video_presentation

# Set page configuration
st.set_page_config(
    page_title="RAIN™ Enterprise Security Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
</style>
""", unsafe_allow_html=True)

# Display the Enterprise Website redirect interface
display_ai_video_presentation()