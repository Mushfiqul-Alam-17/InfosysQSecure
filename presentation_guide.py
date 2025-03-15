import streamlit as st

def display_presentation_guide():
    """Display the presentation guide for creating slides and pitch deck"""
    
    st.header("Presentation Guide")
    
    st.markdown("""
    This guide will help you create an impressive presentation for Infosys, including:
    
    1. Quantum Security Concept visualizations
    2. A 7-slide pitch deck structure
    """)
    
    # Quantum Security Concept Slides
    st.subheader("Quantum Security Concept Slides")
    
    st.markdown("""
    Create these two slides in PowerPoint or Canva to complement your technical demo:
    """)
    
    # First slide
    with st.expander("Slide 1: Quantum Threat to Encryption", expanded=True):
        st.markdown("""
        ### Title: "The Quantum Threat to Modern Encryption"
        
        **Visual Elements:**
        1. Create a graph with:
           - X-axis labeled "Time/Quantum Computing Power"
           - Y-axis labeled "Encryption Security Level (%)"
           - Red line showing RSA security dropping from 100% to 0%
           - Green line showing lattice-based cryptography staying at 100%
           
        **Text Elements:**
        - Brief bullet points explaining:
          - "RSA encryption relies on mathematical problems quantum computers can solve"
          - "Quantum computers with 4000+ qubits could break RSA-2048 in hours"
          - "Lattice-based cryptography relies on problems resistant to quantum attacks"
          
        **Design Tips:**
        - Use contrasting colors for the lines (red vs. green)
        - Add a vertical line labeled "Quantum Supremacy Point" where RSA drops below 50%
        - Include small icons of padlocks (breaking for RSA, secure for lattice)
        """)
        
        # Example visualization (simplified)
        st.markdown("**Example Visualization (simplified):**")
        
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create a visual example for the slide
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(0, 10, 100)
        
        # RSA dropping curve
        y_rsa = 100 * np.exp(-0.4*x)
        
        # Lattice-based flat line at 100%
        y_lattice = np.ones_like(x) * 100
        
        # Plot
        ax.plot(x, y_rsa, 'r-', linewidth=3, label='RSA Encryption')
        ax.plot(x, y_lattice, 'g-', linewidth=3, label='Lattice-based Encryption')
        
        # Add a vertical line for quantum supremacy
        ax.axvline(x=1.7, color='purple', linestyle='--', label='Quantum Supremacy Point')
        
        # Labels and title
        ax.set_xlabel('Time / Quantum Computing Power')
        ax.set_ylabel('Encryption Security Level (%)')
        ax.set_title('The Quantum Threat to Modern Encryption')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
    
    # Second slide
    with st.expander("Slide 2: Quantum Threat Intelligence Dashboard", expanded=True):
        st.markdown("""
        ### Title: "Quantum Threat Intelligence Dashboard"
        
        **Visual Elements:**
        1. Create a dashboard layout with:
           - Timeline showing "Quantum Computing Progress" from 2023 to 2030
           - Indicator showing current approximate qubits (127 as of 2023)
           - Danger zone marked at 4000+ qubits (estimated to break RSA-2048)
           - World map showing countries investing in quantum research
           
        **Text Elements:**
        - "Current Quantum Computing State: 127 qubits (IBM)"
        - "Critical Threshold: 4000+ qubits (estimated)"
        - "Time to Critical Threshold: ~5-10 years"
        - "Organizations at Risk: All using traditional cryptography"
        
        **Design Tips:**
        - Use a gauge/meter visual for the qubit count
        - Add a "threat level" indicator (yellow/orange currently, red at 4000+)
        - Use countdown timer design element showing "Time to Quantum Risk"
        """)
        
        # Example visualization (simplified)
        st.markdown("**Example Visualization (simplified dashboard):**")
        
        # Create a visual example for the dashboard slide
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Timeline from 2023 to 2030
        years = np.array([2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        qubits = np.array([127, 300, 650, 1200, 2000, 3000, 4500, 7000])
        
        # Plot qubit growth
        ax.plot(years, qubits, 'bo-', linewidth=2)
        
        # Add critical threshold line
        ax.axhline(y=4000, color='r', linestyle='--', label='Critical Threshold (4000 qubits)')
        ax.fill_between(years, 4000, 8000, alpha=0.2, color='red', label='Danger Zone')
        
        # Current state marker
        ax.plot(2023, 127, 'ro', markersize=12, label='Current State (127 qubits)')
        
        # Labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Qubits')
        ax.set_title('Quantum Computing Progress Timeline')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
    
    # Pitch Deck Structure
    st.subheader("7-Slide Pitch Deck Structure")
    
    st.markdown("""
    Follow this structure to create your presentation in PowerPoint or Canva:
    """)
    
    slides = {
        "Slide 1: The Quantum Threat (Hook)": 
            """
            - **Title:** "The Quantum Revolution: A Ticking Time Bomb for Cybersecurity"
            - **Content:**
              - Attention-grabbing fact: "Within 10 years, quantum computers will break all RSA encryption"
              - Visual: Timeline showing when quantum computers are expected to break encryption
              - Key message: "Every business using traditional encryption is at risk"
            """,
            
        "Slide 2: The Problem": 
            """
            - **Title:** "Current Security Approaches Are Not Quantum-Ready"
            - **Content:**
              - Problem 1: "Traditional encryption will be obsolete in the quantum era"
              - Problem 2: "Organizations lack real-time security monitoring"
              - Problem 3: "The transition to quantum-resistant security will take years"
              - Visual: Statistics on global readiness for quantum threats (low)
            """,
            
        "Slide 3: Introducing Our Solution": 
            """
            - **Title:** "Quantum-Resistant Zero Trust AI Security System"
            - **Content:**
              - Brief overview: "A complete security solution that combines immediate Zero Trust security with quantum-resistant cryptography"
              - Two key components: "Real-time behavior monitoring + Future-proof encryption"
              - Visual: Simple diagram showing how the system works
            """,
            
        "Slide 4: Zero Trust Component Demo": 
            """
            - **Title:** "Zero Trust in Action"
            - **Content:**
              - Screenshot/image from your live demo
              - 3 key benefits:
                - "Continuous behavior monitoring"
                - "AI-powered anomaly detection"
                - "Immediate threat response"
              - Call to action: "During our discussion, I'll show this working in real time"
            """,
            
        "Slide 5: Quantum-Resistant Component": 
            """
            - **Title:** "Preparing for the Quantum Future"
            - **Content:**
              - Short animation screenshot from your demo
              - Text: "Our system implements lattice-based cryptography that remains secure against quantum attacks"
              - Key benefit: "Future-proof your security infrastructure today"
            """,
            
        "Slide 6: Market Opportunity": 
            """
            - **Title:** "The Quantum Security Market Opportunity"
            - **Content:**
              - Market size: "$XX billion by 2030"
              - Growth rate: "XX% annual growth in quantum security solutions"
              - Target customers: "Financial institutions, government agencies, healthcare, critical infrastructure"
              - Visual: Market growth chart
            """,
            
        "Slide 7: Call to Action": 
            """
            - **Title:** "Secure the Future with Infosys"
            - **Content:**
              - Vision: "Position Infosys as the global leader in quantum-resistant security"
              - Next steps: "Pilot program with select clients"
              - Timeline: "6-month implementation roadmap"
              - Closing statement: "The quantum threat is coming. Let's be prepared."
            """
    }
    
    for i, (title, content) in enumerate(slides.items(), 1):
        with st.expander(f"{title}", expanded=False):
            st.markdown(content)
    
    # Presentation Tips
    st.subheader("Presentation Tips")
    
    st.markdown("""
    ### Before Your Presentation
    
    1. **Practice the demo thoroughly:**
       - Make sure you can run through the Zero Trust demo smoothly
       - Have the animation ready to play
       - Know how to explain the concepts in simple terms
       
    2. **Know the key talking points:**
       - The quantum threat timeline (5-10 years)
       - Why Zero Trust is needed now
       - How lattice-based cryptography works (at a high level)
       - Why this combined approach is powerful
       
    3. **Prepare for questions:**
       - "How does lattice-based cryptography work?"
       - "When will organizations need to implement quantum-resistant encryption?"
       - "How does the Zero Trust model detect anomalies?"
       
    ### During Your Presentation
    
    1. **Start with the threat** to create urgency
    
    2. **Demo the working prototype** to show your technical skills
    
    3. **Show the animation** for the "wow factor"
    
    4. **Connect to Infosys's business** by emphasizing how this positions them as leaders
    
    5. **Keep it concise** - aim for 5-10 minutes total
    """)
    
    st.success("Use this guide to prepare your presentation. With the working prototype, animation, and well-structured pitch, you'll impress Infosys with both technical skills and business vision!")
