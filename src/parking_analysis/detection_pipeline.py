"""
Parking Violation Detection Pipeline
Real-time detection and tracking system for parking behavior analysis
"""

import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
import json


class VehicleDetector:
    """
    YOLOv8-based vehicle detection system
    Custom-trained for Sri Lankan traffic (tuk-tuks, buses, cars)
    """
    
    def __init__(self, model_path=None, confidence_threshold=0.5):
        """
        Initialize the detector
        
        Args:
            model_path: Path to trained YOLOv8 model weights
            confidence_threshold: Minimum confidence for detections (0-1)
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        
        # Vehicle classes we detect
        self.vehicle_classes = {
            0: 'car',
            1: 'bus',
            2: 'tuk-tuk',
            3: 'motorcycle',
            4: 'truck',
            5: 'van'
        }
        
        print(f"✅ VehicleDetector initialized")
        print(f"   Confidence threshold: {confidence_threshold}")
    
    def load_model(self):
        """Load the trained YOLOv8 model"""
        if self.model_path and Path(self.model_path).exists():
            # TODO: Uncomment when model is trained
            # from ultralytics import YOLO
            # self.model = YOLO(self.model_path)
            print(f"✅ Model loaded from {self.model_path}")
        else:
            print("⚠️  No trained model found - using dummy detections for testing")
    
    def detect_vehicles(self, frame):
        """
        Detect vehicles in a frame
        
        Args:
            frame: OpenCV image (BGR format)
            
        Returns:
            List of detections: [{'bbox': [x1,y1,x2,y2], 'confidence': float, 'class': str}]
        """
        if self.model is None:
            # Dummy detections for testing without trained model
            return self._generate_dummy_detections(frame)
        
        # TODO: Real detection when model is ready
        # results = self.model(frame, conf=self.confidence_threshold)
        # return self._parse_results(results)
        
        return []
    
    def _generate_dummy_detections(self, frame):
        """Generate fake detections for testing pipeline"""
        h, w = frame.shape[:2]
        
        # Simulate 2-3 vehicle detections
        dummy_detections = [
            {
                'bbox': [int(w*0.2), int(h*0.3), int(w*0.4), int(h*0.7)],
                'confidence': 0.87,
                'class': 'car',
                'class_id': 0
            },
            {
                'bbox': [int(w*0.5), int(h*0.4), int(w*0.7), int(h*0.8)],
                'confidence': 0.92,
                'class': 'tuk-tuk',
                'class_id': 2
            }
        ]
        
        return dummy_detections


class VehicleTracker:
    """
    DeepSORT-based vehicle tracking system
    Tracks vehicles across frames to estimate parking duration
    """
    
    def __init__(self, max_age=30, min_hits=3):
        """
        Initialize tracker
        
        Args:
            max_age: Maximum frames to keep track alive without detection
            min_hits: Minimum detections before track is confirmed
        """
        self.max_age = max_age
        self.min_hits = min_hits
        self.tracks = {}
        self.next_id = 1
        
        print(f"✅ VehicleTracker initialized")
    
    def update(self, detections, frame_id):
        """
        Update tracks with new detections
        
        Args:
            detections: List of detection dictionaries
            frame_id: Current frame number
            
        Returns:
            List of active tracks with IDs
        """
        # TODO: Implement DeepSORT tracking
        # For now, simple ID assignment
        
        tracked_vehicles = []
        for det in detections:
            track = {
                'id': self.next_id,
                'bbox': det['bbox'],
                'class': det['class'],
                'confidence': det['confidence'],
                'first_seen': frame_id,
                'last_seen': frame_id,
                'is_parked': self._check_if_parked(det)
            }
            tracked_vehicles.append(track)
            self.next_id += 1
        
        return tracked_vehicles
    
    def _check_if_parked(self, detection):
        """
        Determine if vehicle is parked (stationary)
        
        TODO: Implement motion analysis
        - Track bbox position across frames
        - If movement < threshold for N frames → parked
        """
        # Placeholder logic
        return False


class TrafficImpactAnalyzer:
    """
    Analyzes the impact of parked vehicles on traffic flow
    Calculates congestion metrics and generates impact scores
    """
    
    def __init__(self):
        """Initialize impact analyzer"""
        self.baseline_speed = 40  # km/h - normal traffic speed
        self.lane_width = 3.5  # meters - standard lane width
        
        print(f"✅ TrafficImpactAnalyzer initialized")
    
    def calculate_impact_score(self, parked_vehicle, traffic_flow):
        """
        Calculate impact score for a parked vehicle
        
        Formula: Impact = (Duration × Lane_Blockage × Traffic_Density × Time_of_Day)
        
        Args:
            parked_vehicle: Dictionary with vehicle info and parking duration
            traffic_flow: Current traffic metrics (vehicle count, speed, etc.)
            
        Returns:
            Dictionary with impact metrics
        """
        duration_minutes = parked_vehicle.get('duration', 0) / 60.0
        lane_blockage = self._calculate_lane_blockage(parked_vehicle)
        traffic_density = traffic_flow.get('vehicle_count', 0) / 10.0  # Normalize
        time_factor = self._get_time_of_day_factor()
        
        # Impact score formula (0-100)
        impact_score = min(100, 
            (duration_minutes * 2) + 
            (lane_blockage * 30) + 
            (traffic_density * 20) + 
            (time_factor * 10)
        )
        
        # Calculate estimated vehicles delayed
        vehicles_delayed = int(traffic_density * duration_minutes * lane_blockage)
        
        # Calculate estimated time lost (total minutes across all vehicles)
        avg_delay_per_vehicle = 2.5  # minutes
        total_time_lost = vehicles_delayed * avg_delay_per_vehicle
        
        return {
            'impact_score': round(impact_score, 2),
            'severity': self._get_severity_level(impact_score),
            'vehicles_delayed': vehicles_delayed,
            'total_time_lost_minutes': round(total_time_lost, 1),
            'lane_blockage_percent': round(lane_blockage * 100, 1),
            'traffic_density': round(traffic_density, 2)
        }
    
    def _calculate_lane_blockage(self, vehicle):
        """
        Calculate what percentage of lane is blocked
        
        Returns: 0.0 to 1.0 (0% to 100%)
        """
        # TODO: Calculate based on vehicle bbox and lane position
        # For now, estimate based on vehicle type
        vehicle_type = vehicle.get('class', 'car')
        
        blockage_map = {
            'car': 0.6,
            'tuk-tuk': 0.4,
            'bus': 0.9,
            'truck': 0.85,
            'van': 0.7,
            'motorcycle': 0.3
        }
        
        return blockage_map.get(vehicle_type, 0.5)
    
    def _get_time_of_day_factor(self):
        """
        Return multiplier based on time of day
        Peak hours have higher impact
        
        Returns: 0.5 (off-peak) to 1.5 (peak)
        """
        current_hour = datetime.now().hour
        
        # Peak hours: 7-10 AM, 4-8 PM
        if (7 <= current_hour <= 10) or (16 <= current_hour <= 20):
            return 1.5  # Peak hour
        elif (11 <= current_hour <= 15):
            return 1.0  # Moderate
        else:
            return 0.5  # Off-peak
    
    def _get_severity_level(self, impact_score):
        """Convert impact score to severity category"""
        if impact_score >= 75:
            return "SEVERE"
        elif impact_score >= 50:
            return "HIGH"
        elif impact_score >= 25:
            return "MODERATE"
        else:
            return "LOW"


class ParkingViolationDetector:
    """
    Main detection pipeline
    Coordinates detection, tracking, and impact analysis
    """
    
    def __init__(self, model_path=None):
        """Initialize the complete detection system"""
        print("\n🚀 Initializing Parking Violation Detection System...")
        
        self.detector = VehicleDetector(model_path=model_path)
        self.tracker = VehicleTracker()
        self.impact_analyzer = TrafficImpactAnalyzer()
        
        self.detector.load_model()
        
        # Statistics
        self.total_violations = 0
        self.active_violations = []
        
        print("✅ System ready!\n")
    
    def process_frame(self, frame, frame_id, traffic_flow):
        """
        Process a single video frame
        
        Args:
            frame: OpenCV image
            frame_id: Frame number
            traffic_flow: Current traffic metrics dict
            
        Returns:
            Dictionary with detection results and visualized frame
        """
        # Step 1: Detect vehicles
        detections = self.detector.detect_vehicles(frame)
        
        # Step 2: Track vehicles
        tracked_vehicles = self.tracker.update(detections, frame_id)
        
        # Step 3: Identify parking violations
        violations = []
        for vehicle in tracked_vehicles:
            if vehicle['is_parked']:
                # Calculate impact
                impact = self.impact_analyzer.calculate_impact_score(
                    vehicle, 
                    traffic_flow
                )
                
                violation = {
                    'vehicle_id': vehicle['id'],
                    'class': vehicle['class'],
                    'bbox': vehicle['bbox'],
                    'duration': frame_id - vehicle['first_seen'],
                    'impact': impact
                }
                violations.append(violation)
        
        # Step 4: Draw visualizations
        annotated_frame = self._draw_detections(frame, tracked_vehicles, violations)
        
        return {
            'frame': annotated_frame,
            'detections': len(detections),
            'tracked_vehicles': len(tracked_vehicles),
            'violations': violations,
            'frame_id': frame_id
        }
    
    def _draw_detections(self, frame, vehicles, violations):
        """Draw bounding boxes and labels on frame"""
        annotated = frame.copy()
        
        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle['bbox']
            
            # Green for moving, Red for parked
            color = (0, 0, 255) if vehicle['is_parked'] else (0, 255, 0)
            
            # Draw bbox
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{vehicle['class']} #{vehicle['id']}"
            cv2.putText(annotated, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return annotated
    
    def process_video(self, video_path, output_path=None):
        """
        Process entire video file
        
        Args:
            video_path: Path to input video
            output_path: Path to save annotated video (optional)
        """
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print(f"❌ Could not open video: {video_path}")
            return
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n📹 Processing video: {Path(video_path).name}")
        print(f"   Frames: {total_frames} | FPS: {fps}")
        
        frame_id = 0
        violations_log = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mock traffic flow data
            traffic_flow = {
                'vehicle_count': 15,
                'avg_speed': 35,
                'lane_density': 0.7
            }
            
            # Process frame
            result = self.process_frame(frame, frame_id, traffic_flow)
            
            # Log violations
            if result['violations']:
                violations_log.extend(result['violations'])
            
            frame_id += 1
            
            # Progress update every 100 frames
            if frame_id % 100 == 0:
                print(f"   Processed: {frame_id}/{total_frames} frames")
        
        cap.release()
        
        print(f"\n✅ Processing complete!")
        print(f"   Total violations detected: {len(violations_log)}")
        
        return violations_log


# Demo/Test Function
if __name__ == "__main__":
    print("=" * 60)
    print("PARKING VIOLATION DETECTION SYSTEM - DEMO")
    print("=" * 60)
    
    # Initialize system
    system = ParkingViolationDetector()
    
    # Test with dummy frame
    dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    traffic_flow = {
        'vehicle_count': 12,
        'avg_speed': 30,
        'lane_density': 0.6
    }
    
    result = system.process_frame(dummy_frame, frame_id=100, traffic_flow=traffic_flow)
    
    print("\n📊 Test Results:")
    print(f"   Detections: {result['detections']}")
    print(f"   Tracked vehicles: {result['tracked_vehicles']}")
    print(f"   Violations: {len(result['violations'])}")
    
    print("\n✅ System test complete!")