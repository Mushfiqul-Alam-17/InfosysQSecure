import streamlit as st
import time

def display_ai_video_presentation():
    """Display a simple website redirect interface for RAIN Enterprise Security"""
    
    # Simple title and description
    st.title("RAIN™ Enterprise Security Platform")
    st.subheader("Real-Time AI-Driven Threat Interceptor and Neutralizer")
    
    st.markdown("---")
    
    # Center-aligned content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <p style="font-size: 18px; margin-bottom: 30px;">
                Access the complete RAIN™ Enterprise Security Platform website to learn more about our quantum-resistant security solutions.
            </p>
            
            <p>Click the button below to visit the official website:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Large, prominent button to redirect to the website
        if st.button("🌐 Visit RAIN™ Enterprise Website", type="primary", use_container_width=True):
            # Create a redirect using JavaScript
            website_url = "https://q-secure-infosys.vercel.app/"
            st.markdown(f"""
            <meta http-equiv="refresh" content="0;URL='{website_url}'" />
            <script>window.location.href = "{website_url}";</script>
            """, unsafe_allow_html=True)
            
            # Show a message for browsers that don't automatically redirect
            st.success(f"Redirecting to {website_url}...")
            st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                If you are not automatically redirected, please click 
                <a href="{website_url}" target="_blank">here</a> to visit the website.
            </div>
            """, unsafe_allow_html=True)
    
    # Simple footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 14px;">
        <p>© 2025 RAIN Enterprise Security. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)