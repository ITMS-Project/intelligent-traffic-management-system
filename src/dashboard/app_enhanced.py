"""
Enhanced Parking Violation Detection Dashboard
Real-time monitoring with MongoDB and YOLOv8 integration
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import sys
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.detection.realtime_detector import RealtimeDetector
from src.detection.violation_processor import ViolationProcessor
from src.database import db, violation_ops, detection_log_ops

# Page configuration
st.set_page_config(
    page_title="Traffic Management Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh every 5 seconds
count = st_autorefresh(interval=5000, limit=None, key="data_refresh")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
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
    .stMetric {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_system():
    """Initialize detection system and database connection"""
    if 'detector' not in st.session_state:
        try:
            with st.spinner("Loading YOLOv8 model..."):
                st.session_state.detector = RealtimeDetector()
                st.session_state.processor = ViolationProcessor()
                st.success("✅ Detection system loaded!")
        except FileNotFoundError as e:
            st.error(f"❌ Model not found: {e}")
            st.info("Please ensure your trained model is at: runs/parking_violations/exp/weights/best.pt")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading detector: {e}")
            st.stop()

    if 'db_connected' not in st.session_state:
        try:
            db.connect()
            st.session_state.db_connected = True
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            st.warning("Running in offline mode - statistics unavailable")
            st.session_state.db_connected = False


def get_statistics(days=7):
    """Get violation statistics from database"""
    if not st.session_state.get('db_connected', False):
        return None

    try:
        stats = violation_ops.get_statistics(days=days)
        return stats
    except Exception as e:
        st.error(f"Error loading statistics: {e}")
        return None


def create_impact_gauge(impact_score):
    """Create a gauge chart for impact score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=impact_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Traffic Impact Score"},
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

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_violations_timeline(days=7):
    """Create timeline chart of violations from database"""
    if not st.session_state.get('db_connected', False):
        return None

    try:
        # Get violations from last N days
        start_date = datetime.utcnow() - timedelta(days=days)
        violations = violation_ops.collection.find(
            {"timestamp": {"$gte": start_date}}
        ).sort("timestamp", 1)

        violations_list = list(violations)
        if not violations_list:
            return None

        df = pd.DataFrame(violations_list)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('date').size().reset_index(name='count')

        fig = px.line(
            daily_counts,
            x='date',
            y='count',
            title=f'Violations Over Last {days} Days',
            labels={'count': 'Number of Violations', 'date': 'Date'}
        )

        fig.update_traces(line_color='#FF6B6B', line_width=3)
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))

        return fig
    except Exception as e:
        st.error(f"Error creating timeline: {e}")
        return None


def process_video_upload(video_file, location):
    """Process uploaded video and detect violations"""
    # Save uploaded file temporarily
    temp_path = f"/tmp/{video_file.name}"
    with open(temp_path, "wb") as f:
        f.write(video_file.read())

    # Process video
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("Processing video...")

    try:
        stats = st.session_state.detector.process_video(
            temp_path,
            output_path=None  # Don't save annotated video for now
        )

        progress_bar.progress(100)

        # Process detections and create violation records
        if stats['detections']:
            violations = st.session_state.processor.batch_process_detections(
                stats['detections'],
                location=location
            )

            # Save to database if connected
            if st.session_state.get('db_connected', False):
                for violation in violations:
                    violation_ops.create_violation(violation)

            status_text.text(f"✅ Found {len(violations)} violations!")
            return stats, violations
        else:
            status_text.text("✅ No violations detected")
            return stats, []

    except Exception as e:
        st.error(f"Error processing video: {e}")
        return None, []


def main():
    """Main dashboard application"""

    # Initialize
    initialize_system()

    # Header
    st.markdown(
        '<div class="main-header">🚦 Intelligent Traffic Management System</div>',
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.title("Control Panel")
        st.markdown("---")

        # System Status
        st.subheader("🟢 System Status")
        if st.session_state.get('detector'):
            st.success("✅ Detector Online")
        else:
            st.error("❌ Detector Offline")

        if st.session_state.get('db_connected'):
            st.success("✅ Database Connected")
        else:
            st.warning("⚠️ Database Offline")

        st.markdown("---")

        # Time range selector
        st.subheader("📅 Time Range")
        time_range = st.selectbox(
            "Statistics Period",
            [("Last 24 Hours", 1), ("Last 7 Days", 7), ("Last 30 Days", 30)],
            format_func=lambda x: x[0]
        )
        days = time_range[1]

        st.markdown("---")

        # Location selector
        st.subheader("📍 Location")
        location = st.selectbox(
            "Select Junction",
            ["Pettah Market", "Borella Junction", "Baseline Junction", "Kanaththa Junction"]
        )

        st.markdown("---")

        # Model information
        if st.session_state.get('detector'):
            st.subheader("🤖 Model Info")
            model_info = st.session_state.detector.get_model_info()
            st.write(f"**Classes:** {model_info['num_classes']}")
            st.write(f"**Confidence:** {model_info['conf_threshold']}")

            with st.expander("Show Classes"):
                for class_name in model_info['class_names'].values():
                    st.write(f"• {class_name}")

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard", "📹 Process Video", "⚠️ Recent Violations", "📈 Analytics"]
    )

    with tab1:
        show_dashboard_tab(days)

    with tab2:
        show_video_processing_tab(location)

    with tab3:
        show_violations_tab()

    with tab4:
        show_analytics_tab(days)


def show_dashboard_tab(days):
    """Show main dashboard with statistics"""
    st.subheader("📊 Real-time Statistics")

    # Get statistics
    stats = get_statistics(days)

    if stats:
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Violations",
                f"{stats.total_violations:,}",
                help=f"Last {days} days"
            )

        with col2:
            st.metric(
                "Pending Review",
                f"{stats.pending_violations:,}",
                delta=f"-{stats.reviewed_violations}",
                delta_color="inverse"
            )

        with col3:
            st.metric(
                "Total Fines",
                f"LKR {stats.total_fines:,.0f}",
                help="Total fine amount"
            )

        with col4:
            avg_fine = stats.total_fines / stats.total_violations if stats.total_violations > 0 else 0
            st.metric(
                "Average Fine",
                f"LKR {avg_fine:,.0f}"
            )

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            # Violations by vehicle type
            if stats.violations_by_vehicle_type:
                st.subheader("🚗 By Vehicle Type")
                fig = px.pie(
                    values=list(stats.violations_by_vehicle_type.values()),
                    names=[v.replace('parked_', '') for v in stats.violations_by_vehicle_type.keys()],
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Violations by severity
            if stats.violations_by_severity:
                st.subheader("🚨 By Severity")
                fig = px.bar(
                    x=list(stats.violations_by_severity.keys()),
                    y=list(stats.violations_by_severity.values()),
                    color=list(stats.violations_by_severity.keys()),
                    color_discrete_map={
                        'low': 'green',
                        'medium': 'yellow',
                        'high': 'orange',
                        'severe': 'red'
                    }
                )
                fig.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Severity",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)

        # Timeline
        st.markdown("---")
        timeline_fig = create_violations_timeline(days)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)

    else:
        st.info("📊 No statistics available. Process some videos to see data here!")


def show_video_processing_tab(location):
    """Show video upload and processing interface"""
    st.subheader("📹 Process Video for Violations")

    st.write("Upload a video to detect parking violations using your trained YOLOv8 model.")

    video_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload traffic video footage"
    )

    if video_file:
        st.video(video_file)

        col1, col2 = st.columns(2)
        with col1:
            process_location = st.text_input("Location", value=location)
        with col2:
            camera_id = st.text_input("Camera ID", value="CAM-001")

        if st.button("🚀 Process Video", type="primary"):
            stats, violations = process_video_upload(video_file, process_location)

            if stats:
                st.success(f"✅ Processed {stats['total_frames']} frames")
                st.info(f"🚗 Detected {stats['total_detections']} vehicles")
                st.info(f"⚠️ Found {len(violations)} violations")

                if violations:
                    # Show fine summary
                    summary = st.session_state.processor.get_fine_summary(violations)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Violations", summary['total_violations'])
                    with col2:
                        st.metric("Total Fines", f"LKR {summary['total_fines']:,.0f}")
                    with col3:
                        st.metric("Avg Fine", f"LKR {summary['average_fine']:,.0f}")


def show_violations_tab():
    """Show recent violations from database"""
    st.subheader("⚠️ Recent Violations")

    if not st.session_state.get('db_connected', False):
        st.warning("Database offline - cannot display violations")
        return

    try:
        violations = violation_ops.get_recent_violations(limit=20)

        if not violations:
            st.info("📋 No violations recorded yet")
            return

        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "pending", "reviewed", "paid", "dismissed"]
            )
        with col2:
            severity_filter = st.selectbox(
                "Severity",
                ["All", "low", "medium", "high", "severe"]
            )

        # Apply filters
        filtered_violations = violations
        if status_filter != "All":
            filtered_violations = [v for v in filtered_violations if v.get('status') == status_filter]
        if severity_filter != "All":
            filtered_violations = [v for v in filtered_violations if v.get('severity') == severity_filter]

        st.write(f"**Showing {len(filtered_violations)} violation(s)**")

        # Display violations
        for violation in filtered_violations:
            with st.expander(
                f"🚗 {violation['vehicle_type'].replace('parked_', '')} - "
                f"{violation['location']} - "
                f"LKR {violation['fine_amount']:,.0f}",
                expanded=False
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**📅 Date:** {violation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**📍 Location:** {violation['location']}")
                    st.write(f"**🚗 Vehicle:** {violation['vehicle_type']}")
                    st.write(f"**🚨 Severity:** {violation['severity'].upper()}")
                    st.write(f"**💰 Fine:** LKR {violation['fine_amount']:,.0f}")
                    st.write(f"**📊 Confidence:** {violation['confidence']:.2%}")
                    st.write(f"**📝 Status:** {violation['status'].upper()}")

                    if violation.get('notes'):
                        st.write(f"**📌 Notes:** {violation['notes']}")

                with col2:
                    # Status badge
                    status_colors = {
                        'pending': '🟡',
                        'reviewed': '🔵',
                        'paid': '🟢',
                        'dismissed': '⚪'
                    }
                    st.write(f"### {status_colors.get(violation['status'], '⚪')} {violation['status'].upper()}")

                    # Action buttons
                    if violation['status'] == 'pending':
                        if st.button(f"✅ Mark Reviewed", key=f"review_{violation['_id']}"):
                            violation_ops.update_violation_status(
                                str(violation['_id']),
                                'reviewed'
                            )
                            st.success("Updated!")
                            st.rerun()

    except Exception as e:
        st.error(f"Error loading violations: {e}")


def show_analytics_tab(days):
    """Show detailed analytics"""
    st.subheader("📈 Detailed Analytics")

    stats = get_statistics(days)

    if not stats:
        st.info("No data available for analytics")
        return

    # Severity breakdown
    if stats.violations_by_severity:
        st.write("### Severity Breakdown")

        severity_df = pd.DataFrame([
            {"Severity": k.upper(), "Count": v}
            for k, v in stats.violations_by_severity.items()
        ])

        col1, col2 = st.columns([1, 2])

        with col1:
            st.dataframe(severity_df, use_container_width=True, hide_index=True)

        with col2:
            fig = px.funnel(
                severity_df,
                x='Count',
                y='Severity',
                color='Severity',
                color_discrete_map={
                    'LOW': 'green',
                    'MEDIUM': 'yellow',
                    'HIGH': 'orange',
                    'SEVERE': 'red'
                }
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    # Vehicle type breakdown
    if stats.violations_by_vehicle_type:
        st.write("### Vehicle Type Distribution")

        vehicle_df = pd.DataFrame([
            {
                "Vehicle Type": k.replace('parked_', '').title(),
                "Violations": v,
                "Percentage": f"{v/stats.total_violations*100:.1f}%"
            }
            for k, v in stats.violations_by_vehicle_type.items()
        ])

        st.dataframe(vehicle_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
