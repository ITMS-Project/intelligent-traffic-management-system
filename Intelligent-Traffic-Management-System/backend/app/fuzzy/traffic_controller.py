"""
Intelligent Traffic Management System - Fuzzy Logic Traffic Controller
Uses fuzzy logic to determine optimal green light duration based on traffic conditions.

Research Component for University Grading
==========================================
This module demonstrates fuzzy inference systems for traffic signal optimization.
Uses scikit-fuzzy for fuzzy set operations and rule-based inference.
"""

import numpy as np

try:
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    print("⚠️ scikit-fuzzy not installed. Run: pip install scikit-fuzzy")


class FuzzyTrafficController:
    """
    Fuzzy logic controller for adaptive traffic signal timing.
    
    Input: Vehicle count at intersection
    Output: Green light duration in seconds
    
    Fuzzy Rules:
    - Low traffic (0-5 vehicles) → Short green (10-20s)
    - Medium traffic (5-15 vehicles) → Medium green (20-40s)
    - High traffic (15+ vehicles) → Long green (40-60s)
