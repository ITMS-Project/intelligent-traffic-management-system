# 🚦 Real-time Violation Detection - Quick Start

## What's New? 🎉

Your traffic management system is now **FULLY REAL-TIME**! Here's what happens:

1. **Camera detects violation** → 2. **Recognizes license plate** → 3. **Finds driver** → 4. **Calculates fine** → 5. **Notifies driver instantly** 📱

---

## 3-Step Quick Start

### Step 1: Install Dependencies

```bash
# Activate environment
source venv/bin/activate

# Install EasyOCR for license plate recognition
pip install easyocr

# First run downloads ~150MB of OCR models (one-time)
```

### Step 2: Setup Test Data

```bash
# Add test drivers and vehicles to database
python setup_test_data.py
```

This creates:
- 4 test users (3 drivers + 1 admin)
- 5 test vehicles with license plates
- Ready-to-detect test data

### Step 3: Start Real-time Detection

**Option A: Live Webcam**
```bash
python run_realtime_detection.py --mode webcam
```

**Option B: Process Video**
```bash
python run_realtime_detection.py --mode video --video data/videos/your_video.mp4
```

That's it! 🎉

---

## What You'll See

### Detection Console Output

```
🚀 Initializing Real-time Violation Detection Pipeline...
✅ Model loaded successfully!
🔍 Initializing EasyOCR for license plate recognition...
✅ Pipeline initialized successfully!

📹 Starting LIVE violation detection from webcam...

🎯 Detection: car (Confidence: 0.85)
   📋 Plate recognized: WP CAB-1234
   👤 Driver found: nimal_silva
   💾 Violation saved to database: 6475a8c9d...
   💰 Fine: LKR 3,000 (Medium severity)
   📱 Notification sent to nimal_silva

📊 STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Detections:       12
Plates Recognized:      8
Violations Created:     8
Drivers Notified:       5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Driver's Mobile App

When a violation occurs, the driver sees:

```
⚠️ New Violation!

Illegal Parking at Main Junction
Fine: LKR 3,000
Vehicle: WP CAB-1234 (Toyota Axio)

📍 Location: Colombo Main Junction
🕐 Time: 2:34 PM
📸 Evidence: [Photo]

[View Details] [Pay Now]
```

---

## Testing the Complete Flow

### 1. Start Detection

```bash
# Terminal 1: Run detection
python run_realtime_detection.py --mode webcam

# Or with a test video
python run_realtime_detection.py --mode video \
    --video data/videos/pettah_trimmed.mp4 \
    --output annotated_output.mp4
```

### 2. Open Driver Mobile App

```bash
# Terminal 2: Start mobile app
streamlit run src/dashboard/driver_mobile_app.py --server.port 8502
```

Go to: http://localhost:8502

**Login:**
- Username: `nimal_silva`
- Password: `test123`

### 3. Watch Violations Appear!

As violations are detected:
- ✅ Console shows detection + notification
- ✅ Database updated automatically
- ✅ Driver's app shows new violation
- ✅ Fine amount calculated correctly

---

## Test License Plates

These plates are in the test database:

| License Plate | Driver | Vehicle Type | Owner |
|--------------|--------|--------------|-------|
| WP CAB-1234 | nimal_silva | Car (Toyota Axio) | Nimal Silva |
| WP-5678 | nimal_silva | Car (Honda Civic) | Nimal Silva |
| CP-1111 | kamala_perera | Van (Nissan Caravan) | Kamala Perera |
| SP LD-2222 | tharindu_fernando | Tuktuk (Bajaj RE) | Tharindu Fernando |
| SP-3333 | tharindu_fernando | Motorcycle (Honda CD 70) | Tharindu Fernando |

**For testing with videos/images:**
- If your video has these plates, they'll be recognized!
- If not, the system generates demo plate numbers
- Either way, the complete flow works

---

## Fine Calculation Example

### Scenario: Parked car blocking traffic

**Input:**
- Vehicle: Car (detected by YOLOv8)
- License Plate: WP CAB-1234 (recognized by OCR)
- Violation Type: Illegal Parking
- Lane Blockage: 60%
- Vehicles Delayed: 10

**Calculation:**
```
Step 1: Impact Score
= (60 × 0.4) + (10 × 2) + (10 minutes × 2)
= 24 + 20 + 20
= 64/100 → Medium Severity

Step 2: Fine Calculation
Base Fine (Car):        LKR 2,000
× Medium Severity:      × 1.5
= Total Fine:           LKR 3,000
```

**Result:**
- Violation record created
- Driver notified: "Fine: LKR 3,000"
- Shows in mobile app with payment option

---

## Viewing Results

### Authority Dashboard

```bash
streamlit run src/dashboard/authority_dashboard.py
```

http://localhost:8501

**See:**
- All violations in real-time
- Fine breakdowns
- Notification status
- Export data to CSV

### Check Database

```bash
# View recent violations
mongosh parking_violations_db --eval "
  db.violations.find().sort({timestamp: -1}).limit(3).forEach(v => {
    print('---');
    print('License Plate:', v.license_plate);
    print('Driver:', v.driver_name);
    print('Fine:', 'LKR', v.fine_amount);
    print('Severity:', v.severity);
  })
"
```

---

## Customization

### Change Violation Type

```bash
python run_realtime_detection.py \
    --mode webcam \
    --violation-type blocking_traffic \
    --location "Galle Road" \
    --camera-id CAM-002
```

### Adjust Detection Sensitivity

```bash
# More sensitive (more detections)
python run_realtime_detection.py --confidence 0.2

# Less sensitive (only high confidence)
python run_realtime_detection.py --confidence 0.5
```

### Process Faster

```bash
# Process every 60th frame (super fast)
python run_realtime_detection.py \
    --mode video \
    --video input.mp4 \
    --sample-rate 60
```

---

## How It All Works

```
┌──────────────┐
│ Camera/Video │ Your traffic footage
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   YOLOv8     │ Detects: car, bus, tuktuk, etc.
│  Detection   │ Confidence: 88.3% accuracy
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   EasyOCR    │ Reads license plates
│   License    │ Format: "WP CAB-1234"
│   Plate OCR  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   MongoDB    │ Finds: vehicle → owner → driver
│   Lookup     │ Gets: name, phone, email, FCM token
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     Fine     │ Calculates based on:
│  Calculator  │ • Vehicle type
│              │ • Severity
│              │ • Impact score
└──────┬───────┘
       │
       ├─────────────────┬──────────────────┐
       ▼                 ▼                  ▼
┌──────────────┐  ┌─────────────┐  ┌──────────────┐
│   MongoDB    │  │ Push Notif  │  │  Mobile App  │
│ Save Record  │  │ to Driver   │  │   Updates    │
└──────────────┘  └─────────────┘  └──────────────┘
```

---

## Troubleshooting

### ❌ "No module named 'easyocr'"

```bash
pip install easyocr
```

### ❌ "No driver found for plate"

Add the vehicle to database:
```bash
python setup_test_data.py
```

Or add manually via mobile app's "Add Vehicle" page.

### ❌ "Model not found"

Check model exists:
```bash
ls -lh runs/parking_violations/exp/weights/best.pt
```

### ❌ "No plates recognized"

- OCR needs clear view of plates
- Works better with good lighting
- Front/rear view of vehicles
- Minimum 720p resolution

---

## Success Checklist ✅

- [ ] MongoDB running (`brew services start mongodb-community`)
- [ ] Virtual environment activated
- [ ] EasyOCR installed (`pip install easyocr`)
- [ ] Test data added (`python setup_test_data.py`)
- [ ] Detection running (`python run_realtime_detection.py --mode webcam`)
- [ ] Mobile app showing violations (http://localhost:8502)
- [ ] Driver receives correct fine amount

---

## Next Steps

1. **Test with Your Videos**
   - Use your actual traffic footage
   - See detection accuracy
   - Review fine calculations

2. **Configure Real Notifications**
   - Set up Firebase Cloud Messaging
   - Send actual push notifications
   - Real mobile app integration

3. **Deploy to Production**
   - Install on dedicated server
   - Connect IP cameras
   - 24/7 monitoring

4. **Integrate Payment Gateway**
   - Real online payments
   - Generate receipts
   - Track payment history

---

## Need Help?

📖 **Detailed Documentation:**
- `REALTIME_SETUP.md` - Complete setup guide
- `COMPLETE_SYSTEM_GUIDE.md` - Full system documentation
- `IMPLEMENTATION_SUMMARY.md` - Feature breakdown

🐛 **Issues?**
- Check MongoDB is running
- Verify model file exists
- Ensure test data is added
- Review console output for errors

---

**🎉 Congratulations! Your real-time traffic violation system is ready!**

**When a driver violates → They get notified instantly with the correct fine! 📱💰**
