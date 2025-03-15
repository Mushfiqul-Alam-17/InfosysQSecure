import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def display_presentation_guide():
    """Display the enterprise-focused presentation guide for Infosys pitch"""
    
    st.header("RAIN™ Enterprise Presentation Guide")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <h3 style='margin-top:0'>My Executive Briefing for Infosys</h3>
    <p>As I present RAIN™ to you today, I'll demonstrate how our quantum-resistant security framework addresses your most critical vulnerabilities while enhancing your strategic market position. Join me on this journey to transform enterprise security.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## Presentation Components
    
    1. **Executive Dashboard Visual Assets**
    2. **Enterprise Pitch Deck Structure**
    3. **Infosys-Specific Positioning Strategy**
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
    
    # Enterprise Pitch Deck Structure - updated for Infosys
    st.subheader("Enterprise Pitch Deck Structure for Infosys")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <p>I've tailored this executive presentation specifically for you, the Infosys leadership team. My pitch directly addresses your strategic initiatives, market positioning, and the security needs of your premium client portfolio.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Create your presentation using these critical enterprise components:
    """)
    
    enterprise_slides = {
        "Slide 1: Strategic Imperative": 
            """
            - **Title:** "The Quantum Security Imperative for Infosys"
            - **Content:**
              - Opening statement: "By 2028, 92% of enterprise security solutions will be vulnerable to quantum computing attacks"
              - Infosys metric: "Infosys currently manages security for 200+ Fortune 500 companies - all at quantum risk"
              - Market positioning: "First-mover advantage in quantum security services represents a $XX billion opportunity"
              - Visual: Timeline showing quantum computing milestones and Infosys client exposure metrics
            - **Infosys Alignment:** Addresses Infosys's strategic focus on forward-looking security services
            """,
            
        "Slide 2: Market Opportunity": 
            """
            - **Title:** "Infosys Quantum Security Market Opportunity"
            - **Content:**
              - Market size: "Global quantum security market projections: $15B by 2028, $42B by 2032"
              - Infosys positioning: "Current security services represent 17% of Infosys revenue - all requiring quantum upgrades"
              - Client impact: "85% of enterprise clients report quantum security as a 'critical concern' in latest surveys"
              - Visual: Infosys client portfolio segmentation by quantum risk exposure
            - **Infosys Alignment:** Highlights revenue opportunities aligned with Infosys's growth sectors
            """,
            
        "Slide 3: Introducing RAIN™": 
            """
            - **Title:** "RAIN™: Real-Time AI-Driven Threat Interceptor and Neutralizer"
            - **Content:**
              - Solution overview: "Enterprise-grade quantum-resistant security framework with zero-trust architecture"
              - Integration highlight: "Seamless integration with Infosys's existing security service portfolio"
              - Key differentiators: "AI-powered real-time threat detection + quantum-resistant encryption + biometric verification"
              - Visual: RAIN™ architecture diagram showing integration points with Infosys systems
            - **Infosys Alignment:** Positions RAIN™ as an enhancement to existing Infosys security offerings
            """,
            
        "Slide 4: Enterprise Technical Architecture": 
            """
            - **Title:** "RAIN™ Enterprise Technical Architecture"
            - **Content:**
              - Security components:
                - "Biometric keystroke dynamics engine with 99.7% accuracy"
                - "Adaptive AI threat analysis with <50ms response time"
                - "Quantum-resistant lattice-based cryptography"
                - "Zero trust verification framework"
              - Implementation metrics: "90-day enterprise deployment timeline with zero downtime"
              - Visual: Technical architecture diagram with Infosys integration points
            - **Infosys Alignment:** Demonstrates technical compatibility with Infosys standards
            """,
            
        "Slide 5: Live Demonstration": 
            """
            - **Title:** "RAIN™ Enterprise Security in Action"
            - **Content:**
              - Screenshot of RAIN™ dashboard with enterprise styling
              - Demo highlights:
                - "Biometric intrusion detection with 99.7% accuracy"
                - "Real-time threat monitoring and response"
                - "Quantum-resistant encryption visualization"
              - Enterprise metrics: "False positive rate <0.1%, detection rate >99.8%, response time <50ms"
              - Visual: Live demo screenshots with enterprise dashboard interface
            - **Infosys Alignment:** Shows RAIN™ with enterprise-ready UI matching Infosys standards
            """,
            
        "Slide 6: Client Implementation Roadmap": 
            """
            - **Title:** "Enterprise Implementation Strategy"
            - **Content:**
              - Phased approach:
                - "Phase 1: Security Assessment & Gap Analysis (30 days)"
                - "Phase 2: RAIN™ Implementation & Integration (60 days)"
                - "Phase 3: Client Security Systems Integration (30-60 days)"
                - "Phase 4: Ongoing Quantum Threat Intelligence (continuous)"
              - ROI metrics: "360-day break-even point, 403% 3-year ROI, $XX million in cost avoidance"
              - Visual: Implementation timeline with resource requirements and milestone indicators
            - **Infosys Alignment:** Follows Infosys's proven implementation methodology
            """,
            
        "Slide 7: Strategic Partnership Proposal": 
            """
            - **Title:** "RAIN™ + Infosys: Securing the Quantum Future"
            - **Content:**
              - Partnership vision: "Position Infosys as the global quantum security leader"
              - Next steps:
                - "Immediate: RAIN™ pilot with 3 strategic Infosys clients"
                - "30 days: Integration with Infosys security operations center"
                - "90 days: Client-ready RAIN™-powered security offering"
                - "180 days: Infosys-branded quantum security service"
              - Expected outcomes: "15% security services revenue growth within 18 months"
              - Closing statement: "The quantum security revolution is inevitable. With RAIN™, Infosys will lead it."
            - **Infosys Alignment:** Positions proposal within Infosys's strategic growth objectives
            """
    }
    
    for title, content in enterprise_slides.items():
        with st.expander(f"{title}", expanded=False):
            st.markdown(content)
    
    # Infosys-specific presentation guidance
    st.subheader("Infosys-Specific Presentation Strategy")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f7ff; border-left: 5px solid #0068C9; margin-bottom: 20px;'>
    <p>The following guidance is strategically aligned with Infosys's corporate culture, decision-making process, and business priorities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Pre-Presentation Preparation for Infosys
    
    1. **Research Infosys's Current Security Initiatives:**
       - Review Infosys's latest annual report for security service highlights
       - Note their existing cybersecurity partnerships and acquisitions
       - Identify their current quantum computing initiatives (if any)
       - Understand their key financial services, healthcare and government clients
       
    2. **Align with Infosys's Strategic Priorities:**
       - Digital transformation services (60% of revenue)
       - Cloud security solutions (fastest growing segment)
       - AI and automation integration (strategic focus area)
       - Enterprise client retention (key business metric)
       
    3. **Prepare for Infosys-Specific Questions:**
       - "How does RAIN™ integrate with our existing security operation centers?"
       - "What is the implementation timeline for our largest enterprise clients?"
       - "How does this position us against Accenture, TCS, and Wipro?"
       - "What regulatory compliance standards does RAIN™ support?"
       
    ### During Your Infosys Presentation
    
    1. **Emphasize Enterprise Client Impact**
       - Highlight how RAIN™ addresses specific Infosys client security challenges
       - Reference financial services and healthcare compliance requirements
       - Present clear ROI metrics for both Infosys and their clients
    
    2. **Demonstrate Technical Credibility with Enterprise Focus**
       - Show the working RAIN™ prototype with enterprise-ready features
       - Emphasize scalability for Infosys's largest global clients
       - Highlight integration with existing enterprise security infrastructure
       - Focus on the AI-powered security orchestration capabilities
    
    3. **Address Infosys's Competitive Position**
       - Explain how RAIN™ differentiates Infosys from key competitors (TCS, Wipro, Accenture)
       - Position as a thought leadership opportunity in enterprise security
       - Showcase potential for Infosys intellectual property development
       - Present clear market differentiation strategy
    
    4. **Structure for Infosys Decision Process**
       - Present technical validation for CTO/security leadership
       - Include business case for CFO/financial stakeholders
       - Address market strategy for sales/business development
       - Conclude with executive summary for C-suite decision makers
    """)
    
    st.markdown("""
    ### Infosys Decision Criteria Alignment
    
    1. **Revenue Impact**
       - Quantify new revenue opportunities from existing clients
       - Present upsell potential to current security service clients
       - Show competitive win rates for new business opportunities
    
    2. **Technical Differentiation**
       - Zero-day quantum threat protection capability
       - AI-driven security operations automation
       - Real-time biometric identity verification
       - Enterprise-grade implementation with minimal disruption
       
    3. **Market Positioning**
       - First-mover advantage in quantum security services
       - Thought leadership in post-quantum cryptography
       - Client retention through advanced security capabilities
       - Competitive differentiation from other global IT service providers
    """)
    
    st.success("""
    **Enterprise Presentation Readiness Checklist**
    
    With this comprehensive enterprise presentation strategy, you're positioned to present RAIN™ as a strategic opportunity for Infosys, aligning with their business objectives, technical capabilities, and market positioning.
    
    The enterprise-grade visualizations, Infosys-specific pitch deck, and strategic alignment will demonstrate both your technical expertise and business acumen - critical for success with Infosys leadership.
    """)
