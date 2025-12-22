"""
Intelligent Traffic Management System - API Routers
"""

from app.api.video import router as video_router
from app.api.parking import router as parking_router

__all__ = ["video_router", "parking_router"]
