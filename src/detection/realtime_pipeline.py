"""
Real-time Violation Detection Pipeline
Connects: Detection -> OCR -> Database -> Notifications
"""
import cv2
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.detection.realtime_detector import RealtimeDetector
from src.detection.license_plate_ocr import LicensePlateRecognizer
from src.detection.violation_processor import ViolationProcessor
from src.database.connection import Database
from src.notifications.notification_service import notification_service


class RealtimeViolationPipeline:
    """
    Complete real-time violation detection and processing pipeline.

    Flow:
    1. Detect vehicles using YOLOv8
    2. Recognize license plates using OCR
    3. Look up vehicle/driver in database
    4. Calculate fine based on violation type
    5. Create violation record in database
    6. Send push notification to driver's mobile app
    """

    def __init__(
        self,
        model_path: str = None,
        conf_threshold: float = 0.25,
        location: str = "Main Junction",
        camera_id: str = "CAM-001"
    ):
        """
        Initialize the real-time pipeline.

        Args:
            model_path: Path to YOLOv8 model
            conf_threshold: Detection confidence threshold
            location: Camera location description
            camera_id: Camera identifier
        """
        print("🚀 Initializing Real-time Violation Detection Pipeline...")

        # Initialize components
        self.detector = RealtimeDetector(model_path, conf_threshold)
        self.ocr = LicensePlateRecognizer()
        self.processor = ViolationProcessor()

        # Database connection
        db_instance = Database()
        self.db = db_instance.get_db()
        self.violations_col = self.db['violations']
        self.vehicles_col = self.db['vehicles']
        self.users_col = self.db['users']

        # Configuration
        self.location = location
        self.camera_id = camera_id

        # Statistics
        self.stats = {
            'total_detections': 0,
            'plates_recognized': 0,
            'violations_created': 0,
            'notifications_sent': 0,
            'drivers_notified': 0
        }

        print("✅ Pipeline initialized successfully!")

    def find_driver_by_plate(self, license_plate: str) -> Optional[Dict]:
        """
        Find driver information by license plate.

        Args:
            license_plate: Vehicle license plate number

        Returns:
            Driver info dict or None if not found
        """
        if not license_plate:
            return None

        try:
            # Find vehicle
            vehicle = self.vehicles_col.find_one({'license_plate': license_plate})

            if not vehicle:
                return None

            # Find owner/driver
            owner_id = vehicle.get('owner_id')
            if owner_id:
                from bson import ObjectId
                user = self.users_col.find_one({'_id': ObjectId(owner_id)})

                if user:
                    return {
                        'user_id': str(user['_id']),
                        'username': user.get('username'),
                        'email': user.get('email'),
                        'phone': user.get('phone'),
                        'fcm_token': user.get('fcm_token'),  # For push notifications
                        'vehicle_id': str(vehicle['_id']),
                        'vehicle_type': vehicle.get('vehicle_type'),
                        'make': vehicle.get('make'),
                        'model': vehicle.get('model')
                    }

        except Exception as e:
            print(f"❌ Error finding driver: {e}")

        return None

    def process_detection(
        self,
        image: np.ndarray,
        detection: Dict,
        violation_type: str = "illegal_parking"
    ) -> Optional[Dict]:
        """
        Process a single detection through the complete pipeline.

        Args:
            image: Full frame image
            detection: Detection dict from YOLOv8
            violation_type: Type of violation

        Returns:
            Created violation record or None
        """
        # Step 1: Recognize license plate
        plate = self.ocr.recognize_plate(image, detection['bbox'])
        detection['license_plate'] = plate

        if plate:
            self.stats['plates_recognized'] += 1
            print(f"   📋 Plate recognized: {plate}")

            # Step 2: Find driver
            driver_info = self.find_driver_by_plate(plate)

            if driver_info:
                print(f"   👤 Driver found: {driver_info['username']}")
            else:
                print(f"   ⚠️  No driver found for plate: {plate}")
        else:
            print(f"   ⚠️  No plate recognized")
            driver_info = None

        # Step 3: Calculate fine and create violation record
        violation = self.processor.create_violation_record(
            detection=detection,
            location=self.location,
            camera_id=self.camera_id,
            license_plate=plate,
            violation_type=violation_type,
            lane_blockage=60.0,  # Can be calculated from video analysis
            vehicles_delayed=10   # Can be estimated from traffic flow
        )

        # Add driver information if found
        if driver_info:
            violation['user_id'] = driver_info['user_id']
            violation['vehicle_id'] = driver_info['vehicle_id']
            violation['driver_name'] = driver_info.get('username')

        # Step 4: Save to database
        try:
            result = self.violations_col.insert_one(violation)
            violation['_id'] = result.inserted_id
            self.stats['violations_created'] += 1
            print(f"   💾 Violation saved to database: {result.inserted_id}")

            # Step 5: Send notification to driver
            if driver_info and driver_info.get('fcm_token'):
                self._send_driver_notification(violation, driver_info)
                self.stats['drivers_notified'] += 1

            return violation

        except Exception as e:
            print(f"   ❌ Error saving violation: {e}")
            return None

    def _send_driver_notification(self, violation: Dict, driver_info: Dict):
        """
        Send push notification to driver about violation.

        Args:
            violation: Violation record
            driver_info: Driver information including FCM token
        """
        try:
            # Send violation notification
            success = notification_service.send_violation_notification(
                device_token=driver_info['fcm_token'],
                violation_type=self.processor.violation_types.get(
                    violation['violation_type'],
                    violation['violation_type']
                ),
                fine_amount=violation['fine_amount'],
                location=violation['location'],
                violation_id=str(violation['_id'])
            )

            if success:
                self.stats['notifications_sent'] += 1
                print(f"   📱 Notification sent to {driver_info['username']}")
            else:
                print(f"   ⚠️  Failed to send notification")

        except Exception as e:
            print(f"   ❌ Error sending notification: {e}")

    def process_frame(
        self,
        frame: np.ndarray,
        violation_type: str = "illegal_parking",
        visualize: bool = True
    ) -> Dict:
        """
        Process a single frame through the pipeline.

        Args:
            frame: Input frame (BGR)
            violation_type: Type of violation to record
            visualize: Whether to annotate the frame

        Returns:
            Dict with frame results and statistics
        """
        # Detect vehicles
        detections = self.detector.detect_frame(frame)
        self.stats['total_detections'] += len(detections)

        violations = []

        # Process each detection
        for detection in detections:
            violation = self.process_detection(frame, detection, violation_type)
            if violation:
                violations.append(violation)

        # Annotate frame if requested
        annotated_frame = frame
        if visualize:
            annotated_frame = self.detector.annotate_frame(frame, detections)

            # Add plate numbers
            for detection in detections:
                if detection.get('license_plate'):
                    annotated_frame = self.ocr.visualize_plate(
                        annotated_frame,
                        detection['bbox'],
                        detection['license_plate']
                    )

        return {
            'detections': detections,
            'violations': violations,
            'annotated_frame': annotated_frame,
            'stats': self.stats.copy()
        }

    def process_video(
        self,
        video_path: str,
        output_path: str = None,
        violation_type: str = "illegal_parking",
        sample_rate: int = 30
    ) -> Dict:
        """
        Process video file and detect violations in real-time.

        Args:
            video_path: Path to input video
            output_path: Optional path to save annotated video
            violation_type: Type of violation
            sample_rate: Process every Nth frame (default 30 for faster processing)

        Returns:
            Processing statistics
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"\n📹 Processing video: {video_path}")
        print(f"   Frames: {total_frames}, FPS: {fps}, Size: {width}x{height}")
        print(f"   Sample rate: 1/{sample_rate} frames")

        # Setup video writer
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps // sample_rate, (width, height))

        frame_count = 0
        processed_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Sample frames
            if frame_count % sample_rate == 0:
                result = self.process_frame(frame, violation_type, visualize=True)

                if output_path and out:
                    out.write(result['annotated_frame'])

                processed_count += 1

                # Progress update
                if processed_count % 10 == 0:
                    print(f"   Processed: {frame_count}/{total_frames} frames "
                          f"({frame_count/total_frames*100:.1f}%) - "
                          f"Violations: {self.stats['violations_created']}")

            frame_count += 1

        cap.release()
        if out:
            out.release()

        print(f"\n✅ Video processing complete!")
        self._print_statistics()

        return self.stats

    def process_webcam(
        self,
        camera_id: int = 0,
        violation_type: str = "illegal_parking"
    ):
        """
        Process live webcam feed with real-time violation detection.

        Args:
            camera_id: Camera device ID
            violation_type: Type of violation to record
        """
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            raise ValueError(f"Could not open camera: {camera_id}")

        print("\n📹 Starting LIVE violation detection from webcam...")
        print("   Press 'q' to quit")
        print("   Press 's' to save current frame")
        print("   Press 'r' to reset statistics")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame
            result = self.process_frame(frame, violation_type, visualize=True)

            # Display
            cv2.imshow('Real-time Violation Detection', result['annotated_frame'])

            # Handle keyboard
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"violation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, result['annotated_frame'])
                print(f"   💾 Saved: {filename}")
            elif key == ord('r'):
                self._reset_statistics()
                print("   🔄 Statistics reset")

        cap.release()
        cv2.destroyAllWindows()

        print(f"\n✅ Live detection stopped!")
        self._print_statistics()

    def _reset_statistics(self):
        """Reset pipeline statistics."""
        self.stats = {
            'total_detections': 0,
            'plates_recognized': 0,
            'violations_created': 0,
            'notifications_sent': 0,
            'drivers_notified': 0
        }

    def _print_statistics(self):
        """Print pipeline statistics."""
        print("\n" + "="*60)
        print("📊 PIPELINE STATISTICS")
        print("="*60)
        print(f"Total Detections:       {self.stats['total_detections']}")
        print(f"Plates Recognized:      {self.stats['plates_recognized']}")
        print(f"Violations Created:     {self.stats['violations_created']}")
        print(f"Notifications Sent:     {self.stats['notifications_sent']}")
        print(f"Drivers Notified:       {self.stats['drivers_notified']}")

        if self.stats['total_detections'] > 0:
            plate_rate = self.stats['plates_recognized'] / self.stats['total_detections'] * 100
            print(f"Plate Recognition Rate: {plate_rate:.1f}%")

        print("="*60 + "\n")

    def get_statistics(self) -> Dict:
        """Get current pipeline statistics."""
        return self.stats.copy()


# Quick test function
def test_pipeline():
    """Test the real-time pipeline with sample data."""
    print("\n🧪 Testing Real-time Pipeline...\n")

    pipeline = RealtimeViolationPipeline(
        location="Colombo Main Junction",
        camera_id="CAM-DEMO-001"
    )

    print("\n✅ Pipeline test complete!")
    print("   Ready for real-time violation detection!")


if __name__ == "__main__":
    test_pipeline()
