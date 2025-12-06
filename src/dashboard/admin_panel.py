"""
🎯 AUTHORITY DASHBOARD - Cyberpunk Neon Design
Intelligent Traffic Management System
Colors: Neon Green (#00ff88), Cyan (#00d4ff)
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import cv2
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import textwrap

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.detection.fast_detector import FastDetector
from src.detection.violation_processor import ViolationProcessor
from src.database import db, violation_ops
from src.dashboard.styles import (
    DASHBOARD_CSS, 
    get_header_html, 
    get_stat_card_html,
    get_hero_text_html,
    apply_plotly_theme,
    CHART_COLORS,
    SEVERITY_COLORS,
    STATUS_COLORS
)

# ============================================================================
# 🎯 PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Traffic Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Cyberpunk Neon CSS with cache busting
timestamp = int(time.time())
st.markdown(f"{DASHBOARD_CSS} <style>/* v={timestamp} */</style>", unsafe_allow_html=True)


# ============================================================================
# 🔧 INITIALIZATION
# ============================================================================
def initialize_system():
    """Initialize detection system and database"""
    if 'detector' not in st.session_state:
        try:
            with st.spinner(""):
                st.session_state.detector = FastDetector()
                st.session_state.processor = ViolationProcessor()
        except Exception as e:
            st.error(f"❌ System Initialization Failed: {e}")
            st.stop()

    if 'db_connected' not in st.session_state:
        try:
            db.connect()
            st.session_state.db_connected = True
        except:
            st.session_state.db_connected = False


# ============================================================================
# 🎬 VIDEO PROCESSING - NEON HUD
# ============================================================================
def create_annotated_video(input_path, output_path, sample_rate, progress_placeholder, status_placeholder):
    """Create neon HUD-style annotated video"""
    detector = st.session_state.detector

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False, []

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        return False, []

    # Neon color map (BGR format)
    color_map = {
        'parked_car': (136, 255, 0),       # Neon Green
        'parked_tuktuk': (255, 212, 0),    # Neon Cyan
        'parked_bus': (247, 85, 168),      # Neon Purple
        'parked_van': (0, 170, 255),       # Neon Amber
        'parked_truck': (87, 71, 255),     # Neon Red
        'parked_motorcycle': (255, 255, 0), # Cyan
        'parked_jeep': (255, 0, 255)       # Magenta
    }

    frame_count = 0
    total_detections = 0
    last_detections = []
    all_violations = []

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # Loop video
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Simple frame skipping for performance
        if frame_count % sample_rate != 0:
            frame_count += 1
            continue

        detections = detector.detect_frame(frame)
        last_detections = detections
        total_detections += len(detections)
        
        # Save violations to DB
        for det in detections:
            violation = {
                'frame': frame_count,
                'timestamp': datetime.utcnow(),
                'violation_type': det['class_name'],
                'confidence': float(det['confidence']),
                # Mock data for demo
                'fine_amount': 2500,
                'status': 'pending', 
                'vehicle_type': 'car',
            }
            # Only insert occasionally to avoid DB spam in loop
            if frame_count % (sample_rate * 5) == 0:
                 db['violations'].insert_one(violation)

        annotated = frame.copy()
        
        # Darken for contrast
        overlay = np.zeros(annotated.shape, annotated.dtype)
        annotated = cv2.addWeighted(annotated, 0.8, overlay, 0.2, 0)

        for det in last_detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']
            color = color_map.get(class_name, (136, 255, 0))

            # Neon glow effect (draw multiple times with decreasing alpha)
            for glow in range(3, 0, -1):
                glow_color = tuple(int(c * 0.3) for c in color)
                cv2.rectangle(annotated, (x1-glow, y1-glow), (x2+glow, y2+glow), glow_color, 1)
            
            # HUD corners with neon glow
            corner_len = min(int((x2-x1)*0.2), int((y2-y1)*0.2), 35)
            thickness = 2
            
            cv2.line(annotated, (x1, y1), (x1 + corner_len, y1), color, thickness)
            cv2.line(annotated, (x1, y1), (x1, y1 + corner_len), color, thickness)
            cv2.line(annotated, (x2, y1), (x2 - corner_len, y1), color, thickness)
            cv2.line(annotated, (x2, y1), (x2, y1 + corner_len), color, thickness)
            cv2.line(annotated, (x1, y2), (x1 + corner_len, y2), color, thickness)
            cv2.line(annotated, (x1, y2), (x1, y2 - corner_len), color, thickness)
            cv2.line(annotated, (x2, y2), (x2 - corner_len, y2), color, thickness)
            cv2.line(annotated, (x2, y2), (x2, y2 - corner_len), color, thickness)

            # Label with neon effect
            label = f"{class_name.replace('parked_', '').upper()} {confidence:.0%}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            
            cv2.rectangle(annotated, (x1, y1-25), (x1 + lw + 10, y1-5), (0, 0, 0), -1)
            cv2.putText(annotated, label, (x1 + 5, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        # Neon top bar
        cv2.rectangle(annotated, (0, 0), (width, 50), (5, 5, 5), -1)
        cv2.line(annotated, (0, 50), (width, 50), (136, 255, 0), 1)  # Neon green line

        # Neon text
        cv2.putText(annotated, "LIVE SIMULATION", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (136, 255, 0), 2, cv2.LINE_AA)
        
        # Pulsing dot
        if int(time.time() * 2) % 2 == 0:
            cv2.circle(annotated, (250, 30), 8, (136, 255, 0), -1)
        
        info_text = f"DETECTIONS: {total_detections}"
        cv2.putText(annotated, info_text, (width - 250, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 212, 0), 1, cv2.LINE_AA)
        

        # Convert to RGB for Streamlit
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        progress_placeholder.image(annotated_rgb, use_column_width=True)
        
        frame_count += 1
        
        # Stop button logic (needs to be passed in or check session state)
        if not st.session_state.get('simulation_running', False):
            break

    cap.release()
    return True, []


# ============================================================================
# 📊 ANALYTICS TAB - NEON
# ============================================================================
def show_analytics_tab():
    """Display traffic impact analytics with neon theme"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 3px;">
            TRAFFIC IMPACT ANALYTICS
        </h2>
        <p style="color: #888; font-size: 0.9rem;">Real-time analysis of traffic violations and their impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Violations", "540", "+12%")
    with col2:
        st.metric("Vehicles Affected", "2,340", "+8%")
    with col3:
        st.metric("Avg. Delay Added", "4.2 min", "-5%")
    with col4:
        st.metric("Economic Loss", "LKR 145K", "+15%")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_type = pd.DataFrame({
            'Type': ['Illegal Parking', 'Bus Lane', 'Double Parking', 'Blocking Driveway', 'No Parking Zone'],
            'Count': [245, 89, 67, 95, 44]
        })
        
        fig = go.Figure(data=[go.Pie(
            labels=df_type['Type'],
            values=df_type['Count'],
            hole=0.6,
            marker_colors=['#ffffff', '#cccccc', '#888888', '#444444', '#aaaaaa'],
            textinfo='percent',
            textfont=dict(size=12, color='black'),
        )])
        
        fig.update_layout(
            title=dict(text='Violations by Type', font=dict(color='#ffffff', size=14)),
            paper_bgcolor='rgba(0, 0, 0, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0.8)',
            font=dict(color='#888'),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=10, color='#888')),
            margin=dict(t=50, b=80, l=20, r=20),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        hours = list(range(24))
        violations = [2, 1, 0, 0, 1, 3, 12, 28, 45, 38, 25, 20, 18, 22, 30, 48, 55, 50, 35, 25, 15, 8, 4, 2]
        colors = ['#ffffff' if 7 <= h <= 10 or 16 <= h <= 20 else '#888888' for h in hours]
        
        fig = go.Figure(data=[go.Bar(
            x=hours,
            y=violations,
            marker_color=colors,
            marker_line_width=0,
        )])
        
        fig.update_layout(
            title=dict(text='Hourly Violation Pattern', font=dict(color='#ffffff', size=14)),
            paper_bgcolor='rgba(0, 0, 0, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0.8)',
            font=dict(color='#888'),
            xaxis=dict(title='Hour', gridcolor='rgba(0, 255, 136, 0.05)', tickmode='array', tickvals=[0, 6, 12, 18, 23], ticktext=['12AM', '6AM', '12PM', '6PM', '11PM']),
            yaxis=dict(title='Violations', gridcolor='rgba(0, 255, 136, 0.05)'),
            margin=dict(t=50, b=50, l=50, r=20),
            height=350,
            bargap=0.3
        )
        
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# 📋 EVENTS TAB - NEON
# ============================================================================
def show_events_tab():
    """Display violation events with neon styling"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 3px;">
            DETECTED VIOLATIONS
        </h2>
        <p style="color: #888; font-size: 0.9rem;">Complete list of detected illegal parking events</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Pending", "Warning", "Notified", "Paid"])
    with col2:
        severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Severe"])
    with col3:
        vehicle_filter = st.selectbox("Vehicle Type", ["All", "Car", "TukTuk", "Bus", "Motorcycle", "Van"])
    with col4:
        st.date_input("Date", datetime.now())
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    events = [
        {"ID": "VIO-001", "Plate": "CAB-1234", "Type": "Car", "Location": "Pettah Market", "Time": "10:45 AM", "Duration": "12m", "Status": "Pending", "Severity": "High", "Fine": 3500},
        {"ID": "VIO-002", "Plate": "WP-4567", "Type": "TukTuk", "Location": "Fort Station", "Time": "11:02 AM", "Duration": "5m", "Status": "Warning", "Severity": "Low", "Fine": 0},
        {"ID": "VIO-003", "Plate": "NB-9876", "Type": "Van", "Location": "Borella Junction", "Time": "11:15 AM", "Duration": "45m", "Status": "Notified", "Severity": "Severe", "Fine": 7500},
        {"ID": "VIO-004", "Plate": "KV-1122", "Type": "Bus", "Location": "Maradana", "Time": "11:30 AM", "Duration": "8m", "Status": "Paid", "Severity": "Medium", "Fine": 5000},
        {"ID": "VIO-005", "Plate": "SP-3344", "Type": "Motorcycle", "Location": "Kollupitiya", "Time": "12:05 PM", "Duration": "20m", "Status": "Pending", "Severity": "Medium", "Fine": 2000},
    ]
    
    for event in events:
        status_color = '#ffffff' if event['Status'] == 'Paid' else '#cccccc' if event['Status'] == 'Pending' else '#888888'
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, rgba(0, 0, 0, 0.85), rgba(10, 10, 10, 0.9));
            border: 1px solid rgba(0, 255, 136, 0.15);
            border-left: 4px solid {status_color};
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 1rem;
            align-items: center;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.05);
        ">
            <div>
                <div style="font-family: monospace; font-size: 0.75rem; color: #888888; margin-bottom: 0.25rem;">{event['ID']}</div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #ffffff; letter-spacing: 2px;">{event['Plate']}</div>
                <div style="font-size: 0.8rem; color: #888; margin-top: 0.25rem;">{event['Type']}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #888888; margin-bottom: 0.25rem;">📍 Location</div>
                <div style="color: white; font-size: 0.9rem;">{event['Location']}</div>
                <div style="font-size: 0.8rem; color: #888; margin-top: 0.25rem;">{event['Time']} • {event['Duration']}</div>
            </div>
            <div>
                <span style="
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: rgba(255, 255, 255, 0.1);
                    color: {status_color};
                    border: 1px solid {status_color}40;
                    border-radius: 50px;
                    font-size: 0.7rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 0.5rem;
                    box-shadow: 0 0 10px {status_color}30;
                ">{event['Status']}</span>
                <div style="font-size: 0.75rem; color: #888;">
                    Severity: <span style="color: #ffaa00;">{event['Severity']}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.25rem; color: #ffffff;">
                    LKR {event['Fine']:,}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# ⚠️ WARNINGS TAB - NEON
# ============================================================================
def show_warnings_tab():
    """Display warning system status"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 3px;">
            WARNING SYSTEM STATUS
        </h2>
        <p style="color: #888; font-size: 0.9rem;">Predictive warnings sent to drivers approaching no-parking zones</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Warnings Sent Today", "127", "+15")
    with col2:
        st.metric("Response Rate", "68%", "+5%")
    with col3:
        st.metric("Violations Prevented", "86", "+12")
    with col4:
        st.metric("Avg Response Time", "45s", "-8s")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.1);
    ">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">🎯</span>
            <div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #ffffff; letter-spacing: 2px;">
                    PREDICTIVE WARNING SYSTEM
                </div>
                <div style="font-size: 0.8rem; color: #888888;">NOVELTY FEATURE</div>
            </div>
        </div>
        <p style="color: #888; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Our AI-powered system detects vehicles approaching no-parking zones and sends 
            <strong style="color: #ffffff;">real-time warnings</strong> to drivers before they commit a violation. 
            This preventive approach has reduced violations by <strong style="color: #ffffff;">35%</strong> 
            in monitored areas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Send Test Warning")
    
    col1, col2 = st.columns(2)
    with col1:
        driver_id = st.text_input("Driver ID / Phone", placeholder="Enter driver ID or phone number")
    with col2:
        location = st.selectbox("Location", ["Pettah Market", "Fort Station", "Borella Junction", "Maradana", "Kollupitiya"])
    
    warning_message = st.text_area("Warning Message", 
        value="⚠️ Warning: You are approaching a no-parking zone. Please find an authorized parking area.",
        height=80)
    
    if st.button("📤 Send Warning", type="primary"):
        with st.spinner("Sending warning..."):
            time.sleep(1)
        st.success("✅ Warning sent successfully!")


# ============================================================================
# 💰 FINES TAB - NEON
# ============================================================================
def show_fines_tab():
    """Display fine calculation"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 3px;">
            FINE CALCULATION ENGINE
        </h2>
        <p style="color: #888; font-size: 0.9rem;">Dynamic fine calculation based on vehicle type, duration, and traffic impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Base Fine Structure")
    
    fine_rules = pd.DataFrame({
        'Vehicle Type': ['Car', 'TukTuk', 'Bus', 'Van', 'Truck', 'Motorcycle', 'Jeep'],
        'Base Fine (LKR)': [2000, 1500, 5000, 3000, 4000, 1000, 2500],
        'Peak Hour (1.5x)': [3000, 2250, 7500, 4500, 6000, 1500, 3750],
        'Repeat Offender (+50%)': [3000, 2250, 7500, 4500, 6000, 1500, 3750]
    })
    
    st.dataframe(fine_rules, use_container_width=True, hide_index=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("### Fine Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "TukTuk", "Bus", "Van", "Truck", "Motorcycle", "Jeep"])
        duration = st.slider("Parking Duration (minutes)", 1, 120, 30)
        is_peak = st.checkbox("Peak Hour (7-10 AM, 4-8 PM)")
    
    with col2:
        is_repeat = st.checkbox("Repeat Offender")
        impact_level = st.select_slider("Traffic Impact", options=["Low", "Medium", "High", "Severe"], value="Medium")
    
    base_fines = {'Car': 2000, 'TukTuk': 1500, 'Bus': 5000, 'Van': 3000, 'Truck': 4000, 'Motorcycle': 1000, 'Jeep': 2500}
    impact_multipliers = {'Low': 1.0, 'Medium': 1.5, 'High': 2.0, 'Severe': 2.5}
    
    base = base_fines[vehicle_type]
    duration_factor = min(1 + (duration / 60) * 0.5, 2.0)
    impact_mult = impact_multipliers[impact_level]
    peak_mult = 1.5 if is_peak else 1.0
    repeat_mult = 1.5 if is_repeat else 1.0
    
    final_fine = base * duration_factor * impact_mult * peak_mult * repeat_mult
    
    # Flattened HTML to prevent code block rendering
    html_content = f"""<div style="background: rgba(20, 20, 20, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 4px; padding: 1.5rem; margin-top: 1rem;">
    <div style="font-family: 'Orbitron', sans-serif; color: #ffffff; font-size: 0.9rem; margin-bottom: 1rem; letter-spacing: 2px;">FINE BREAKDOWN</div>
    <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; color: #888; font-size: 0.9rem;">
    <div>Base Fine ({vehicle_type})</div><div style="text-align: right; color: #ffffff;">LKR {base:,}</div>
    <div>Duration Factor ({duration} min)</div><div style="text-align: right; color: #cccccc;">× {duration_factor:.2f}</div>
    <div>Traffic Impact ({impact_level})</div><div style="text-align: right; color: #cccccc;">× {impact_mult:.1f}</div>
    <div>Peak Hour Multiplier</div><div style="text-align: right; color: {'#ffffff' if is_peak else '#666'};">× {peak_mult:.1f}</div>
    <div>Repeat Offender Penalty</div><div style="text-align: right; color: {'#ffffff' if is_repeat else '#666'};">× {repeat_mult:.1f}</div>
    </div>
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.15); margin-top: 1rem; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; text-transform: uppercase; letter-spacing: 1px;">Final Fine</div>
    <div style="font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #ffffff;">LKR {final_fine:,.0f}</div>
    </div></div>"""
    st.markdown(html_content, unsafe_allow_html=True)


# ============================================================================
# ⚙️ ADMIN TAB
# ============================================================================
def show_admin_tab():
    """Admin control panel"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: 3px;">
            ADMIN CONTROL PANEL
        </h2>
        <p style="color: #888; font-size: 0.9rem;">System configuration and management</p>
    </div>
    """, unsafe_allow_html=True)
    
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📷 Cameras", "🚫 No-Parking Zones", "💰 Fine Rules"])
    
    with admin_tab1:
        st.markdown("### Camera Management")
        
        with st.expander("➕ Add New Camera"):
            col1, col2 = st.columns(2)
            with col1:
                cam_name = st.text_input("Camera Name", placeholder="e.g., Pettah Main")
                cam_location = st.text_input("Location", placeholder="e.g., Pettah Market Entrance")
            with col2:
                cam_lat = st.number_input("Latitude", value=6.9271, format="%.4f")
                cam_lng = st.number_input("Longitude", value=79.8612, format="%.4f")
            
            cam_url = st.text_input("Stream URL", placeholder="rtsp://...")
            
            if st.button("➕ Add Camera"):
                st.success(f"✅ Camera '{cam_name}' added successfully!")
        
        cameras = [
            {"name": "Pettah Main", "location": "Pettah Market", "status": "Online", "detections": 245},
            {"name": "Fort Station", "location": "Fort Railway", "status": "Online", "detections": 189},
            {"name": "Borella Cam-1", "location": "Borella Junction", "status": "Offline", "detections": 0},
        ]
        
        for cam in cameras:
            status_color = "#ffffff" if cam['status'] == "Online" else "#888888"
            st.markdown(f"""
            <div style="
                background: rgba(0, 0, 0, 0.7);
                border: 1px solid rgba(0, 255, 136, 0.15);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 0.75rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <div style="color: white; font-weight: 600;">{cam['name']}</div>
                    <div style="color: #666; font-size: 0.8rem;">📍 {cam['location']}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="color: #cccccc; font-size: 0.8rem;">{cam['detections']} detections</div>
                    <div style="
                        padding: 0.25rem 0.75rem;
                        background: {status_color}20;
                        color: {status_color};
                        border: 1px solid {status_color}40;
                        border-radius: 50px;
                        font-size: 0.7rem;
                        font-weight: 600;
                        box-shadow: 0 0 10px {status_color}30;
                    ">{cam['status']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with admin_tab2:
        st.markdown("### No-Parking Zone Configuration")
        st.info("Configure polygon coordinates for no-parking detection zones.")
        
        zone_name = st.text_input("Zone Name", placeholder="e.g., Pettah Bus Stop Area")
        zone_coords = st.text_area("Polygon Coordinates (JSON)", 
            value='[[6.9271, 79.8612], [6.9275, 79.8615], [6.9273, 79.8620], [6.9269, 79.8617]]',
            height=100)
        
        if st.button("💾 Save Zone"):
            st.success("✅ Zone saved successfully!")
    
    with admin_tab3:
        st.markdown("### Fine Rules Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Car Base Fine (LKR)", value=2000, step=100)
            st.number_input("TukTuk Base Fine (LKR)", value=1500, step=100)
            st.number_input("Bus Base Fine (LKR)", value=5000, step=100)
        with col2:
            st.number_input("Van Base Fine (LKR)", value=3000, step=100)
            st.number_input("Truck Base Fine (LKR)", value=4000, step=100)
            st.number_input("Peak Hour Multiplier", value=1.5, step=0.1)
        
        if st.button("💾 Save Fine Rules"):
            st.success("✅ Fine rules updated successfully!")


# ============================================================================
# 🎬 MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    st.markdown(get_header_html("INTELLIGENT TRAFFIC MANAGEMENT SYSTEM", "TRAFFIC COMMAND CENTER | SYSTEM ONLINE"), unsafe_allow_html=True)
    
    initialize_system()
    
    
    # Placeholder for Results (appends via container logic)
    # This empty container sits at the top. Content is injected below.
    results_container = st.container()
    
    st.markdown("---")

    # ============================================================================
    # 🕹️ BOTTOM CONTROL PANEL
    # ============================================================================
    
    # Main Input Section
    st.markdown("""
    <div style="background: rgba(20, 20, 20, 0.5); padding: 20px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 2rem;">
        <h3 style="margin-top: 0; color: #fff; font-family: 'Orbitron', sans-serif;">📡 SIMULATION FEED</h3>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_settings, col_status = st.columns([2, 1, 1])
    
    with col_input:
        st.info("ℹ️ System is running in **Simulation Mode**. Violations will be generated automatically from the demo feed.")
    
    with col_settings:
        st.markdown("**⚡ Analysis Speed**")
        sample_rate = st.slider("Frame Skip", min_value=1, max_value=10, value=3, help="Higher = Faster, Lower = More Accurate")
        
    with col_status:
        st.markdown("**🖥️ System Status**")
        db_status = "Online" if st.session_state.get('db_connected', False) else "Offline"
        db_color = "green" if st.session_state.get('db_connected', False) else "red"
        st.markdown(f"AI Engine: **Ready**")
        st.markdown(f"Database: **:{db_color}[{db_status}]**")
    
    
    with results_container:
        # Default Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📹 LIVE MONITOR", 
            "📊 ANALYTICS", 
            "📋 VIOLATIONS",
            "⚠️ WARNINGS",
            "💰 FINES",
            "⚙️ ADMIN"
        ])
        
        with tab1:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("""
                <div style="margin-bottom: 1rem;">
                    <h3 style="font-family: 'Rajdhani', sans-serif; color: #ffffff; margin: 0;">
                        LIVE FEED ANALYSIS
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Check for simulation file
                sim_path = Path(__file__).parent.parent.parent / "assets" / "simulation.mp4"
                
                if not sim_path.exists():
                    st.error(f"❌ Simulation video not found at: `{sim_path}`")
                    st.warning("Please upload a video file named `simulation.mp4` to the `assets` folder.")
                else:
                    # Toggle for start/stop
                    if 'simulation_running' not in st.session_state:
                        st.session_state.simulation_running = False
                    
                    col_start, col_stop = st.columns(2)
                    with col_start:
                        if st.button("▶ START SIMULATION", type="primary", use_container_width=True, disabled=st.session_state.simulation_running):
                            st.session_state.simulation_running = True
                            st.rerun()
                    with col_stop:
                        if st.button("⏹ STOP SIMULATION", type="secondary", use_container_width=True, disabled=not st.session_state.simulation_running):
                            st.session_state.simulation_running = False
                            st.rerun()

                    if st.session_state.simulation_running:
                        progress_placeholder = st.empty()
                        status_placeholder = st.empty()
                        
                        try:
                            # Run simulation loop
                            create_annotated_video(
                                str(sim_path), None, sample_rate,
                                progress_placeholder, status_placeholder
                            )
                        except Exception as e:
                            st.error(f"❌ Simulation Error: {e}")
                            st.session_state.simulation_running = False

            with col2:
                # Stats are already handled in the loop/above
                pass

        with tab2:
            show_analytics_tab()
        
        with tab3:
            show_events_tab()
        
        with tab4:
            show_warnings_tab()
        
        with tab5:
            show_fines_tab()
        
        with tab6:
            show_admin_tab()
        st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Model Accuracy", "88.3%")
        with col2:
            st.metric("Vehicle Classes", "7")
        with col3:
            st.metric("Total Detections", "540+")
        with col4:
            st.metric("System Status", "Online")

if __name__ == "__main__":
    main()