"""Real-time parking violation detection using trained YOLOv8 model."""
import os
from pathlib import Path
from typing import List, Dict, Tuple
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class RealtimeDetector:
    """Real-time parking violation detector using trained YOLOv8 model."""

    def __init__(self, model_path: str = None, conf_threshold: float = None):
        """
        Initialize the detector.

        Args:
            model_path: Path to trained YOLOv8 model
            conf_threshold: Confidence threshold for detections
        """
        # Load configuration from .env
        self.model_path = model_path or os.getenv('MODEL_PATH', 'runs/parking_violations/exp/weights/best.pt')
        self.conf_threshold = conf_threshold or float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))

        # Check if model exists
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        # Load the trained model
        print(f"Loading model from: {self.model_path}")
        self.model = YOLO(self.model_path)
        self.class_names = self.model.names
        print(f"✅ Model loaded successfully!")
        print(f"📊 Detected classes: {list(self.class_names.values())}")

        # Color map for different vehicle types
        self.color_map = {
            'parked_car': (0, 255, 0),           # Green
            'parked_tuktuk': (255, 0, 255),      # Magenta
            'parked_bus': (0, 0, 255),           # Red
            'parked_van': (255, 255, 0),         # Cyan
            'parked_truck': (0, 165, 255),       # Orange
            'parked_motorcycle': (255, 0, 0),    # Blue
            'parked_jeep': (0, 255, 255)         # Yellow
        }

    def detect_frame(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect parking violations in a single frame.

        Args:
            frame: Input frame (BGR format from OpenCV)

        Returns:
            List of detection dictionaries containing:
                - class_id: Vehicle class ID
                - class_name: Vehicle class name
                - confidence: Detection confidence
                - bbox: Bounding box [x1, y1, x2, y2]
                - timestamp: Detection timestamp
        """
        # Run inference
        results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'class_id': int(box.cls[0]),
                    'class_name': self.class_names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].cpu().numpy().tolist(),  # [x1, y1, x2, y2]
                    'timestamp': datetime.utcnow()
                }
                detections.append(detection)

        return detections

    def annotate_frame(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame.

        Args:
            frame: Input frame
            detections: List of detections from detect_frame()

        Returns:
            Annotated frame with bounding boxes and labels
        """
        annotated = frame.copy()

        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            class_name = det['class_name']
            confidence = det['confidence']

            # Get color for this vehicle type
            color = self.color_map.get(class_name, (255, 255, 255))

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            # Create label
            label = f"{class_name.replace('parked_', '')}: {confidence:.2f}"

            # Get label size
            (label_width, label_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )

            # Draw label background
            cv2.rectangle(
                annotated,
                (x1, y1 - label_height - 10),
                (x1 + label_width, y1),
                color,
                -1
            )

            # Draw label text
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                2
            )

        # Add detection count
        count_text = f"Detections: {len(detections)}"
        cv2.putText(
            annotated,
            count_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        return annotated

    def process_video(self, video_path: str, output_path: str = None) -> Dict:
        """
        Process entire video and detect violations.

        Args:
            video_path: Path to input video
            output_path: Path to save annotated video (optional)

        Returns:
            Dictionary with processing statistics
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"📹 Processing video: {video_path}")
        print(f"   Frames: {total_frames}, FPS: {fps}, Size: {width}x{height}")

        # Setup video writer if output path provided
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"   Saving to: {output_path}")

        frame_count = 0
        total_detections = 0
        all_detections = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detect violations
            detections = self.detect_frame(frame)
            total_detections += len(detections)
            all_detections.extend(detections)

            # Annotate frame
            if output_path:
                annotated = self.annotate_frame(frame, detections)
                out.write(annotated)

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"   Processed: {frame_count}/{total_frames} frames ({frame_count/total_frames*100:.1f}%)")

        cap.release()
        if out:
            out.release()

        stats = {
            'total_frames': frame_count,
            'total_detections': total_detections,
            'avg_detections_per_frame': total_detections / frame_count if frame_count > 0 else 0,
            'fps': fps,
            'detections': all_detections
        }

        print(f"✅ Processing complete!")
        print(f"   Total detections: {total_detections}")
        print(f"   Average per frame: {stats['avg_detections_per_frame']:.2f}")

        return stats

    def process_webcam(self, camera_id: int = 0, save_violations: bool = False):
        """
        Process live webcam feed.

        Args:
            camera_id: Camera device ID (usually 0 for default camera)
            save_violations: Whether to save detected violations
        """
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            raise ValueError(f"Could not open camera: {camera_id}")

        print("📹 Starting live detection from webcam...")
        print("   Press 'q' to quit, 's' to save current frame")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detect violations
            detections = self.detect_frame(frame)

            # Annotate frame
            annotated = self.annotate_frame(frame, detections)

            # Show frame
            cv2.imshow('Parking Violation Detection', annotated)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                filename = f"violation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, annotated)
                print(f"   Saved: {filename}")

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()
        print(f"✅ Processed {frame_count} frames from webcam")

    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        return {
            'model_path': self.model_path,
            'conf_threshold': self.conf_threshold,
            'class_names': self.class_names,
            'num_classes': len(self.class_names)
        }
