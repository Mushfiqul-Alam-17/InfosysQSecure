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
    
    # Create 5 frames to illustrate the progression
    frames = 5
    figs = []
    for frame in range(frames):
        progress = frame * 100 // (frames - 1)  # 0, 25, 50, 75, 100
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1f1f2e')
        ax.set_facecolor('#1f1f2e')
        
        # Set up axis limits and labels with enhanced styling
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 110)
        ax.set_xlabel('Time (Quantum Attack Progress)', fontsize=12, color='white')
        ax.set_ylabel('Encryption Strength (%)', fontsize=12, color='white')
        ax.set_title(f'Quantum-Resistant Security Visualization (Progress: {progress}%)', 
                     fontsize=16, fontweight='bold', color='white')
        
        # Generate data points up to current progress
        x = np.arange(progress + 1)
        if len(x) > 0:
            # RSA strength - starts high, drops exponentially
            rsa_y = 100 * np.exp(-0.05 * x) * (1 + 0.05 * np.sin(x/5))
            
            # Lattice strength - starts at base level, rises to replace RSA
            lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x)) * (1 + 0.02 * np.sin(x/4))
            
            # Plot RSA and Lattice lines
            ax.plot(x, rsa_y, '-', linewidth=4, label='RSA Encryption', color='#ff5252', alpha=0.9)
            ax.plot(x, lattice_y, '-', linewidth=4, label='Lattice-based Encryption', color='#69f0ae', alpha=0.9)
            
            # Add highlight at important points
            if progress >= 50:  # RSA breaking point
                ax.scatter([50], [rsa_y[50] if len(rsa_y) > 50 else rsa_y[-1]], 
                           s=150, color='red', alpha=0.7, marker='*')
                ax.text(50, 30, '⚠️ RSA BROKEN', color='#ff5252', 
                        fontsize=12, fontweight='bold', ha='center')
                
            if progress >= 75:  # Lattice success
                ax.scatter([75], [lattice_y[75] if len(lattice_y) > 75 else lattice_y[-1]], 
                           s=150, color='green', alpha=0.7, marker='*')
                ax.text(75, 80, '✓ LATTICE SECURE', color='#69f0ae', 
                        fontsize=12, fontweight='bold', ha='center')
        
        # Add a legend
        legend = ax.legend(loc='upper right', framealpha=0.7, facecolor='#2d2d3a', edgecolor='#6c7ae0')
        plt.setp(legend.get_texts(), color='white')
        
        # Add grid
        ax.grid(True, alpha=0.2, color='gray', linestyle='-')
        
        # Add timeline markers
        timeline_events = [
            (20, 'Quantum Computer\nReaches 1000 Qubits'),
            (50, 'RSA-2048\nBreakthrough'),
            (75, 'Global Encryption\nCrisis')
        ]
        
        for x_pos, label in timeline_events:
            if progress >= x_pos:
                ax.axvline(x=x_pos, color='#6c7ae0', linestyle='--', alpha=0.5)
                ax.text(x_pos, 10, label, rotation=90, ha='center', fontsize=9, color='white',
                      bbox=dict(facecolor='#2d2d3a', alpha=0.7, boxstyle='round,pad=0.3'))
        
        figs.append(fig)
    
    # Generate folder of images to be used as an animation
    try:
        temp_dir = tempfile.mkdtemp()
        animation_frames = []
        
        for i, fig in enumerate(figs):
            # Save each frame as a PNG
            frame_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
            fig.savefig(frame_path, facecolor=fig.get_facecolor(), dpi=100)
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
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1f1f2e')
        ax.set_facecolor('#1f1f2e')
        
        # Create static visualization
        x = np.arange(101)
        rsa_y = 100 * np.exp(-0.05 * x)
        lattice_y = 60 + 40 * (1 - np.exp(-0.05 * x))
        
        ax.plot(x, rsa_y, color='#ff5252', linewidth=4, label='RSA Encryption')
        ax.plot(x, lattice_y, color='#69f0ae', linewidth=4, label='Lattice-based Encryption')
        
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 110)
        ax.set_xlabel('Time (Quantum Attack Progress)', color='white')
        ax.set_ylabel('Encryption Strength (%)', color='white')
        ax.set_title('Quantum-Resistant Security Visualization', fontsize=14, color='white')
        
        # Highlight critical points
        ax.scatter([50], [rsa_y[50]], s=150, color='red', alpha=0.7, marker='*')
        ax.text(50, 30, 'RSA BROKEN', color='#ff5252', fontsize=10, ha='center')
        
        ax.scatter([75], [lattice_y[75]], s=150, color='green', alpha=0.7, marker='*')
        ax.text(75, 80, 'LATTICE SECURE', color='#69f0ae', fontsize=10, ha='center')
        
        legend = ax.legend(facecolor='#2d2d3a', edgecolor='#6c7ae0')
        plt.setp(legend.get_texts(), color='white')
        ax.grid(True, alpha=0.2, color='gray')
        
        # Save static image
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png', facecolor=fig.get_facecolor(), dpi=100)
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
