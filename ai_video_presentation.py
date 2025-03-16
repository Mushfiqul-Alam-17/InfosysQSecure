import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime

class AIPresentationGenerator:
    """
    Generate an AI-powered video presentation explaining RAIN™ security features
    using first-person narrative style for executive presentations.
    """
    
    def __init__(self):
        """Initialize the presentation generator with necessary components"""
        # Set presentation styles
        self.styles = {
            'background_color': '#0a192f',
            'text_color': '#ffffff',
            'accent_color': '#64ffda',
            'highlight_color': '#ff5252',
            'infosys_blue': '#2e2e38',
            'infosys_green': '#6bc04b',
            'infosys_teal': '#0099a9'
        }
        
        # Initialize frames collection
        self.frames = []
        self.current_frame = 0
        self.total_frames = 0
        
        # Store presentation narrative points
        self.narrative_points = [
            "As the CTO of Infosys, I present RAIN™: our next-generation security platform.",
            "RAIN™ uses biometric analysis to detect unauthorized access in real-time.",
            "Our quantum-resistant encryption protects against future threats.",
            "The zero-trust architecture verifies every user interaction continuously.",
            "AI-powered threat detection identifies patterns invisible to traditional systems.",
            "Integration with your existing infrastructure takes just 90 days.",
            "Let me demonstrate how RAIN™ protects your enterprise from sophisticated threats."
        ]
    
    def generate_presentation(self, duration=20, fps=5):
        """
        Generate the complete video presentation.
        
        Parameters:
        -----------
        duration: int
            Duration of the video in seconds
        fps: int
            Frames per second
            
        Returns:
        --------
        video_path: str
            Path to the generated video file
        """
        # Calculate total frames
        self.total_frames = duration * fps
        
        # Generate frames
        with st.spinner("Generating AI video presentation..."):
            progress_bar = st.progress(0)
            
            for i in range(self.total_frames):
                # Create frames with different visual elements based on timing
                if i < self.total_frames * 0.1:  # Introduction/title
                    frame = self._create_intro_frame(i)
                elif i < self.total_frames * 0.3:  # Problem statement
                    frame = self._create_problem_frame(i)
                elif i < self.total_frames * 0.6:  # Solution/features
                    frame = self._create_features_frame(i)
                elif i < self.total_frames * 0.8:  # Implementation
                    frame = self._create_implementation_frame(i)
                else:  # Call to action
                    frame = self._create_conclusion_frame(i)
                
                # Save the frame
                self.frames.append(frame)
                
                # Update progress
                progress = (i + 1) / self.total_frames
                progress_bar.progress(progress)
            
            # Finalize presentation
            progress_bar.progress(1.0)
            st.success("AI presentation successfully generated!")
            
            return self._save_presentation_to_html(fps)
    
    def _create_intro_frame(self, frame_num):
        """Create an introduction frame with title animation"""
        # Create figure with corporate styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.styles['background_color'])
        ax.set_facecolor(self.styles['background_color'])
        
        # Remove axes
        ax.set_axis_off()
        
        # Animation timing
        progress = frame_num / (self.total_frames * 0.1)
        
        # Title with animated reveal
        title_text = "RAIN™"
        subtitle_text = "Real-Time AI-Driven Threat Interceptor & Neutralizer"
        
        # Animate title
        if progress > 0.2:
            reveal_length = int(min(1.0, (progress - 0.2) / 0.5) * len(title_text))
            title = title_text[:reveal_length]
            ax.text(0.5, 0.5, title, color=self.styles['accent_color'], 
                   fontsize=50, ha='center', va='center', weight='bold')
        
        # Animate subtitle
        if progress > 0.6:
            reveal_length = int(min(1.0, (progress - 0.6) / 0.4) * len(subtitle_text))
            subtitle = subtitle_text[:reveal_length]
            ax.text(0.5, 0.65, subtitle, color=self.styles['text_color'], 
                   fontsize=16, ha='center', va='center')
        
        # Add first-person narrative
        if progress > 0.8:
            narrative = self.narrative_points[0]
            ax.text(0.5, 0.85, narrative, color=self.styles['text_color'],
                   fontsize=14, ha='center', va='center', style='italic',
                   bbox=dict(facecolor=self.styles['infosys_blue'], alpha=0.5, 
                             boxstyle='round,pad=0.5'))
        
        # Add corporate branding
        if progress > 0.9:
            ax.text(0.95, 0.95, "INFOSYS", color=self.styles['infosys_green'],
                   fontsize=14, ha='right', va='top', weight='bold')
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        
        return img
    
    def _create_problem_frame(self, frame_num):
        """Create a frame highlighting the security problems RAIN™ solves"""
        # Calculate relative frame position
        section_start = int(self.total_frames * 0.1)
        section_length = int(self.total_frames * 0.2)
        relative_frame = frame_num - section_start
        progress = relative_frame / section_length
        
        # Create figure with corporate styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.styles['background_color'])
        ax.set_facecolor(self.styles['background_color'])
        
        # Remove axes
        ax.set_axis_off()
        
        # Section title
        ax.text(0.5, 0.1, "THE QUANTUM SECURITY CHALLENGE", color=self.styles['accent_color'], 
               fontsize=24, ha='center', va='center', weight='bold')
        
        # Animated threat statistics
        threats = [
            "92% of current encryption vulnerable to quantum attacks by 2028",
            "287 days: Average time to identify a breach (IBM)",
            "Zero-day exploits increased by 45% in the past year",
            "Insider threats account for 34% of all breaches"
        ]
        
        max_threats_to_show = min(len(threats), int(progress * 6))
        
        for i in range(max_threats_to_show):
            if i < len(threats):
                y_pos = 0.3 + (i * 0.1)
                # Animation effect: threats appear one by one
                ax.text(0.1, y_pos, "•", color=self.styles['highlight_color'], 
                       fontsize=20, ha='center', va='center')
                ax.text(0.15, y_pos, threats[i], color=self.styles['text_color'], 
                       fontsize=14, ha='left', va='center',
                       alpha=min(1.0, (progress * 5) - i))
        
        # Add narrative text
        if progress > 0.5:
            narrative_idx = min(1, int(progress * 3))
            narrative = self.narrative_points[narrative_idx]
            ax.text(0.5, 0.85, narrative, color=self.styles['text_color'],
                   fontsize=14, ha='center', va='center', style='italic',
                   bbox=dict(facecolor=self.styles['infosys_blue'], alpha=0.5, 
                             boxstyle='round,pad=0.5'))
        
        # Add quantum computer visual representation
        if progress > 0.7:
            # Simple representation of quantum computer visual
            qc_x = 0.75
            qc_y = 0.5
            qc_size = 0.15
            
            # Base quantum processor
            quantum_processor = patches.Circle((qc_x, qc_y), qc_size, 
                                             fill=True, color=self.styles['infosys_teal'], alpha=0.7)
            ax.add_patch(quantum_processor)
            
            # Add quantum bits (animated)
            num_qubits = int(min(8, progress * 12))
            for i in range(num_qubits):
                angle = (i / 8) * 2 * np.pi
                radius = qc_size * 0.7
                qubit_x = qc_x + radius * np.cos(angle)
                qubit_y = qc_y + radius * np.sin(angle)
                qubit = patches.Circle((qubit_x, qubit_y), qc_size * 0.15, 
                                     fill=True, color=self.styles['highlight_color'])
                ax.add_patch(qubit)
                
            # Label
            ax.text(qc_x, qc_y - qc_size - 0.05, "Quantum Threat", 
                   color=self.styles['text_color'], ha='center', va='top', fontsize=12)
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        
        return img
    
    def _create_features_frame(self, frame_num):
        """Create a frame showcasing RAIN™ key features"""
        # Calculate relative frame position
        section_start = int(self.total_frames * 0.3)
        section_length = int(self.total_frames * 0.3)
        relative_frame = frame_num - section_start
        progress = relative_frame / section_length
        
        # Create figure with corporate styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.styles['background_color'])
        ax.set_facecolor(self.styles['background_color'])
        
        # Remove axes
        ax.set_axis_off()
        
        # Section title
        ax.text(0.5, 0.1, "RAIN™ ENTERPRISE SECURITY FEATURES", color=self.styles['accent_color'], 
               fontsize=24, ha='center', va='center', weight='bold')
        
        # Key features with icons and animated appearance
        features = [
            "🔐 Quantum-Resistant Encryption",
            "🧠 AI Threat Intelligence Engine",
            "👆 Biometric Behavioral Analysis",
            "🛡️ Zero Trust Architecture",
            "🔄 Continuous Authentication"
        ]
        
        # Determine which features to show based on progress
        max_features = min(len(features), int(progress * 7))
        
        for i in range(max_features):
            if i < len(features):
                y_pos = 0.3 + (i * 0.1)
                # Animation: features appear one by one
                feature_alpha = max(0.0, min(1.0, (progress * 5) - i))
                ax.text(0.2, y_pos, features[i], color=self.styles['text_color'], 
                       fontsize=16, ha='left', va='center', alpha=feature_alpha)
                
                # Add animated feature meters
                meter_width = 0.3 * min(1.0, (progress * 5) - i)
                meter_height = 0.03
                meter = patches.Rectangle((0.6, y_pos - meter_height/2), meter_width, meter_height, 
                                         color=self.styles['accent_color'], alpha=0.8)
                ax.add_patch(meter)
                
                # Add percentage
                if (progress * 5) - i > 0.5:
                    percentage = int(min(100, ((progress * 5) - i) * 100))
                    ax.text(0.6 + meter_width + 0.02, y_pos, f"{percentage}%", 
                           color=self.styles['accent_color'], fontsize=12, ha='left', va='center')
        
        # Add narrative
        if progress > 0.6:
            narrative_idx = min(3, 2 + int(progress * 2))
            narrative = self.narrative_points[narrative_idx]
            ax.text(0.5, 0.85, narrative, color=self.styles['text_color'],
                   fontsize=14, ha='center', va='center', style='italic',
                   bbox=dict(facecolor=self.styles['infosys_blue'], alpha=0.5, 
                             boxstyle='round,pad=0.5'))
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        
        return img
    
    def _create_implementation_frame(self, frame_num):
        """Create a frame explaining implementation timeline and ROI"""
        # Calculate relative frame position
        section_start = int(self.total_frames * 0.6)
        section_length = int(self.total_frames * 0.2)
        relative_frame = frame_num - section_start
        progress = relative_frame / section_length
        
        # Create figure with corporate styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.styles['background_color'])
        ax.set_facecolor(self.styles['background_color'])
        
        # Remove axes
        ax.set_axis_off()
        
        # Section title
        ax.text(0.5, 0.1, "IMPLEMENTATION ROADMAP", color=self.styles['accent_color'], 
               fontsize=24, ha='center', va='center', weight='bold')
        
        # Timeline phases
        phases = [
            "Phase 1: Security Assessment & Gap Analysis (30 days)",
            "Phase 2: RAIN™ Implementation & Integration (60 days)",
            "Phase 3: Client Security Systems Integration (30 days)",
            "Phase 4: Ongoing Quantum Threat Intelligence (continuous)"
        ]
        
        # Implementation timeline visualization
        timeline_y = 0.3
        timeline_start = 0.1
        timeline_end = 0.9
        timeline_width = timeline_end - timeline_start
        
        # Draw timeline base
        ax.plot([timeline_start, timeline_end], [timeline_y, timeline_y], 
               color=self.styles['text_color'], linewidth=2, alpha=0.5)
        
        # Add phase markers and labels based on progress
        num_phases = min(len(phases), int(progress * 7))
        
        for i in range(num_phases):
            if i < len(phases):
                # Position marker on timeline
                marker_x = timeline_start + ((i + 1) / (len(phases) + 1)) * timeline_width
                
                # Draw marker
                marker_color = self.styles['infosys_green'] if i < 3 else self.styles['accent_color']
                marker = patches.Circle((marker_x, timeline_y), 0.015, 
                                      fill=True, color=marker_color)
                ax.add_patch(marker)
                
                # Draw connector line
                connector_height = 0.06 + (i * 0.08)
                ax.plot([marker_x, marker_x], [timeline_y, timeline_y + connector_height], 
                       color=marker_color, linewidth=1.5, alpha=0.7)
                
                # Phase label with animated appearance
                phase_alpha = max(0.0, min(1.0, (progress * 5) - i))
                ax.text(marker_x, timeline_y + connector_height + 0.02, phases[i].split(":")[0], 
                       color=marker_color, fontsize=12, ha='center', va='bottom', 
                       weight='bold', alpha=phase_alpha)
                
                # Phase description
                phase_desc = phases[i].split(": ")[1] if ": " in phases[i] else ""
                ax.text(marker_x, timeline_y + connector_height + 0.06, phase_desc, 
                       color=self.styles['text_color'], fontsize=10, ha='center', va='bottom', 
                       alpha=phase_alpha)
        
        # Add ROI information
        if progress > 0.5:
            roi_metrics = [
                "360-day break-even point",
                "403% 3-year ROI",
                "99.9% threat detection rate",
                "Zero downtime implementation"
            ]
            
            roi_box = patches.Rectangle((0.2, 0.58), 0.6, 0.2, 
                                      facecolor=self.styles['infosys_blue'], alpha=0.3,
                                      edgecolor=self.styles['accent_color'], linewidth=2)
            ax.add_patch(roi_box)
            
            ax.text(0.5, 0.6, "Enterprise ROI Metrics", color=self.styles['accent_color'], 
                   fontsize=16, ha='center', va='center', weight='bold')
            
            metrics_to_show = min(len(roi_metrics), int((progress - 0.5) * 10))
            for i in range(metrics_to_show):
                if i < len(roi_metrics):
                    y_pos = 0.65 + (i * 0.03)
                    ax.text(0.25, y_pos, "✓", color=self.styles['infosys_green'], 
                           fontsize=12, ha='center', va='center', weight='bold')
                    ax.text(0.28, y_pos, roi_metrics[i], color=self.styles['text_color'], 
                           fontsize=12, ha='left', va='center')
        
        # Add narrative
        if progress > 0.6:
            narrative = self.narrative_points[5]
            ax.text(0.5, 0.9, narrative, color=self.styles['text_color'],
                   fontsize=14, ha='center', va='center', style='italic',
                   bbox=dict(facecolor=self.styles['infosys_blue'], alpha=0.5, 
                             boxstyle='round,pad=0.5'))
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        
        return img
    
    def _create_conclusion_frame(self, frame_num):
        """Create a conclusion frame with call to action"""
        # Calculate relative frame position
        section_start = int(self.total_frames * 0.8)
        section_length = int(self.total_frames * 0.2)
        relative_frame = frame_num - section_start
        progress = relative_frame / section_length
        
        # Create figure with corporate styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.styles['background_color'])
        ax.set_facecolor(self.styles['background_color'])
        
        # Remove axes
        ax.set_axis_off()
        
        # Call to action with animated appearance
        if progress > 0.2:
            # Title
            title_opacity = max(0.0, min(1.0, (progress - 0.2) * 3))
            ax.text(0.5, 0.3, "SECURE YOUR ENTERPRISE TODAY", color=self.styles['accent_color'], 
                   fontsize=28, ha='center', va='center', weight='bold', alpha=title_opacity)
        
        if progress > 0.4:
            # RAIN logo
            logo_size = 0.15 * min(1.0, (progress - 0.4) * 3)
            logo = patches.Circle((0.5, 0.5), logo_size, 
                                fill=True, color=self.styles['infosys_blue'], alpha=0.8)
            ax.add_patch(logo)
            
            # Animated logo elements
            if progress > 0.5:
                for i in range(8):
                    angle = (i / 8) * 2 * np.pi
                    radius = logo_size * 1.3
                    element_x = 0.5 + radius * np.cos(angle)
                    element_y = 0.5 + radius * np.sin(angle)
                    element_size = 0.02 * min(1.0, (progress - 0.5) * 5)
                    element = patches.Circle((element_x, element_y), element_size, 
                                          fill=True, color=self.styles['accent_color'])
                    ax.add_patch(element)
                    
                    # Add connecting lines
                    line_alpha = max(0.0, min(1.0, (progress - 0.5) * 5))
                    ax.plot([0.5, element_x], [0.5, element_y], 
                           color=self.styles['accent_color'], linewidth=1, alpha=line_alpha * 0.5)
        
        # Add contact information with animated appearance
        if progress > 0.6:
            contact_opacity = max(0.0, min(1.0, (progress - 0.6) * 3))
            ax.text(0.5, 0.7, "Ready to implement RAIN™ in your enterprise?", 
                   color=self.styles['text_color'], fontsize=16, ha='center', va='center', 
                   alpha=contact_opacity)
            
            if progress > 0.7:
                ax.text(0.5, 0.75, "Contact our security team today:", 
                       color=self.styles['text_color'], fontsize=14, ha='center', va='center', 
                       alpha=contact_opacity)
                
                if progress > 0.8:
                    ax.text(0.5, 0.8, "security@infosys.com | +1 (800) 555-RAIN", 
                           color=self.styles['accent_color'], fontsize=14, ha='center', 
                           va='center', weight='bold', alpha=contact_opacity)
        
        # Add final narrative
        if progress > 0.9:
            narrative = self.narrative_points[6]
            ax.text(0.5, 0.9, narrative, color=self.styles['text_color'],
                   fontsize=14, ha='center', va='center', style='italic',
                   bbox=dict(facecolor=self.styles['infosys_blue'], alpha=0.5, 
                             boxstyle='round,pad=0.5'))
        
        # Add date and corporate footer
        ax.text(0.05, 0.95, datetime.now().strftime('%Y-%m-%d'), 
               color=self.styles['text_color'], fontsize=10, ha='left', va='top')
        
        ax.text(0.95, 0.95, "© 2025 Infosys", color=self.styles['infosys_green'],
               fontsize=10, ha='right', va='top')
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        
        return img
    
    def _save_presentation_to_html(self, fps=5):
        """Save the sequence of frames as an HTML animation"""
        html_content = []
        html_content.append("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAIN™ Executive Presentation</title>
            <style>
                body {
                    background-color: #0a192f; 
                    color: white;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }
                .presentation-container {
                    max-width: 800px;
                    margin: 0 auto;
                    text-align: center;
                }
                h1 {
                    color: #64ffda;
                    margin-bottom: 20px;
                }
                .animation-container {
                    margin: 20px 0;
                    border: 2px solid #333;
                    border-radius: 10px;
                    overflow: hidden;
                }
                .controls {
                    margin-top: 20px;
                    display: flex;
                    justify-content: center;
                    gap: 10px;
                }
                button {
                    background-color: #0099a9;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                }
                button:hover {
                    background-color: #6bc04b;
                }
                footer {
                    margin-top: 30px;
                    font-size: 12px;
                    color: #aaa;
                }
                .frame {
                    display: none;
                }
                .frame.active {
                    display: block;
                }
            </style>
        </head>
        <body>
            <div class="presentation-container">
                <h1>RAIN™ Enterprise Security Presentation</h1>
                <div class="animation-container">
        """)
        
        # Add all frames to HTML
        for i, frame in enumerate(self.frames):
            # Convert PIL image to base64 string
            buffer = io.BytesIO()
            frame.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Add image with CSS class to control visibility
            active_class = "active" if i == 0 else ""
            html_content.append(f'<img class="frame {active_class}" id="frame{i}" src="data:image/png;base64,{img_str}" width="800">')
        
        # Add animation controls and JavaScript
        html_content.append(f"""
                </div>
                <div class="controls">
                    <button id="play-pause">Pause</button>
                    <button id="restart">Restart</button>
                </div>
                <footer>
                    © Infosys 2025 | RAIN™ Real-Time AI-Driven Threat Interceptor and Neutralizer
                </footer>
            </div>
            
            <script>
                // Animation settings
                const frameCount = {len(self.frames)};
                const fps = {fps};
                let currentFrame = 0;
                let isPlaying = true;
                let animationInterval;
                
                // Control elements
                const playPauseButton = document.getElementById('play-pause');
                const restartButton = document.getElementById('restart');
                
                // Start animation
                startAnimation();
                
                // Handle play/pause
                playPauseButton.addEventListener('click', function() {{
                    isPlaying = !isPlaying;
                    playPauseButton.textContent = isPlaying ? 'Pause' : 'Play';
                    
                    if (isPlaying) {{
                        startAnimation();
                    }} else {{
                        clearInterval(animationInterval);
                    }}
                }});
                
                // Handle restart
                restartButton.addEventListener('click', function() {{
                    clearInterval(animationInterval);
                    currentFrame = 0;
                    updateFrame();
                    
                    if (isPlaying) {{
                        startAnimation();
                    }}
                }});
                
                function startAnimation() {{
                    animationInterval = setInterval(function() {{
                        currentFrame = (currentFrame + 1) % frameCount;
                        updateFrame();
                    }}, 1000 / fps);
                }}
                
                function updateFrame() {{
                    // Hide all frames
                    const frames = document.querySelectorAll('.frame');
                    frames.forEach(frame => frame.classList.remove('active'));
                    
                    // Show current frame
                    document.getElementById(`frame${{currentFrame}}`).classList.add('active');
                }}
            </script>
        </body>
        </html>
        """)
        
        # Combine all HTML content
        full_html = "\n".join(html_content)
        
        # Create an HTML file with the presentation
        html_file = "rain_presentation.html"
        with open(html_file, "w") as f:
            f.write(full_html)
        
        return html_file

def display_ai_video_presentation():
    """Display a website redirect interface for RAIN Enterprise Security
    
    Note: Function name kept as display_ai_video_presentation for backward compatibility,
    though this now displays the Enterprise Website interface instead.
    """
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0f7ff; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #0068C9;">RAIN™ Enterprise Website</h1>
        <p style="font-style: italic;">Access the full RAIN™ Enterprise Security Platform website for comprehensive information and resources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        ### RAIN™ Enterprise Portal
        
        Our enterprise website provides comprehensive information and resources about RAIN™ Enterprise Security Platform:
        
        * 🏢 **Company Information** - Learn about our mission and leadership
        * 📊 **Case Studies** - See how RAIN™ has transformed security for Fortune 500 companies
        * 📈 **ROI Calculator** - Estimate your potential cost savings with RAIN™
        * 📑 **White Papers** - Download technical documentation and research
        * 🛠️ **API Documentation** - Integration guides for developers
        * 📞 **Enterprise Support** - 24/7 dedicated support for enterprise customers
        
        Access the full experience by clicking the button to visit the official website.
        """)
        
        # Mock website URL (would be a real URL in production)
        website_url = "https://rain-enterprise-security.com" 
        
        st.markdown("""
        ### Preview
        
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #fff; margin-top: 20px;">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="background-color: #0068C9; color: white; border-radius: 5px; padding: 10px; margin-right: 15px;">
                    <span style="font-size: 24px; font-weight: bold;">RAIN™</span>
                </div>
                <div>
                    <span style="color: #333; font-weight: bold; font-size: 18px;">Enterprise Security Platform</span>
                </div>
                <div style="margin-left: auto;">
                    <span style="padding: 8px 12px; background-color: #f1f1f1; border-radius: 5px; margin-right: 10px;">Login</span>
                    <span style="padding: 8px 12px; background-color: #0068C9; color: white; border-radius: 5px;">Get Started</span>
                </div>
            </div>
            <div style="height: 200px; background: linear-gradient(135deg, #0068C9, #00C9FF); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: bold; margin-bottom: 20px;">
                Enterprise Security for the AI Age
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div style="width: 30%; height: 80px; background-color: #f5f7fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                        <div style="font-weight: bold; color: #0068C9;">Zero Trust</div>
                        <div style="font-size: 12px; color: #666;">Identity Management</div>
                    </div>
                </div>
                <div style="width: 30%; height: 80px; background-color: #f5f7fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                        <div style="font-weight: bold; color: #0068C9;">AI Analysis</div>
                        <div style="font-size: 12px; color: #666;">Threat Intelligence</div>
                    </div>
                </div>
                <div style="width: 30%; height: 80px; background-color: #f5f7fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                        <div style="font-weight: bold; color: #0068C9;">Quantum Security</div>
                        <div style="font-size: 12px; color: #666;">Future-Proof Protection</div>
                    </div>
                </div>
            </div>
            <div style="color: #999; font-size: 12px; text-align: center; margin-top: 15px;">
                © 2025 RAIN Enterprise Security, Inc. All rights reserved.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Website Access")
        if st.button("🌐 Visit RAIN™ Website", type="primary"):
            st.success("Redirecting to RAIN™ Enterprise Website...")
            # In a real app, this would redirect to the actual website
            # For demonstration purposes, we'll just show a success message
            
            # Show simulated redirect animation
            progress_text = "Redirecting to external website..."
            progress_bar = st.progress(0)
            for i in range(100):
                # Update progress bar
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            
            st.markdown(f"""
            <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px; text-align: center;">
                <p>If you're not automatically redirected, please click:</p>
                <a href="{website_url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #0068C9; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">Open Website</a>
            </div>
            """, unsafe_allow_html=True)
        
        # Add supporting info section
        st.markdown("### Why Visit Our Website?")
        st.markdown("""
        * 🔄 **Always Up-to-Date** - Latest product information and security advisories
        * 🎯 **Personalized Experience** - Content tailored to your industry and needs
        * 💬 **Live Chat Support** - Instant assistance from security experts
        * 🎓 **Training Resources** - Self-paced courses and certification paths
        * 🔍 **Detailed Documentation** - Complete technical specifications
        """)
        
        st.markdown("### Related Resources")
        # Create styled link buttons for related resources
        for resource, icon in [
            ("Security Blog", "📰"),
            ("Customer Portal", "🔑"),
            ("Partner Network", "🤝"),
            ("Developer Hub", "👨‍💻")
        ]:
            st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <a href="#" style="display: block; padding: 8px 12px; background-color: #f5f7fa; border-radius: 5px; color: #333; text-decoration: none; font-size: 14px;">
                    {icon} {resource}
                </a>
            </div>
            """, unsafe_allow_html=True)