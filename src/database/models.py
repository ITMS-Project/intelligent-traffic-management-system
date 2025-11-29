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
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: str
    hashed_password: str
    role: str = "viewer"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {ObjectId: str}


class Vehicle(BaseModel):
    """Vehicle model for detected vehicles."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    license_plate: Optional[str] = None
    vehicle_type: str
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    
    class Config:
        json_encoders = {ObjectId: str}


class Violation(BaseModel):
    """Parking violation model."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
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
    
    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class DetectionLog(BaseModel):
    """Log of all detections."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    vehicle_type: str
    confidence: float
    is_violation: bool
    violation_id: Optional[PyObjectId] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: str
    image_path: Optional[str] = None
    
    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class ViolationStats(BaseModel):
    """Statistics for violations."""
    total_violations: int
    pending_violations: int
    reviewed_violations: int
    total_fines: float
    violations_by_type: dict
    violations_by_vehicle: dict
    violations_by_severity: dict