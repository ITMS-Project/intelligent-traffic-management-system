"""Database CRUD operations for parking violations system."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bson import ObjectId
import bcrypt
from .connection import db
from .models import User, Vehicle, Violation, DetectionLog, ViolationStats


class UserOperations:
    """User database operations."""

    def __init__(self):
        self.collection = db.get_db()['users']
        self._create_indexes()

    def _create_indexes(self):
        """Create indexes for efficient querying."""
        self.collection.create_index("email", unique=True)
        self.collection.create_index("username", unique=True)

    def create_user(self, username: str, email: str, password: str, role: str = "viewer") -> str:
        """Create a new user."""
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )

        result = self.collection.insert_one(user.dict(by_alias=True, exclude={'id'}))
        return str(result.inserted_id)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        return self.collection.find_one({"email": email})

    def verify_password(self, email: str, password: str) -> bool:
        """Verify user password."""
        user = self.get_user_by_email(email)
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8'))

    def get_all_users(self) -> List[Dict]:
        """Get all users."""
        return list(self.collection.find({}, {'hashed_password': 0}))


class VehicleOperations:
    """Vehicle database operations."""

    def __init__(self):
        self.collection = db.get_db()['vehicles']
        self._create_indexes()

    def _create_indexes(self):
        """Create indexes for efficient querying."""
        self.collection.create_index("license_plate", unique=True, sparse=True)

    def register_vehicle(self, license_plate: str, vehicle_type: str,
                        color: str = None, make: str = None, model: str = None) -> str:
        """Register a new vehicle."""
        vehicle = Vehicle(
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            color=color,
            make=make,
            model=model
        )

        result = self.collection.insert_one(vehicle.dict(by_alias=True, exclude={'id'}))
        return str(result.inserted_id)

    def get_vehicle_by_plate(self, license_plate: str) -> Optional[Dict]:
        """Get vehicle by license plate."""
        return self.collection.find_one({"license_plate": license_plate})

    def get_all_vehicles(self) -> List[Dict]:
        """Get all registered vehicles."""
        return list(self.collection.find())


class ViolationOperations:
    """Violation database operations."""

    def __init__(self):
        self.collection = db.get_db()['violations']
        self._create_indexes()

    def _create_indexes(self):
        """Create indexes for efficient querying."""
        self.collection.create_index([("timestamp", -1)])
        self.collection.create_index("license_plate")
        self.collection.create_index("status")

    def create_violation(self, violation_data: Dict) -> str:
        """Create a new violation record."""
        violation = Violation(**violation_data)
        result = self.collection.insert_one(violation.dict(by_alias=True, exclude={'id'}))
        return str(result.inserted_id)

    def get_recent_violations(self, limit: int = 50) -> List[Dict]:
        """Get recent violations."""
        return list(self.collection.find().sort("timestamp", -1).limit(limit))

    def get_violations_by_plate(self, license_plate: str) -> List[Dict]:
        """Get all violations for a specific vehicle."""
        return list(self.collection.find({"license_plate": license_plate}).sort("timestamp", -1))

    def get_pending_violations(self) -> List[Dict]:
        """Get all pending violations."""
        return list(self.collection.find({"status": "pending"}).sort("timestamp", -1))

    def update_violation_status(self, violation_id: str, status: str, officer_id: str = None, notes: str = None) -> bool:
        """Update violation status."""
        update_data = {"status": status}
        if officer_id:
            update_data["officer_id"] = ObjectId(officer_id)
        if notes:
            update_data["notes"] = notes

        result = self.collection.update_one(
            {"_id": ObjectId(violation_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def get_statistics(self, days: int = 7) -> ViolationStats:
        """Get violation statistics for the last N days."""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Total violations
        total_violations = self.collection.count_documents({"timestamp": {"$gte": start_date}})

        # Pending violations
        pending_violations = self.collection.count_documents({
            "timestamp": {"$gte": start_date},
            "status": "pending"
        })

        # Reviewed violations
        reviewed_violations = self.collection.count_documents({
            "timestamp": {"$gte": start_date},
            "status": {"$in": ["reviewed", "paid"]}
        })

        # Total fines
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$fine_amount"}}}
        ]
        fines_result = list(self.collection.aggregate(pipeline))
        total_fines = fines_result[0]["total"] if fines_result else 0

        # Violations by type
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {"_id": "$violation_type", "count": {"$sum": 1}}}
        ]
        violations_by_type = {item["_id"]: item["count"] for item in self.collection.aggregate(pipeline)}

        # Violations by vehicle type
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {"_id": "$vehicle_type", "count": {"$sum": 1}}}
        ]
        violations_by_vehicle = {item["_id"]: item["count"] for item in self.collection.aggregate(pipeline)}

        # Violations by severity
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}}
        ]
        violations_by_severity = {item["_id"]: item["count"] for item in self.collection.aggregate(pipeline)}

        return ViolationStats(
            total_violations=total_violations,
            pending_violations=pending_violations,
            reviewed_violations=reviewed_violations,
            total_fines=total_fines,
            violations_by_type=violations_by_type,
            violations_by_vehicle=violations_by_vehicle,
            violations_by_severity=violations_by_severity
        )

    def get_violations_by_location(self, location: str) -> List[Dict]:
        """Get violations by location."""
        return list(self.collection.find({"location": location}).sort("timestamp", -1))


class DetectionLogOperations:
    """Detection log database operations."""

    def __init__(self):
        self.collection = db.get_db()['detection_logs']
        self._create_indexes()

    def _create_indexes(self):
        """Create indexes for efficient querying."""
        self.collection.create_index([("timestamp", -1)])

    def log_detection(self, detection_data: Dict) -> str:
        """Log a detection event."""
        log = DetectionLog(**detection_data)
        result = self.collection.insert_one(log.dict(by_alias=True, exclude={'id'}))
        return str(result.inserted_id)

    def get_recent_detections(self, limit: int = 100) -> List[Dict]:
        """Get recent detection logs."""
        return list(self.collection.find().sort("timestamp", -1).limit(limit))

    def get_detection_count(self, hours: int = 24) -> int:
        """Get detection count for the last N hours."""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        return self.collection.count_documents({"timestamp": {"$gte": start_time}})


# Global instances
user_ops = UserOperations()
vehicle_ops = VehicleOperations()
violation_ops = ViolationOperations()
detection_log_ops = DetectionLogOperations()
