"""Pydantic models for MongoDB documents."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class User(BaseModel):
    """User model for authentication."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "driver"  # "driver", "officer", "admin", "viewer"
    safety_score: int = 100
    score_badge: str = "Good"
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


class Vehicle(BaseModel):
    """Vehicle model for detected vehicles."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner_id: Optional[PyObjectId] = None  # User ID of owner
    license_plate: Optional[str] = None
    vehicle_type: str
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registered_at: datetime = Field(default_factory=datetime.utcnow)


class Violation(BaseModel):
    """Parking violation model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    vehicle_id: Optional[PyObjectId] = None
    vehicle_type: str
    license_plate: Optional[str] = None
    violation_type: str
    severity: str
    fine_amount: float
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    image_path: Optional[str] = None
    confidence: float
    status: str = "pending"
    officer_id: Optional[PyObjectId] = None
    notes: Optional[str] = None


class DetectionLog(BaseModel):
    """Log of all detections."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    vehicle_type: str
    confidence: float
    is_violation: bool
    violation_id: Optional[PyObjectId] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: str
    image_path: Optional[str] = None


class ViolationStats(BaseModel):
    """Statistics for violations."""
    total_violations: int
    pending_violations: int
    reviewed_violations: int
    total_fines: float
    violations_by_type: dict
    violations_by_vehicle: dict
    violations_by_severity: dict


class Warning(BaseModel):
    """Predictive warning model for real-time alerts."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    vehicle_id: PyObjectId
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    warning_type: str = "predictive_parking"  # "predictive_parking", "speed", "zone"
    message: str
    severity: str = "medium"  # "low", "medium", "high"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    responded: bool = False  # Did driver move away?
    response_time: Optional[int] = None  # Seconds to respond
    escalated_to_violation: bool = False
    violation_id: Optional[PyObjectId] = None


class DriverProfile(BaseModel):
    """Driver profile with safety score and history."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    full_name: str
    phone: str
    email: str
    license_number: Optional[str] = None
    safety_score: int = 100  # 0-100
    score_badge: str = "Good"  # "Excellent", "Good", "Average", "Poor"
    total_warnings: int = 0
    total_violations: int = 0
    warnings_heeded: int = 0  # Warnings responded to
    total_fines_paid: float = 0.0
    total_fines_pending: float = 0.0
    registered_vehicles: List[str] = []  # List of vehicle IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class Payment(BaseModel):
    """Payment record for violations."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    violation_id: PyObjectId
    user_id: PyObjectId
    amount: float
    payment_method: str  # "card", "ezcash", "bank_transfer", "online"
    transaction_id: Optional[str] = None
    status: str = "pending"  # "pending", "completed", "failed", "refunded"
    payment_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    receipt_url: Optional[str] = None


class TrafficImpact(BaseModel):
    """Traffic impact analysis for violations."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: lambda v: v.isoformat()}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    violation_id: PyObjectId
    vehicles_affected: int  # Number of vehicles in queue/blocked
    congestion_level: str  # "low", "medium", "high", "severe"
    congestion_score: float  # 0.0 to 1.0
    duration_seconds: int  # How long the violation lasted
    lane_blocked: bool
    impact_multiplier: float  # Fine multiplier based on impact
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    estimated_delay_minutes: float  # Total delay caused


class Camera(BaseModel):
    """Camera/monitoring location model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    location: str
    latitude: float
    longitude: float
    camera_type: str = "fixed"  # "fixed", "mobile", "drone"
    status: str = "active"  # "active", "inactive", "maintenance"
    no_parking_zone: bool = True
    zone_polygon: Optional[List[List[float]]] = None  # [[x,y], [x,y], ...]
    stream_url: Optional[str] = None
    last_detection: Optional[datetime] = None
    total_detections: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)