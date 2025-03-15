import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import streamlit as st
import matplotlib.colors as mcolors
import os, tempfile
from matplotlib.patheffects import withStroke
import time

def create_quantum_animation():
    """
    Create a series of visualizations showing RSA encryption breaking under quantum attack, 
    while lattice-based cryptography rises to save the day.
    
    Returns:
    --------
    animation_path: str
        Path to the animation file or None if using static visualization
    """
    # Create an enhanced static visualization instead of animation
    plt.style.use('dark_background')
    
    # Create more frames for smoother animation
    frames = 8  # Increased from 5 to 8 for smoother transitions
    figs = []
    
    # Enterprise color scheme
    enterprise_colors = {
        'background': '#0F172A',  # Deep navy blue
        'foreground': '#F1F5F9',  # Light blue-gray
        'grid': '#334155',        # Slate gray
        'rsa': '#EF4444',         # Vibrant red
        'lattice': '#10B981',     # Emerald green
        'quantum': '#8B5CF6',     # Purple
        'accent': '#3B82F6',      # Bright blue
        'warning': '#F59E0B',     # Amber
        'secure': '#34D399'       # Green
    }
    
    for frame in range(frames):
        progress = frame * 100 // (frames - 1)  # 0, 14, 28, 42, 57, 71, 85, 100
        
        # Create figure with enterprise styling
        fig, ax = plt.subplots(figsize=(12, 7), facecolor=enterprise_colors['background'])
        ax.set_facecolor(enterprise_colors['background'])
        
        # Set up axis limits and labels with premium styling
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 120)
        ax.set_xlabel('Quantum Computing Evolution Timeline', fontsize=12, color=enterprise_colors['foreground'])
        ax.set_ylabel('Security Protocol Integrity (%)', fontsize=12, color=enterprise_colors['foreground'])
        
        # Add RAIN™ branding to title
        title = f'RAIN™ QUANTUM-RESISTANT SECURITY FRAMEWORK (Progress: {progress}%)'
        ax.set_title(title, fontsize=16, fontweight='bold', color=enterprise_colors['foreground'])
        
        # Generate data points up to current progress
        x = np.arange(progress + 1)
        if len(x) > 0:
            # RSA strength - starts high, drops exponentially with realistic fluctuations
            rsa_y = 100 * np.exp(-0.05 * x) * (1 + 0.05 * np.sin(x/5))
            
            # Lattice strength - starts at base level, rises to replace RSA with minor fluctuations
            lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x)) * (1 + 0.02 * np.sin(x/4))
            
            # Add a third line representing a combined hybrid approach for enterprise clients
            hybrid_y = np.minimum(rsa_y, lattice_y) + 5 + 0.2 * x * (1 + 0.03 * np.sin(x/6))
            hybrid_y = np.minimum(hybrid_y, 115)  # Cap at 115% to stay within bounds
            
            # Plot the three security protocols with enhanced styling
            ax.plot(x, rsa_y, '-', linewidth=4, label='Traditional RSA/ECC', 
                   color=enterprise_colors['rsa'], alpha=0.9)
            ax.plot(x, lattice_y, '-', linewidth=4, label='Lattice-based Post-Quantum', 
                   color=enterprise_colors['lattice'], alpha=0.9)
            ax.plot(x, hybrid_y, '-', linewidth=4, label='RAIN™ Adaptive Hybrid Security', 
                   color=enterprise_colors['accent'], alpha=0.9)
            
            # Add highlight at important points with enhanced visuals
            # RSA breaking point
            if progress >= 50:
                rsa_y_value = rsa_y[50] if len(rsa_y) > 50 else rsa_y[-1]
                ax.scatter([50], [rsa_y_value], s=180, color=enterprise_colors['rsa'], 
                           alpha=0.8, marker='X', edgecolors='white', linewidths=1)
                
                # Add a security breach effect
                breach_radius = min(progress - 50, 25)  # Grows over time
                if breach_radius > 0:
                    breach_circle = plt.Circle((50, rsa_y_value), breach_radius, 
                                             color=enterprise_colors['rsa'], alpha=0.1)
                    ax.add_patch(breach_circle)
                
                # Add warning text with enhanced styling
                ax.text(50, 30, '⚠️ CRITICAL VULNERABILITY', color=enterprise_colors['rsa'],
                        fontsize=12, fontweight='bold', ha='center',
                        bbox=dict(facecolor='#300', alpha=0.7, boxstyle='round,pad=0.5',
                                 edgecolor=enterprise_colors['rsa']))
                
            # Lattice success point
            if progress >= 75:
                lattice_y_value = lattice_y[75] if len(lattice_y) > 75 else lattice_y[-1]
                ax.scatter([75], [lattice_y_value], s=180, color=enterprise_colors['lattice'], 
                           alpha=0.8, marker='*', edgecolors='white', linewidths=1)
                
                # Add a security shield effect
                shield_height = min(progress - 75, 25) * 1.5  # Grows over time
                if shield_height > 0:
                    shield_x = np.linspace(70, 80, 50)
                    shield_y = lattice_y_value + np.sin(np.linspace(0, np.pi, 50)) * shield_height
                    ax.fill_between(shield_x, lattice_y_value, shield_y, 
                                  color=enterprise_colors['lattice'], alpha=0.1)
                
                # Add success text with enhanced styling
                ax.text(75, 80, '✓ QUANTUM SECURE', color=enterprise_colors['lattice'],
                        fontsize=12, fontweight='bold', ha='center',
                        bbox=dict(facecolor='#030', alpha=0.7, boxstyle='round,pad=0.5',
                                 edgecolor=enterprise_colors['lattice']))
            
            # Hybrid solution ultimate security (for RAIN™ branding)
            if progress >= 90 and len(hybrid_y) > 90:
                hybrid_y_value = hybrid_y[90]
                ax.scatter([90], [hybrid_y_value], s=200, color=enterprise_colors['accent'], 
                           alpha=0.9, marker='★', edgecolors='white', linewidths=1.5)
                
                # Add enterprise shield effect
                ax.text(90, hybrid_y_value + 5, '🛡️ RAIN™ PROTECTION', color=enterprise_colors['accent'],
                        fontsize=13, fontweight='bold', ha='center',
                        bbox=dict(facecolor='#001030', alpha=0.8, boxstyle='round,pad=0.5',
                                 edgecolor=enterprise_colors['accent']))
        
        # Add a premium styled legend
        legend = ax.legend(loc='upper right', framealpha=0.8, 
                          facecolor='#101f35', edgecolor=enterprise_colors['accent'],
                          fontsize=10)
        plt.setp(legend.get_texts(), color=enterprise_colors['foreground'])
        
        # Add visually appealing grid
        ax.grid(True, alpha=0.2, color=enterprise_colors['grid'], linestyle='-')
        
        # Add enterprise timeline markers with enhanced visuals
        timeline_events = [
            (20, 'Quantum Computer\nAchieves 4,000 Qubits'),
            (50, 'RSA/ECC\nCryptographic Breach'),
            (75, 'Global Encryption\nMigration Crisis'),
            (90, 'RAIN™ Enterprise\nSecure Framework')
        ]
        
        # Draw timeline with enterprise styling
        ax.axhline(y=5, xmin=0, xmax=1, color=enterprise_colors['grid'], 
                  linewidth=3, alpha=0.5, zorder=0)
        
        for x_pos, label in timeline_events:
            if progress >= x_pos:
                # Vertical timeline marker
                ax.axvline(x=x_pos, color=enterprise_colors['accent'], 
                          linestyle='--', alpha=0.5, linewidth=1.5)
                
                # Enhanced event marker on timeline
                ax.scatter([x_pos], [5], s=100, 
                          color=enterprise_colors['background'],
                          edgecolors=enterprise_colors['accent'], 
                          linewidths=2, zorder=5)
                
                # Event label with professional styling
                ax.text(x_pos, 13, label, rotation=0, ha='center', va='top',
                      fontsize=9, color=enterprise_colors['foreground'], fontweight='bold',
                      bbox=dict(facecolor='#101f35', alpha=0.9, 
                              boxstyle='round,pad=0.4',
                              edgecolor=enterprise_colors['accent']))
        
        # Add explanatory annotations for enterprise clients
        if progress >= 60:
            ax.annotate('Traditional encryption systems\nfail under quantum attack',
                      xy=(50, rsa_y[50] if len(rsa_y) > 50 else rsa_y[-1]),
                      xytext=(30, 60),
                      color=enterprise_colors['foreground'],
                      arrowprops=dict(arrowstyle='->',
                                    color=enterprise_colors['foreground'],
                                    alpha=0.6),
                      fontsize=9, ha='center')
        
        if progress >= 85:
            ax.annotate('RAIN™ adaptive security\nmaintains integrity\nthroughout transition',
                      xy=(85, hybrid_y[85] if len(hybrid_y) > 85 else hybrid_y[-1]),
                      xytext=(70, 110),
                      color=enterprise_colors['foreground'],
                      arrowprops=dict(arrowstyle='->',
                                    color=enterprise_colors['foreground'],
                                    alpha=0.6),
                      fontsize=9, ha='center')
        
        # Add enterprise footer
        footer_text = 'RAIN™ - REAL-TIME AI-DRIVEN QUANTUM-RESISTANT SECURITY FRAMEWORK'
        fig.text(0.5, 0.01, footer_text, ha='center', color=enterprise_colors['foreground'],
                fontsize=9, fontweight='bold', alpha=0.8)
        
        # Add enterprise security metrics for context
        if progress > 30:
            # Create a small metrics panel
            metrics_x, metrics_y = 0.14, 0.15
            metrics_width, metrics_height = 0.2, 0.25
            metrics_ax = fig.add_axes([metrics_x, metrics_y, metrics_width, metrics_height])
            metrics_ax.set_facecolor('#101f35')
            metrics_ax.set_xlim(0, 10)
            metrics_ax.set_ylim(0, 10)
            metrics_ax.axis('off')
            
            # Add metrics title
            metrics_ax.text(5, 9, 'SECURITY METRICS', ha='center', va='top',
                          color=enterprise_colors['foreground'], fontsize=10, fontweight='bold')
            
            # Add security metrics with relevant values that change with progress
            metrics = [
                ('Key Strength:', f"{max(0, 100-progress)}%", enterprise_colors['rsa']),
                ('Attack Risk:', f"{min(100, progress)}%", enterprise_colors['warning']),
                ('Response Time:', f"{min(50, progress//2)}ms", enterprise_colors['accent']),
                ('RAIN™ Protection:', f"{min(99, progress)}%", enterprise_colors['secure']),
            ]
            
            for i, (label, value, color) in enumerate(metrics):
                y_pos = 7.5 - i*1.5
                metrics_ax.text(2, y_pos, label, ha='left', va='center',
                              color=enterprise_colors['foreground'], fontsize=9)
                metrics_ax.text(8, y_pos, value, ha='right', va='center',
                              color=color, fontsize=9, fontweight='bold')
        
        figs.append(fig)
    
    # Generate folder of images to be used as an animation
    try:
        temp_dir = tempfile.mkdtemp()
        animation_frames = []
        
        for i, fig in enumerate(figs):
            # Save each frame as a PNG
            frame_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
            fig.savefig(frame_path, facecolor=fig.get_facecolor(), dpi=100, bbox_inches='tight')
            plt.close(fig)
            animation_frames.append(frame_path)
        
        # Return path to first image along with all frame paths
        if animation_frames:
            # Store paths in session state
            st.session_state.animation_frames = animation_frames
            st.session_state.current_frame = 0
            st.session_state.temp_dir = temp_dir
            
            # Read the first image for immediate display
            with open(animation_frames[0], "rb") as f:
                return f.read()
        
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        
        # Fallback to single static visualization
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 7), facecolor=enterprise_colors['background'])
        ax.set_facecolor(enterprise_colors['background'])
        
        # Create static visualization
        x = np.arange(101)
        rsa_y = 100 * np.exp(-0.05 * x)
        lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x))
        hybrid_y = np.minimum(rsa_y, lattice_y) + 5 + 0.2 * x
        hybrid_y = np.minimum(hybrid_y, 115)
        
        # Plot with professional styling
        ax.plot(x, rsa_y, color=enterprise_colors['rsa'], linewidth=4, label='Traditional RSA/ECC')
        ax.plot(x, lattice_y, color=enterprise_colors['lattice'], linewidth=4, label='Lattice-based Post-Quantum')
        ax.plot(x, hybrid_y, color=enterprise_colors['accent'], linewidth=4, label='RAIN™ Adaptive Hybrid Security')
        
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 120)
        ax.set_xlabel('Quantum Computing Evolution Timeline', color=enterprise_colors['foreground'])
        ax.set_ylabel('Security Protocol Integrity (%)', color=enterprise_colors['foreground'])
        ax.set_title('RAIN™ QUANTUM-RESISTANT SECURITY FRAMEWORK', fontsize=16, fontweight='bold', color=enterprise_colors['foreground'])
        
        # Highlight critical points
        ax.scatter([50], [rsa_y[50]], s=180, color=enterprise_colors['rsa'], marker='X', edgecolors='white', linewidths=1)
        ax.text(50, 30, '⚠️ CRITICAL VULNERABILITY', color=enterprise_colors['rsa'], fontsize=12, fontweight='bold', ha='center')
        
        ax.scatter([75], [lattice_y[75]], s=180, color=enterprise_colors['lattice'], marker='*', edgecolors='white', linewidths=1)
        ax.text(75, 80, '✓ QUANTUM SECURE', color=enterprise_colors['lattice'], fontsize=12, fontweight='bold', ha='center')
        
        ax.scatter([90], [hybrid_y[90]], s=200, color=enterprise_colors['accent'], marker='★', edgecolors='white', linewidths=1.5)
        ax.text(90, hybrid_y[90] + 5, '🛡️ RAIN™ PROTECTION', color=enterprise_colors['accent'], fontsize=13, fontweight='bold', ha='center')
        
        # Professional legend
        legend = ax.legend(loc='upper right', framealpha=0.8, facecolor='#101f35', edgecolor=enterprise_colors['accent'])
        plt.setp(legend.get_texts(), color=enterprise_colors['foreground'])
        ax.grid(True, alpha=0.2, color=enterprise_colors['grid'])
        
        # Footer
        footer_text = 'RAIN™ - REAL-TIME AI-DRIVEN QUANTUM-RESISTANT SECURITY FRAMEWORK'
        fig.text(0.5, 0.01, footer_text, ha='center', color=enterprise_colors['foreground'], fontsize=9, fontweight='bold', alpha=0.8)
        
        # Save static image
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png', facecolor=fig.get_facecolor(), dpi=100, bbox_inches='tight')
        img_bytes.seek(0)
        plt.close(fig)
        
        return img_bytes.read()

def get_next_animation_frame():
    """Get the next frame of the animation if it exists"""
    if 'animation_frames' not in st.session_state or not st.session_state.animation_frames:
        return None
    
    # Increment frame counter
    st.session_state.current_frame = (st.session_state.current_frame + 1) % len(st.session_state.animation_frames)
    frame_path = st.session_state.animation_frames[st.session_state.current_frame]
    
    # Read the next frame
    try:
        with open(frame_path, "rb") as f:
            return f.read()
    except Exception:
        return None
