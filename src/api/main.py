"""
FastAPI Backend for Intelligent Traffic Management System
Complete REST API with authentication, CRUD operations, and real-time features
"""

from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pydantic import BaseModel
from bson import ObjectId
import bcrypt
import jwt
import os
from dotenv import load_dotenv

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.connection import Database
from src.database.models import (
    User, Vehicle, Violation, DetectionLog, Warning,
    DriverProfile, Payment, TrafficImpact, Camera
)

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Traffic Management API",
    description="REST API for traffic violation detection and management",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
db_instance = Database()
db = db_instance.get_db()

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================================
# PYDANTIC SCHEMAS FOR REQUEST/RESPONSE
# ============================================================================

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "driver"


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str


class VehicleCreate(BaseModel):
    license_plate: str
    vehicle_type: str
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class ViolationCreate(BaseModel):
    vehicle_id: Optional[str] = None
    vehicle_type: str
    license_plate: Optional[str] = None
    violation_type: str
    severity: str
    fine_amount: float
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confidence: float
    image_path: Optional[str] = None


class WarningCreate(BaseModel):
    user_id: str
    vehicle_id: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    warning_type: str = "predictive_parking"
    message: str
    severity: str = "medium"


class PaymentCreate(BaseModel):
    violation_id: str
    amount: float
    payment_method: str
    transaction_id: Optional[str] = None


# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Decode and validate JWT token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_safety_score(user_id: str) -> int:
    """Calculate driver safety score based on violations and warnings."""
    user_obj_id = ObjectId(user_id)

    # Get violation count
    violation_count = db.violations.count_documents({"vehicle_id": user_obj_id})

    # Get warning count
    warning_count = db.warnings.count_documents({"user_id": user_obj_id})

    # Get warnings heeded (responded to)
    warnings_heeded = db.warnings.count_documents({
        "user_id": user_obj_id,
        "responded": True
    })

    # Calculate score (start at 100)
    score = 100
    score -= (violation_count * 5)  # -5 per violation
    score -= (warning_count * 2)  # -2 per warning
    score += (warnings_heeded * 3)  # +3 for heeding warnings

    return max(0, min(100, score))  # Keep between 0-100


def get_score_badge(score: int) -> str:
    """Get badge based on safety score."""
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Poor"


# ============================================================================
# ROOT & HEALTH CHECK
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Intelligent Traffic Management API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    """Register a new user."""
    # Check if user exists
    if db.users.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    if db.users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "full_name": user_data.full_name,
        "phone": user_data.phone,
        "role": user_data.role,
        "safety_score": 100,
        "score_badge": "Good",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_login": None
    }

    result = db.users.insert_one(user_dict)
    user_id = str(result.inserted_id)

    # Create access token
    access_token = create_access_token(
        data={"sub": user_id, "username": user_data.username, "role": user_data.role}
    )

    return TokenResponse(
        access_token=access_token,
        user_id=user_id,
        username=user_data.username,
        role=user_data.role
    )


@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user and return JWT token."""
    user = db.users.find_one({"username": credentials.username})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Update last login
    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    # Create access token
    user_id = str(user["_id"])
    access_token = create_access_token(
        data={"sub": user_id, "username": user["username"], "role": user["role"]}
    )

    return TokenResponse(
        access_token=access_token,
        user_id=user_id,
        username=user["username"],
        role=user["role"]
    )


@app.get("/auth/me")
async def get_current_user(token_data: dict = Depends(decode_token)):
    """Get current authenticated user."""
    user = db.users.find_one({"_id": ObjectId(token_data["sub"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    user.pop("hashed_password", None)
    return user


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.get("/users/{user_id}")
async def get_user(user_id: str, token_data: dict = Depends(decode_token)):
    """Get user by ID."""
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    user.pop("hashed_password", None)
    return user


@app.put("/users/{user_id}/safety-score")
async def update_safety_score(user_id: str, token_data: dict = Depends(decode_token)):
    """Recalculate and update user safety score."""
    score = calculate_safety_score(user_id)
    badge = get_score_badge(score)

    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"safety_score": score, "score_badge": badge}}
    )

    return {"user_id": user_id, "safety_score": score, "score_badge": badge}


# ============================================================================
# VEHICLE ENDPOINTS
# ============================================================================

@app.post("/vehicles")
async def create_vehicle(vehicle: VehicleCreate, token_data: dict = Depends(decode_token)):
    """Register a new vehicle."""
    vehicle_dict = {
        "owner_id": ObjectId(token_data["sub"]),
        "license_plate": vehicle.license_plate,
        "vehicle_type": vehicle.vehicle_type,
        "color": vehicle.color,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "registered_at": datetime.utcnow()
    }

    result = db.vehicles.insert_one(vehicle_dict)
    vehicle_dict["_id"] = str(result.inserted_id)
    vehicle_dict["owner_id"] = str(vehicle_dict["owner_id"])

    return vehicle_dict


@app.get("/vehicles")
async def get_user_vehicles(token_data: dict = Depends(decode_token)):
    """Get all vehicles for current user."""
    vehicles = list(db.vehicles.find({"owner_id": ObjectId(token_data["sub"])}))
    for v in vehicles:
        v["_id"] = str(v["_id"])
        v["owner_id"] = str(v["owner_id"])
    return vehicles


@app.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: str, token_data: dict = Depends(decode_token)):
    """Get vehicle by ID."""
    vehicle = db.vehicles.find_one({"_id": ObjectId(vehicle_id)})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle["_id"] = str(vehicle["_id"])
    if vehicle.get("owner_id"):
        vehicle["owner_id"] = str(vehicle["owner_id"])
    return vehicle


# ============================================================================
# VIOLATION ENDPOINTS
# ============================================================================

@app.post("/violations")
async def create_violation(violation: ViolationCreate, token_data: dict = Depends(decode_token)):
    """Create a new violation record."""
    violation_dict = {
        "vehicle_id": ObjectId(violation.vehicle_id) if violation.vehicle_id else None,
        "vehicle_type": violation.vehicle_type,
        "license_plate": violation.license_plate,
        "violation_type": violation.violation_type,
        "severity": violation.severity,
        "fine_amount": violation.fine_amount,
        "location": violation.location,
        "latitude": violation.latitude,
        "longitude": violation.longitude,
        "timestamp": datetime.utcnow(),
        "image_path": violation.image_path,
        "confidence": violation.confidence,
        "status": "pending",
        "officer_id": ObjectId(token_data["sub"]),
        "notes": None
    }

    result = db.violations.insert_one(violation_dict)
    violation_dict["_id"] = str(result.inserted_id)
    if violation_dict.get("vehicle_id"):
        violation_dict["vehicle_id"] = str(violation_dict["vehicle_id"])
    if violation_dict.get("officer_id"):
        violation_dict["officer_id"] = str(violation_dict["officer_id"])

    return violation_dict


@app.get("/violations")
async def get_violations(
    status: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    token_data: dict = Depends(decode_token)
):
    """Get all violations with optional filtering."""
    query = {}
    if status:
        query["status"] = status

    violations = list(db.violations.find(query).sort("timestamp", -1).limit(limit).skip(skip))

    for v in violations:
        v["_id"] = str(v["_id"])
        if v.get("vehicle_id"):
            v["vehicle_id"] = str(v["vehicle_id"])
        if v.get("officer_id"):
            v["officer_id"] = str(v["officer_id"])

    return violations


@app.get("/violations/{violation_id}")
async def get_violation(violation_id: str, token_data: dict = Depends(decode_token)):
    """Get violation by ID."""
    violation = db.violations.find_one({"_id": ObjectId(violation_id)})
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    violation["_id"] = str(violation["_id"])
    if violation.get("vehicle_id"):
        violation["vehicle_id"] = str(violation["vehicle_id"])
    if violation.get("officer_id"):
        violation["officer_id"] = str(violation["officer_id"])

    return violation


@app.delete("/violations/{violation_id}")
async def delete_violation(violation_id: str, token_data: dict = Depends(decode_token)):
    """Delete a violation (admin/officer only)."""
    if token_data.get("role") not in ["admin", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    result = db.violations.delete_one({"_id": ObjectId(violation_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Violation not found")

    return {"message": "Violation deleted successfully"}


@app.get("/violations/user/{user_id}")
async def get_user_violations(user_id: str, token_data: dict = Depends(decode_token)):
    """Get all violations for a specific user's vehicles."""
    # Get user's vehicles
    vehicles = list(db.vehicles.find({"owner_id": ObjectId(user_id)}))
    vehicle_ids = [v["_id"] for v in vehicles]

    # Get violations for those vehicles
    violations = list(db.violations.find({"vehicle_id": {"$in": vehicle_ids}}).sort("timestamp", -1))

    for v in violations:
        v["_id"] = str(v["_id"])
        if v.get("vehicle_id"):
            v["vehicle_id"] = str(v["vehicle_id"])
        if v.get("officer_id"):
            v["officer_id"] = str(v["officer_id"])

    return violations


# ============================================================================
# WARNING ENDPOINTS
# ============================================================================

@app.post("/warnings")
async def create_warning(warning: WarningCreate, token_data: dict = Depends(decode_token)):
    """Create a predictive warning."""
    warning_dict = {
        "user_id": ObjectId(warning.user_id),
        "vehicle_id": ObjectId(warning.vehicle_id),
        "location": warning.location,
        "latitude": warning.latitude,
        "longitude": warning.longitude,
        "warning_type": warning.warning_type,
        "message": warning.message,
        "severity": warning.severity,
        "timestamp": datetime.utcnow(),
        "responded": False,
        "response_time": None,
        "escalated_to_violation": False,
        "violation_id": None
    }

    result = db.warnings.insert_one(warning_dict)
    warning_dict["_id"] = str(result.inserted_id)
    warning_dict["user_id"] = str(warning_dict["user_id"])
    warning_dict["vehicle_id"] = str(warning_dict["vehicle_id"])

    # TODO: Send push notification to user

    return warning_dict


@app.get("/warnings/user/{user_id}")
async def get_user_warnings(user_id: str, limit: int = 50, token_data: dict = Depends(decode_token)):
    """Get warnings for a specific user."""
    warnings = list(db.warnings.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1).limit(limit))

    for w in warnings:
        w["_id"] = str(w["_id"])
        w["user_id"] = str(w["user_id"])
        w["vehicle_id"] = str(w["vehicle_id"])
        if w.get("violation_id"):
            w["violation_id"] = str(w["violation_id"])

    return warnings


@app.put("/warnings/{warning_id}/respond")
async def respond_to_warning(warning_id: str, token_data: dict = Depends(decode_token)):
    """Mark warning as responded to."""
    warning = db.warnings.find_one({"_id": ObjectId(warning_id)})
    if not warning:
        raise HTTPException(status_code=404, detail="Warning not found")

    # Calculate response time
    response_time = (datetime.utcnow() - warning["timestamp"]).total_seconds()

    db.warnings.update_one(
        {"_id": ObjectId(warning_id)},
        {"$set": {"responded": True, "response_time": int(response_time)}}
    )

    # Update user safety score
    user_id = str(warning["user_id"])
    await update_safety_score(user_id, token_data)

    return {"message": "Warning marked as responded", "response_time": response_time}


# ============================================================================
# PAYMENT ENDPOINTS
# ============================================================================

@app.post("/payments")
async def create_payment(payment: PaymentCreate, token_data: dict = Depends(decode_token)):
    """Process a payment for a violation."""
    # Verify violation exists
    violation = db.violations.find_one({"_id": ObjectId(payment.violation_id)})
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    payment_dict = {
        "violation_id": ObjectId(payment.violation_id),
        "user_id": ObjectId(token_data["sub"]),
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "transaction_id": payment.transaction_id,
        "status": "completed",  # In production, this would be "pending" initially
        "payment_date": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "receipt_url": None
    }

    result = db.payments.insert_one(payment_dict)

    # Update violation status
    db.violations.update_one(
        {"_id": ObjectId(payment.violation_id)},
        {"$set": {"status": "paid"}}
    )

    payment_dict["_id"] = str(result.inserted_id)
    payment_dict["violation_id"] = str(payment_dict["violation_id"])
    payment_dict["user_id"] = str(payment_dict["user_id"])

    return payment_dict


@app.get("/payments/user/{user_id}")
async def get_user_payments(user_id: str, token_data: dict = Depends(decode_token)):
    """Get all payments for a user."""
    payments = list(db.payments.find({"user_id": ObjectId(user_id)}).sort("created_at", -1))

    for p in payments:
        p["_id"] = str(p["_id"])
        p["violation_id"] = str(p["violation_id"])
        p["user_id"] = str(p["user_id"])

    return payments


# ============================================================================
# TRAFFIC IMPACT ENDPOINTS
# ============================================================================

@app.post("/traffic-impact")
async def create_traffic_impact(
    violation_id: str,
    vehicles_affected: int,
    duration_seconds: int,
    lane_blocked: bool,
    token_data: dict = Depends(decode_token)
):
    """Record traffic impact for a violation."""
    # Calculate congestion metrics
    congestion_score = min(1.0, vehicles_affected / 20.0)  # Normalized to 1.0

    if congestion_score < 0.25:
        congestion_level = "low"
        impact_multiplier = 1.0
    elif congestion_score < 0.5:
        congestion_level = "medium"
        impact_multiplier = 1.5
    elif congestion_score < 0.75:
        congestion_level = "high"
        impact_multiplier = 2.0
    else:
        congestion_level = "severe"
        impact_multiplier = 3.0

    estimated_delay = (vehicles_affected * duration_seconds) / 60.0  # minutes

    impact_dict = {
        "violation_id": ObjectId(violation_id),
        "vehicles_affected": vehicles_affected,
        "congestion_level": congestion_level,
        "congestion_score": congestion_score,
        "duration_seconds": duration_seconds,
        "lane_blocked": lane_blocked,
        "impact_multiplier": impact_multiplier,
        "timestamp": datetime.utcnow(),
        "estimated_delay_minutes": estimated_delay
    }

    result = db.traffic_impact.insert_one(impact_dict)
    impact_dict["_id"] = str(result.inserted_id)
    impact_dict["violation_id"] = str(impact_dict["violation_id"])

    return impact_dict


# ============================================================================
# DASHBOARD ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/dashboard/stats")
async def get_dashboard_stats(token_data: dict = Depends(decode_token)):
    """Get overall dashboard statistics."""
    total_violations = db.violations.count_documents({})
    pending_violations = db.violations.count_documents({"status": "pending"})
    paid_violations = db.violations.count_documents({"status": "paid"})
    total_warnings = db.warnings.count_documents({})
    warnings_heeded = db.warnings.count_documents({"responded": True})

    # Calculate total fines
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$fine_amount"}}}
    ]
    fine_result = list(db.violations.aggregate(pipeline))
    total_fines = fine_result[0]["total"] if fine_result else 0

    # Violations by type
    violations_by_type = list(db.violations.aggregate([
        {"$group": {"_id": "$violation_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))

    # Violations by vehicle type
    violations_by_vehicle = list(db.violations.aggregate([
        {"$group": {"_id": "$vehicle_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))

    # Violations by hour (for heat map)
    violations_by_hour = list(db.violations.aggregate([
        {
            "$group": {
                "_id": {"$hour": "$timestamp"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]))

    return {
        "total_violations": total_violations,
        "pending_violations": pending_violations,
        "paid_violations": paid_violations,
        "total_warnings": total_warnings,
        "warnings_heeded": warnings_heeded,
        "warning_success_rate": (warnings_heeded / total_warnings * 100) if total_warnings > 0 else 0,
        "total_fines": total_fines,
        "violations_by_type": violations_by_type,
        "violations_by_vehicle": violations_by_vehicle,
        "violations_by_hour": violations_by_hour
    }


@app.get("/dashboard/recent-violations")
async def get_recent_violations(limit: int = 10, token_data: dict = Depends(decode_token)):
    """Get recent violations with full details."""
    violations = list(db.violations.find().sort("timestamp", -1).limit(limit))

    for v in violations:
        v["_id"] = str(v["_id"])
        if v.get("vehicle_id"):
            v["vehicle_id"] = str(v["vehicle_id"])
        if v.get("officer_id"):
            v["officer_id"] = str(v["officer_id"])

    return violations


@app.get("/dashboard/traffic-impact-summary")
async def get_traffic_impact_summary(token_data: dict = Depends(decode_token)):
    """Get summary of traffic impact."""
    impacts = list(db.traffic_impact.find().sort("timestamp", -1).limit(100))

    total_vehicles_affected = sum(i["vehicles_affected"] for i in impacts)
    total_delay_minutes = sum(i["estimated_delay_minutes"] for i in impacts)
    avg_congestion_score = sum(i["congestion_score"] for i in impacts) / len(impacts) if impacts else 0

    congestion_breakdown = {}
    for i in impacts:
        level = i["congestion_level"]
        congestion_breakdown[level] = congestion_breakdown.get(level, 0) + 1

    return {
        "total_vehicles_affected": total_vehicles_affected,
        "total_delay_minutes": total_delay_minutes,
        "average_congestion_score": avg_congestion_score,
        "congestion_breakdown": congestion_breakdown,
        "total_incidents": len(impacts)
    }


# ============================================================================
# CAMERA MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/cameras")
async def create_camera(
    name: str,
    location: str,
    latitude: float,
    longitude: float,
    token_data: dict = Depends(decode_token)
):
    """Add a new camera location."""
    if token_data.get("role") not in ["admin", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    camera_dict = {
        "name": name,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "camera_type": "fixed",
        "status": "active",
        "no_parking_zone": True,
        "zone_polygon": None,
        "stream_url": None,
        "last_detection": None,
        "total_detections": 0,
        "created_at": datetime.utcnow()
    }

    result = db.cameras.insert_one(camera_dict)
    camera_dict["_id"] = str(result.inserted_id)

    return camera_dict


@app.get("/cameras")
async def get_cameras(token_data: dict = Depends(decode_token)):
    """Get all cameras."""
    cameras = list(db.cameras.find())
    for c in cameras:
        c["_id"] = str(c["_id"])
    return cameras


@app.delete("/cameras/{camera_id}")
async def delete_camera(camera_id: str, token_data: dict = Depends(decode_token)):
    """Delete a camera."""
    if token_data.get("role") not in ["admin", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    result = db.cameras.delete_one({"_id": ObjectId(camera_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Camera not found")

    return {"message": "Camera deleted successfully"}


# ============================================================================
# EXPORT ENDPOINTS
# ============================================================================

@app.get("/export/violations/csv")
async def export_violations_csv(token_data: dict = Depends(decode_token)):
    """Export violations as CSV data."""
    if token_data.get("role") not in ["admin", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    violations = list(db.violations.find().sort("timestamp", -1))

    # Convert to CSV format
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID", "Vehicle Type", "License Plate", "Violation Type",
        "Severity", "Fine Amount", "Location", "Timestamp", "Status"
    ])

    # Data
    for v in violations:
        writer.writerow([
            str(v["_id"]),
            v.get("vehicle_type", ""),
            v.get("license_plate", ""),
            v.get("violation_type", ""),
            v.get("severity", ""),
            v.get("fine_amount", 0),
            v.get("location", ""),
            v.get("timestamp", ""),
            v.get("status", "")
        ])

    return {"csv_data": output.getvalue()}


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
