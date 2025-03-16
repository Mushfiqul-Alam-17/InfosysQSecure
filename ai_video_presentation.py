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
    # Remove default Streamlit padding
    st.markdown("""
    <style>
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
            padding-left: 0;
            padding-right: 0;
        }
        .stApp {
            background-color: #f5f7fa;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation bar
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background-color: white; border-bottom: 1px solid #eaeaea;">
        <div>
            <span style="color: #00a3bf; font-size: 24px; font-weight: bold;">RAIN™</span>
        </div>
        <div style="display: flex; align-items: center;">
            <a href="#" style="color: #00a3bf; margin: 0 15px; text-decoration: none; border-bottom: 2px solid #00a3bf; padding-bottom: 5px;">Home</a>
            <a href="#" style="color: #333; margin: 0 15px; text-decoration: none;">Value</a>
            <a href="#" style="color: #333; margin: 0 15px; text-decoration: none;">Dashboard</a>
            <a href="#" style="color: #333; margin: 0 15px; text-decoration: none;">Phases</a>
            <a href="#" style="color: #333; margin: 0 15px; text-decoration: none;">Pitch</a>
        </div>
        <div>
            <button style="background-color: white; color: #00a3bf; border: 1px solid #00a3bf; border-radius: 20px; padding: 8px 15px; font-weight: bold;">Infosys Portal</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; background-color: #f5f7fa; padding: 0 20px; text-align: center;">
        <div style="display: inline-block; background-color: #e6f7f9; color: #00a3bf; padding: 5px 15px; border-radius: 20px; margin-bottom: 20px; font-size: 14px;">
            Real-time AI-driven threat INterceptor and NEutralizer
        </div>
        
        <h1 style="font-size: 62px; font-weight: bold; margin-bottom: 20px; color: #333;">I'm RAIN™</h1>
        
        <p style="font-size: 24px; color: #555; margin-bottom: 40px; max-width: 800px;">
            Here to transform Infosys into the <span style="color: #00a3bf; font-weight: bold;">quantum security leader</span>, saving your clients billions.
        </p>
        
        <button style="background-color: #00a3bf; color: white; border: none; border-radius: 25px; padding: 12px 25px; font-weight: bold; display: flex; align-items: center; cursor: pointer;">
            Discover My Power
            <span style="margin-left: 10px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 5V19M12 19L5 12M12 19L19 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </span>
        </button>
        
        <div style="margin-top: 80px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M12 19L5 12M12 19L19 12" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add the ability to switch between sections
    st.markdown("<br>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Home", "Value", "Dashboard", "Phases", "Pitch"])
    
    with tabs[0]:
        st.markdown("""
        <div style="padding: 40px 20px; background-color: white; border-radius: 10px;">
            <h2 style="color: #333; font-weight: bold; margin-bottom: 20px;">RAIN™ Platform Overview</h2>
            <p style="color: #555; font-size: 18px; line-height: 1.6;">
                RAIN™ is a comprehensive security platform that leverages advanced AI and quantum-resistant cryptography to protect your organization from both current and future threats. Our solution provides real-time monitoring, anomaly detection, and automated response capabilities.
            </p>
            
            <div style="display: flex; justify-content: space-between; margin-top: 40px;">
                <div style="width: 30%; background-color: #f5f7fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #00a3bf; font-weight: bold;">AI-Driven Detection</h3>
                    <p style="color: #555;">Advanced threat intelligence that learns and adapts to emerging attack vectors</p>
                </div>
                <div style="width: 30%; background-color: #f5f7fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #00a3bf; font-weight: bold;">Quantum-Resistant</h3>
                    <p style="color: #555;">Future-proof security that withstands attacks from quantum computers</p>
                </div>
                <div style="width: 30%; background-color: #f5f7fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #00a3bf; font-weight: bold;">Zero Trust Architecture</h3>
                    <p style="color: #555;">Continuous verification of every user, device, and transaction</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("""
        <div style="padding: 40px 20px; background-color: white; border-radius: 10px;">
            <h2 style="color: #333; font-weight: bold; margin-bottom: 20px;">Value Proposition</h2>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 60px; height: 60px; background-color: #e6f7f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 24px; font-weight: bold;">1</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Cost Reduction</h3>
                    <p style="color: #555; font-size: 16px;">
                        Reduce security breach costs by up to 48% through AI-powered early detection and automated response
                    </p>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 60px; height: 60px; background-color: #e6f7f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 24px; font-weight: bold;">2</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Future-Proofing</h3>
                    <p style="color: #555; font-size: 16px;">
                        Protect against quantum computing threats today, avoiding costly emergency upgrades in the future
                    </p>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 60px; height: 60px; background-color: #e6f7f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 24px; font-weight: bold;">3</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Competitive Advantage</h3>
                    <p style="color: #555; font-size: 16px;">
                        Position Infosys as the innovator in quantum security, capturing market share from less prepared competitors
                    </p>
                </div>
            </div>
            
            <div style="background-color: #f5f7fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
                <h3 style="color: #00a3bf; font-weight: bold; text-align: center;">ROI Analysis</h3>
                <p style="color: #555; text-align: center;">
                    Clients implementing RAIN™ have seen an average ROI of 287% within the first 18 months
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("""
        <div style="padding: 40px 20px; background-color: white; border-radius: 10px;">
            <h2 style="color: #333; font-weight: bold; margin-bottom: 20px;">Interactive Security Dashboard</h2>
            <p style="color: #555; font-size: 16px; margin-bottom: 30px;">
                Experience a preview of RAIN™'s enterprise security dashboard, providing real-time threat intelligence and defense metrics.
            </p>
            
            <div style="border: 1px solid #eaeaea; border-radius: 10px; padding: 20px; margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <div style="width: 23%; background-color: #f5f7fa; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="color: #00a3bf; font-weight: bold; margin-bottom: 5px;">96.8%</h4>
                        <p style="color: #555; font-size: 14px; margin: 0;">Threat Detection Rate</p>
                    </div>
                    <div style="width: 23%; background-color: #f5f7fa; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="color: #00a3bf; font-weight: bold; margin-bottom: 5px;">0.3%</h4>
                        <p style="color: #555; font-size: 14px; margin: 0;">False Positive Rate</p>
                    </div>
                    <div style="width: 23%; background-color: #f5f7fa; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="color: #00a3bf; font-weight: bold; margin-bottom: 5px;">1.8s</h4>
                        <p style="color: #555; font-size: 14px; margin: 0;">Avg. Response Time</p>
                    </div>
                    <div style="width: 23%; background-color: #f5f7fa; padding: 15px; border-radius: 8px; text-align: center;">
                        <h4 style="color: #00a3bf; font-weight: bold; margin-bottom: 5px;">29,842</h4>
                        <p style="color: #555; font-size: 14px; margin: 0;">Attacks Prevented (30d)</p>
                    </div>
                </div>
                
                <div style="height: 200px; background-color: #f5f7fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <p style="color: #777; font-style: italic;">Interactive threat map visualization</p>
                </div>
                
                <div style="display: flex; justify-content: space-between;">
                    <div style="width: 48%; height: 150px; background-color: #f5f7fa; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <p style="color: #777; font-style: italic;">Attack vector analysis</p>
                    </div>
                    <div style="width: 48%; height: 150px; background-color: #f5f7fa; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <p style="color: #777; font-style: italic;">Threat actor intelligence</p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <button style="background-color: #00a3bf; color: white; border: none; border-radius: 25px; padding: 10px 20px; font-weight: bold;">
                    Request Live Demo
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("""
        <div style="padding: 40px 20px; background-color: white; border-radius: 10px;">
            <h2 style="color: #333; font-weight: bold; margin-bottom: 20px;">Implementation Phases</h2>
            
            <div style="margin-bottom: 40px;">
                <div style="height: 5px; background-color: #e6e6e6; border-radius: 3px; position: relative; margin: 40px 0;">
                    <div style="position: absolute; left: 0%; top: -8px; width: 20px; height: 20px; background-color: #00a3bf; border-radius: 50%; z-index: 2;"></div>
                    <div style="position: absolute; left: 33%; top: -8px; width: 20px; height: 20px; background-color: #00a3bf; border-radius: 50%; z-index: 2;"></div>
                    <div style="position: absolute; left: 66%; top: -8px; width: 20px; height: 20px; background-color: #00a3bf; border-radius: 50%; z-index: 2;"></div>
                    <div style="position: absolute; left: 100%; top: -8px; width: 20px; height: 20px; background-color: #e6e6e6; border-radius: 50%; z-index: 2;"></div>
                    <div style="position: absolute; left: 0; top: 0; width: 66%; height: 5px; background-color: #00a3bf; border-radius: 3px; z-index: 1;"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div style="width: 25%; text-align: center;">
                        <p style="font-weight: bold; color: #00a3bf;">Phase 1</p>
                        <p style="color: #555; font-size: 14px;">Assessment</p>
                    </div>
                    <div style="width: 25%; text-align: center;">
                        <p style="font-weight: bold; color: #00a3bf;">Phase 2</p>
                        <p style="color: #555; font-size: 14px;">Implementation</p>
                    </div>
                    <div style="width: 25%; text-align: center;">
                        <p style="font-weight: bold; color: #00a3bf;">Phase 3</p>
                        <p style="color: #555; font-size: 14px;">Integration</p>
                    </div>
                    <div style="width: 25%; text-align: center;">
                        <p style="font-weight: bold; color: #777;">Phase 4</p>
                        <p style="color: #555; font-size: 14px;">Optimization</p>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 80px; height: 80px; background-color: #e6f7f9; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 30px; font-weight: bold;">1</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Security Assessment (4 weeks)</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        <li>Comprehensive security audit of existing infrastructure</li>
                        <li>Identify vulnerabilities and integration points</li>
                        <li>Define implementation strategy and success metrics</li>
                    </ul>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 80px; height: 80px; background-color: #e6f7f9; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 30px; font-weight: bold;">2</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Implementation (8 weeks)</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        <li>Deploy core RAIN™ infrastructure and monitoring systems</li>
                        <li>Configure AI models and threat detection algorithms</li>
                        <li>Implement quantum-resistant encryption protocols</li>
                    </ul>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 80px; height: 80px; background-color: #e6f7f9; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #00a3bf; font-size: 30px; font-weight: bold;">3</span>
                </div>
                <div>
                    <h3 style="color: #333; font-weight: bold;">Integration (6 weeks)</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        <li>Connect to existing security systems and data sources</li>
                        <li>Integrate with identity management and access control</li>
                        <li>Configure automated response workflows</li>
                    </ul>
                </div>
            </div>
            
            <div style="display: flex; margin-bottom: 30px;">
                <div style="min-width: 80px; height: 80px; background-color: #f5f7fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                    <span style="color: #777; font-size: 30px; font-weight: bold;">4</span>
                </div>
                <div>
                    <h3 style="color: #777; font-weight: bold;">Optimization (Ongoing)</h3>
                    <ul style="color: #555; padding-left: 20px;">
                        <li>Continuous improvement of detection algorithms</li>
                        <li>Regular security posture assessments</li>
                        <li>Threat intelligence updates and system expansion</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown("""
        <div style="padding: 40px 20px; background-color: white; border-radius: 10px;">
            <h2 style="color: #333; font-weight: bold; margin-bottom: 20px;">Executive Pitch</h2>
            
            <div style="background-color: #f5f7fa; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
                <h3 style="color: #00a3bf; font-weight: bold; margin-bottom: 15px;">The Problem</h3>
                <p style="color: #555; font-size: 16px; line-height: 1.6;">
                    Organizations are facing an unprecedented convergence of security challenges: sophisticated AI-powered attacks, 
                    the looming quantum threat that will break current encryption, and increasingly complex hybrid environments 
                    that traditional security models can't protect.
                </p>
            </div>
            
            <div style="background-color: #f5f7fa; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
                <h3 style="color: #00a3bf; font-weight: bold; margin-bottom: 15px;">Our Solution</h3>
                <p style="color: #555; font-size: 16px; line-height: 1.6;">
                    RAIN™ is a revolutionary security platform that combines quantum-resistant encryption, 
                    AI-driven threat detection, and zero trust architecture in a unified solution that safeguards organizations 
                    against both current and future threats.
                </p>
            </div>
            
            <div style="background-color: #f5f7fa; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
                <h3 style="color: #00a3bf; font-weight: bold; margin-bottom: 15px;">Market Opportunity</h3>
                <ul style="color: #555; font-size: 16px; line-height: 1.6; padding-left: 20px;">
                    <li>$178B global cybersecurity market with 12.3% CAGR</li>
                    <li>Quantum security segment projected to reach $35B by 2028</li>
                    <li>Enterprises allocating 15% more budget to security annually</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <button style="background-color: #00a3bf; color: white; border: none; border-radius: 25px; padding: 12px 25px; font-weight: bold; margin-right: 15px;">
                    Download Pitch Deck
                </button>
                <button style="background-color: white; color: #00a3bf; border: 1px solid #00a3bf; border-radius: 25px; padding: 12px 25px; font-weight: bold;">
                    Book a Demo
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Footer
    st.markdown("""
    <div style="background-color: #333; color: white; padding: 40px 20px; margin-top: 40px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
            <div style="width: 30%;">
                <h3 style="color: #00a3bf; font-weight: bold; margin-bottom: 20px;">RAIN™</h3>
                <p style="color: #ccc; font-size: 14px;">
                    The future of quantum-resistant, AI-driven enterprise security. Protecting what matters most.
                </p>
            </div>
            <div style="width: 20%;">
                <h4 style="color: white; font-weight: bold; margin-bottom: 15px;">Company</h4>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">About Us</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Careers</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Partners</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Contact</a></li>
                </ul>
            </div>
            <div style="width: 20%;">
                <h4 style="color: white; font-weight: bold; margin-bottom: 15px;">Resources</h4>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Documentation</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">White Papers</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Case Studies</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Blog</a></li>
                </ul>
            </div>
            <div style="width: 20%;">
                <h4 style="color: white; font-weight: bold; margin-bottom: 15px;">Connect</h4>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">LinkedIn</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">Twitter</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">YouTube</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" style="color: #ccc; text-decoration: none;">GitHub</a></li>
                </ul>
            </div>
        </div>
        <div style="border-top: 1px solid #555; padding-top: 20px; text-align: center; color: #aaa; font-size: 12px;">
            © 2025 RAIN Enterprise Security, Inc. All rights reserved. | Privacy Policy | Terms of Service
        </div>
    </div>
    """, unsafe_allow_html=True)
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