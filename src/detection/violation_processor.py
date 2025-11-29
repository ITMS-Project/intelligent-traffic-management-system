"""Process detections and create violation records with fine calculation."""
from typing import Dict, List
from datetime import datetime
import uuid
import os


class ViolationProcessor:
    """Process detections and create violation records."""

    def __init__(self):
        """Initialize violation processor with fine structure."""
        # Base fines for each vehicle type (in LKR - Sri Lankan Rupees)
        self.base_fines = {
            'parked_car': 2000,
            'parked_tuktuk': 1500,
            'parked_bus': 5000,
            'parked_van': 3000,
            'parked_truck': 4000,
            'parked_motorcycle': 1000,
            'parked_jeep': 2500
        }

        # Violation type descriptions
        self.violation_types = {
            'illegal_parking': 'Illegal Parking in Restricted Zone',
            'no_parking_zone': 'Parking in No-Parking Zone',
            'blocking_traffic': 'Blocking Traffic Flow',
            'bus_lane': 'Parking in Bus Lane',
            'pedestrian_crossing': 'Parking on Pedestrian Crossing',
            'double_parking': 'Double Parking'
        }

    def calculate_impact_score(self, lane_blockage: float, vehicles_delayed: int,
                               duration_minutes: int = 10) -> float:
        """
        Calculate traffic impact score (0-100).

        Args:
            lane_blockage: Percentage of lane blocked (0-100)
            vehicles_delayed: Number of vehicles affected
            duration_minutes: Parking duration in minutes

        Returns:
            Impact score (0-100)
        """
        # Weighted formula for impact
        blockage_score = lane_blockage * 0.4  # Max 40 points
        delay_score = min(vehicles_delayed * 2, 40)  # Max 40 points
        duration_score = min(duration_minutes * 2, 20)  # Max 20 points

        total_score = blockage_score + delay_score + duration_score
        return min(total_score, 100)  # Cap at 100

    def determine_severity(self, impact_score: float) -> str:
        """
        Determine severity level based on impact score.

        Args:
            impact_score: Traffic impact score (0-100)

        Returns:
            Severity level: 'low', 'medium', 'high', or 'severe'
        """
        if impact_score < 25:
            return 'low'
        elif impact_score < 50:
            return 'medium'
        elif impact_score < 75:
            return 'high'
        else:
            return 'severe'

    def calculate_fine(self, vehicle_type: str, severity: str,
                      is_repeat_offender: bool = False) -> float:
        """
        Calculate fine amount based on vehicle type, severity, and offender status.

        Args:
            vehicle_type: Type of vehicle (from detection)
            severity: Severity level
            is_repeat_offender: Whether this is a repeat offense

        Returns:
            Fine amount in LKR
        """
        # Get base fine
        base_fine = self.base_fines.get(vehicle_type, 2000)

        # Severity multipliers
        severity_multipliers = {
            'low': 1.0,
            'medium': 1.5,
            'high': 2.0,
            'severe': 2.5
        }

        # Calculate fine
        fine = base_fine * severity_multipliers.get(severity, 1.0)

        # Add 50% penalty for repeat offenders
        if is_repeat_offender:
            fine *= 1.5

        return round(fine, 2)

    def create_violation_record(self, detection: Dict, location: str,
                               camera_id: str = "CAM-001",
                               license_plate: str = None,
                               violation_type: str = "illegal_parking",
                               lane_blockage: float = 50.0,
                               vehicles_delayed: int = 5,
                               image_path: str = None) -> Dict:
        """
        Create a complete violation record from detection.

        Args:
            detection: Detection dict from RealtimeDetector
            location: Location description
            camera_id: Camera identifier
            license_plate: Vehicle license plate (if detected)
            violation_type: Type of violation
            lane_blockage: Percentage of lane blocked
            vehicles_delayed: Number of vehicles delayed
            image_path: Path to violation image

        Returns:
            Complete violation record dict
        """
        # Calculate metrics
        impact_score = self.calculate_impact_score(lane_blockage, vehicles_delayed)
        severity = self.determine_severity(impact_score)
        fine_amount = self.calculate_fine(detection['class_name'], severity)

        # Create violation record
        violation = {
            'vehicle_type': detection['class_name'],
            'license_plate': license_plate,
            'violation_type': violation_type,
            'severity': severity,
            'fine_amount': fine_amount,
            'location': location,
            'latitude': None,  # Can be added if GPS available
            'longitude': None,
            'timestamp': detection.get('timestamp', datetime.utcnow()),
            'image_path': image_path,
            'confidence': detection['confidence'],
            'status': 'pending',
            'officer_id': None,
            'notes': f"Auto-detected {detection['class_name']} with {detection['confidence']:.2%} confidence. "
                    f"Impact score: {impact_score:.1f}/100"
        }

        return violation

    def batch_process_detections(self, detections: List[Dict], location: str,
                                 camera_id: str = "CAM-001") -> List[Dict]:
        """
        Process multiple detections in batch.

        Args:
            detections: List of detection dicts
            location: Location description
            camera_id: Camera identifier

        Returns:
            List of violation records
        """
        violations = []

        for detection in detections:
            violation = self.create_violation_record(
                detection=detection,
                location=location,
                camera_id=camera_id
            )
            violations.append(violation)

        return violations

    def get_fine_summary(self, violations: List[Dict]) -> Dict:
        """
        Get summary of fines from violations.

        Args:
            violations: List of violation records

        Returns:
            Summary dict with totals by severity, vehicle type, etc.
        """
        total_fines = sum(v['fine_amount'] for v in violations)
        total_violations = len(violations)

        # Group by severity
        by_severity = {}
        for v in violations:
            severity = v['severity']
            if severity not in by_severity:
                by_severity[severity] = {'count': 0, 'fines': 0}
            by_severity[severity]['count'] += 1
            by_severity[severity]['fines'] += v['fine_amount']

        # Group by vehicle type
        by_vehicle = {}
        for v in violations:
            vtype = v['vehicle_type']
            if vtype not in by_vehicle:
                by_vehicle[vtype] = {'count': 0, 'fines': 0}
            by_vehicle[vtype]['count'] += 1
            by_vehicle[vtype]['fines'] += v['fine_amount']

        return {
            'total_violations': total_violations,
            'total_fines': total_fines,
            'average_fine': total_fines / total_violations if total_violations > 0 else 0,
            'by_severity': by_severity,
            'by_vehicle_type': by_vehicle
        }

    def format_violation_notice(self, violation: Dict) -> str:
        """
        Format a violation as a notice string.

        Args:
            violation: Violation record dict

        Returns:
            Formatted notice string
        """
        notice = f"""
╔═══════════════════════════════════════════════════════════╗
║          PARKING VIOLATION NOTICE                         ║
╚═══════════════════════════════════════════════════════════╝

Violation ID: {violation.get('_id', 'N/A')}
Date/Time: {violation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
Location: {violation['location']}

Vehicle Information:
  Type: {violation['vehicle_type'].replace('parked_', '').title()}
  License Plate: {violation.get('license_plate', 'Not Detected')}

Violation Details:
  Type: {self.violation_types.get(violation['violation_type'], violation['violation_type'])}
  Severity: {violation['severity'].upper()}
  Confidence: {violation['confidence']:.2%}

Fine Information:
  Amount: LKR {violation['fine_amount']:,.2f}
  Status: {violation['status'].upper()}

{violation.get('notes', '')}

──────────────────────────────────────────────────────────
This is an automated violation notice generated by
Intelligent Traffic Management System
        """
        return notice
