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
