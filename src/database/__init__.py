"""Database package for parking violations system."""
from .connection import db, Database
from .models import User, Vehicle, Violation, DetectionLog, ViolationStats
from .operations import (
    user_ops,
    vehicle_ops,
    violation_ops,
    detection_log_ops,
    UserOperations,
    VehicleOperations,
    ViolationOperations,
    DetectionLogOperations
)

__all__ = [
    'db',
    'Database',
    'User',
    'Vehicle',
    'Violation',
    'DetectionLog',
    'ViolationStats',
    'user_ops',
    'vehicle_ops',
    'violation_ops',
    'detection_log_ops',
    'UserOperations',
    'VehicleOperations',
    'ViolationOperations',
    'DetectionLogOperations'
]
