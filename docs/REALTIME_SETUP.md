# Real-time Violation Detection Setup Guide

## Overview

Your system can now **detect violations in real-time** and **automatically notify drivers** via the mobile app! Here's how it works:

```
Camera/Video → YOLOv8 Detection → License Plate OCR → Database Lookup
→ Fine Calculation → Violation Record → Push Notification to Driver
```

---

## Features

✅ **Real-time vehicle detection** using trained YOLOv8 model
✅ **License plate recognition** using EasyOCR
✅ **Automatic driver lookup** from database
✅ **Accurate fine calculation** based on violation type & severity
✅ **Database integration** - automatic violation recording
✅ **Push notifications** - drivers instantly notified on mobile app
✅ **Live webcam support** - detect from live camera feed
✅ **Video processing** - batch process recorded footage

---

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install new dependencies (EasyOCR for license plate recognition)
pip install easyocr

# Or install all requirements
pip install -r requirements.txt
```

**Note:** First run of EasyOCR will download ~150MB of OCR models.

### 2. Ensure MongoDB is Running

```bash
brew services start mongodb-community
```

### 3. Add Test Drivers & Vehicles

For the system to work, you need drivers and vehicles in the database. Let's add a test user:

```python
# Run this in Python or create a test script
from src.database.connection import Database
import bcrypt

db = Database()
users_col = db.get_collection('users')
vehicles_col = db.get_collection('vehicles')

# Create test driver
user_data = {
    'username': 'testdriver',
    'email': 'test@example.com',
    'password_hash': bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()),
    'role': 'driver',
    'full_name': 'Test Driver',
    'phone': '+94771234567',
    'safety_score': 100,
    'score_badge': 'Excellent',
    'fcm_token': 'demo-token-123'  # For notifications
}

user_result = users_col.insert_one(user_data)
print(f"User created: {user_result.inserted_id}")

# Add their vehicle
vehicle_data = {
    'owner_id': str(user_result.inserted_id),
    'license_plate': 'WP CAB-1234',  # This plate will be detected
    'vehicle_type': 'car',
    'make': 'Toyota',
    'model': 'Axio',
    'color': 'white',
    'year': 2020
}

vehicle_result = vehicles_col.insert_one(vehicle_data)
print(f"Vehicle added: {vehicle_result.inserted_id}")
```

---

## Running Real-time Detection

### Option 1: Live Webcam Detection

```bash
python run_realtime_detection.py --mode webcam --location "Colombo Junction" --camera-id CAM-001
```

**Controls:**
- `q` - Quit
- `s` - Save current frame
- `r` - Reset statistics

### Option 2: Video File Processing

```bash
python run_realtime_detection.py \
    --mode video \
    --video data/videos/your_traffic_video.mp4 \
    --output output_annotated.mp4 \
    --location "Pettah Market" \
    --sample-rate 30
```

### Option 3: Custom Violation Types

```bash
python run_realtime_detection.py \
    --mode webcam \
    --violation-type blocking_traffic \
    --confidence 0.3
```

**Available violation types:**
- `illegal_parking`
- `no_parking_zone`
- `blocking_traffic`
- `bus_lane`
- `pedestrian_crossing`
- `double_parking`

---

## What Happens When a Violation is Detected?

### Step-by-step Flow:

1. **Detection** 🎯
   - YOLOv8 detects a parked vehicle
   - Confidence > 25% (configurable)

2. **License Plate Recognition** 📋
   - EasyOCR extracts license plate number
   - Formats to Sri Lankan standard (e.g., "WP CAB-1234")

3. **Driver Lookup** 👤
   - Searches database for vehicle by plate
   - Finds registered owner/driver

4. **Fine Calculation** 💰
   - Base fine by vehicle type
   - Severity multiplier (low/medium/high/severe)
   - Impact score (lane blockage, vehicles delayed)
   - **Example:**
     ```
     Parked Car: LKR 2,000 (base)
     × 1.5 (medium severity)
     = LKR 3,000 total fine
     ```

5. **Database Record** 💾
   - Creates violation record with:
     - User ID
     - Vehicle ID
     - License plate
     - Location & timestamp
     - Fine amount
     - Evidence image
     - Violation type & severity

6. **Push Notification** 📱
   - Sends to driver's mobile app:
     ```
     ⚠️ Traffic Violation Detected

     Illegal Parking at Colombo Junction
     Fine: LKR 3,000

     Tap to view details and pay
     ```

7. **Mobile App Updates** 📲
   - Violation appears in driver's app immediately
   - Shows on "Violations" page
   - Displays fine amount
   - Shows evidence image
   - Allows payment

---

## Fine Calculation Details

### Base Fines (LKR)
- Car: 2,000
- Tuktuk: 1,500
- Bus: 5,000
- Van: 3,000
- Truck: 4,000
- Motorcycle: 1,000
- Jeep: 2,500

### Severity Multipliers
- Low (impact 0-25): ×1.0
- Medium (impact 25-50): ×1.5
- High (impact 50-75): ×2.0
- Severe (impact 75-100): ×2.5

### Impact Score Calculation
```python
impact_score = (lane_blockage × 0.4) + (vehicles_delayed × 2) + (duration_minutes × 2)
```

**Example:**
- Lane blockage: 60%
- Vehicles delayed: 10
- Duration: 15 minutes
```
= (60 × 0.4) + (10 × 2) + (15 × 2)
= 24 + 20 + 30
= 74/100 (High severity)
```

---

## Viewing Results

### 1. Check Database

```bash
# View recent violations
mongosh parking_violations_db --eval "
  db.violations.find().sort({timestamp: -1}).limit(5).pretty()
"

# Count total violations
mongosh parking_violations_db --eval "
  db.violations.countDocuments()
"
```

### 2. Authority Dashboard

```bash
streamlit run src/dashboard/authority_dashboard.py
```

Go to: http://localhost:8501
- View real-time violations
- See all detected vehicles
- Monitor notifications sent
- Export data

### 3. Driver Mobile App

```bash
streamlit run src/dashboard/driver_mobile_app.py --server.port 8502
```

Go to: http://localhost:8502
- Login as test driver
- View violations in real-time
- See fine amounts
- Pay violations

---

## Testing the Complete Flow

### Test Script

Create `test_realtime.py`:

```python
#!/usr/bin/env python3
"""Test the complete real-time violation detection flow."""
from src.detection.realtime_pipeline import RealtimeViolationPipeline
import cv2
import numpy as np

# Initialize pipeline
pipeline = RealtimeViolationPipeline(
    location="Test Junction",
    camera_id="TEST-001"
)

# Create a dummy frame (or load real image)
frame = cv2.imread('path/to/traffic/image.jpg')

# Process single frame
result = pipeline.process_frame(frame, violation_type='illegal_parking')

print("\n✅ Test Results:")
print(f"   Detections: {len(result['detections'])}")
print(f"   Violations created: {len(result['violations'])}")
print(f"   Stats: {result['stats']}")

# Show annotated frame
cv2.imshow('Test Result', result['annotated_frame'])
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Run:
```bash
python test_realtime.py
```

---

## Troubleshooting

### Issue: EasyOCR not detecting plates

**Solution:**
- Plates are in bottom 40% of vehicle bounding box
- Ensure good image quality
- Adjust confidence threshold
- Check camera angle (plates should be visible)

### Issue: No driver found for plate

**Solution:**
- Add vehicles to database with correct license plate format
- Format: "WP CAB-1234" or "CP-1234"
- Case-insensitive, spaces/hyphens flexible

### Issue: Notifications not sending

**Solutions:**
- Running in DEMO mode (normal if Firebase not configured)
- Check user has `fcm_token` in database
- Notifications log to console in demo mode

### Issue: No detections

**Solutions:**
- Lower confidence threshold: `--confidence 0.2`
- Ensure model file exists: `runs/parking_violations/exp/weights/best.pt`
- Check video/camera feed is working

---

## Performance Tips

### For Video Processing
- Use `--sample-rate 30` to process every 30th frame (faster)
- Reduce to `--sample-rate 10` for more accuracy
- Lower resolution videos process faster

### For Live Webcam
- Position camera for clear license plate view
- Ensure good lighting
- Stable mounting (avoid shake/vibration)

### For OCR Accuracy
- Good camera resolution (720p minimum)
- Clear, unobstructed plate view
- Proper lighting (not too bright/dark)

---

## Next Steps

1. **Configure Firebase** (Optional)
   - For real push notifications
   - Add Firebase credentials
   - Update user FCM tokens

2. **Train Custom OCR** (Advanced)
   - For better Sri Lankan plate recognition
   - Use your own plate dataset

3. **Deploy to Production**
   - Set up on dedicated server
   - Use IP cameras instead of webcam
   - Configure automatic processing

4. **Integrate Payment Gateway**
   - Connect real payment API
   - Enable online fine payments
   - Generate receipts

---

## System Architecture

```
┌─────────────────┐
│  Camera/Video   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ YOLOv8 Detector │ ← Trained model (88.3% mAP)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  EasyOCR        │ ← License plate recognition
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vehicle Lookup  │ ← MongoDB query
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fine Calculator │ ← Impact score + severity
└────────┬────────┘
         │
         ├───────────────────┬──────────────────┐
         ▼                   ▼                  ▼
┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
│    MongoDB      │  │ Notification │  │  Mobile App  │
│  (Violations)   │  │   Service    │  │   Update     │
└─────────────────┘  └──────────────┘  └──────────────┘
```

---

## Success! 🎉

You now have a **complete real-time traffic violation detection system** that:

✅ Detects violations automatically
✅ Identifies drivers via license plates
✅ Calculates accurate fines
✅ Notifies drivers instantly
✅ Maintains complete records

**Your drivers will receive violations in real-time on their mobile app with correct fine amounts!**

---

For support or questions, check the main `README.md` or `COMPLETE_SYSTEM_GUIDE.md`.
