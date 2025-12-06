"""License Plate Recognition using EasyOCR for Sri Lankan vehicles."""
import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import re


class LicensePlateRecognizer:
    """Recognize license plates from detected vehicle images."""

    def __init__(self):
        """Initialize the OCR recognizer."""
        self.reader = None
        self._initialize_reader()

        # Sri Lankan license plate patterns
        # Format: ABC-1234 or ABC 1234 or WP CAB-1234
        self.plate_patterns = [
            r'[A-Z]{2,3}[\s\-]?[A-Z]{0,3}[\s\-]?\d{4}',  # Standard format
            r'[A-Z]{2}[\s\-]\d{1}[\s\-]\d{4}',  # Old format
        ]

    def _initialize_reader(self):
        """Initialize EasyOCR reader lazily."""
        try:
            import easyocr
            print("🔍 Initializing EasyOCR for license plate recognition...")
            # Use English for Sri Lankan plates
            self.reader = easyocr.Reader(['en'], gpu=False)
            print("✅ EasyOCR initialized successfully!")
        except ImportError:
            print("⚠️  EasyOCR not installed. Install with: pip install easyocr")
            print("⚠️  Running in DEMO mode - will generate mock plate numbers")
            self.reader = None
        except Exception as e:
            print(f"⚠️  Failed to initialize EasyOCR: {e}")
            print("⚠️  Running in DEMO mode")
            self.reader = None

    def preprocess_plate_region(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image region for better OCR accuracy.

        Args:
            image: Input image (BGR format)

        Returns:
            Preprocessed grayscale image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filter to reduce noise while keeping edges
        denoised = cv2.bilateralFilter(gray, 11, 17, 17)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return morph

    def extract_plate_region(self, image: np.ndarray, bbox: List[float]) -> np.ndarray:
        """
        Extract license plate region from full image.

        Args:
            image: Full vehicle image
            bbox: Bounding box [x1, y1, x2, y2]

        Returns:
            Cropped plate region
        """
        x1, y1, x2, y2 = map(int, bbox)

        # Ensure coordinates are within image bounds
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        # Crop the region
        plate_region = image[y1:y2, x1:x2]

        # Focus on bottom 1/3 where plates usually are
        region_h = plate_region.shape[0]
        plate_region = plate_region[int(region_h * 0.6):, :]

        return plate_region

    def clean_plate_text(self, text: str) -> str:
        """
        Clean and format detected text to match Sri Lankan plate format.

        Args:
            text: Raw OCR text

        Returns:
            Cleaned plate number
        """
        # Remove special characters except hyphen and space
        text = re.sub(r'[^A-Z0-9\s\-]', '', text.upper())

        # Remove extra spaces
        text = ' '.join(text.split())

        # Try to match known patterns
        for pattern in self.plate_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        # If no pattern matches, return cleaned text
        return text.strip()

    def recognize_plate(self, image: np.ndarray, bbox: List[float] = None) -> Optional[str]:
        """
        Recognize license plate from vehicle image.

        Args:
            image: Vehicle image (BGR format)
            bbox: Optional bounding box to crop plate region

        Returns:
            Recognized plate number or None
        """
        # Extract plate region if bbox provided
        if bbox is not None:
            plate_region = self.extract_plate_region(image, bbox)
        else:
            plate_region = image

        # Check if region is valid
        if plate_region.size == 0 or plate_region.shape[0] < 10 or plate_region.shape[1] < 10:
            return None

        # DEMO mode - generate mock plate
        if self.reader is None:
            return self._generate_mock_plate()

        try:
            # Preprocess
            processed = self.preprocess_plate_region(plate_region)

            # Run OCR
            results = self.reader.readtext(processed)

            if not results:
                # Try on original image without preprocessing
                results = self.reader.readtext(plate_region)

            # Extract text with highest confidence
            if results:
                # Get text with best confidence
                best_result = max(results, key=lambda x: x[2])
                text = best_result[1]
                confidence = best_result[2]

                # Only accept if confidence > 0.3
                if confidence > 0.3:
                    cleaned = self.clean_plate_text(text)
                    if len(cleaned) >= 5:  # Minimum viable plate length
                        return cleaned

            return None

        except Exception as e:
            print(f"❌ Error during OCR: {e}")
            return None

    def _generate_mock_plate(self) -> str:
        """Generate a mock Sri Lankan license plate for demo mode."""
        import random

        # Sri Lankan province codes
        provinces = ['WP', 'CP', 'SP', 'NP', 'EP', 'NC', 'NW', 'SG', 'UVA']
        # Vehicle types
        types = ['CAB', 'CAR', 'BUS', 'LD', 'KL']

        province = random.choice(provinces)
        vtype = random.choice(types) if random.random() > 0.5 else ''
        number = random.randint(1000, 9999)

        if vtype:
            return f"{province} {vtype}-{number}"
        else:
            return f"{province}-{number}"

    def recognize_multiple_vehicles(
        self,
        image: np.ndarray,
        detections: List[Dict]
    ) -> List[Dict]:
        """
        Recognize license plates for multiple detected vehicles.

        Args:
            image: Full frame image
            detections: List of vehicle detections with bboxes

        Returns:
            Detections with added license_plate field
        """
        enhanced_detections = []

        for detection in detections:
            bbox = detection['bbox']
            plate = self.recognize_plate(image, bbox)

            enhanced_detection = detection.copy()
            enhanced_detection['license_plate'] = plate
            enhanced_detections.append(enhanced_detection)

        return enhanced_detections

    def visualize_plate(
        self,
        image: np.ndarray,
        bbox: List[float],
        plate_text: str
    ) -> np.ndarray:
        """
        Draw license plate on image for visualization.

        Args:
            image: Input image
            bbox: Vehicle bounding box
            plate_text: Recognized plate text

        Returns:
            Image with plate visualization
        """
        annotated = image.copy()

        x1, y1, x2, y2 = map(int, bbox)

        # Draw plate text below vehicle bbox
        if plate_text:
            # Calculate text position
            text_y = y2 + 25

            # Draw background rectangle
            (text_w, text_h), _ = cv2.getTextSize(
                plate_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )
            cv2.rectangle(
                annotated,
                (x1, text_y - text_h - 5),
                (x1 + text_w + 10, text_y + 5),
                (255, 255, 0),  # Yellow background
                -1
            )

            # Draw text
            cv2.putText(
                annotated,
                plate_text,
                (x1 + 5, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),  # Black text
                2
            )

        return annotated
