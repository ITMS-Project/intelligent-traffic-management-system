"""Fast detector that samples frames instead of processing every frame"""
import os
from pathlib import Path
from typing import List, Dict
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class FastDetector:
    """Fast parking violation detector that samples frames"""

    def __init__(self, model_path: str = None, conf_threshold: float = None):
        """Initialize the detector"""
        self.model_path = model_path or os.getenv('MODEL_PATH', 'runs/parking_violations/exp/weights/best.pt')
        self.conf_threshold = conf_threshold or float(os.getenv('CONFIDENCE_THRESHOLD', 0.25))

        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        print(f"Loading model from: {self.model_path}")
        self.model = YOLO(self.model_path)
        self.class_names = self.model.names
        print(f"✅ Model loaded successfully!")

    def detect_frame(self, frame: np.ndarray) -> List[Dict]:
        """Detect violations in a single frame"""
        results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'class_id': int(box.cls[0]),
                    'class_name': self.class_names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].cpu().numpy().tolist(),
                    'timestamp': datetime.utcnow()
                }
                detections.append(detection)

        return detections

    def process_video_fast(self, video_path: str, sample_rate: int = 10) -> Dict:
        """
        Process video by sampling frames (much faster!)

        Args:
            video_path: Path to video
            sample_rate: Process every Nth frame (default: 10 = 10x faster)

        Returns:
            Dictionary with statistics
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        print(f"📹 Video: {total_frames} frames @ {fps} FPS ({duration:.1f}s)")
        print(f"⚡ Fast mode: Processing every {sample_rate}th frame")
        print(f"   Frames to process: {total_frames // sample_rate}")

        frame_count = 0
        processed_count = 0
        total_detections = 0
        all_detections = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Only process sampled frames
            if frame_count % sample_rate == 0:
                detections = self.detect_frame(frame)
                total_detections += len(detections)
                all_detections.extend(detections)
                processed_count += 1

                if processed_count % 10 == 0:
                    print(f"   Processed: {processed_count}/{total_frames // sample_rate} sampled frames")

            frame_count += 1

        cap.release()

        stats = {
            'total_frames': frame_count,
            'processed_frames': processed_count,
            'sample_rate': sample_rate,
            'total_detections': total_detections,
            'avg_detections_per_frame': total_detections / processed_count if processed_count > 0 else 0,
            'fps': fps,
            'detections': all_detections
        }

        print(f"✅ Done! Processed {processed_count} frames, found {total_detections} detections")

        return stats

    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            'model_path': self.model_path,
            'conf_threshold': self.conf_threshold,
            'class_names': self.class_names,
            'num_classes': len(self.class_names)
        }
