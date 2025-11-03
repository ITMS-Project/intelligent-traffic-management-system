"""
Parking Violation Detection Dashboard
Real-time monitoring and visualization system
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import sys
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path to import detection pipeline
sys.path.append(str(Path(__file__).parent.parent))
from parking_analysis.detection_pipeline import ParkingViolationDetector


# Page configuration
st.set_page_config(
    page_title="Traffic Management Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .violation-alert {
        background: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .success-alert {
        background: #00C851;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'detector' not in st.session_state:
        st.session_state.detector = None
    if 'violations_history' not in st.session_state:
        st.session_state.violations_history = []
    if 'detection_count' not in st.session_state:
        st.session_state.detection_count = 0


def create_sample_frame(width=1280, height=720):
    """Create a sample frame with simulated traffic"""
    frame = np.ones((height, width, 3), dtype=np.uint8) * 50
    
    # Draw road
    cv2.rectangle(frame, (0, height//3), (width, 2*height//3), (60, 60, 60), -1)
    
    # Draw lane markings
    for i in range(0, width, 100):
        cv2.rectangle(frame, (i, height//2-5), (i+50, height//2+5), (255, 255, 255), -1)
    
    # Draw some "buildings" in background
    cv2.rectangle(frame, (50, 50), (200, height//3), (100, 100, 120), -1)
    cv2.rectangle(frame, (width-200, 50), (width-50, height//3), (100, 100, 120), -1)
    
    # Add text
    cv2.putText(frame, "Baseline Junction - Live Feed", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (width-300, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return frame


def draw_vehicle_boxes(frame, detections):
    """Draw bounding boxes for detected vehicles"""
    annotated = frame.copy()
    
    colors = {
        'car': (0, 255, 0),
        'bus': (255, 165, 0),
        'tuk-tuk': (255, 255, 0),
        'truck': (0, 165, 255),
        'motorcycle': (255, 0, 255)
    }
    
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        color = colors.get(det['class'], (0, 255, 0))
        
        # Draw bbox
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
        
        # Draw label background
        label = f"{det['class']} ({det['confidence']:.2f})"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(annotated, (x1, y1-label_size[1]-10), 
                     (x1+label_size[0], y1), color, -1)
        
        # Draw label text
        cv2.putText(annotated, label, (x1, y1-5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return annotated


def create_impact_gauge(impact_score):
    """Create a gauge chart for impact score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=impact_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Traffic Impact Score"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig


def create_violations_timeline(violations_history):
    """Create timeline chart of violations"""
    if not violations_history:
        return None
    
    df = pd.DataFrame(violations_history)
    
    fig = px.line(df, x='timestamp', y='count', 
                  title='Violations Over Time',
                  labels={'count': 'Number of Violations', 'timestamp': 'Time'})
    
    fig.update_traces(line_color='#FF6B6B', line_width=3)
    fig.update_layout(height=300)
    
    return fig


def main():
    """Main dashboard application"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚦 Intelligent Traffic Management System</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png", 
                width=100)
        st.title("Control Panel")
        
        st.markdown("---")
        
        # System Status
        st.subheader("🟢 System Status")
        st.success("Online and Monitoring")
        
        st.markdown("---")
        
        # Settings
        st.subheader("⚙️ Settings")
        
        confidence_threshold = st.slider(
            "Detection Confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence for vehicle detection"
        )
        
        impact_threshold = st.slider(
            "Impact Alert Threshold",
            min_value=0,
            max_value=100,
            value=75,
            help="Alert when impact score exceeds this value"
        )
        
        st.markdown("---")
        
        # Junction Selection
        st.subheader("📍 Location")
        junction = st.selectbox(
            "Select Junction",
            ["Baseline Junction", "Kanaththa Junction"]
        )
        
        st.markdown("---")
        
        # Statistics
        st.subheader("📊 Session Stats")
        st.metric("Total Detections", st.session_state.detection_count)
        st.metric("Total Violations", len(st.session_state.violations_history))
        
        st.markdown("---")
        
        # Actions
        if st.button("🔄 Reset Statistics", type="primary"):
            st.session_state.violations_history = []
            st.session_state.detection_count = 0
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Live Detection Feed")
        
        # Create placeholder for video feed
        video_placeholder = st.empty()
        
        # Initialize detector if not done
        if st.session_state.detector is None:
            with st.spinner("Initializing detection system..."):
                st.session_state.detector = ParkingViolationDetector()
        
        # Generate sample frame
        frame = create_sample_frame()
        
        # Mock traffic flow data
        traffic_flow = {
            'vehicle_count': np.random.randint(10, 25),
            'avg_speed': np.random.randint(25, 45),
            'lane_density': np.random.uniform(0.4, 0.9)
        }
        
        # Process frame
        result = st.session_state.detector.process_frame(
            frame, 
            frame_id=st.session_state.detection_count,
            traffic_flow=traffic_flow
        )
        
        # Draw detections on frame
        if result['detections'] > 0:
            detections = st.session_state.detector.detector.detect_vehicles(frame)
            annotated_frame = draw_vehicle_boxes(frame, detections)
        else:
            annotated_frame = frame
        
        # Display frame
        video_placeholder.image(
            cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_container_width=True
        )
        
        st.session_state.detection_count += 1
        
        # Detection info
        st.info(f"**Detections:** {result['detections']} vehicles | **Tracked:** {result['tracked_vehicles']} | **Violations:** {len(result['violations'])}")
    
    with col2:
        st.subheader("⚠️ Active Violations")
        
        if result['violations']:
            for violation in result['violations']:
                impact = violation['impact']
                
                severity_emoji = {
                    'LOW': '🟢',
                    'MODERATE': '🟡',
                    'HIGH': '🟠',
                    'SEVERE': '🔴'
                }
                
                emoji = severity_emoji.get(impact['severity'], '⚪')
                
                with st.expander(f"{emoji} {violation['class'].upper()} - {impact['severity']}", expanded=True):
                    st.write(f"**Vehicle ID:** #{violation['vehicle_id']}")
                    st.write(f"**Duration:** {violation['duration']} frames (~{violation['duration']//30}s)")
                    st.write(f"**Impact Score:** {impact['impact_score']}/100")
                    st.write(f"**Vehicles Delayed:** {impact['vehicles_delayed']}")
                    st.write(f"**Time Lost:** {impact['total_time_lost_minutes']} min")
                    
                    if impact['impact_score'] > impact_threshold:
                        st.error("🚨 HIGH IMPACT - IMMEDIATE ACTION REQUIRED")
        else:
            st.success("✅ No active violations detected")
        
        st.markdown("---")
        
        # Traffic metrics
        st.subheader("📊 Traffic Metrics")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                "Vehicle Count",
                traffic_flow['vehicle_count'],
                delta=np.random.randint(-3, 4)
            )
            
            st.metric(
                "Avg Speed",
                f"{traffic_flow['avg_speed']} km/h",
                delta=f"{np.random.randint(-5, 6)} km/h"
            )
        
        with metric_col2:
            st.metric(
                "Lane Density",
                f"{traffic_flow['lane_density']:.0%}",
                delta=f"{np.random.uniform(-0.1, 0.1):.1%}"
            )
            
            congestion_level = "High" if traffic_flow['lane_density'] > 0.7 else "Moderate" if traffic_flow['lane_density'] > 0.4 else "Low"
            st.metric("Congestion", congestion_level)
    
    # Bottom section - Charts
    st.markdown("---")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Impact gauge
        if result['violations']:
            avg_impact = np.mean([v['impact']['impact_score'] for v in result['violations']])
        else:
            avg_impact = np.random.randint(10, 40)
        
        fig_gauge = create_impact_gauge(avg_impact)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with chart_col2:
        # Vehicle distribution
        vehicle_types = ['Car', 'Bus', 'Tuk-tuk', 'Motorcycle', 'Truck']
        vehicle_counts = [np.random.randint(5, 20) for _ in vehicle_types]
        
        fig_pie = px.pie(
            values=vehicle_counts,
            names=vehicle_types,
            title='Vehicle Type Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Auto-refresh
    time.sleep(2)
    st.rerun()


if __name__ == "__main__":
    main()