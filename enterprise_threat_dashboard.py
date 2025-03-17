import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import random
import json
import math

class EnterpriseThreatDashboard:
    """
    Enterprise-grade threat dashboard with active monitoring capabilities
    for the RAIN™ Real-Time AI-Driven Threat Interceptor and Neutralizer
    """
    
    def __init__(self):
        """Initialize the enterprise threat dashboard with advanced simulation capabilities"""
        # Initialize session state variables for enterprise dashboard
        if 'threat_history' not in st.session_state:
            st.session_state.threat_history = []
        if 'network_events' not in st.session_state:
            # Initialize with realistic network events
            st.session_state.network_events = self._generate_sample_network_events()
        if 'security_posture' not in st.session_state:
            st.session_state.security_posture = 85  # Default security score out of 100
        if 'active_threats' not in st.session_state:
            st.session_state.active_threats = []
            
        # Live Threat Intelligence Simulation
        if 'last_threat_update' not in st.session_state:
            st.session_state.last_threat_update = time.time()
            
        if 'simulation_data' not in st.session_state:
            # Predefined threat scenarios for simulation
            st.session_state.simulation_data = {
                'threat_scenarios': [
                    {"type": "Ransomware", "severity": "Critical", "location": "Mumbai", "coords": [19.0760, 72.8777], "actor": "BlackMamba"},
                    {"type": "Phishing Campaign", "severity": "High", "location": "Bangalore", "coords": [12.9716, 77.5946], "actor": "SilentViper"},
                    {"type": "Data Exfiltration", "severity": "Critical", "location": "Delhi", "coords": [28.6139, 77.2090], "actor": "CosmicPanda"},
                    {"type": "DDoS Attack", "severity": "Medium", "location": "Chennai", "coords": [13.0827, 80.2707], "actor": "StormRider"},
                    {"type": "Zero-day Exploit", "severity": "Critical", "location": "Hyderabad", "coords": [17.3850, 78.4867], "actor": "Equation Group"},
                    {"type": "Credential Theft", "severity": "High", "location": "Pune", "coords": [18.5204, 73.8567], "actor": "ShadowHammer"},
                    {"type": "Supply Chain Attack", "severity": "Critical", "location": "Kolkata", "coords": [22.5726, 88.3639], "actor": "EmberBear"},
                    {"type": "Insider Threat", "severity": "Medium", "location": "Ahmedabad", "coords": [23.0225, 72.5714], "actor": "Internal Actor"},
                ],
                'global_hotspots': [
                    {"location": "Beijing", "coords": [39.9042, 116.4074], "threat_level": 0.8},
                    {"location": "Moscow", "coords": [55.7558, 37.6173], "threat_level": 0.75},
                    {"location": "Tehran", "coords": [35.6892, 51.3890], "threat_level": 0.7},
                    {"location": "Pyongyang", "coords": [39.0392, 125.7625], "threat_level": 0.65},
                    {"location": "Kiev", "coords": [50.4501, 30.5234], "threat_level": 0.6},
                    {"location": "San Francisco", "coords": [37.7749, -122.4194], "threat_level": 0.55},
                    {"location": "London", "coords": [51.5074, -0.1278], "threat_level": 0.5},
                    {"location": "Singapore", "coords": [1.3521, 103.8198], "threat_level": 0.45},
                ],
                'user_profiles': [
                    {"id": "admin_user", "typing_patterns": [4.2, 4.5, 4.3, 4.6, 4.4], "mouse_patterns": [320, 330, 310, 325, 315]},
                    {"id": "finance_user", "typing_patterns": [3.8, 3.9, 4.0, 3.7, 3.8], "mouse_patterns": [290, 300, 285, 295, 305]},
                    {"id": "suspicious_user", "typing_patterns": [8.5, 8.7, 8.9, 8.6, 8.8], "mouse_patterns": [550, 560, 570, 555, 565]},
                    {"id": "bot_user", "typing_patterns": [1.5, 1.6, 1.5, 1.5, 1.6], "mouse_patterns": [120, 120, 121, 120, 120]},
                ]
            }
        
        # Auto-update simulation timer
        if 'auto_update_enabled' not in st.session_state:
            st.session_state.auto_update_enabled = True
            
        # Incident progression for demo
        if 'incident_phase' not in st.session_state:
            st.session_state.incident_phase = 0
            
        # Hidden demonstration controls
        if 'demo_controls_visible' not in st.session_state:
            st.session_state.demo_controls_visible = False
            
        # STIX/TAXII Feed Integration Simulation
        if 'stix_taxii_connected' not in st.session_state:
            st.session_state.stix_taxii_connected = False
            
        if 'stix_intelligence' not in st.session_state:
            # Intelligence data from simulated STIX/TAXII feed
            st.session_state.stix_intelligence = {
                'threat_actors': ['APT29', 'Lazarus Group', 'Sandworm Team', 'BlackMamba', 'SilentViper', 'CosmicPanda'],
                'malware_types': ['Ransomware', 'Backdoor', 'Trojan', 'Wiper', 'Cryptojacker', 'Rootkit'],
                'attack_vectors': ['Phishing', 'Supply Chain', 'Zero-day Exploit', 'Credential Stuffing', 'Man-in-the-Middle'],
                'industries_targeted': ['Financial', 'Healthcare', 'Critical Infrastructure', 'Government', 'Technology', 'Education']
            }
            
    def _generate_sample_network_events(self):
        """Generate sample network events for demonstration purposes"""
        # Create sample timestamps in the last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        # Create 50 random events
        timestamps = [start_time + timedelta(minutes=random.randint(1, 24*60)) for _ in range(50)]
        timestamps.sort()
        
        # Different types of events
        event_types = [
            "Authentication",
            "File Access",
            "Network Connection",
            "Database Query",
            "API Request",
            "System Command"
        ]
        
        # Event outcomes
        outcomes = ["Success", "Success", "Success", "Success", "Failure", "Suspicious"]
        
        # Generate source IPs with some patterns
        def generate_ip():
            if random.random() < 0.7:  # 70% internal
                return f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
            else:  # 30% external
                return f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        
        # Create event data
        events = []
        for ts in timestamps:
            event_type = random.choice(event_types)
            outcome = random.choice(outcomes)
            source_ip = generate_ip()
            
            # Create risk score - higher for suspicious/failure outcomes
            if outcome == "Suspicious":
                risk_score = random.randint(70, 95)
            elif outcome == "Failure":
                risk_score = random.randint(40, 70)
            else:
                risk_score = random.randint(5, 40)
                
            events.append({
                "timestamp": ts,
                "event_type": event_type,
                "outcome": outcome,
                "source_ip": source_ip,
                "risk_score": risk_score,
                "target_resource": f"srv-{random.randint(1, 20):02d}.{random.choice(['web', 'db', 'auth', 'api', 'app'])}.internal",
                "user": f"user{random.randint(1, 50):03d}"
            })
        
        return events
    
    def add_threat_event(self, threat_level, details, source="Biometric Analysis"):
        """Add a new threat event to the history"""
        event = {
            "timestamp": datetime.now(),
            "threat_level": threat_level,
            "details": details,
            "source": source,
            "status": "Active" if threat_level in ["Critical", "High"] else "Monitoring"
        }
        
        st.session_state.threat_history.append(event)
        
        # If it's a high or critical threat, add to active threats
        if threat_level in ["Critical", "High"]:
            st.session_state.active_threats.append(event)
            
        # Update security posture score based on threat
        if threat_level == "Critical":
            st.session_state.security_posture = max(40, st.session_state.security_posture - 20)
        elif threat_level == "High":
            st.session_state.security_posture = max(60, st.session_state.security_posture - 10)
        elif threat_level == "Medium":
            st.session_state.security_posture = max(70, st.session_state.security_posture - 5)
    
    def display_security_posture(self):
        """Display the enterprise security posture score with animated lightning bolt effect"""
        score = st.session_state.security_posture
        
        # Determine color based on score - using blue theme as requested
        if score >= 80:
            color = "#1565C0"  # Blue
            status = "Strong"
            gradient = "linear-gradient(135deg, #051937, #004d7a, #008793)"
        elif score >= 60:
            color = "#0277BD"  # Lighter blue
            status = "Caution"
            gradient = "linear-gradient(135deg, #023475, #0277BD, #039BE5)"
        else:
            color = "#01579B"  # Deeper blue
            status = "At Risk"
            gradient = "linear-gradient(135deg, #01579B, #0288D1, #03A9F4)"
            
        # Use streamlit components.html for more advanced visualization
        from streamlit.components.v1 import html
        
        # Create enhanced security posture display with lightning bolt animation
        
        # First, define the CSS part as a separate string to avoid f-string parsing issues
        css_part = """
        <style>
            @keyframes lightning-flash {
                0% { opacity: 0; }
                10% { opacity: 0.8; background: white; }
                15% { opacity: 0.2; }
                20% { opacity: 0.9; background: rgba(255,255,255,0.9); }
                25% { opacity: 0.3; }
                30% { opacity: 0; }
                100% { opacity: 0; }
            }
            
            @keyframes pulse {
                0% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 rgba(255,255,255,0.7); }
                70% { transform: scale(1.2); opacity: 0.7; box-shadow: 0 0 0 10px rgba(255,255,255,0); }
                100% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 rgba(255,255,255,0); }
            }
            
            .pulse-circle {
                animation: pulse 2s infinite;
            }
            
            .lightning {
                opacity: 0;
                clip-path: polygon(
                    50% 0%, 
                    65% 30%, 
                    100% 30%, 
                    60% 50%, 
                    75% 70%, 
                    40% 70%, 
                    40% 100%, 
                    25% 60%, 
                    0% 60%, 
                    35% 40%
                );
            }
            
            .bolt1 {
                animation: lightning-flash 7s infinite;
                animation-delay: 1s;
            }
            
            .bolt2 {
                animation: lightning-flash 8s infinite;
                animation-delay: 3s;
            }
            
            .bolt3 {
                animation: lightning-flash 6s infinite;
                animation-delay: 5s;
            }
        </style>
        """
        
        # Now create the HTML with dynamic content
        security_posture_html = f"""
        <div style="padding: 20px; border-radius: 10px; background: {gradient}; color: white; position: relative; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <!-- Animated lightning bolts in the background -->
            <div id="lightning-container" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; overflow: hidden;">
                <div class="lightning bolt1" style="position: absolute; top: 10%; left: 15%; height: 60%; width: 8%;"></div>
                <div class="lightning bolt2" style="position: absolute; top: 5%; left: 60%; height: 50%; width: 6%;"></div>
                <div class="lightning bolt3" style="position: absolute; top: 40%; left: 80%; height: 45%; width: 5%;"></div>
            </div>
            
            <!-- Content container above the lightning -->
            <div style="position: relative; z-index: 2;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Security Posture</h2>
                    <div class="pulse-circle" style="background-color: white; width: 15px; height: 15px; border-radius: 50%; margin-right: 10px;"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 25px 0 15px 0;">
                    <div style="font-size: 18px; font-weight: bold;">Status: <span style="font-size: 22px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">{status}</span></div>
                    <div style="font-size: 42px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.4);">{score}</div>
                </div>
                
                <div style="height: 15px; background-color: rgba(255,255,255,0.3); border-radius: 10px; width: 100%; margin-bottom: 15px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);">
                    <div style="height: 100%; width: {score}%; background-color: white; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; font-size: 14px; opacity: 0.9;">
                    <div>Last updated: Today at {datetime.now().strftime('%H:%M:%S')}</div>
                    <div>Trend: {'+2 points' if score > 70 else '-1 point'} this week</div>
                </div>
            </div>
        </div>
        
        {css_part}
        """
        
        # Display using HTML component
        html(security_posture_html, height=250)
        
    def display_active_threats_summary(self):
        """Display a summary of active threats"""
        active_threats = st.session_state.active_threats
        
        if not active_threats:
            st.success("No active threats detected in your environment")
            return
        
        # Group threats by level
        critical = [t for t in active_threats if t["threat_level"] == "Critical"]
        high = [t for t in active_threats if t["threat_level"] == "High"]
        medium = [t for t in active_threats if t["threat_level"] == "Medium"]
        
        # Display summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if critical:
                st.error(f"**Critical Threats:** {len(critical)}")
            else:
                st.success("**Critical Threats:** 0")
                
        with col2:
            if high:
                st.warning(f"**High Threats:** {len(high)}")
            else:
                st.success("**High Threats:** 0")
                
        with col3:
            if medium:
                st.info(f"**Medium Threats:** {len(medium)}")
            else:
                st.success("**Medium Threats:** 0")
        
        # Display the most recent active threat
        if active_threats:
            most_recent = max(active_threats, key=lambda x: x["timestamp"])
            
            st.markdown("### Most Recent Threat")
            
            if most_recent["threat_level"] == "Critical":
                alert_color = "#0d47a1"  # Blue
            elif most_recent["threat_level"] == "High":
                alert_color = "#ff9800"  # Orange
            else:
                alert_color = "#2196f3"  # Blue
                
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 5px; background-color: {alert_color}15; border-left: 5px solid {alert_color}; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; color: {alert_color};">{most_recent["threat_level"]} Threat</span>
                    <span style="color: #666;">{most_recent["timestamp"].strftime("%Y-%m-%d %H:%M:%S")}</span>
                </div>
                <p style="margin-bottom: 0;"><strong>Source:</strong> {most_recent["source"]}</p>
                <p style="margin-bottom: 0;"><strong>Details:</strong> {most_recent["details"]}</p>
            </div>
            """, unsafe_allow_html=True)

    def display_threat_timeline(self):
        """Display a timeline of detected threats"""
        threats = st.session_state.threat_history
        
        if not threats:
            st.info("No threat history available yet")
            return
            
        # Create timeline data
        dates = [t["timestamp"] for t in threats]
        threat_levels = [t["threat_level"] for t in threats]
        
        # Map threat levels to numeric values for visualization
        level_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "None": 0}
        y_values = [level_map[level] for level in threat_levels]
        
        # Create mapped colors for threat levels
        colors = {
            "Critical": "#0d47a1",  # Blue
            "High": "#ff9800",      # Orange
            "Medium": "#ffeb3b",    # Yellow
            "Low": "#4caf50",       # Green
            "None": "#2196f3"       # Blue
        }
        point_colors = [colors[level] for level in threat_levels]
        
        # Create the timeline visualization
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Plot events as scatter points
        ax.scatter(dates, y_values, c=point_colors, s=100, zorder=5)
        
        # Connect points with lines
        ax.plot(dates, y_values, color='#aaaaaa', linestyle='-', linewidth=1, alpha=0.3, zorder=1)
        
        # Format y-axis to show threat levels
        ax.set_yticks(list(level_map.values()))
        ax.set_yticklabels(list(level_map.keys()))
        
        # Format x-axis to show dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        fig.autofmt_xdate()
        
        # Add grid and styling
        ax.grid(True, alpha=0.3)
        ax.set_title("RAIN™ Threat Detection Timeline", fontsize=14)
        ax.set_xlabel("Date & Time")
        ax.set_ylabel("Threat Level")
        
        # Show the timeline
        st.pyplot(fig)
        
        # Display a table of recent threats
        st.markdown("### Recent Threat Events")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(threats)
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Show most recent 5 entries
        st.dataframe(df.tail(5)[['timestamp', 'threat_level', 'source', 'details', 'status']], 
                    use_container_width=True)
        
    def display_network_activity(self):
        """Display network activity with potential threat detection"""
        events = st.session_state.network_events
        
        if not events:
            st.info("No network activity data available")
            return
            
        # Create a time-based visualization of events
        st.markdown("### Network Activity Monitoring")
        
        # Convert to DataFrame
        df = pd.DataFrame(events)
        
        # Group by event type
        event_counts = df.groupby('event_type').size().reset_index(name='count')
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(event_counts['event_type'], event_counts['count'], alpha=0.7)
        
        # Color bars by count (higher counts get attention colors)
        norm = plt.Normalize(event_counts['count'].min(), event_counts['count'].max())
        colors = plt.cm.YlOrRd(norm(event_counts['count']))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
            
        ax.set_xlabel('Event Type')
        ax.set_ylabel('Event Count (24h)')
        ax.set_title('Network Activity by Event Type')
        
        # Rotate labels for better readability
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        
        # Display the chart
        st.pyplot(fig)
        
        # Show high-risk events
        high_risk_events = df[df['risk_score'] > 60].sort_values('risk_score', ascending=False)
        
        if not high_risk_events.empty:
            st.markdown("### High Risk Network Events")
            
            # Format timestamps
            high_risk_events['timestamp'] = high_risk_events['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Display as a table
            st.dataframe(
                high_risk_events[['timestamp', 'event_type', 'source_ip', 'risk_score', 'outcome', 'target_resource']], 
                use_container_width=True
            )
        else:
            st.success("No high-risk network events detected")

    def display_enterprise_threat_map(self):
        """Display a global threat map visualization"""
        st.markdown("### RAIN™ Global Threat Intelligence Map")
        
        # Add STIX/TAXII connection options
        with st.expander("STIX/TAXII Integration Settings"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                stix_taxii_url = st.text_input(
                    "STIX/TAXII Feed URL",
                    value="https://cti-taxii.mitre.org/taxii/",
                    help="Enter the URL of your STIX/TAXII server"
                )
                
                stix_collection = st.selectbox(
                    "Select Collection",
                    ["enterprise-attack", "mobile-attack", "ics-attack", "pre-attack"]
                )
                
            with col2:
                if st.button("Connect to STIX Feed", type="primary"):
                    with st.spinner("Connecting to STIX/TAXII feed..."):
                        # In a real implementation, this would use taxii2client to connect
                        time.sleep(2)  # Simulate connection time
                        st.session_state.stix_taxii_connected = True
                        st.success("Connected to STIX/TAXII feed!")
                        
                if st.session_state.stix_taxii_connected:
                    if st.button("Refresh Intelligence"):
                        with st.spinner("Updating threat intelligence..."):
                            time.sleep(1.5)  # Simulate refresh time
                            st.success("Threat intelligence updated!")
                
        # Display the global threat map with real-time intelligence
        if st.session_state.stix_taxii_connected:
            st.markdown("""
            <div style="background-color: #0a192f; padding: 20px; border-radius: 5px; position: relative; height: 300px; overflow: hidden;">
                <div style="position: absolute; top: 10px; left: 10px; color: white; font-size: 18px; font-weight: bold;">
                    Global Threat Intelligence
                </div>
                <div style="position: absolute; top: 40px; left: 10px; color: #64ffda; font-size: 14px;">
                    Live monitoring active • 152 nodes reporting
                </div>
                <div style="position: absolute; bottom: 10px; right: 10px; color: white; font-size: 12px;">
                    Data refreshed: Just now
                </div>
                <div style="position: absolute; top: 80px; left: 50%; transform: translateX(-50%); color: white; text-align: center;">
                    <span style="font-size: 22px; color: #64ffda;">Enterprise Threat Map</span><br>
                    <span style="font-size: 14px; color: #4caf50;">✓ STIX/TAXII feed connected</span>
                </div>
                
                <!-- Simulated threat indicators on map -->
                <div style="position: absolute; top: 150px; left: 120px; width: 8px; height: 8px; background-color: #1976D2; border-radius: 50%; box-shadow: 0 0 10px #1976D2;"></div>
                <div style="position: absolute; top: 180px; left: 250px; width: 6px; height: 6px; background-color: #2196F3; border-radius: 50%; box-shadow: 0 0 8px #2196F3;"></div>
                <div style="position: absolute; top: 120px; left: 320px; width: 10px; height: 10px; background-color: #0d47a1; border-radius: 50%; box-shadow: 0 0 12px #0d47a1;"></div>
                <div style="position: absolute; top: 200px; left: 180px; width: 7px; height: 7px; background-color: #42a5f5; border-radius: 50%; box-shadow: 0 0 9px #42a5f5;"></div>
                <div style="position: absolute; top: 140px; left: 380px; width: 6px; height: 6px; background-color: #64b5f6; border-radius: 50%; box-shadow: 0 0 8px #64b5f6;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display STIX intelligence below the map
            st.markdown("### Current Threat Intelligence")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Active Threat Actors")
                # Ensure all arrays have the same length
                threat_actors_list = st.session_state.stix_intelligence["threat_actors"]
                actors_count = len(threat_actors_list)
                
                # Generate matching confidence and dates arrays
                confidence_scores = [92, 88, 76, 85, 79, 83][:actors_count]
                first_seen_dates = ["2023-11-15", "2024-01-03", "2024-02-27", "2024-01-18", "2023-12-10", "2024-02-05"][:actors_count]
                
                threat_actors = pd.DataFrame({
                    "Actor": threat_actors_list,
                    "Confidence": confidence_scores,
                    "First Seen": first_seen_dates
                })
                st.dataframe(threat_actors, use_container_width=True)
            
            with col2:
                st.markdown("#### Attack Vectors")
                # Ensure all arrays have the same length
                attack_vectors_list = st.session_state.stix_intelligence["attack_vectors"]
                vectors_count = len(attack_vectors_list)
                
                # Generate matching frequency array
                frequencies = ["High", "Medium", "Low", "Critical", "Low"][:vectors_count]
                
                attack_vectors = pd.DataFrame({
                    "Vector": attack_vectors_list,
                    "Frequency": frequencies
                })
                st.dataframe(attack_vectors, use_container_width=True)
        else:
            # Original display without STIX/TAXII connection
            st.markdown("""
            <div style="background-color: #0a192f; padding: 20px; border-radius: 5px; position: relative; height: 300px; overflow: hidden;">
                <div style="position: absolute; top: 10px; left: 10px; color: white; font-size: 18px; font-weight: bold;">
                    Global Threat Intelligence
                </div>
                <div style="position: absolute; top: 40px; left: 10px; color: #64ffda; font-size: 14px;">
                    Live monitoring active • 152 nodes reporting
                </div>
                <div style="position: absolute; bottom: 10px; right: 10px; color: white; font-size: 12px;">
                    Data refreshed: Just now
                </div>
                <div style="position: absolute; top: 120px; left: 50%; transform: translateX(-50%); color: white; text-align: center;">
                    <span style="font-size: 22px; color: #64ffda;">Enterprise Threat Map</span><br>
                    <span style="font-size: 14px; color: #8892b0;">Connect to live STIX/TAXII feed for actual threat intelligence</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display statistics below the map
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Threats", "17", delta="-3")
            
        with col2:
            st.metric("Blocked Attacks", "1,284", delta="26")
            
        with col3:
            st.metric("Time to Detect", "1.2s", delta="-0.3s")
            
        with col4:
            st.metric("Current Risk Level", "Medium", delta=None)
    
    def display_keystroke_rhythm_analysis(self, typing_data=None):
        """Display advanced keystroke rhythm analysis"""
        st.markdown("### Keystroke Rhythm Analysis")
        
        if typing_data is None or len(typing_data) < 5:
            st.info("Insufficient typing data for rhythm analysis")
            return
            
        # Create sample keystroke rhythm data
        # In a real system, this would be actual intervals between keypresses
        intervals = np.diff(typing_data)
        
        if len(intervals) == 0:
            st.info("More typing data needed for rhythm analysis")
            return
            
        # Calculate metrics
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        consistency = 100 * (1 - min(1, std_interval / mean_interval))
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Interval", f"{mean_interval:.2f}s")
            
        with col2:
            st.metric("Rhythm Consistency", f"{consistency:.1f}%")
            
        with col3:
            rhythm_match = random.randint(70, 99)  # In real system, this would be compared to baseline
            st.metric("Baseline Match", f"{rhythm_match}%", delta=f"{rhythm_match-85}" if rhythm_match != 85 else None)
        
        # Visualize the keystroke pattern
        fig, ax = plt.subplots(figsize=(10, 3))
        
        # Plot intervals
        x = np.arange(len(intervals))
        ax.plot(x, intervals, color='#0068C9', linewidth=2, marker='o')
        
        # Add user baseline for comparison (simulated)
        baseline = np.random.normal(mean_interval, std_interval*0.8, len(intervals))
        ax.plot(x, baseline, color='gray', linewidth=1, linestyle='--', alpha=0.5, label='User Baseline')
        
        # Add styling
        ax.set_xlabel('Keystroke Number')
        ax.set_ylabel('Time Between Keystrokes (s)')
        ax.set_title('Keystroke Rhythm Pattern Analysis')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Add typing pattern analysis
        st.markdown("""
        #### Biometric Authentication Factors
        
        RAIN™ analyzes multiple factors in your typing pattern:
        
        1. **Rhythm Consistency**: How regular your typing intervals are
        2. **Pressure Pattern**: Key hold durations and release timing
        3. **Error Correction**: How you fix typing mistakes
        4. **Digraph Timing**: Speeds between specific character combinations
        5. **Trigraph Patterns**: Three-character sequence timing
        
        These factors create a unique behavioral fingerprint that's extremely difficult to forge.
        """)
    
    def display_enterprise_dashboard(self):
        """Display the main enterprise security dashboard"""
        st.markdown("""
        <div style="text-align: center; padding: 10px; background-color: #f0f7ff; border-radius: 5px; margin-bottom: 20px;">
            <h1 style="color: #0068C9; margin-bottom: 0;">RAIN™ Enterprise Security Command Center</h1>
            <p style="color: #666;">Real-Time AI-Driven Threat Interceptor and Neutralizer</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the security posture score
        self.display_security_posture()
        
        # Show active threats summary
        st.markdown("## Threat Status")
        self.display_active_threats_summary()
        
        # Display map and network status
        col1, col2 = st.columns([3, 2])
        
        with col1:
            self.display_enterprise_threat_map()
            
        with col2:
            # Simulate security notifications
            st.markdown("### Security Notifications")
            
            st.markdown("""
            <div style="border-left: 4px solid #0d47a1; padding-left: 15px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #0d47a1;">Critical: Unusual Admin Activity</div>
                <div style="font-size: 12px; color: #666;">2 minutes ago</div>
                <div>Administrative account accessed outside business hours</div>
            </div>
            
            <div style="border-left: 4px solid #1976D2; padding-left: 15px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #1976D2;">Warning: Multiple Failed Logins</div>
                <div style="font-size: 12px; color: #666;">15 minutes ago</div>
                <div>5 failed login attempts for user jsmith</div>
            </div>
            
            <div style="border-left: 4px solid #2196f3; padding-left: 15px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #2196f3;">Info: Security Scan Complete</div>
                <div style="font-size: 12px; color: #666;">1 hour ago</div>
                <div>Scheduled endpoint scan completed with 0 issues</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add response options
            st.markdown("### Autonomous Response")
            st.selectbox("Set response level:", 
                       ["Monitor Only", "Alert Only", "Active Response (User Approval)", "Full Autonomous Response"],
                       index=2)
                       
            response_col1, response_col2 = st.columns(2)
            with response_col1:
                st.button("Acknowledge All", type="primary")
            with response_col2:
                st.button("Escalate to SOC")
        
        # Show detailed sections
        tab1, tab2, tab3 = st.tabs(["Threat Timeline", "Network Activity", "Keystroke Analysis"])
        
        with tab1:
            self.display_threat_timeline()
            
        with tab2:
            self.display_network_activity()
            
        with tab3:
            if 'typing_speeds' in st.session_state:
                self.display_keystroke_rhythm_analysis(st.session_state.typing_speeds)
            else:
                st.info("No typing data available yet. Use the biometric analyzer to generate data.")
        
        # Add compliance and reporting footer
        st.markdown("""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-weight: bold;">Compliance Status:</span> SOC 2, ISO 27001, GDPR, HIPAA
                </div>
                <div>
                    <span style="font-weight: bold;">Last Report:</span> Daily Security Summary (Today, 00:00)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)