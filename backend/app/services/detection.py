"""
Intelligent Traffic Management System - YOLOv8 Advanced Detection Module
FINAL VERSION: Full Integration with TTS, Scoring, Traffic Control

Features:
=========
1. Two-Stage Detection: Vehicle Tracking → Plate Detection (Zoom)
2. OCR Caching: Only run OCR every 2+ seconds per vehicle
3. Frame Skipping: Run YOLO every 2nd frame, reuse boxes on skipped frames
4. Speed Estimation: Calculate vehicle speed from centroid movement
5. Parking Zones: Configurable red zones with warning/violation phases
6. TTS Warnings: Voice alerts for parking violations
7. Database Integration: Save violations to SQLite via ScoringEngine
8. Signal Automation: Fuzzy logic traffic light control
9. Visual Effects: Flashing purple boxes for penalized vehicles
"""

import sys
import time
import json
from pathlib import Path
from typing import Generator, Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

import cv2
import numpy as np

# Add parent to path for imports when running as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.core.config import get_settings

settings = get_settings()


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Frame skipping - only run YOLO every N frames
YOLO_DETECTION_INTERVAL: int = 2

# Plate detection interval
PLATE_DETECTION_INTERVAL: int = 3

# OCR cooldown per vehicle (seconds)
OCR_COOLDOWN_SECONDS: float = 2.0

# Speed estimation (pixels/sec to km/h)
SPEED_SCALE_FACTOR: float = 0.5
SPEEDING_THRESHOLD_KMH: float = 80.0
SPEEDING_THRESHOLD_PIXELS: float = 150.0  # pixels/second for demo

# Parking violation timing
# Parking violation timing
PARKING_WARNING_SECONDS: float = 5.0 
PARKING_VIOLATION_SECONDS: float = 15.0

# Signal automation interval
SIGNAL_UPDATE_INTERVAL: int = 30  # frames (~1 second at 30fps)

# History cleanup
PLATE_HISTORY_MAX_AGE: int = 3000
TRACKING_HISTORY_MAX_AGE: int = 60

# TTS cooldown (don't spam warnings)
TTS_COOLDOWN_SECONDS: float = 10.0


# ============================================================================
# PARKING ZONES CONFIGURATION
# ============================================================================

# Define parking zones as polygons (x, y) in frame coordinates
# These are "no parking" zones - red boxes will be drawn
# Adjust these coordinates based on your video feed
DEFAULT_PARKING_ZONES = []


# ============================================================================
# GLOBAL STATE & CACHING
# ============================================================================

# Model cache
_model_cache: Dict[str, Any] = {}

# Plate history: track_id -> {"bbox", "text", "timestamp", "frame_count"}
plate_history: Dict[int, Dict[str, Any]] = {}

# OCR cooldown: track_id -> last_ocr_time
ocr_cooldown: Dict[int, float] = {}

# Speed tracking: track_id -> {"prev_centroid", "prev_time", "speed", "is_speeding", "speed_pixels"}
speed_history: Dict[int, Dict[str, Any]] = {}

# Parking tracking: track_id -> {"entry_time", "zone_id", "warned", "penalized", "plate", "tts_time"}
parking_tracker: Dict[int, Dict[str, Any]] = {}

# Penalized vehicles (for flashing effect)
penalized_vehicles: Dict[int, float] = {}  # track_id -> penalize_time

# Previous frame detections (for frame skipping)
_prev_detections: List[Any] = []
_prev_plate_boxes: List[Tuple[int, int, int, int]] = []

# Frame counter
_frame_counter: int = 0

# Parking zones persistence
ZONES_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "parking_zones.json"

def load_zones_from_disk() -> List[Dict]:
    """Load parking zones from JSON file."""
    if not ZONES_FILE.exists():
        return []
    try:
        with open(ZONES_FILE, "r") as f:
            zones = json.load(f)
            # Ensure polygons are tuples
            for z in zones:
                z["polygon"] = [tuple(p) for p in z["polygon"]]
                z["color"] = tuple(z["color"])
            return zones
    except Exception as e:
        print(f"Error loading zones: {e}")
        return []

def save_zones_to_disk(zones: List[Dict]):
    """Save parking zones to JSON file."""
    try:
        # Convert tuples to lists for JSON
        serializable_zones = []
        for z in zones:
            sz = z.copy()
            sz["polygon"] = [list(p) for p in z["polygon"]]
            sz["color"] = list(z["color"])
            serializable_zones.append(sz)
        
        with open(ZONES_FILE, "w") as f:
            json.dump(serializable_zones, f, indent=2)
    except Exception as e:
        print(f"Error saving zones: {e}")

# Initialize zones from disk
parking_zones: List[Dict] = load_zones_from_disk()


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Detection:
    """Container for a single detection result."""
    track_id: int
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    centroid: Tuple[int, int]
    area: int
    timestamp: float = field(default_factory=time.time)
    has_plate: bool = False
    plate_bbox: Optional[Tuple[int, int, int, int]] = None
    plate_text: Optional[str] = None
    parking_time: float = 0.0
    parking_status: str = ""  # "", "warning", "violation"
    parking_zone: Optional[str] = None
    is_penalized: bool = False
    
    def to_dict(self) -> dict:
        return {
            "track_id": self.track_id,
            "class_id": self.class_id,
            "class_name": self.class_name,
            "confidence": round(self.confidence, 3),
            "bbox": self.bbox,
            "centroid": self.centroid,
            "area": self.area,
            "timestamp": self.timestamp,
            "has_plate": self.has_plate,
            "plate_bbox": self.plate_bbox,
            "plate_text": self.plate_text,
            "parking_time": round(self.parking_time, 1),
            "parking_status": self.parking_status,
            "parking_zone": self.parking_zone,
            "is_penalized": self.is_penalized,
        }


@dataclass 
class FrameResult:
    """Container for detection results from a single frame."""
    frame_id: int
    timestamp: float
    detections: List[Detection]
    inference_time_ms: float
    plate_boxes: List[Tuple[int, int, int, int]] = field(default_factory=list)
    image: Optional[np.ndarray] = None
    vehicle_count: int = 0
    parking_warnings: int = 0
    parking_violations: int = 0
    
    def to_dict(self) -> dict:
        return {
            "frame_id": self.frame_id,
            "timestamp": self.timestamp,
            "detection_count": len(self.detections),
            "plate_count": len(self.plate_boxes),
            "inference_time_ms": round(self.inference_time_ms, 2),
            "vehicle_count": self.vehicle_count,
            "parking_warnings": self.parking_warnings,
            "parking_violations": self.parking_violations,
            "detections": [d.to_dict() for d in self.detections],
        }


# ============================================================================
# CLASS DEFINITIONS
# ============================================================================

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle", 
    5: "bus",
    7: "truck",
}

TRAFFIC_CLASSES = {
    **VEHICLE_CLASSES,
    0: "person",
    1: "bicycle",
}

VEHICLE_CLASS_IDS = [2, 3, 5, 7]


# ============================================================================
# LAZY SERVICE IMPORTS
# ============================================================================

_ocr_service = None
_scoring_engine = None
_traffic_controller = None
_tts_service = None


def get_ocr_service():
    """Lazy load OCR service."""
    global _ocr_service
    if _ocr_service is None:
        try:
            from app.services.ocr import read_plate
            _ocr_service = read_plate
            print("✅ OCR service loaded")
        except ImportError as e:
            print(f"⚠️ OCR service not available: {e}")
            _ocr_service = lambda x: None
    return _ocr_service


def get_scoring_engine():
    """Lazy load scoring engine for database violations."""
    global _scoring_engine
    if _scoring_engine is None:
        try:
            from app.services.scoring import get_scoring_engine as _get_engine, ViolationType
            _scoring_engine = {"engine": _get_engine(), "ViolationType": ViolationType}
            print("✅ Scoring engine loaded")
        except ImportError as e:
            print(f"⚠️ Scoring engine not available: {e}")
            _scoring_engine = {"engine": None, "ViolationType": None}
    return _scoring_engine





def get_tts_service():
    """Lazy load TTS service for voice warnings."""
    global _tts_service
    if _tts_service is None:
        try:
            from app.services.tts import get_tts_service as _get_tts
            _tts_service = _get_tts()
            print("✅ TTS service loaded")
        except ImportError as e:
            print(f"⚠️ TTS service not available: {e}")
            _tts_service = None
    return _tts_service


# ============================================================================
# TTS WARNING FUNCTION
# ============================================================================

def speak_warning(message: str, track_id: int = None, warning_type: str = None):
    """
    Play a voice warning using cached audio files (instant, non-blocking).
    
    Args:
        message: The warning message (used for logging)
        track_id: Vehicle track ID (for cooldown tracking)
        warning_type: Type of warning - 'parking_warning', 'parking_violation', 
                     'speeding_warning'. If None, tries to detect from message.
    
    Includes cooldown to prevent spam.
    """
    global parking_tracker
    
    current_time = time.time()
    
    # Check TTS cooldown for this vehicle
    if track_id is not None and track_id in parking_tracker:
        last_tts = parking_tracker[track_id].get("tts_time", 0)
        if (current_time - last_tts) < TTS_COOLDOWN_SECONDS:
            return  # Skip, too soon
        parking_tracker[track_id]["tts_time"] = current_time
    
    # Log to console
    print(f"[AUDIO] 🔊 {message}")
    
    # Detect warning type from message if not provided
    if warning_type is None:
        msg_lower = message.lower()
        if "parking" in msg_lower and "violation" in msg_lower:
            warning_type = "parking_violation"
        elif "parking" in msg_lower:
            warning_type = "parking_warning"
        elif "speed" in msg_lower:
            warning_type = "speeding_warning"
        else:
            warning_type = "parking_warning"  # Default
    
    # Try to use TTS service
    tts = get_tts_service()
    if tts:
        try:
            # Generate and play specific message (Vehicle ID etc)
            # This ensures we don't rely on potentially missing cached files
            print(f"[TTS] 🎙️ Generating audio for: '{message}'")
            tts.speak(message, play=True)
            
        except Exception as e:
            print(f"[TTS] Error: {e}")


# ============================================================================
# MODEL LOADING
# ============================================================================

def load_model(model_path: str, device: str = "cpu") -> Any:
    """Load a YOLOv8 model with caching."""
    global _model_cache
    
    cache_key = f"{model_path}_{device}"
    
    if cache_key not in _model_cache:
        from ultralytics import YOLO
        
        print(f"🔄 Loading model: {model_path} on {device}...")
        start = time.time()
        
        model = YOLO(model_path)
        model.to(device)
        
        print(f"✅ Model loaded in {time.time() - start:.2f}s")
        _model_cache[cache_key] = model
    
    return _model_cache[cache_key]


def load_vehicle_model(device: str = "cpu") -> Any:
    """Load the YOLOv8 vehicle detection model."""
    model_path = settings.models_dir / settings.vehicle_model
    if not model_path.exists():
        # Fallback for download
        return load_model("yolov8n.pt", device)
    return load_model(str(model_path), device)


def load_plate_model(device: str = "cpu") -> Any:
    """Load the custom license plate detection model."""
    # Prioritize config path
    path = settings.models_dir / settings.plate_model
    
    if path and path.exists():
        print(f"📋 Found plate model at: {path}")
        return load_model(str(path), device)
    
    # Fallback checks (legacy)
    possible_paths = [
        Path("models") / "best_plate.pt",
        Path(__file__).parent.parent.parent.parent / "models" / "best_plate.pt",
    ]
    
    for p in possible_paths:
        if p.exists():
             print(f"📋 Found plate model at: {p}")
             return load_model(str(p), device)
    
    print(f"⚠️ Plate model not found at {path}")
    return None


def get_models(device: str = "cpu") -> Tuple[Any, Any]:
    """Initialize and return both models."""
    return load_vehicle_model(device), load_plate_model(device)


# ============================================================================
# ZONE HELPER FUNCTIONS
# ============================================================================

def point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """Check if a point is inside a polygon using cv2.pointPolygonTest."""
    polygon_np = np.array(polygon, dtype=np.int32)
    result = cv2.pointPolygonTest(polygon_np, point, False)
    return result >= 0


def get_zone_for_point(point: Tuple[int, int], frame_size: Tuple[int, int] = (1, 1)) -> Optional[Dict]:
    """Find which parking zone contains a point, if any."""
    w, h = frame_size
    
    for zone in parking_zones:
        poly_points = zone["polygon"]
        
        # Normalize check
        is_normalized = all(all(c <= 1.0 for c in p) for p in poly_points)
        
        if is_normalized:
            # Scale up for check
            check_poly = [[int(x * w), int(y * h)] for x, y in poly_points]
        else:
            check_poly = poly_points

        if point_in_polygon(point, check_poly):
            return zone
    return None


# ============================================================================
# SPEED ESTIMATION
# ============================================================================




# ============================================================================
# PARKING VIOLATION DETECTION
# ============================================================================

def check_parking_violation(
    det: Detection,
    current_time: float,
    frame_shape: Tuple[int, int] = (1920, 1080), # Default to HD if not provided
) -> Tuple[float, str, Optional[str], bool]:
    """
    Check if a vehicle is in a parking violation zone.
    
    Returns:
        Tuple of (time_in_zone, status, zone_id, is_penalized)
    """
    global parking_tracker, penalized_vehicles
    
    track_id = det.track_id
    
    # Check if vehicle centroid is in any parking zone
    zone = get_zone_for_point(det.centroid, frame_shape)
    
    # GHOST LOGIC: If lost but in grace period, treat as present
    if zone is None and track_id in parking_tracker:
        entry = parking_tracker[track_id]
        # Use stored zone ID to create a fake zone object for logic continuity
        # We don't need polygon here, just ID
        zone = {"id": entry["zone_id"]}
        
        time_since_seen = current_time - entry.get("last_seen", current_time)
        
        if time_since_seen <= 5.0:  # Within grace period
            # Restore ghost zone
             pass # zone is already set above
            # Do NOT update last_seen (it's lost)
        else:
            print(f"[DEBUG] Vehicle {track_id} lost for >5s -> Timer Reset")
            del parking_tracker[track_id]
            return 0.0, "", None, track_id in penalized_vehicles
            
    if zone is None:
        return 0.0, "", None, track_id in penalized_vehicles
    
    zone_id = zone["id"]
    
    # Wrapper for stationary check (since speed detection was removed)
    # We rely on the duration in zone to determine parking.
    is_stationary = True
    
    if track_id in parking_tracker:
        entry = parking_tracker[track_id]
        time_in_zone = current_time - entry["entry_time"]
        
        if time_in_zone >= PARKING_VIOLATION_SECONDS:
            status = "violation"
            
            if not entry.get("penalized", False):
                # Retrieve best plate (history or current)
                best_plate = get_best_plate_text(track_id) or det.plate_text or entry.get("plate")
                
                if not best_plate:
                     # print(f"[DEBUG] ❌ Failed to find plate for ID={track_id}...")
                     pass
                
                # APPLY PENALTY TO DATABASE
                _apply_parking_penalty(
                    track_id=track_id,
                    plate_text=best_plate,
                    zone_id=zone_id,
                )
                entry["penalized"] = True
                penalized_vehicles[track_id] = current_time
                
                # TTS Violation announcement
                plate_display = best_plate or f"Vehicle {track_id}"
                speak_warning(
                    f"Violation recorded for {plate_display}. Fine has been issued.",
                    track_id
                )
                
        elif time_in_zone >= PARKING_WARNING_SECONDS:
            status = "warning"
            
            if not entry.get("warned", False):
                # TTS Warning
                best_plate = get_best_plate_text(track_id) or det.plate_text or f"Vehicle {track_id}"
                print(f"[WARNING] 🎙️ Voice Warning Issued to Vehicle {track_id} (Plate: {best_plate}) - 'Please move immediately'")
                speak_warning(
                    f"{best_plate}, please move immediately. You are in a no parking zone.",
                    track_id
                )
                entry["warned"] = True
        else:
            status = ""
        
        # Update plate if available
        if det.plate_text and not entry.get("plate"):
            entry["plate"] = det.plate_text
        
        # Only update last_seen if we actually see it (zone is not None originally)
        # We know zone is not None here because of the Ghost logic above
        # But we need to distinguish Ghost vs Real
        real_zone = get_zone_for_point(det.centroid, frame_shape)
        if real_zone:
            entry["last_seen"] = current_time
        
        is_penalized = entry.get("penalized", False) or track_id in penalized_vehicles
        return time_in_zone, status, zone_id, is_penalized
    
    else:
        # Start tracking if vehicle is stationary in zone
        # Only start if REAL zone
        if zone and is_stationary:
            # print(f"[DEBUG] Vehicle {track_id} stationary in {zone_id} at {current_time:.1f}")
            parking_tracker[track_id] = {
                "entry_time": current_time,
                "zone_id": zone_id,
                "warned": False,
                "penalized": False,
                "plate": det.plate_text,
                "tts_time": 0,
                "last_seen": current_time,
            }
        return 0.0, "", zone_id, track_id in penalized_vehicles


def _apply_parking_penalty(track_id: int, plate_text: str, zone_id: str):
    """Apply parking violation penalty to database via ScoringEngine."""
    scoring = get_scoring_engine()
    
    driver_id = plate_text or f"UNKNOWN-{track_id}"
    
    if scoring["engine"] is None:
        print(f"[PENALTY] ⚠️ Scoring engine not available. Would penalize: {driver_id}")
        return
    
    ViolationType = scoring["ViolationType"]
    
    try:
        driver, violation = scoring["engine"].record_violation(
            driver_id=driver_id,
            violation_type=ViolationType.PARKING_NO_PARKING,
            location=f"Zone: {zone_id}",
            license_plate=plate_text,
            notes="Automated detection - illegal parking > 15 seconds",
        )
        print(f"\n[VIOLATION DETECTED] 🚨 PARKING VIOLATION > 15s")
        print(f"Vehicle ID: {track_id}")
        print(f"Plate No  : {plate_text or 'Unknown'}")
        print(f"Fine Fee  : LKR {violation.fine_amount}")
        print(f"Details   : Score Deducted (-{violation.points_deducted}), Current Score: {driver.current_score}\n")
        
    except Exception as e:
        print(f"[PENALTY] Error saving to DB: {e}")





def get_best_plate_text(track_id: int) -> Optional[str]:
    """Retrieve the best available plate text from history."""
    # 1. Check current history
    if track_id in plate_history:
        text = plate_history[track_id].get("text")
        if text and len(text) > 3:
            return text
            
    # 2. Check parking tracker
    if track_id in parking_tracker:
        text = parking_tracker[track_id].get("plate")
        if text and len(text) > 3:
            return text
            
    return None

def cleanup_parking_tracker(active_track_ids: set):
    """Remove parking entries for vehicles no longer tracked (with grace period)."""
    global parking_tracker
    
    current_time = time.time()
    grace_period = 5.0  # Keep tracking for 5s even if detection is lost
    
    to_remove = []
    
    for tid, entry in parking_tracker.items():
        if tid not in active_track_ids:
            # Vehicle lost - check grace period
            time_since_seen = current_time - entry.get("last_seen", current_time)
            if time_since_seen > grace_period:
                to_remove.append(tid)
    
    for tid in to_remove:
        print(f"[DEBUG] Vehicle {tid} lost for >{grace_period}s -> Timer Reset")
        del parking_tracker[tid]


# ============================================================================
# SIGNAL AUTOMATION
# ============================================================================




# ============================================================================
# STAGE 1: VEHICLE TRACKING
# ============================================================================

def track_vehicles(
    model: Any,
    frame: np.ndarray,
    confidence: float = 0.5,
    frame_id: int = 0,
) -> Tuple[List[Detection], bool]:
    """
    Stage 1: Vehicle detection with tracking and frame skipping.
    """
    global _prev_detections
    
    run_detection = (frame_id % YOLO_DETECTION_INTERVAL == 0)
    
    if not run_detection and _prev_detections:
        return _prev_detections, False
    
    results = model.track(
        source=frame,
        conf=confidence,
        classes=VEHICLE_CLASS_IDS,
        persist=True,
        verbose=False,
    )
    
    detections = []
    current_time = time.time()
    
    if results and len(results) > 0:
        result = results[0]
        
        if result.boxes is not None:
            boxes = result.boxes
            
            for i in range(len(boxes)):
                xyxy = boxes.xyxy[i].cpu().numpy()
                x1, y1, x2, y2 = map(int, xyxy)
                
                conf = float(boxes.conf[i].cpu().numpy())
                cls_id = int(boxes.cls[i].cpu().numpy())
                
                track_id = int(boxes.id[i].cpu().numpy()) if boxes.id is not None else -1
                
                centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
                area = (x2 - x1) * (y2 - y1)
                class_name = VEHICLE_CLASSES.get(cls_id, f"class_{cls_id}")
                
                detection = Detection(
                    track_id=track_id,
                    class_id=cls_id,
                    class_name=class_name,
                    confidence=conf,
                    bbox=(x1, y1, x2, y2),
                    centroid=centroid,
                    area=area,
                    timestamp=current_time,
                )
                
                detections.append(detection)
    
    _prev_detections = detections
    
    active_ids = {d.track_id for d in detections}
    cleanup_parking_tracker(active_ids)
    
    return detections, True


# ============================================================================
# STAGE 2: PLATE DETECTION WITH OCR
# ============================================================================

def detect_plates_in_crops(
    plate_model: Any,
    frame: np.ndarray,
    vehicle_detections: List[Detection],
    confidence: float = 0.2,
) -> Tuple[List[Tuple[int, int, int, int]], Dict[int, Dict[str, Any]]]:
    """Stage 2: Plate detection with OCR caching."""
    global plate_history, ocr_cooldown
    
    if plate_model is None:
        return [], {}
    
    all_plates = []
    vehicle_plate_map = {}
    
    read_plate = get_ocr_service()
    current_time = time.time()
    
    for det in vehicle_detections:
        vx1, vy1, vx2, vy2 = det.bbox
        
        h, w = frame.shape[:2]
        vx1, vy1 = max(0, vx1), max(0, vy1)
        vx2, vy2 = min(w, vx2), min(h, vy2)
        
        crop_w, crop_h = vx2 - vx1, vy2 - vy1
        if crop_w < 20 or crop_h < 20:
            # print(f"[DEBUG] Skip ID {det.track_id} too small {crop_w}x{crop_h}")
            continue
        
        vehicle_crop = frame[vy1:vy2, vx1:vx2]
        
        # Debug for specific stationary vehicles
        # if det.track_id in parking_tracker:
        #      print(f"[DEBUG] 🔍 Scanning parked vehicle {det.track_id} for plates. Size: {crop_w}x{crop_h}")

        # Adaptive confidence: Lower threshold for vehicles already tracked in parking zones
        eff_conf = 0.1 if det.track_id in parking_tracker else confidence
        
        results = plate_model.predict(source=vehicle_crop, conf=eff_conf, verbose=False)
        
        if results and len(results) > 0 and results[0].boxes is not None:
             # ... existing match logic ...
            boxes = results[0].boxes
            
            for i in range(len(boxes)):
                xyxy = boxes.xyxy[i].cpu().numpy()
                px1, py1, px2, py2 = map(int, xyxy)
                
                # Geometric filter: ignore top 30%
                if (py1 + py2) // 2 < (crop_h * 0.3):
                    continue
                
                # Convert to real coordinates
                real_px1, real_py1 = vx1 + px1, vy1 + py1
                real_px2, real_py2 = vx1 + px2, vy1 + py2
                plate_bbox = (real_px1, real_py1, real_px2, real_py2)
                
                # OCR with caching
                plate_text = None
                should_run_ocr = True
                track_id = det.track_id
                
                if track_id in plate_history and plate_history[track_id].get("text"):
                    plate_text = plate_history[track_id]["text"]
                    last_ocr_time = ocr_cooldown.get(track_id, 0)
                    if (current_time - last_ocr_time) < OCR_COOLDOWN_SECONDS:
                        should_run_ocr = False
                
                if should_run_ocr:
                    plate_crop = vehicle_crop[py1:py2, px1:px2]
                    if plate_crop.size > 0:
                        new_text = read_plate(plate_crop)
                        if new_text:
                            plate_text = new_text
                            # OCR success
                            track_id = det.track_id
                            print(f"[DEBUG] 👁️ OCR READ: ID={track_id}, Text={new_text}")
                            if track_id:
                                ocr_cooldown[track_id] = current_time
                
                all_plates.append(plate_bbox)
                vehicle_plate_map[track_id] = {"bbox": plate_bbox, "text": plate_text}
                
                plate_history[track_id] = {
                    "bbox": plate_bbox,
                    "text": plate_text,
                    "timestamp": current_time,
                    "frame_count": 0,
                }
                break
    
    return all_plates, vehicle_plate_map


def update_plate_history(vehicle_detections: List[Detection]) -> Dict[int, Dict[str, Any]]:
    """Update plate history and return remembered plates."""
    global plate_history
    
    current_track_ids = {det.track_id for det in vehicle_detections}
    remembered_plates = {}
    
    to_remove = []
    for track_id, info in plate_history.items():
        info["frame_count"] += 1
        
        if track_id in current_track_ids and info["frame_count"] < PLATE_HISTORY_MAX_AGE:
            remembered_plates[track_id] = {"bbox": info["bbox"], "text": info.get("text")}
        
        if info["frame_count"] >= PLATE_HISTORY_MAX_AGE:
            to_remove.append(track_id)
    
    for track_id in to_remove:
        del plate_history[track_id]
        if track_id in ocr_cooldown:
            del ocr_cooldown[track_id]
    
    return remembered_plates


# ============================================================================
# MAIN DETECTION PIPELINE
# ============================================================================

def detect_and_track(
    vehicle_model: Any,
    frame: np.ndarray,
    frame_id: int = 0,
    confidence: float = 0.5,
    plate_model: Any = None,
    run_plate_detection: bool = True,
) -> FrameResult:
    """
    Complete detection pipeline with all integrations.
    """
    global _frame_counter, _prev_plate_boxes
    
    timestamp = time.time()
    start_time = time.time()
    
    # Stage 1: Vehicle tracking
    detections, _ = track_vehicles(vehicle_model, frame, confidence, _frame_counter)
    
    # Stage 2: Plate detection
    all_plates = []
    vehicle_plate_map = {}
    
    if run_plate_detection and plate_model is not None:
        if _frame_counter % PLATE_DETECTION_INTERVAL == 0:
            all_plates, vehicle_plate_map = detect_plates_in_crops(plate_model, frame, detections)
            _prev_plate_boxes = all_plates
        else:
            all_plates = _prev_plate_boxes
        
        remembered_plates = update_plate_history(detections)
        for track_id, plate_info in remembered_plates.items():
            if track_id not in vehicle_plate_map:
                vehicle_plate_map[track_id] = plate_info
                if plate_info["bbox"] not in all_plates:
                    all_plates.append(plate_info["bbox"])
    
    # Enrich detections
    parking_warnings = 0
    parking_violations = 0
    
    for det in detections:
        # Add plate info
        if det.track_id in vehicle_plate_map:
            plate_info = vehicle_plate_map[det.track_id]
            det.has_plate = True
            det.plate_bbox = plate_info["bbox"]
            det.plate_text = plate_info.get("text")
        
        # Check parking violations
        # Pass (width, height)
        h, w = frame.shape[:2]
        parking_time, parking_status, zone_id, is_penalized = check_parking_violation(
            det, 
            timestamp,
            frame_shape=(w, h)
        )
        det.parking_time = parking_time
        det.parking_status = parking_status
        det.parking_zone = zone_id
        det.is_penalized = is_penalized
        
        if parking_status == "warning":
            parking_warnings += 1
        elif parking_status == "violation":
            parking_violations += 1
    
    vehicle_count = len(detections)
    
    _frame_counter += 1
    inference_time = (time.time() - start_time) * 1000
    
    return FrameResult(
        frame_id=frame_id,
        timestamp=timestamp,
        detections=detections,
        inference_time_ms=inference_time,
        plate_boxes=all_plates,
        image=frame,
        vehicle_count=vehicle_count,
        parking_warnings=parking_warnings,
        parking_violations=parking_violations,
    )


# ============================================================================
# VISUALIZATION
# ============================================================================

def draw_parking_zones(frame: np.ndarray) -> np.ndarray:
    """Draw the parking zone boundaries on the frame."""
    h, w = frame.shape[:2]
    
    for zone in parking_zones:
        poly_points = zone["polygon"]
        
        # Check if normalized (all values <= 1.0)
        is_normalized = all(all(c <= 1.0 for c in p) for p in poly_points)
        
        if is_normalized:
            # Scale up
            scaled_poly = [[int(x * w), int(y * h)] for x, y in poly_points]
            polygon = np.array(scaled_poly, dtype=np.int32)
        else:
            polygon = np.array(poly_points, dtype=np.int32)

        color = zone.get("color", (0, 0, 255))
        
        # Draw filled polygon with transparency
        overlay = frame.copy()
        cv2.fillPoly(overlay, [polygon], color)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        
        # Draw boundary
        cv2.polylines(frame, [polygon], True, color, 2)
        
        # Draw zone label
        x, y = polygon[0]
        cv2.putText(frame, zone["name"], (x + 5, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame


def draw_detections(
    frame: np.ndarray,
    result: FrameResult,
    show_labels: bool = True,
    show_track_id: bool = True,
    show_parking_zones: bool = True,
    box_thickness: int = 2,
) -> np.ndarray:
    """
    Draw detection boxes, plates, parking status.
    
    Flashing purple for penalized vehicles.
    """
    annotated = frame.copy()
    
    # Draw parking zones first
    if show_parking_zones:
        annotated = draw_parking_zones(annotated)
    
    colors = {
        "car": (0, 255, 0),
        "motorcycle": (0, 200, 255),
        "bus": (255, 100, 0),
        "truck": (255, 0, 255),
        "warning": (0, 165, 255),
        "violation": (255, 0, 255),
        "penalized": (255, 0, 255),  # Purple
    }
    plate_color = (255, 255, 0)
    
    # Draw plate boxes
    for px1, py1, px2, py2 in result.plate_boxes:
        cv2.rectangle(annotated, (px1, py1), (px2, py2), plate_color, box_thickness)
    
    current_time = time.time()
    
    for det in result.detections:
        x1, y1, x2, y2 = det.bbox
        
        # Choose color based on status
        if det.is_penalized:
            # Flashing purple effect
            if int(current_time * 4) % 2 == 0:
                color = colors["penalized"]
            else:
                color = (128, 0, 128)  # Darker purple
        elif det.parking_status == "violation":
            color = colors["violation"]
        elif det.parking_status == "warning":
            color = colors["warning"]
        else:
            color = colors.get(det.class_name, (0, 255, 0))
        
        # Draw vehicle box
        thickness = 3 if det.is_penalized else box_thickness
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
        
        # Build label
        if show_labels or show_track_id:
            label_parts = []
            
            if show_track_id and det.track_id >= 0:
                label_parts.append(f"ID:{det.track_id}")
            
            if show_labels:
                label_parts.append(det.class_name)
            
            label = " | ".join(label_parts)
            
            if det.plate_text:
                label += f" | {det.plate_text}"
            elif det.has_plate:
                label += " [Plate]"
            
            # Parking timer
            if det.parking_time > 0:
                label += f" | Parked: {det.parking_time:.0f}s"
                if det.parking_status:
                    label += f" [{det.parking_status.upper()}]"
            
            if det.is_penalized:
                label += " | PENALIZED!"
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8  # INCREASED for visibility
            font_thickness = 2 # INCREASED thickness
            
            (tw, th), _ = cv2.getTextSize(label, font, font_scale, font_thickness)
            
            # Draw label background with slight padding
            cv2.rectangle(annotated, (x1, y1 - th - 12), (x1 + tw + 6, y1), color, -1)
            # Draw label text
            cv2.putText(annotated, label, (x1 + 3, y1 - 5), font, font_scale, (255, 255, 255), font_thickness)
    
    return annotated


def draw_frame_info(frame: np.ndarray, result: FrameResult, extra_info: str = "") -> np.ndarray:
    """Draw frame information overlay."""
    info_parts = [
        f"Frame: {result.frame_id}",
        f"Vehicles: {result.vehicle_count}",
        f"Plates: {len(result.plate_boxes)}",
        f"Parking: W={result.parking_warnings} V={result.parking_violations}",
        f"{result.inference_time_ms:.0f}ms",
    ]
    
    if extra_info:
        info_parts.append(extra_info)
    
    info_text = " | ".join(info_parts)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(info_text, font, 0.8, 2)
    
    # Draw thicker black background for better contrast
    cv2.rectangle(frame, (5, 5), (tw + 20, th + 20), (0, 0, 0), -1)
    # Gold color in BGR is (0, 215, 255)
    cv2.putText(frame, info_text, (10, th + 10), font, 0.8, (0, 215, 255), 2)
    
    return frame


# ============================================================================
# VIDEO PROCESSING
# ============================================================================

def process_video(
    video_path: str,
    vehicle_model: Any = None,
    plate_model: Any = None,
    confidence: float = 0.5,
    skip_frames: int = 0,
    max_frames: Optional[int] = None,
    enable_plate_detection: bool = True,
) -> Generator[FrameResult, None, None]:
    """Process a video file with full detection pipeline."""
    global _frame_counter, _prev_detections, _prev_plate_boxes
    
    _frame_counter = 0
    _prev_detections = []
    _prev_plate_boxes = []
    
    if vehicle_model is None:
        vehicle_model = load_vehicle_model()
    if plate_model is None and enable_plate_detection:
        plate_model = load_plate_model()
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    frame_id = 0
    processed = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if skip_frames > 0 and frame_id % (skip_frames + 1) != 0:
                frame_id += 1
                continue
            
            result = detect_and_track(
                vehicle_model=vehicle_model,
                frame=frame,
                frame_id=frame_id,
                confidence=confidence,
                plate_model=plate_model,
                run_plate_detection=enable_plate_detection,
            )
            
            yield result
            
            processed += 1
            frame_id += 1
            
            if max_frames and processed >= max_frames:
                break
    finally:
        cap.release()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def reset_state():
    """Reset all global tracking state."""
    global _frame_counter, _prev_detections, _prev_plate_boxes
    global plate_history, ocr_cooldown, speed_history, parking_tracker, penalized_vehicles
    
    _frame_counter = 0
    _prev_detections = []
    _prev_plate_boxes = []
    plate_history.clear()
    ocr_cooldown.clear()
    speed_history.clear()
    parking_tracker.clear()
    penalized_vehicles.clear()
    
    print("🔄 Detection state reset")


    global parking_zones
    parking_zones = zones
    save_zones_to_disk(zones)
    print(f"📍 Updated parking zones: {len(zones)} zones")

def add_parking_zone(zone: Dict):
    """Add a new parking zone and save."""
    global parking_zones
    # Check if exists
    for z in parking_zones:
        if z["id"] == zone["id"]:
            return # Already exists
    parking_zones.append(zone)
    save_zones_to_disk(parking_zones)
    print(f"📍 Added zone: {zone['id']}")

def remove_parking_zone(zone_id: str) -> bool:
    """Remove a parking zone and save."""
    global parking_zones
    initial_len = len(parking_zones)
    parking_zones = [z for z in parking_zones if z["id"] != zone_id]
    
    if len(parking_zones) < initial_len:
        save_zones_to_disk(parking_zones)
        print(f"📍 Removed zone: {zone_id}")
        return True
    return False

def reset_parking_zones():
    """Clear all parking zones."""
    global parking_zones
    parking_zones = []
    save_zones_to_disk(parking_zones)
    print("📍 Reset all parking zones")


def detect_plates(plate_model, frame, vehicle_detections, confidence=0.3):
    """Legacy compatibility function."""
    plates, plate_map = detect_plates_in_crops(plate_model, frame, vehicle_detections, confidence)
    legacy_map = {tid: info["bbox"] for tid, info in plate_map.items()}
    return plates, legacy_map


# ============================================================================
# MAIN - Standalone testing
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Full Integration Detection")
    parser.add_argument("--video", type=str, help="Path to video file")
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--no-plates", action="store_true")
    parser.add_argument("--display", action="store_true")
    args = parser.parse_args()
    
    print("🚀 Full Integration Detection Pipeline")
    print(f"   YOLO Interval: {YOLO_DETECTION_INTERVAL}")
    print(f"   Plate Interval: {PLATE_DETECTION_INTERVAL}")
    print(f"   OCR Cooldown: {OCR_COOLDOWN_SECONDS}s")
    print(f"   Speeding: {SPEEDING_THRESHOLD_PIXELS} px/s")
    print(f"   Parking Warning: {PARKING_WARNING_SECONDS}s")
    print(f"   Parking Violation: {PARKING_VIOLATION_SECONDS}s")
    print(f"   Parking Zones: {len(parking_zones)}")
    
    vehicle_model, plate_model = get_models()
    
    video_path = args.video or str(Path(__file__).parent.parent.parent.parent / "data" / "videos" / "SriLankan_Traffic_Video.mp4")
    
    print(f"📹 Processing: {video_path}")
    reset_state()
    
    for result in process_video(
        video_path,
        vehicle_model=vehicle_model,
        plate_model=plate_model if not args.no_plates else None,
        confidence=args.confidence,
        enable_plate_detection=not args.no_plates,
    ):
        annotated = draw_detections(result.image, result)
        annotated = draw_frame_info(annotated, result)
        
        print(f"F{result.frame_id}: V={result.vehicle_count} P={len(result.plate_boxes)} S={result.speeding_count} Park={result.parking_warnings}/{result.parking_violations} {result.inference_time_ms:.0f}ms")
        
        if args.display:
            cv2.imshow("Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    if args.display:
        cv2.destroyAllWindows()
    
    print("✅ Complete!")
