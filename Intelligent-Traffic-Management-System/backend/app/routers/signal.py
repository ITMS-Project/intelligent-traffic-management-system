"""
Intelligent Traffic Management System - Signal Control Router
API endpoints for traffic signal control using fuzzy logic.
"""

from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.fuzzy.traffic_controller import (
    FuzzyTrafficController,
    TrafficSignal,
    get_signal,
    FUZZY_AVAILABLE,
)

router = APIRouter(prefix="/signal", tags=["Signal Control"])


# =============================================================================
# Pydantic Models
# =============================================================================

class SignalUpdateRequest(BaseModel):
    """Request model for updating signal timing."""
    vehicle_count: int
    signal_id: Optional[str] = "main"


class SignalStateRequest(BaseModel):
    """Request model for setting signal state."""
    state: str  # 'red', 'yellow', 'green'
    duration: Optional[int] = None


class SignalResponse(BaseModel):
    """Response model for signal status."""
    signal_id: str
    state: str
    remaining_time: int
    green_duration: int
    yellow_duration: int
    red_duration: int
    vehicle_count: int
    traffic_level: str


# =============================================================================
# Endpoints
# =============================================================================

@router.get("/status", summary="Get signal status")
async def get_signal_status():
    """Get current traffic signal status."""
    signal = get_signal()
    return signal.get_status()


@router.post("/update", summary="Update signal timing based on traffic")
async def update_signal(request: SignalUpdateRequest):
    """
    Update signal timing based on vehicle count using fuzzy logic.
    
    This endpoint:
    1. Takes the current vehicle count
    2. Runs fuzzy inference to determine optimal green duration
    3. Updates the signal timing parameters
    
    The fuzzy rules:
    - Low traffic (0-5 vehicles) → Short green (~10-20s)
    - Medium traffic (5-15 vehicles) → Medium green (~20-40s)
    - High traffic (15+ vehicles) → Long green (~40-60s)
    """
    signal = get_signal()
