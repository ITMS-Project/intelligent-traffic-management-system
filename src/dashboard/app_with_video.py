"""
Dashboard with Live Video Detection - Download annotated video!
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import traceback
import cv2
import numpy as np
import time

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.detection.fast_detector import FastDetector
from src.detection.violation_processor import ViolationProcessor
from src.database import db, violation_ops
from src.dashboard.styles import DASHBOARD_CSS

st.set_page_config(
    page_title="VRNAVS - Traffic Control",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def initialize_system():
    """Initialize detection system"""
    if 'detector' not in st.session_state:
        try:
            with st.spinner("🔄 Initializing AI Core..."):
                st.session_state.detector = FastDetector()
                st.session_state.processor = ViolationProcessor()
            st.success("✅ AI Core Online")
        except Exception as e:
            st.error(f"❌ System Failure: {e}")
            st.stop()

    if 'db_connected' not in st.session_state:
        try:
            db.connect()
            st.session_state.db_connected = True
        except:
            st.session_state.db_connected = False


def create_annotated_video(input_path, output_path, sample_rate, progress_placeholder, status_placeholder):
    """Create annotated video with progress updates"""

    detector = st.session_state.detector

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False

    # Get properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Setup writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        return False

    # Color map (Neon/Cyberpunk colors)
    color_map = {
        'parked_car': (0, 255, 127),      # Spring Green
        'parked_tuktuk': (255, 0, 255),   # Magenta
        'parked_bus': (0, 69, 255),       # Orange Red (BGR)
        'parked_van': (255, 255, 0),      # Cyan (BGR)
        'parked_truck': (0, 165, 255),    # Orange
        'parked_motorcycle': (255, 0, 0), # Blue (BGR)
        'parked_jeep': (0, 255, 255)      # Yellow
    }

    frame_count = 0
    total_detections = 0
    last_detections = []

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

        # Annotate frame
        annotated = frame.copy()
        
        # Darken frame slightly for HUD contrast
        annotated = cv2.addWeighted(annotated, 0.8, np.zeros(annotated.shape, annotated.dtype), 0, 0)

        for det in last_detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']
            color = color_map.get(class_name, (255, 255, 255))

            # HUD Style Box (Corners only or thin lines)
            # Draw full box with low opacity
            overlay = annotated.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            cv2.addWeighted(overlay, 0.1, annotated, 0.9, 0, annotated)
            
            # Draw corners
            line_len = min(int((x2-x1)*0.2), int((y2-y1)*0.2))
            thickness = 2
            
            # Top Left
            cv2.line(annotated, (x1, y1), (x1 + line_len, y1), color, thickness)
            cv2.line(annotated, (x1, y1), (x1, y1 + line_len), color, thickness)
            
            # Top Right
            cv2.line(annotated, (x2, y1), (x2 - line_len, y1), color, thickness)
            cv2.line(annotated, (x2, y1), (x2, y1 + line_len), color, thickness)
            
            # Bottom Left
            cv2.line(annotated, (x1, y2), (x1 + line_len, y2), color, thickness)
            cv2.line(annotated, (x1, y2), (x1, y2 - line_len), color, thickness)
            
            # Bottom Right
            cv2.line(annotated, (x2, y2), (x2 - line_len, y2), color, thickness)
            cv2.line(annotated, (x2, y2), (x2, y2 - line_len), color, thickness)

            # Label with background
            label = f"{class_name.replace('parked_', '').upper()} {confidence:.0%}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            
            # Label line connecting to box
            cv2.line(annotated, (x1, y1), (x1, y1-20), color, 1)
            cv2.line(annotated, (x1, y1-20), (x1+lw+10, y1-20), color, 1)
            
            cv2.putText(annotated, label, (x1+5, y1-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # HUD Info overlay
        # Top bar
        cv2.rectangle(annotated, (0, 0), (width, 60), (0, 0, 0), -1)
        
        # Grid lines on top bar
        for i in range(0, width, 40):
            cv2.line(annotated, (i, 55), (i, 60), (50, 50, 50), 1)

        timestamp = frame_count / fps if fps > 0 else 0
        
        # Left Info
        cv2.putText(annotated, "LIVE FEED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.circle(annotated, (170, 32), 6, (0, 0, 255), -1) # Rec dot
        
        # Right Info
        cv2.putText(annotated, f"OBJECTS: {len(last_detections)}", (width-250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(annotated, f"TIME: {timestamp:.1f}s", (width-450, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        out.write(annotated)
        frame_count += 1

        # Update progress
        if frame_count % 50 == 0:
            progress = frame_count / total_frames
            progress_placeholder.progress(progress)
            elapsed = time.time() - start_time
            eta = (elapsed / frame_count) * (total_frames - frame_count)
            status_placeholder.info(f"⚡ Processing: {frame_count}/{total_frames} frames | "
                                   f"ETA: {eta/60:.1f} min | Detections: {total_detections}")

    cap.release()
    out.release()

    progress_placeholder.progress(1.0)
    status_placeholder.success(f"✅ Analysis Complete! {total_detections} violations detected.")

    return True


def main():
    """Main app"""
    
    # Custom Header
    st.markdown("""
        <div class="main-header">
            <div class="header-title">VRNAVS <span style="font-weight:300; opacity:0.7">| TRAFFIC CONTROL</span></div>
            <div style="font-size: 0.8rem; opacity: 0.7">SYSTEM ONLINE</div>
        </div>
    """, unsafe_allow_html=True)

    initialize_system()

    # Layout: Sidebar for controls, Main for video
    with st.sidebar:
        st.write("### ⚙️ CONTROL PANEL")
        
        video_file = st.file_uploader(
            "Upload Feed",
            type=['mp4', 'avi', 'mov', 'mkv']
        )
        
        st.write("---")
        st.write("### 🎯 PARAMETERS")
        sample_rate = st.slider(
            "Analysis Speed",
            min_value=1,
            max_value=10,
            value=3,
            help="Higher = Faster but less accurate"
        )
        
        st.metric("Processing Rate", f"{sample_rate}x")
        
        st.write("---")
        st.info("System Ready. Waiting for input stream.")

    if video_file:
        # Main Content Area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write("### 📹 LIVE FEED ANALYSIS")
            
            # Save input
            input_path = f"/tmp/{video_file.name}"
            with open(input_path, "wb") as f:
                f.write(video_file.read())

            output_path = f"/tmp/annotated_{video_file.name}"
            
            # Placeholder for video
            video_placeholder = st.empty()
            
            if st.button("▶ INITIATE ANALYSIS", type="primary", use_container_width=True):
                
                progress_placeholder = st.progress(0)
                status_placeholder = st.empty()
                
                try:
                    success = create_annotated_video(
                        input_path,
                        output_path,
                        sample_rate,
                        progress_placeholder,
                        status_placeholder
                    )

                    if success and Path(output_path).exists():
                        # Display result in custom container
                        st.markdown('<div class="video-container">', unsafe_allow_html=True)
                        st.video(output_path)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download button
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="⬇ EXPORT DATA",
                                data=f,
                                file_name=f"annotated_{video_file.name}",
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"System Error: {e}")
                    st.code(traceback.format_exc())
        
        with col2:
            st.write("### 📊 METRICS")
            st.metric("Active Violations", "0", delta="0")
            st.metric("System Load", "12%", delta="-2%")
            st.metric("Network", "1.2 GB/s", delta="+0.1")
            
            st.write("---")
            st.write("### 📍 LOCATION")
            st.map(data={'lat': [6.9271], 'lon': [79.8612]}, zoom=13)

    else:
        # Empty state
        st.markdown("""
            <div style="text-align: center; padding: 5rem; opacity: 0.5;">
                <h1>NO SIGNAL</h1>
                <p>Please upload video feed to initialize HUD</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
