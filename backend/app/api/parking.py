"""
Intelligent Traffic Management System - Parking API Router
Endpoints for managing parking zones and violations.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.config import get_settings
from app.services.detection import (
    parking_zones, 
    add_parking_zone, 
    remove_parking_zone, 
    reset_parking_zones
)

settings = get_settings()
router = APIRouter(prefix="/parking", tags=["Parking"])

# =============================================================================
# Pydantic models for request/response
# =============================================================================

class ZoneCreate(BaseModel):
    """Request model for creating a parking zone."""
    zone_id: str
    name: str = "No Parking Zone"
    polygon: List[List[float]]  # List of [x, y] points (normalized 0-1)
    zone_type: str = "no_parking"
    max_duration_sec: float = 5.0
    color: List[int] = [0, 0, 255]  # BGR
    active: bool = True


class ZoneResponse(BaseModel):
    """Response model for a parking zone."""
    id: str
    name: str
    polygon: List[List[float]]
    color: List[int]


# =============================================================================
# Zone Management Endpoints
# =============================================================================

@router.get("/zones", response_model=List[ZoneResponse])
async def list_zones():
    """List all parking zones."""
    return [
        ZoneResponse(
            id=z["id"],
            name=z.get("name", "Unknown"),
            polygon=[list(p) for p in z["polygon"]],
            color=list(z["color"]),
        )
        for z in parking_zones
    ]


@router.post("/zones")
async def create_zone(zone: ZoneCreate):
    """Create a new parking zone."""
    # Convert [x, y] lists to tuples for backend
    new_zone = {
        "id": zone.zone_id,
        "name": zone.name,
        "polygon": [tuple(p) for p in zone.polygon],
        "color": tuple(zone.color),
        "zone_type": zone.zone_type,
        "active": zone.active
    }
    
    add_parking_zone(new_zone)
    return {"status": "created", "zone_id": zone.zone_id}


@router.delete("/zones/{zone_id}")
async def delete_zone_endpoint(zone_id: str):
    """Delete a parking zone."""
    if remove_parking_zone(zone_id):
        return {"status": "deleted", "zone_id": zone_id}
    raise HTTPException(status_code=404, detail=f"Zone not found: {zone_id}")


@router.delete("/zones")
async def clear_zones():
    """Clear ALL parking zones (Reset)."""
    reset_parking_zones()
    return {"status": "cleared", "message": "All parking zones removed"}
