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
