import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import streamlit as st

def create_quantum_animation():
    """
    Create an animation showing RSA encryption breaking under quantum attack, 
    while lattice-based cryptography rises to save the day.
    
    Returns:
    --------
    animation_bytes: bytes
        Animation encoded as bytes for display or download
    """
    try:
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Set up axis limits and labels
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 110)
        ax.set_xlabel('Time (Quantum Attack Progress)', fontsize=12)
        ax.set_ylabel('Encryption Strength (%)', fontsize=12)
        ax.set_title('Quantum-Resistant Security', fontsize=14, fontweight='bold')
        
        # Initial empty lines
        rsa_line, = ax.plot([], [], 'r-', linewidth=3, label='RSA Encryption')
        lattice_line, = ax.plot([], [], 'g-', linewidth=3, label='Lattice-based Encryption')
        
        # Text annotations
        progress_text = ax.text(10, 85, '', fontsize=10)
        event_text = ax.text(50, 50, '', fontsize=12, ha='center', fontweight='bold')
        
        # Legend
        ax.legend(loc='upper right')
        
        # Add grid for better readability
        ax.grid(True, alpha=0.3)
        
        # Timeline markers
        timeline_events = [
            (20, 'Quantum Computer\nReaches 1000 Qubits'),
            (50, 'RSA-2048\nBroken'),
            (75, 'Global Encryption\nCrisis')
        ]
        
        for x, label in timeline_events:
            ax.axvline(x=x, color='gray', linestyle='--', alpha=0.5)
            ax.text(x, 10, label, rotation=90, ha='center', fontsize=8)
        
        # Animation function
        def animate(i):
            # Data for each frame
            x = np.arange(i+1)
            
            # RSA strength - starts high, drops exponentially
            rsa_y = 100 * np.exp(-0.05 * x)
            
            # Lattice strength - starts at base level, rises to replace RSA
            lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x))
            
            # Update lines
            rsa_line.set_data(x, rsa_y)
            lattice_line.set_data(x, lattice_y)
            
            # Update text
            progress_text.set_text(f'Attack Progress: {i}%')
            
            # Add dramatic events text
            if 45 <= i <= 55:
                event_text.set_text('RSA ENCRYPTION COMPROMISED!')
                event_text.set_position((50, 50))
                event_text.set_color('red')
            elif 75 <= i <= 85:
                event_text.set_text('LATTICE CRYPTOGRAPHY SAVES THE DAY')
                event_text.set_position((50, 70))
                event_text.set_color('green')
            else:
                event_text.set_text('')
            
            return rsa_line, lattice_line, progress_text, event_text
        
        # Create animation (100 frames)
        ani = animation.FuncAnimation(
            fig, animate, frames=100, interval=100, blit=True
        )
        
        # Save animation to bytes
        animation_bytes = BytesIO()
        writer = animation.FFMpegWriter(fps=15, bitrate=1800)
        
        try:
            ani.save(animation_bytes, writer=writer)
            animation_bytes.seek(0)
            return animation_bytes.read()
        except Exception as e:
            # If FFMpeg is not available, create a fallback static image
            st.warning(f"Could not create animation: {str(e)}. Displaying static image instead.")
            
            # Create static image showing beginning and end states
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Beginning state
            x_start = np.arange(10)
            rsa_y_start = 100 * np.exp(-0.05 * x_start)
            lattice_y_start = 60 + 40 * (1 - np.exp(-0.05 * x_start))
            
            ax1.plot(x_start, rsa_y_start, 'r-', linewidth=3, label='RSA Encryption')
            ax1.plot(x_start, lattice_y_start, 'g-', linewidth=3, label='Lattice-based Encryption')
            ax1.set_title('Start of Quantum Attack')
            ax1.set_xlabel('Time (Quantum Attack Progress)')
            ax1.set_ylabel('Encryption Strength (%)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # End state
            x_end = np.arange(100)
            rsa_y_end = 100 * np.exp(-0.05 * x_end)
            lattice_y_end = 60 + 40 * (1 - np.exp(-0.05 * x_end))
            
            ax2.plot(x_end, rsa_y_end, 'r-', linewidth=3, label='RSA Encryption')
            ax2.plot(x_end, lattice_y_end, 'g-', linewidth=3, label='Lattice-based Encryption')
            ax2.set_title('End of Quantum Attack')
            ax2.set_xlabel('Time (Quantum Attack Progress)')
            ax2.set_ylabel('Encryption Strength (%)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save static image to bytes
            img_bytes = BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            return img_bytes.read()
        
    except Exception as e:
        st.error(f"Error creating animation: {str(e)}")
        # Return empty bytes if there's an error
        return BytesIO().read()
