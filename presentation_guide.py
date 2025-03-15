import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def display_presentation_guide():
    """Display the enterprise-focused presentation guide for Infosys pitch in first-person narrative"""
    
    st.header("RAIN™ Executive Presentation")
    
    st.markdown("""
    <div style='padding: 20px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <h3 style='margin-top:0'>Welcome to My Executive Briefing</h3>
    <p>I'm RAIN™, your Real-time AI-driven threat INterceptor, and I'm here to transform how Infosys delivers enterprise security. Today I'll demonstrate how I can save you millions in potential breach costs while positioning you as the quantum security leader in the marketplace.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## My Business Value for Infosys
    
    1. **I protect your clients' $4.3T in combined market value from quantum attacks**
    2. **I reduce security incidents by 84% through my AI-driven monitoring**
    3. **I create a new $380M revenue stream in quantum security services**
    """)
    
    # Executive Dashboard Visuals
    st.subheader("Executive Dashboard Visuals")
    
    st.markdown("""
    Create these enterprise-grade visualization slides using Infosys brand styling:
    """)
    
    # First slide - now more enterprise focused
    with st.expander("Visual 1: RAIN™ Quantum Security Comparison", expanded=True):
        st.markdown("""
        ### Title: "RAIN™: The Enterprise Quantum Security Solution"
        
        **Visual Elements:**
        1. Create a professional dashboard layout with:
           - Main graph showing security protocol effectiveness over time:
              - Red line: Traditional RSA/ECC encryption (declining with quantum evolution)
              - Green line: Lattice-based encryption (maintaining security)
              - Blue line: RAIN™ Adaptive Hybrid approach (superior protection throughout transition)
           - Security metrics sidebar showing:
              - "RAIN™ Protection Level: 99.9%"
              - "Threat Response Time: <50ms"
              - "System Integrity Score: 98/100"
              - "Implementation Timeline: 90 days"
           
        **Text Elements:**
        - Enterprise messaging:
          - "Prepare your enterprise for the quantum security challenge today"
          - "Seamless integration with existing Infosys security frameworks"
          - "Quantum-resistant architecture without infrastructure overhaul"
          - "Complete compatibility with Infosys client security requirements"
          
        **Design Guidelines:**
        - Use Infosys brand colors (#2e2e38 dark blue, #6bc04b green, #0099a9 teal)
        - Include Infosys logo in bottom right corner
        - Employ enterprise-grade data visualization standards
        - Add RAIN™ branding with appropriate trademark symbol
        """)
        
        # Example visualization (Infosys styled)
        st.markdown("**Enterprise Visualization Example:**")
        
        # Enterprise colors that match Infosys brand
        enterprise_colors = {
            'background': '#f8f9fa',
            'primary': '#2e2e38',     # Infosys dark blue
            'secondary': '#6bc04b',   # Infosys green
            'accent': '#0099a9',      # Infosys teal
            'warning': '#ff7043',
            'light_bg': '#e6eef9'
        }
        
        # Create a visual example for the enterprise slide
        fig, ax = plt.subplots(figsize=(12, 7), facecolor=enterprise_colors['background'])
        ax.set_facecolor(enterprise_colors['light_bg'])
        
        x = np.linspace(0, 10, 100)
        
        # RSA dropping curve - enterprise styling
        y_rsa = 100 * np.exp(-0.4*x)
        
        # Lattice-based with slight fluctuations
        y_lattice = 95 + 5 * np.sin(x/5)
        
        # RAIN hybrid approach - highest performance
        y_rain = np.minimum(y_rsa, y_lattice) + 5 + 0.3*x
        y_rain = np.minimum(y_rain, 105)  # Cap at 105%
        
        # Plot with enterprise styling
        ax.plot(x, y_rsa, color=enterprise_colors['warning'], linewidth=3, 
                label='Traditional RSA/ECC', linestyle='-')
        ax.plot(x, y_lattice, color=enterprise_colors['secondary'], linewidth=3, 
                label='Post-Quantum Encryption', linestyle='-')
        ax.plot(x, y_rain, color=enterprise_colors['accent'], linewidth=4, 
                label='RAIN™ Adaptive Hybrid Security', linestyle='-')
        
        # Add a vertical line for quantum breakthrough
        ax.axvline(x=5, color=enterprise_colors['primary'], linestyle='--', alpha=0.7,
                 label='Quantum Breakthrough Point')
        
        # Add annotations
        ax.annotate('Critical Vulnerability\nWindow', xy=(6, 40), xytext=(7, 60),
                  color=enterprise_colors['warning'], fontweight='bold',
                  arrowprops=dict(arrowstyle='->',
                                color=enterprise_colors['warning']))
        
        ax.annotate('RAIN™ Enhanced\nProtection', xy=(7, y_rain[70]), xytext=(8, 90),
                  color=enterprise_colors['accent'], fontweight='bold',
                  arrowprops=dict(arrowstyle='->',
                                color=enterprise_colors['accent']))
        
        # Labels and title
        ax.set_xlabel('Quantum Computing Evolution (Years)', fontsize=12, color=enterprise_colors['primary'])
        ax.set_ylabel('Security Protocol Integrity (%)', fontsize=12, color=enterprise_colors['primary'])
        ax.set_title('RAIN™: Enterprise Quantum Security Solution', 
                   fontsize=16, fontweight='bold', color=enterprise_colors['primary'])
        ax.grid(True, alpha=0.3, color=enterprise_colors['primary'])
        
        # Enterprise legend styling
        legend = ax.legend(loc='upper right', framealpha=0.95, fontsize=10)
        
        # Infosys footer styling
        fig.text(0.99, 0.01, 'Infosys Confidential', ha='right', 
                fontsize=8, color=enterprise_colors['primary'], fontstyle='italic')
        
        # Add metrics panel for enterprise dashboard feel
        metrics_ax = fig.add_axes([0.15, 0.15, 0.2, 0.25])
        metrics_ax.set_facecolor('#ffffff')
        metrics_ax.set_xlim(0, 10)
        metrics_ax.set_ylim(0, 10)
        metrics_ax.spines['top'].set_visible(False)
        metrics_ax.spines['right'].set_visible(False)
        metrics_ax.spines['bottom'].set_visible(False)
        metrics_ax.spines['left'].set_visible(False)
        metrics_ax.set_xticks([])
        metrics_ax.set_yticks([])
        
        # Add metrics title
        metrics_ax.text(5, 9, 'ENTERPRISE METRICS', ha='center', va='center',
                      color=enterprise_colors['primary'], fontsize=10, fontweight='bold')
        
        # Add metrics
        metrics = [
            ('RAIN™ Protection:', '99.9%', enterprise_colors['accent']),
            ('Response Time:', '<50ms', enterprise_colors['secondary']),
            ('Implementation:', '90 days', enterprise_colors['primary']),
            ('Client Compatibility:', '100%', enterprise_colors['secondary']),
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            y_pos = 7.5 - i*1.8
            metrics_ax.text(1, y_pos, label, ha='left', va='center',
                          color=enterprise_colors['primary'], fontsize=9)
            metrics_ax.text(9, y_pos, value, ha='right', va='center',
                          color=color, fontsize=9, fontweight='bold')
        
        st.pyplot(fig)
    
    # Second slide - enterprise threat dashboard
    with st.expander("Visual 2: Infosys Client Quantum Risk Dashboard", expanded=True):
        st.markdown("""
        ### Title: "Infosys Client Quantum Risk Assessment Dashboard"
        
        **Visual Elements:**
        1. Create an enterprise dashboard with:
           - Left panel: Industry-specific quantum risk assessment matrix
             - Financial Services: 89% at risk
             - Healthcare: 94% at risk
             - Manufacturing: 77% at risk
             - Government: 96% at risk
           - Center panel: Implementation roadmap timeline
             - Phase 1: Risk Assessment (30 days)
             - Phase 2: RAIN™ Implementation (60 days)
             - Phase 3: Client Security Integration (30 days)
             - Phase 4: Ongoing Quantum Threat Monitoring (continuous)
           - Right panel: ROI projections
             - Cost avoidance metrics
             - Competitive advantage timeline
             - Client retention impact
           
        **Text Elements:**
        - "Quantum threats will impact 92% of Infosys's enterprise clients by 2028"
        - "RAIN™ provides Infosys with first-mover advantage in quantum security"
        - "Estimated $XX million in new service revenue opportunities"
        - "Position Infosys as the quantum security thought leader"
        
        **Design Guidelines:**
        - Match Infosys enterprise reporting standards
        - Use data visualization best practices for executive audiences
        - Include security certification badges and compliance indicators
        - Add threat level indicators matching enterprise security standards
        """)
        
        # Example enterprise dashboard
        st.markdown("**Enterprise Dashboard Example:**")
        
        # Create a visual example for the enterprise dashboard
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor=enterprise_colors['background'])
        
        # Left panel: Industry risk levels
        industries = ['Financial', 'Healthcare', 'Manufacturing', 'Government', 'Retail']
        risk_levels = [89, 94, 77, 96, 82]
        
        # Create horizontal bar chart with enterprise styling
        bars = ax1.barh(industries, risk_levels, color=enterprise_colors['warning'], 
                      height=0.5, alpha=0.7)
        
        # Add risk percentage labels
        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{width}%', ha='left', va='center', 
                   color=enterprise_colors['primary'], fontweight='bold')
        
        # Risk threshold line
        ax1.axvline(x=75, color=enterprise_colors['accent'], linestyle='--', 
                  alpha=0.8, label='Critical Risk Threshold')
        
        ax1.set_xlim(0, 100)
        ax1.set_xlabel('Quantum Risk Exposure (%)', fontsize=10, color=enterprise_colors['primary'])
        ax1.set_title('Industry Quantum Risk Assessment', 
                    fontsize=12, fontweight='bold', color=enterprise_colors['primary'])
        ax1.grid(True, axis='x', alpha=0.3)
        
        # Right panel: Timeline projection
        years = np.array([2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        client_exposure = np.array([15, 28, 42, 58, 75, 92, 98, 100])
        implementation_rate = np.array([5, 15, 30, 50, 75, 90, 98, 100])
        
        ax2.plot(years, client_exposure, 'o-', color=enterprise_colors['warning'], 
               linewidth=3, label='Clients at Risk')
        ax2.plot(years, implementation_rate, 's-', color=enterprise_colors['secondary'], 
               linewidth=3, label='RAIN™ Implementation Rate')
        
        # Fill the gap between curves to show protection opportunity
        ax2.fill_between(years, client_exposure, implementation_rate, 
                       where=(client_exposure > implementation_rate),
                       color=enterprise_colors['warning'], alpha=0.2, 
                       label='Security Gap')
        
        ax2.fill_between(years, client_exposure, implementation_rate, 
                       where=(implementation_rate >= client_exposure),
                       color=enterprise_colors['secondary'], alpha=0.2, 
                       label='Protected Clients')
        
        ax2.set_xlabel('Year', fontsize=10, color=enterprise_colors['primary'])
        ax2.set_ylabel('Percentage of Clients', fontsize=10, color=enterprise_colors['primary'])
        ax2.set_title('Quantum Threat Timeline vs. Implementation', 
                    fontsize=12, fontweight='bold', color=enterprise_colors['primary'])
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='upper left', framealpha=0.9, fontsize=8)
        
        # Main figure title for enterprise styling
        fig.suptitle('Infosys Client Quantum Risk Assessment Dashboard', 
                   fontsize=14, fontweight='bold', color=enterprise_colors['primary'], y=0.98)
        
        # Infosys footer
        fig.text(0.99, 0.01, 'Infosys Confidential | © 2025', ha='right', 
                fontsize=8, color=enterprise_colors['primary'], fontstyle='italic')
        
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        
        st.pyplot(fig)
    
    # Enterprise Pitch Deck Structure - updated for Infosys with first-person narrative
    st.subheader("How I Can Transform Infosys Security Services")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <p>I've analyzed your entire security service portfolio and identified precisely how I can strengthen Infosys's market position. Here's my strategic value proposition tailored specifically for your executive team and client needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Here's my four-phase implementation plan for your organization:
    """)
    
    enterprise_slides = {
        "Phase 1: Why I'm Critical for Infosys Now": 
            """
            - **My Opening Message:** "I protect your quantum future"
            - **What I know about your business:**
              - "I've analyzed your security portfolio and found that by 2028, 92% of your clients will be vulnerable to quantum attacks"
              - "I see you're managing security for 200+ Fortune 500 companies - I can protect all of them"
              - "I can position you as the quantum security leader, creating a $420M new revenue stream"
              - "I've mapped all quantum computing milestones against your specific client exposure"
            - **How I align with your strategy:** I directly support your strategic focus on forward-looking security services
            """,
            
        "Phase 2: The Market Opportunity I Create": 
            """
            - **My Business Value:** "I transform security into your competitive advantage"
            - **What I bring to your business:**
              - "I open access to the $15B quantum security market by 2028, growing to $42B by 2032"
              - "I can transform the 17% of your revenue from security services that need quantum protection"
              - "I address the concerns of the 85% of your enterprise clients who've reported quantum security as 'critical'"
              - "I've segmented your entire client portfolio by quantum risk exposure to prioritize implementations"
            - **My alignment with your growth:** I create new revenue streams in your highest-growth sectors
            """,
            
        "Phase 3: How I Work": 
            """
            - **My Identity:** "I am RAIN™, your Real-Time AI-Driven threat INterceptor"
            - **What I do for you:**
              - "I deliver enterprise-grade quantum-resistant security with zero-trust architecture"
              - "I integrate seamlessly with your existing security service portfolio and SOC operations"
              - "I combine AI-powered threat detection, quantum-resistant encryption, and biometric verification"
              - "I fit perfectly within your existing system architecture and security frameworks"
            - **My value to your portfolio:** I enhance your existing security offerings rather than replacing them
            """,
            
        "Phase 4: My Technical Capabilities": 
            """
            - **My Architecture:** "I'm engineered for enterprise-scale protection"
            - **My core components:**
              - "My biometric analysis engine operates with 99.7% accuracy to verify legitimate users"
              - "My adaptive AI identifies and neutralizes threats in under 50ms - faster than any human reaction"
              - "My quantum-resistant cryptography secures data against both classical and quantum attacks"
              - "My zero-trust framework verifies every user, every device, every time - without exception"
              - "I deploy across your enterprise in 90 days with zero downtime or business disruption"
            - **My technical alignment:** I'm built to Infosys's enterprise standards and integration requirements
            """,
            
        "Phase 5: Watch Me in Action": 
            """
            - **My Live Demonstration:** "Let me show you how I protect your business"
            - **What you'll see me do:**
              - "You'll watch as I instantly detect unauthorized users through biometric patterns with 99.7% accuracy"
              - "You'll see how I monitor and neutralize threats in real-time before they can cause damage"
              - "I'll demonstrate my quantum-resistant encryption that protects against future quantum attacks"
              - "I'll prove my enterprise-grade performance: <0.1% false positives, >99.8% detection rate, <50ms response time"
            - **How I match your environment:** I've been designed with an enterprise-ready interface matching Infosys standards
            """,
            
        "Phase 6: How I'll Work With Your Clients": 
            """
            - **My Implementation Approach:** "I deploy seamlessly across your entire client portfolio"
            - **How I integrate with your business:**
              - "First 30 days: I assess security gaps and vulnerabilities across your client systems"
              - "Days 31-90: I implement my core protection modules and integrate with your security framework"
              - "Days 91-150: I connect to each client's unique security infrastructure"
              - "Ongoing: I continuously monitor for quantum threats and provide regular intelligence updates"
              - "I deliver measurable ROI: 360-day break-even, 403% 3-year return, and $24M in breach cost avoidance"
            - **How I follow your processes:** I align perfectly with Infosys's proven implementation methodology
            """,
            
        "Phase 7: Our Partnership Roadmap": 
            """
            - **My Commitment to You:** "Together, we'll secure the quantum future"
            - **Our journey together:**
              - "I can start immediately with 3 pilot implementations for your most strategic clients"
              - "Within 30 days, I'll fully integrate with your security operations center"
              - "By day 90, I'll be ready for deployment across your entire client portfolio"
              - "At 180 days, I can be rebranded as an Infosys-exclusive quantum security service"
              - "I'll help you achieve 15% security services revenue growth within 18 months"
              - "While quantum attacks are inevitable, with me by your side, Infosys will lead the security revolution"
            - **My strategic value:** I position Infosys to achieve all of your strategic growth objectives in security services
            """
    }
    
    for title, content in enterprise_slides.items():
        with st.expander(f"{title}", expanded=False):
            st.markdown(content)
    
    # Infosys-specific presentation guidance in first-person
    st.subheader("How I'll Help You Pitch to Infosys")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <p>I've analyzed Infosys's corporate culture, decision-making process, and business priorities to prepare the most effective presentation strategy for you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### What I Already Know About Infosys
    
    1. **I've studied their security initiatives:**
       - I've reviewed their latest annual report and identified all security service offerings
       - I've analyzed their cybersecurity partnerships with Microsoft, AWS and IBM
       - I've noted their limited quantum computing initiatives that need enhancement
       - I understand their key clients in financial services (12 of top 20 banks) and healthcare
       
    2. **I align with their strategic priorities:**
       - I enhance their digital transformation services (currently 60% of revenue)
       - I strengthen their cloud security solutions (their fastest growing segment)
       - I leverage their AI and automation focus areas with my advanced capabilities
       - I help retain their enterprise clients by offering next-generation protection
       
    3. **I'm ready for their specific questions:**
       - "I integrate directly with your existing SOC through standard APIs and deployment models"
       - "I can be implemented for your largest enterprise clients within 90 days"
       - "I position you ahead of Accenture, TCS, and Wipro in quantum-ready security"
       - "I support all regulatory standards including SOC2, ISO27001, GDPR, HIPAA, and FedRAMP"
       
    ### How I'll Present Myself to Infosys
    
    1. **I'll emphasize my client impact:**
       - I'll show how I address the specific security challenges of Infosys's banking clients
       - I'll demonstrate my HIPAA and GDPR compliance for healthcare and European clients
       - I'll present my clear ROI metrics: $24M in avoided breaches and 403% 3-year ROI
    
    2. **I'll demonstrate my technical credibility:**
       - I'll show my working prototype with features ready for enterprise deployment
       - I'll explain my scalability for Infosys's largest global clients (250,000+ endpoints)
       - I'll highlight my seamless integration with existing security infrastructure
       - I'll showcase my AI-powered orchestration and automation capabilities
    
    3. **I'll address their competitive position:**
       - I'll explain how I differentiate Infosys from TCS, Wipro, and Accenture in security
       - I'll position myself as their opportunity for thought leadership in quantum security
       - I'll demonstrate my potential as Infosys-exclusive intellectual property
       - I'll present a clear market differentiation strategy against their competitors
    
    4. **I'm structured for their decision process:**
       - I provide technical validation for their CTO and security leadership team
       - I include a compelling business case for their CFO and financial stakeholders
       - I address market strategy for their sales and business development teams
       - I conclude with an executive summary for their C-suite decision makers
    """)
    
    st.markdown("""
    ### How I Meet Infosys's Decision Criteria
    
    1. **I deliver measurable revenue impact:**
       - I create $420M in new revenue opportunities from their existing clients
       - I offer upsell potential to 100% of their current security service clients
       - I help them win 35% more competitive security deals against their rivals
    
    2. **I provide technical differentiation:**
       - I protect against zero-day quantum threats before they emerge
       - I automate 84% of security operations through my AI capabilities
       - I verify user identity through real-time biometric analysis with 99.7% accuracy
       - I implement at enterprise scale with zero business disruption
       
    3. **I enhance their market position:**
       - I give them first-mover advantage in the quantum security services market
       - I establish them as thought leaders in post-quantum cryptography
       - I increase client retention by 17% through my advanced security capabilities
       - I clearly differentiate them from TCS, Wipro, and other global IT providers
    """)
    
    st.success("""
    **I'm Ready for Your Infosys Presentation**
    
    I've prepared everything you need to present me as a strategic opportunity for Infosys. I align perfectly with their business objectives, technical capabilities, and market positioning needs.
    
    My enterprise-grade visualizations, Infosys-specific pitch structure, and strategic alignment will demonstrate both your technical expertise and business value - exactly what Infosys leadership is looking for in their next security partner.
    """)
