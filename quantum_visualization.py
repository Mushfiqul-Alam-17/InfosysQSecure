import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import streamlit as st
import matplotlib.colors as mcolors
import os
from matplotlib.patheffects import withStroke

def create_quantum_animation():
    """
    Create an enhanced animation showing RSA encryption breaking under quantum attack, 
    while lattice-based cryptography rises to save the day.
    
    Returns:
    --------
    animation_bytes: bytes
        Animation encoded as bytes for display or download
    """
    try:
        # Create figure and axis with a darker background for a more professional look
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='#1f1f2e')
        ax.set_facecolor('#1f1f2e')
        
        # Set up axis limits and labels with enhanced styling
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 110)
        ax.set_xlabel('Time (Quantum Attack Progress)', fontsize=12, color='white')
        ax.set_ylabel('Encryption Strength (%)', fontsize=12, color='white')
        ax.set_title('Quantum-Resistant Security Visualization', fontsize=16, 
                    fontweight='bold', color='white', 
                    path_effects=[withStroke(linewidth=1, foreground='#6c7ae0')])
        
        # Create a gradient color for the RSA line (red to dark red)
        rsa_cmap = mcolors.LinearSegmentedColormap.from_list("", ["#ff5252", "#b71c1c"])
        rsa_colors = rsa_cmap(np.linspace(0, 1, 100))
        
        # Create a gradient color for the lattice line (light green to dark green)
        lattice_cmap = mcolors.LinearSegmentedColormap.from_list("", ["#69f0ae", "#00c853"])
        lattice_colors = lattice_cmap(np.linspace(0, 1, 100))
        
        # Initial empty lines with glowing effect
        rsa_line, = ax.plot([], [], '-', linewidth=4, label='RSA Encryption', 
                           color=rsa_colors[0], alpha=0.9)
        lattice_line, = ax.plot([], [], '-', linewidth=4, label='Lattice-based Encryption', 
                              color=lattice_colors[0], alpha=0.9)
        
        # Add glow effects (multiple lines with decreasing alpha)
        rsa_glow = []
        lattice_glow = []
        for i, width in enumerate([6, 8, 10]):
            alpha = 0.1 - i * 0.03
            rsa_glow.append(ax.plot([], [], '-', color=rsa_colors[0], 
                                   linewidth=width, alpha=alpha)[0])
            lattice_glow.append(ax.plot([], [], '-', color=lattice_colors[0], 
                                      linewidth=width, alpha=alpha)[0])
        
        # Text annotations with enhanced styling
        progress_text = ax.text(5, 105, '', fontsize=12, color='white', 
                               bbox=dict(facecolor='#2d2d3a', alpha=0.7, boxstyle='round,pad=0.5'))
        event_text = ax.text(50, 50, '', fontsize=14, ha='center', fontweight='bold', 
                            color='white', alpha=0)
        
        # Add a legend with enhanced styling
        legend = ax.legend(loc='upper right', framealpha=0.7, facecolor='#2d2d3a', 
                         edgecolor='#6c7ae0', fontsize=10)
        plt.setp(legend.get_texts(), color='white')
        
        # Add stylized grid for better readability
        ax.grid(True, alpha=0.2, color='gray', linestyle='-')
        
        # Timeline markers with enhanced styling
        timeline_events = [
            (20, 'Quantum Computer\nReaches 1000 Qubits'),
            (50, 'RSA-2048\nBreakthrough'),
            (75, 'Global Encryption\nCrisis')
        ]
        
        for x, label in timeline_events:
            # Vertical line with pulsing effect
            ax.axvline(x=x, color='#6c7ae0', linestyle='--', alpha=0.5)
            # Text with background
            ax.text(x, 10, label, rotation=90, ha='center', fontsize=9, color='white',
                  bbox=dict(facecolor='#2d2d3a', alpha=0.7, boxstyle='round,pad=0.3'))
        
        # Animation function with enhanced visual effects
        def animate(i):
            # Data for each frame
            x = np.arange(i+1)
            
            # RSA strength - starts high, drops exponentially with a slight oscillation
            rsa_y = 100 * np.exp(-0.05 * x) * (1 + 0.05 * np.sin(x/5))
            
            # Lattice strength - starts at base level, rises to replace RSA with slight oscillation
            lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x)) * (1 + 0.02 * np.sin(x/4))
            
            # Add oscillation for visual interest
            if i > 0:
                rsa_oscillation = 1 + 0.02 * np.sin(i/3)
                lattice_oscillation = 1 + 0.01 * np.sin(i/4)
            else:
                rsa_oscillation = 1
                lattice_oscillation = 1
            
            # Update main lines with dynamic colors
            if i < len(rsa_colors):
                rsa_line.set_color(rsa_colors[i])
                lattice_line.set_color(lattice_colors[i])
            
            rsa_line.set_data(x, rsa_y * rsa_oscillation)
            lattice_line.set_data(x, lattice_y * lattice_oscillation)
            
            # Update glow effects
            for glow in rsa_glow:
                glow.set_data(x, rsa_y * rsa_oscillation)
                if i < len(rsa_colors):
                    glow.set_color(rsa_colors[i])
            
            for glow in lattice_glow:
                glow.set_data(x, lattice_y * lattice_oscillation)
                if i < len(lattice_colors):
                    glow.set_color(lattice_colors[i])
            
            # Update progress text with enhanced styling
            progress_text.set_text(f'Attack Progress: {i}%')
            
            # Dynamic event text appearance with fade-in/fade-out
            if 45 <= i <= 55:
                # RSA compromise alert
                event_alpha = min(1.0, (i - 44) / 2) if i < 50 else max(0, 1 - (i - 50) / 5)
                event_text.set_text('⚠️ RSA ENCRYPTION COMPROMISED! ⚠️')
                event_text.set_position((50, 60))
                event_text.set_color('#ff5252')
                event_text.set_alpha(event_alpha)
                # Add pulsing effect
                size = 14 + np.sin(i/2) * 2
                event_text.set_fontsize(size)
            elif 75 <= i <= 85:
                # Lattice success alert
                event_alpha = min(1.0, (i - 74) / 2) if i < 80 else max(0, 1 - (i - 80) / 5)
                event_text.set_text('✓ LATTICE CRYPTOGRAPHY SECURE ✓')
                event_text.set_position((50, 80))
                event_text.set_color('#69f0ae')
                event_text.set_alpha(event_alpha)
                # Add pulsing effect
                size = 14 + np.sin(i/2) * 2
                event_text.set_fontsize(size)
            else:
                event_text.set_alpha(0)
            
            # Add visual indicators at critical points
            if i == 50:  # RSA breaking point
                ax.scatter([50], [rsa_y[-1]], s=150, color='red', alpha=0.7, marker='*')
            if i == 75:  # Lattice taking over
                ax.scatter([75], [lattice_y[-1]], s=150, color='green', alpha=0.7, marker='*')
            
            return [rsa_line, lattice_line, progress_text, event_text] + rsa_glow + lattice_glow
        
        # Create animation with higher FPS for smoother motion
        ani = animation.FuncAnimation(
            fig, animate, frames=100, interval=80, blit=True
        )
        
        # Save animation to bytes with high quality
        animation_bytes = BytesIO()
        writer = animation.FFMpegWriter(fps=24, bitrate=2400)
        
        try:
            # Save with high quality settings
            ani.save(animation_bytes, writer=writer, dpi=100)
            animation_bytes.seek(0)
            return animation_bytes.read()
        except Exception as e:
            st.warning(f"Could not create animation with FFmpeg: {str(e)}. Using alternative method...")
            # Try alternative method using PillowWriter
            try:
                from matplotlib.animation import PillowWriter
                animation_bytes = BytesIO()
                writer = PillowWriter(fps=15)
                ani.save(animation_bytes, writer=writer)
                animation_bytes.seek(0)
                return animation_bytes.read()
            except Exception as e2:
                st.warning(f"Alternative animation method failed: {str(e2)}. Creating static visualization...")
                
                # Create an enhanced static visualization as fallback
                plt.style.use('dark_background')
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#1f1f2e')
                ax1.set_facecolor('#1f1f2e')
                ax2.set_facecolor('#1f1f2e')
                
                # Beginning state with enhanced styling
                x_start = np.arange(20)
                rsa_y_start = 100 * np.exp(-0.05 * x_start)
                lattice_y_start = 60 + 40 * (1 - np.exp(-0.05 * x_start))
                
                ax1.plot(x_start, rsa_y_start, color='#ff5252', linewidth=4, label='RSA Encryption')
                ax1.plot(x_start, lattice_y_start, color='#69f0ae', linewidth=4, label='Lattice-based Encryption')
                ax1.set_title('Initial Quantum Attack Phase', fontsize=14, color='white')
                ax1.set_xlabel('Time (Quantum Attack Progress)', color='white')
                ax1.set_ylabel('Encryption Strength (%)', color='white')
                ax1.legend(facecolor='#2d2d3a', edgecolor='#6c7ae0')
                ax1.grid(True, alpha=0.2, color='gray')
                ax1.set_xlim(0, 100)
                ax1.set_ylim(0, 110)
                ax1.text(10, 90, 'RSA still secure', color='white', fontsize=10)
                
                # End state with enhanced styling
                x_end = np.arange(100)
                rsa_y_end = 100 * np.exp(-0.05 * x_end)
                lattice_y_end = 60 + 40 * (1 - np.exp(-0.05 * x_end))
                
                ax2.plot(x_end, rsa_y_end, color='#ff5252', linewidth=4, label='RSA Encryption')
                ax2.plot(x_end, lattice_y_end, color='#69f0ae', linewidth=4, label='Lattice-based Encryption')
                ax2.set_title('Final Quantum Attack Phase', fontsize=14, color='white')
                ax2.set_xlabel('Time (Quantum Attack Progress)', color='white')
                ax2.set_ylabel('Encryption Strength (%)', color='white')
                ax2.legend(facecolor='#2d2d3a', edgecolor='#6c7ae0')
                ax2.grid(True, alpha=0.2, color='gray')
                ax2.set_xlim(0, 100)
                ax2.set_ylim(0, 110)
                ax2.text(70, 20, 'RSA compromised', color='#ff5252', fontsize=10)
                ax2.text(70, 80, 'Lattice-based secure', color='#69f0ae', fontsize=10)
                
                plt.tight_layout()
                
                # Save enhanced static image to bytes
                img_bytes = BytesIO()
                plt.savefig(img_bytes, format='png', facecolor=fig.get_facecolor(), dpi=120)
                img_bytes.seek(0)
                return img_bytes.read()
        
    except Exception as e:
        st.error(f"Error creating animation: {str(e)}")
        # Return empty bytes if there's an error
        return BytesIO().read()
