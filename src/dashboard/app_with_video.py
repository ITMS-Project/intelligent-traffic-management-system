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

st.set_page_config(
    page_title="Live Detection Video",
    page_icon="🎬",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)


def initialize_system():
    """Initialize detection system"""
    if 'detector' not in st.session_state:
        try:
            with st.spinner("🔄 Loading YOLOv8 model..."):
                st.session_state.detector = FastDetector()
                st.session_state.processor = ViolationProcessor()
            st.success("✅ Detector loaded!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
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

    # Color map
    color_map = {
        'parked_car': (0, 255, 0),
        'parked_tuktuk': (255, 0, 255),
        'parked_bus': (0, 0, 255),
        'parked_van': (255, 255, 0),
        'parked_truck': (0, 165, 255),
        'parked_motorcycle': (255, 0, 0),
        'parked_jeep': (0, 255, 255)
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

        for det in last_detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']
            color = color_map.get(class_name, (255, 255, 255))

            # Box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)

            # Label
            label = f"{class_name.replace('parked_', '')}: {confidence:.1%}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(annotated, (x1, y1-lh-10), (x1+lw+10, y1), color, -1)
            cv2.putText(annotated, label, (x1+5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

        # Info overlay
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (width, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, annotated, 0.4, 0, annotated)

        timestamp = frame_count / fps if fps > 0 else 0
        cv2.putText(annotated, f"Detections: {len(last_detections)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated, f"Time: {timestamp:.1f}s", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        out.write(annotated)
        frame_count += 1

        # Update progress
        if frame_count % 50 == 0:
            progress = frame_count / total_frames
            progress_placeholder.progress(progress)
            elapsed = time.time() - start_time
            eta = (elapsed / frame_count) * (total_frames - frame_count)
            status_placeholder.info(f"⏳ Processing: {frame_count}/{total_frames} frames | "
                                   f"ETA: {eta/60:.1f} min | Detections: {total_detections}")

    cap.release()
    out.release()

    progress_placeholder.progress(1.0)
    status_placeholder.success(f"✅ Complete! Processed {frame_count} frames with {total_detections} detections")

    return True


def main():
    """Main app"""

    st.markdown(
        '<div class="main-header">🎬 Live Detection Video Creator</div>',
        unsafe_allow_html=True
    )

    initialize_system()

    st.write("## 📹 Create Annotated Video with Live Detections")
    st.info("🎥 This will create a video you can watch to see detections happening in real-time!")

    video_file = st.file_uploader(
        "Upload your video",
        type=['mp4', 'avi', 'mov', 'mkv']
    )

    if video_file:
        st.success(f"✅ Uploaded: {video_file.name}")

        col1, col2 = st.columns(2)
        with col1:
            sample_rate = st.slider(
                "Detection speed (higher = faster processing)",
                min_value=1,
                max_value=10,
                value=3,
                help="1 = Detect on every frame (slow, smooth), 5 = Every 5th frame (faster)"
            )
        with col2:
            st.write("")
            st.write("")
            st.metric("Processing Speed", f"{sample_rate}x faster" if sample_rate > 1 else "Full Quality")

        if st.button("🎬 Create Annotated Video", type="primary", use_container_width=True):

            # Save input
            input_path = f"/tmp/{video_file.name}"
            with open(input_path, "wb") as f:
                f.write(video_file.read())

            output_path = f"/tmp/annotated_{video_file.name}"

            st.write("---")
            st.subheader("🎬 Creating Your Annotated Video")

            progress_placeholder = st.progress(0)
            status_placeholder = st.empty()

            status_placeholder.info("🔄 Starting video processing...")

            try:
                success = create_annotated_video(
                    input_path,
                    output_path,
                    sample_rate,
                    progress_placeholder,
                    status_placeholder
                )

                if success and Path(output_path).exists():
                    file_size = Path(output_path).stat().st_size / (1024*1024)

                    st.success(f"🎉 Annotated video created successfully! ({file_size:.1f} MB)")

                    # Show video
                    st.write("### 📺 Preview Annotated Video:")
                    st.video(output_path)

                    # Download button
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Annotated Video",
                            data=f,
                            file_name=f"annotated_{video_file.name}",
                            mime="video/mp4",
                            use_container_width=True
                        )

                    st.success("💡 You can now watch this video to see live detections with bounding boxes!")

                else:
                    st.error("❌ Failed to create annotated video")

            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.code(traceback.format_exc())

    else:
        st.info("👆 Upload a video to get started")


if __name__ == "__main__":
    main()
