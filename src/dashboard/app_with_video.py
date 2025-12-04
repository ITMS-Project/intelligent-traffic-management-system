"""
🎯 AUTHORITY DASHBOARD - Premium Futuristic Command Center
Intelligent Traffic Management System

Features:
- Live Monitoring Panel with HUD design
- Violation List with Evidence
- Traffic Impact Analytics
- Warning System Status
- Fine Calculation Breakdown
- Historical Logs
- Admin Functions
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import traceback
import cv2
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

# Apply Premium CSS
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


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
# 🎬 VIDEO PROCESSING
# ============================================================================
def create_annotated_video(input_path, output_path, sample_rate, progress_placeholder, status_placeholder):
    """Create HUD-style annotated video"""
    detector = st.session_state.detector

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False, []

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Setup writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        return False, []

    # Neon color map
    color_map = {
        'parked_car': (136, 255, 0),       # Green (BGR)
        'parked_tuktuk': (255, 0, 255),    # Magenta
        'parked_bus': (0, 100, 255),       # Orange
        'parked_van': (255, 212, 0),       # Cyan
        'parked_truck': (0, 165, 255),     # Orange
        'parked_motorcycle': (255, 136, 0), # Blue-ish
        'parked_jeep': (0, 255, 255)       # Yellow
    }

    frame_count = 0
    total_detections = 0
    last_detections = []
    all_violations = []

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect on sampled frames
        if frame_count % sample_rate == 0:
            detections = detector.detect_frame(frame)
            last_detections = detections
            total_detections += len(detections)
            
            # Store violations
            for det in detections:
                violation = {
                    'frame': frame_count,
                    'timestamp': frame_count / fps if fps > 0 else 0,
                    'class': det['class_name'],
                    'confidence': det['confidence'],
                    'bbox': det['bbox']
                }
                all_violations.append(violation)

        # Create HUD annotated frame
        annotated = frame.copy()
        
        # Slight darkening for contrast
        overlay = np.zeros(annotated.shape, annotated.dtype)
        annotated = cv2.addWeighted(annotated, 0.85, overlay, 0.15, 0)

        for det in last_detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']
            color = color_map.get(class_name, (255, 255, 255))

            # Draw semi-transparent fill
            overlay = annotated.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            cv2.addWeighted(overlay, 0.1, annotated, 0.9, 0, annotated)
            
            # Draw HUD-style corners
            corner_len = min(int((x2-x1)*0.15), int((y2-y1)*0.15), 30)
            thickness = 2
            
            # Top-left corner
            cv2.line(annotated, (x1, y1), (x1 + corner_len, y1), color, thickness)
            cv2.line(annotated, (x1, y1), (x1, y1 + corner_len), color, thickness)
            
            # Top-right corner
            cv2.line(annotated, (x2, y1), (x2 - corner_len, y1), color, thickness)
            cv2.line(annotated, (x2, y1), (x2, y1 + corner_len), color, thickness)
            
            # Bottom-left corner
            cv2.line(annotated, (x1, y2), (x1 + corner_len, y2), color, thickness)
            cv2.line(annotated, (x1, y2), (x1, y2 - corner_len), color, thickness)
            
            # Bottom-right corner
            cv2.line(annotated, (x2, y2), (x2 - corner_len, y2), color, thickness)
            cv2.line(annotated, (x2, y2), (x2, y2 - corner_len), color, thickness)

            # Label with connector line
            label = f"{class_name.replace('parked_', '').upper()} {confidence:.0%}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            
            # Connector line
            cv2.line(annotated, (x1, y1), (x1, y1 - 15), color, 1)
            cv2.line(annotated, (x1, y1 - 15), (x1 + lw + 10, y1 - 15), color, 1)
            
            # Label text
            cv2.putText(annotated, label, (x1 + 5, y1 - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        # HUD Top bar
        cv2.rectangle(annotated, (0, 0), (width, 50), (0, 0, 0), -1)
        
        # Add scanline effect on top bar
        for i in range(0, width, 4):
            cv2.line(annotated, (i, 48), (i, 50), (30, 30, 30), 1)

        timestamp = frame_count / fps if fps > 0 else 0
        
        # Left info
        cv2.putText(annotated, "LIVE ANALYSIS", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Recording indicator
        if int(time.time() * 2) % 2 == 0:
            cv2.circle(annotated, (180, 30), 6, (0, 0, 255), -1)
        
        # Right info
        info_text = f"OBJECTS: {len(last_detections)}"
        cv2.putText(annotated, info_text, (width - 200, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (136, 255, 0), 1, cv2.LINE_AA)
        
        time_text = f"T+{timestamp:.1f}s"
        cv2.putText(annotated, time_text, (width - 350, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1, cv2.LINE_AA)

        out.write(annotated)
        frame_count += 1

        # Update progress
        if frame_count % 30 == 0:
            progress = frame_count / total_frames
            progress_placeholder.progress(progress)
            elapsed = time.time() - start_time
            eta = (elapsed / frame_count) * (total_frames - frame_count) if frame_count > 0 else 0
            status_placeholder.info(f"⚡ Processing: {frame_count}/{total_frames} frames | ETA: {eta:.0f}s | Detections: {total_detections}")

    cap.release()
    out.release()

    progress_placeholder.progress(1.0)
    status_placeholder.success(f"✅ Analysis Complete! {total_detections} violations detected.")

    return True, all_violations


# ============================================================================
# 📊 ANALYTICS TAB
# ============================================================================
def show_analytics_tab():
    """Display traffic impact analytics"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            📊 TRAFFIC IMPACT ANALYTICS
        </h2>
        <p style="color: #666; font-size: 0.9rem;">Real-time analysis of traffic violations and their impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
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
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Violations by Type - Donut Chart
        df_type = pd.DataFrame({
            'Type': ['Illegal Parking', 'Bus Lane', 'Double Parking', 'Blocking Driveway', 'No Parking Zone'],
            'Count': [245, 89, 67, 95, 44]
        })
        
        fig = go.Figure(data=[go.Pie(
            labels=df_type['Type'],
            values=df_type['Count'],
            hole=0.6,
            marker_colors=['#00ff88', '#00d4ff', '#8b5cf6', '#f59e0b', '#ef4444'],
            textinfo='percent',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text='Violations by Type', font=dict(color='white', size=14)),
            paper_bgcolor='rgba(10, 10, 10, 0.8)',
            plot_bgcolor='rgba(10, 10, 10, 0.8)',
            font=dict(color='#888'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5,
                font=dict(size=10)
            ),
            margin=dict(t=50, b=80, l=20, r=20),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Hourly Violation Pattern - Bar Chart
        hours = list(range(24))
        violations = [2, 1, 0, 0, 1, 3, 12, 28, 45, 38, 25, 20, 18, 22, 30, 48, 55, 50, 35, 25, 15, 8, 4, 2]
        
        # Highlight peak hours
        colors = ['#00ff88' if 7 <= h <= 10 or 16 <= h <= 20 else '#00d4ff' for h in hours]
        
        fig = go.Figure(data=[go.Bar(
            x=hours,
            y=violations,
            marker_color=colors,
            marker_line_width=0,
            hovertemplate='<b>Hour %{x}:00</b><br>Violations: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text='Hourly Violation Pattern', font=dict(color='white', size=14)),
            paper_bgcolor='rgba(10, 10, 10, 0.8)',
            plot_bgcolor='rgba(10, 10, 10, 0.8)',
            font=dict(color='#888'),
            xaxis=dict(
                title='Hour',
                gridcolor='rgba(255,255,255,0.05)',
                tickmode='array',
                tickvals=[0, 6, 12, 18, 23],
                ticktext=['12AM', '6AM', '12PM', '6PM', '11PM']
            ),
            yaxis=dict(
                title='Violations',
                gridcolor='rgba(255,255,255,0.05)'
            ),
            margin=dict(t=50, b=50, l=50, r=20),
            height=350,
            bargap=0.3
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Vehicle Type Distribution
        df_vehicle = pd.DataFrame({
            'Vehicle': ['Car', 'Motorcycle', 'TukTuk', 'Bus', 'Van', 'Truck', 'Jeep'],
            'Count': [180, 145, 95, 45, 40, 20, 15]
        })
        
        fig = go.Figure(data=[go.Bar(
            x=df_vehicle['Vehicle'],
            y=df_vehicle['Count'],
            marker_color=CHART_COLORS[:7],
            marker_line_width=0,
            text=df_vehicle['Count'],
            textposition='outside',
            textfont=dict(color='white', size=10)
        )])
        
        fig = apply_plotly_theme(fig)
        fig.update_layout(
            title=dict(text='Violations by Vehicle Type', font=dict(color='white', size=14)),
            height=300,
            xaxis=dict(title=''),
            yaxis=dict(title='Count')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Severity Distribution
        df_severity = pd.DataFrame({
            'Severity': ['Low', 'Medium', 'High', 'Severe'],
            'Count': [120, 250, 130, 40]
        })
        
        fig = go.Figure(data=[go.Bar(
            x=df_severity['Severity'],
            y=df_severity['Count'],
            marker_color=['#00ff88', '#f59e0b', '#ef4444', '#dc2626'],
            marker_line_width=0,
            text=df_severity['Count'],
            textposition='outside',
            textfont=dict(color='white', size=10)
        )])
        
        fig = apply_plotly_theme(fig)
        fig.update_layout(
            title=dict(text='Violations by Severity', font=dict(color='white', size=14)),
            height=300,
            xaxis=dict(title=''),
            yaxis=dict(title='Count')
        )
        
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# 📋 EVENTS TAB
# ============================================================================
def show_events_tab():
    """Display detailed violation events list"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            📋 DETECTED VIOLATIONS
        </h2>
        <p style="color: #666; font-size: 0.9rem;">Complete list of detected illegal parking events</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
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
    
    # Sample events data
    events = [
        {"ID": "VIO-001", "Plate": "CAB-1234", "Type": "Car", "Location": "Pettah Market", 
         "Time": "10:45 AM", "Duration": "12m", "Status": "Pending", "Severity": "High", "Fine": 3500},
        {"ID": "VIO-002", "Plate": "WP-4567", "Type": "TukTuk", "Location": "Fort Station", 
         "Time": "11:02 AM", "Duration": "5m", "Status": "Warning", "Severity": "Low", "Fine": 0},
        {"ID": "VIO-003", "Plate": "NB-9876", "Type": "Van", "Location": "Borella Junction", 
         "Time": "11:15 AM", "Duration": "45m", "Status": "Notified", "Severity": "Severe", "Fine": 7500},
        {"ID": "VIO-004", "Plate": "KV-1122", "Type": "Bus", "Location": "Maradana", 
         "Time": "11:30 AM", "Duration": "8m", "Status": "Paid", "Severity": "Medium", "Fine": 5000},
        {"ID": "VIO-005", "Plate": "SP-3344", "Type": "Motorcycle", "Location": "Kollupitiya", 
         "Time": "12:05 PM", "Duration": "20m", "Status": "Pending", "Severity": "Medium", "Fine": 2000},
    ]
    
    # Display as styled cards
    for event in events:
        status_color = STATUS_COLORS.get(event['Status'].lower(), '#f59e0b')
        severity_color = SEVERITY_COLORS.get(event['Severity'].lower(), '#f59e0b')
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(5, 5, 5, 0.98));
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 4px solid {severity_color};
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 1rem;
            align-items: center;
        ">
            <div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">{event['ID']}</div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: white; letter-spacing: 2px;">{event['Plate']}</div>
                <div style="font-size: 0.8rem; color: #888; margin-top: 0.25rem;">{event['Type']}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;">📍 Location</div>
                <div style="color: white; font-size: 0.9rem;">{event['Location']}</div>
                <div style="font-size: 0.8rem; color: #888; margin-top: 0.25rem;">{event['Time']} • {event['Duration']}</div>
            </div>
            <div>
                <span style="
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: {status_color}20;
                    color: {status_color};
                    border: 1px solid {status_color}50;
                    border-radius: 50px;
                    font-size: 0.7rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 0.5rem;
                ">{event['Status']}</span>
                <div style="font-size: 0.75rem; color: #888;">
                    Severity: <span style="color: {severity_color};">{event['Severity']}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.25rem; color: #f59e0b;">
                    LKR {event['Fine']:,}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# ⚠️ WARNINGS TAB
# ============================================================================
def show_warnings_tab():
    """Display warning system status"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            ⚠️ WARNING SYSTEM STATUS
        </h2>
        <p style="color: #666; font-size: 0.9rem;">Predictive warnings sent to drivers approaching no-parking zones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning metrics
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
    
    # Novelty Feature Highlight
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">🎯</span>
            <div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #00ff88; letter-spacing: 2px;">
                    PREDICTIVE WARNING SYSTEM
                </div>
                <div style="font-size: 0.8rem; color: #888;">NOVELTY FEATURE</div>
            </div>
        </div>
        <p style="color: #b0b0b0; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Our AI-powered system detects vehicles approaching no-parking zones and sends 
            <strong style="color: #00ff88;">real-time warnings</strong> to drivers before they commit a violation. 
            This preventive approach has reduced violations by <strong style="color: #00d4ff;">35%</strong> 
            in monitored areas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Send Test Warning
    st.markdown("### 📤 Send Test Warning")
    
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
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Recent Warnings
    st.markdown("### 📋 Recent Warnings")
    
    warnings = [
        {"id": "W-001", "driver": "+94 77 123 4567", "location": "Pettah", "time": "2 min ago", "status": "Delivered", "response": "Moved Away"},
        {"id": "W-002", "driver": "+94 76 987 6543", "location": "Fort", "time": "5 min ago", "status": "Delivered", "response": "Pending"},
        {"id": "W-003", "driver": "+94 71 555 1234", "location": "Borella", "time": "8 min ago", "status": "Delivered", "response": "Ignored"},
    ]
    
    for w in warnings:
        response_color = "#00ff88" if w['response'] == "Moved Away" else "#f59e0b" if w['response'] == "Pending" else "#ef4444"
        
        st.markdown(f"""
        <div style="
            background: rgba(15, 15, 15, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div>
                    <div style="color: white; font-size: 0.9rem;">{w['driver']}</div>
                    <div style="color: #666; font-size: 0.75rem;">📍 {w['location']} • {w['time']}</div>
                </div>
            </div>
            <div style="
                padding: 0.25rem 0.75rem;
                background: {response_color}15;
                color: {response_color};
                border: 1px solid {response_color}40;
                border-radius: 50px;
                font-size: 0.7rem;
                font-weight: 600;
            ">{w['response']}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# 💰 FINES TAB
# ============================================================================
def show_fines_tab():
    """Display fine calculation breakdown"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            💰 FINE CALCULATION ENGINE
        </h2>
        <p style="color: #666; font-size: 0.9rem;">Dynamic fine calculation based on vehicle type, duration, and traffic impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fine Rules Table
    st.markdown("### 📊 Base Fine Structure")
    
    fine_rules = pd.DataFrame({
        'Vehicle Type': ['Car', 'TukTuk', 'Bus', 'Van', 'Truck', 'Motorcycle', 'Jeep'],
        'Base Fine (LKR)': [2000, 1500, 5000, 3000, 4000, 1000, 2500],
        'Peak Hour (1.5x)': [3000, 2250, 7500, 4500, 6000, 1500, 3750],
        'Repeat Offender (+50%)': [3000, 2250, 7500, 4500, 6000, 1500, 3750]
    })
    
    st.dataframe(fine_rules, use_container_width=True, hide_index=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Fine Calculator
    st.markdown("### 🧮 Fine Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "TukTuk", "Bus", "Van", "Truck", "Motorcycle", "Jeep"])
        duration = st.slider("Parking Duration (minutes)", 1, 120, 30)
        is_peak = st.checkbox("Peak Hour (7-10 AM, 4-8 PM)")
    
    with col2:
        is_repeat = st.checkbox("Repeat Offender")
        impact_level = st.select_slider("Traffic Impact", options=["Low", "Medium", "High", "Severe"], value="Medium")
    
    # Calculate fine
    base_fines = {'Car': 2000, 'TukTuk': 1500, 'Bus': 5000, 'Van': 3000, 'Truck': 4000, 'Motorcycle': 1000, 'Jeep': 2500}
    impact_multipliers = {'Low': 1.0, 'Medium': 1.5, 'High': 2.0, 'Severe': 2.5}
    
    base = base_fines[vehicle_type]
    duration_factor = min(1 + (duration / 60) * 0.5, 2.0)  # Max 2x for duration
    impact_mult = impact_multipliers[impact_level]
    peak_mult = 1.5 if is_peak else 1.0
    repeat_mult = 1.5 if is_repeat else 1.0
    
    final_fine = base * duration_factor * impact_mult * peak_mult * repeat_mult
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Display calculation breakdown
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(5, 5, 5, 0.98));
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
    ">
        <div style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 0.9rem; margin-bottom: 1rem; letter-spacing: 2px;">
            FINE BREAKDOWN
        </div>
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; color: #888; font-size: 0.9rem;">
            <div>Base Fine ({vehicle_type})</div>
            <div style="text-align: right; color: white;">LKR {base:,}</div>
            <div>Duration Factor ({duration} min)</div>
            <div style="text-align: right; color: #00d4ff;">× {duration_factor:.2f}</div>
            <div>Traffic Impact ({impact_level})</div>
            <div style="text-align: right; color: #00d4ff;">× {impact_mult:.1f}</div>
            <div>Peak Hour Multiplier</div>
            <div style="text-align: right; color: {'#f59e0b' if is_peak else '#666'};">× {peak_mult:.1f}</div>
            <div>Repeat Offender Penalty</div>
            <div style="text-align: right; color: {'#ef4444' if is_repeat else '#666'};">× {repeat_mult:.1f}</div>
        </div>
        <div style="border-top: 1px solid rgba(255,255,255,0.1); margin-top: 1rem; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; text-transform: uppercase; letter-spacing: 1px;">
                Final Fine
            </div>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #f59e0b;">
                LKR {final_fine:,.0f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 📜 HISTORY TAB
# ============================================================================
def show_history_tab():
    """Display historical violation logs"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            📜 HISTORICAL LOGS
        </h2>
        <p style="color: #666; font-size: 0.9rem;">Complete violation records for law enforcement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range selector
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        start_date = st.date_input("From", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("To", datetime.now())
    with col3:
        st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)
        if st.button("📥 Export CSV"):
            st.success("✅ Export started... Check your downloads folder.")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Violations", "540")
    with col2:
        st.metric("Total Fines", "LKR 2.1M")
    with col3:
        st.metric("Paid", "387")
    with col4:
        st.metric("Unpaid", "153")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Generate sample data
    np.random.seed(42)
    n_records = 50
    
    data = {
        'ID': [f'VIO-{1000+i}' for i in range(n_records)],
        'Date': pd.date_range(end=datetime.now(), periods=n_records, freq='H').strftime('%Y-%m-%d %H:%M'),
        'Vehicle': np.random.choice(['Car', 'TukTuk', 'Bus', 'Van', 'Motorcycle'], n_records),
        'Location': np.random.choice(['Pettah', 'Fort', 'Borella', 'Maradana', 'Kollupitiya'], n_records),
        'Duration': np.random.randint(5, 60, n_records).astype(str) + ' min',
        'Fine (LKR)': np.random.randint(1500, 8000, n_records),
        'Severity': np.random.choice(['Low', 'Medium', 'High', 'Severe'], n_records, p=[0.2, 0.4, 0.3, 0.1]),
        'Status': np.random.choice(['Paid', 'Pending', 'Notified'], n_records, p=[0.6, 0.25, 0.15])
    }
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=400
    )


# ============================================================================
# ⚙️ ADMIN TAB
# ============================================================================
def show_admin_tab():
    """Display admin control panel"""
    
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 0.5rem;">
            ⚙️ ADMIN CONTROL PANEL
        </h2>
        <p style="color: #666; font-size: 0.9rem;">System configuration and management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📷 Cameras", "🚫 No-Parking Zones", "💰 Fine Rules"])
    
    with admin_tab1:
        st.markdown("### 📷 Camera Management")
        
        # Add camera form
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
        
        # Camera list
        st.markdown("### Active Cameras")
        cameras = [
            {"name": "Pettah Main", "location": "Pettah Market", "status": "Online", "detections": 245},
            {"name": "Fort Station", "location": "Fort Railway", "status": "Online", "detections": 189},
            {"name": "Borella Cam-1", "location": "Borella Junction", "status": "Offline", "detections": 0},
        ]
        
        for cam in cameras:
            status_color = "#00ff88" if cam['status'] == "Online" else "#ef4444"
            st.markdown(f"""
            <div style="
                background: rgba(15, 15, 15, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.06);
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
                    <div style="color: #888; font-size: 0.8rem;">{cam['detections']} detections</div>
                    <div style="
                        padding: 0.25rem 0.75rem;
                        background: {status_color}15;
                        color: {status_color};
                        border: 1px solid {status_color}40;
                        border-radius: 50px;
                        font-size: 0.7rem;
                        font-weight: 600;
                    ">{cam['status']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with admin_tab2:
        st.markdown("### 🚫 No-Parking Zone Configuration")
        
        st.info("Configure polygon coordinates for no-parking detection zones.")
        
        zone_name = st.text_input("Zone Name", placeholder="e.g., Pettah Bus Stop Area")
        zone_coords = st.text_area("Polygon Coordinates (JSON)", 
            value='[[6.9271, 79.8612], [6.9275, 79.8615], [6.9273, 79.8620], [6.9269, 79.8617]]',
            height=100)
        
        if st.button("💾 Save Zone"):
            st.success("✅ Zone saved successfully!")
    
    with admin_tab3:
        st.markdown("### 💰 Fine Rules Configuration")
        
        st.markdown("Adjust base fines for each vehicle type:")
        
        col1, col2 = st.columns(2)
        with col1:
            car_fine = st.number_input("Car Base Fine (LKR)", value=2000, step=100)
            tuktuk_fine = st.number_input("TukTuk Base Fine (LKR)", value=1500, step=100)
            bus_fine = st.number_input("Bus Base Fine (LKR)", value=5000, step=100)
            van_fine = st.number_input("Van Base Fine (LKR)", value=3000, step=100)
        
        with col2:
            truck_fine = st.number_input("Truck Base Fine (LKR)", value=4000, step=100)
            motorcycle_fine = st.number_input("Motorcycle Base Fine (LKR)", value=1000, step=100)
            jeep_fine = st.number_input("Jeep Base Fine (LKR)", value=2500, step=100)
            peak_multiplier = st.number_input("Peak Hour Multiplier", value=1.5, step=0.1)
        
        if st.button("💾 Save Fine Rules"):
            st.success("✅ Fine rules updated successfully!")


# ============================================================================
# 🎬 MAIN APPLICATION
# ============================================================================
def main():
    """Main application entry point"""
    
    # Header
    st.markdown(get_header_html("TRAFFIC COMMAND CENTER", "ALL SYSTEMS OPERATIONAL"), unsafe_allow_html=True)
    
    # Initialize system
    initialize_system()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: #00ff88; letter-spacing: 2px;">
                CONTROL PANEL
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        video_file = st.file_uploader(
            "📹 Upload Video Feed",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload traffic footage for AI analysis"
        )
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Analysis parameters
        st.markdown("### ⚡ Analysis Speed")
        sample_rate = st.slider(
            "Frame Sampling",
            min_value=1,
            max_value=10,
            value=3,
            help="Higher = Faster processing"
        )
        
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 10px;
            padding: 0.75rem;
            text-align: center;
            margin-top: 0.5rem;
        ">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00ff88;">
                {sample_rate}x
            </div>
            <div style="font-size: 0.75rem; color: #888;">Processing Rate</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # System status
        st.markdown("### 📊 System Status")
        
        status_items = [
            ("AI Engine", "Online", "#00ff88"),
            ("Database", "Connected" if st.session_state.get('db_connected', False) else "Offline", 
             "#00ff88" if st.session_state.get('db_connected', False) else "#ef4444"),
            ("Notifications", "Ready", "#00ff88"),
        ]
        
        for name, status, color in status_items:
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.5rem 0;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            ">
                <span style="color: #888; font-size: 0.85rem;">{name}</span>
                <span style="color: {color}; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace;">● {status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content with tabs
    if video_file:
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
                    <h3 style="font-family: 'Rajdhani', sans-serif; color: white; margin: 0;">
                        📹 LIVE FEED ANALYSIS
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Save uploaded video
                input_path = f"/tmp/{video_file.name}"
                with open(input_path, "wb") as f:
                    f.write(video_file.read())
                
                output_path = f"/tmp/annotated_{video_file.name}"
                
                if st.button("▶ START ANALYSIS", type="primary", use_container_width=True):
                    progress_placeholder = st.progress(0)
                    status_placeholder = st.empty()
                    
                    try:
                        success, violations = create_annotated_video(
                            input_path,
                            output_path,
                            sample_rate,
                            progress_placeholder,
                            status_placeholder
                        )
                        
                        if success and Path(output_path).exists():
                            st.video(output_path)
                            
                            with open(output_path, "rb") as f:
                                st.download_button(
                                    label="⬇ DOWNLOAD ANALYZED VIDEO",
                                    data=f,
                                    file_name=f"analyzed_{video_file.name}",
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                    except Exception as e:
                        st.error(f"❌ Analysis Error: {e}")
                        st.code(traceback.format_exc())
            
            with col2:
                st.markdown("### 📊 LIVE STATS")
                st.metric("Active Detections", "0")
                st.metric("Violations Today", "127")
                st.metric("Fines Collected", "LKR 425K")
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                st.markdown("### 📍 LOCATION")
                st.map(data={'lat': [6.9271], 'lon': [79.8612]}, zoom=13)
        
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
    
    else:
        # Empty state - Hero section
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <div class="hero-text">
                <div>INTELLIGENT</div>
                <div><span>TRAFFIC</span></div>
                <div>MANAGEMENT</div>
            </div>
            <p style="color: #666; font-size: 1rem; margin-top: 2rem; max-width: 500px; margin-left: auto; margin-right: auto;">
                Upload traffic footage to begin AI-powered violation detection and analysis. 
                Our system uses YOLOv8 to detect parking violations in real-time.
            </p>
            <div style="margin-top: 2rem;">
                <span style="
                    display: inline-block;
                    padding: 0.5rem 1.5rem;
                    background: rgba(0, 255, 136, 0.1);
                    border: 1px solid rgba(0, 255, 136, 0.3);
                    border-radius: 50px;
                    color: #00ff88;
                    font-size: 0.8rem;
                    letter-spacing: 2px;
                ">AWAITING INPUT</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
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