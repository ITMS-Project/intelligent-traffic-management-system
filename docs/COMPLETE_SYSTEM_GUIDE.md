# 🚀 Complete System Guide - Intelligent Traffic Management System

**Version:** 2.0
**Last Updated:** December 1, 2025
**Platform:** MacBook Pro M2

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Installation](#installation)
5. [Running the System](#running-the-system)
6. [Features](#features)
7. [API Documentation](#api-documentation)
8. [Database Schema](#database-schema)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

The Intelligent Traffic Management System is a comprehensive solution for detecting and managing parking violations using AI (YOLOv8), real-time notifications, and predictive warnings.

### Key Innovations

- **Predictive Warning System**: Warns drivers BEFORE they commit violations (NOVELTY)
- **Real-time Safety Score**: Gamified 100-point system for driver behavior
- **Traffic Impact Analytics**: Calculates congestion and delay caused by violations
- **Dual Interface**: Authority dashboard + Driver mobile app

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │  Authority Dashboard │  │   Driver Mobile App      │    │
│  │   (Streamlit:8501)   │  │   (Streamlit:8502)       │    │
│  └──────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         FastAPI REST API (Port 8000)                 │   │
│  │  - Authentication (JWT)                              │   │
│  │  - CRUD Operations                                   │   │
│  │  - Real-time Analytics                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Detection  │  │ Notification │  │ Fine Calculator │  │
│  │   (YOLOv8)   │  │   Service    │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              MongoDB Database                         │  │
│  │  - users       - warnings      - payments            │  │
│  │  - vehicles    - violations    - traffic_impact      │  │
│  │  - cameras     - detection_logs                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Components

### 1. **FastAPI Backend** (`src/api/main.py`)

RESTful API server handling all business logic.

**Key Features:**
- JWT authentication
- 40+ API endpoints
- Real-time analytics
- Safety score calculation
- Fine calculation engine

**Endpoints:**
- `/auth/register`, `/auth/login` - Authentication
- `/violations`, `/warnings`, `/payments` - CRUD operations
- `/dashboard/stats` - Analytics
- `/export/violations/csv` - Data export

### 2. **Authority Dashboard** (`src/dashboard/authority_dashboard.py`)

Web interface for traffic police and administrators.

**Features:**
- ✅ Live Monitoring Panel
- ✅ Violation List with Evidence
- ✅ Traffic Impact Analytics
- ✅ Warning System Status
- ✅ Fine Calculation Breakdown
- ✅ Historical Logs
- ✅ Admin Functions (Camera management, bulk delete, export)

### 3. **Driver Mobile App** (`src/dashboard/driver_mobile_app.py`)

Mobile-responsive web app for drivers.

**Features:**
- ✅ Real-Time Predictive Warnings (NOVELTY)
- ✅ Violation Notifications
- ✅ Driver Safety Score (100 points)
- ✅ Violation History
- ✅ Fine Payment Integration
- ✅ Profile & Vehicle Management

### 4. **Detection System** (`src/detection/`)

YOLOv8-based vehicle detection.

- `realtime_detector.py` - Standard frame-by-frame detection
- `fast_detector.py` - Optimized with frame sampling
- `violation_processor.py` - Fine calculation logic

### 5. **Notification Service** (`src/notifications/`)

Firebase Cloud Messaging integration.

- Push notifications for warnings
- Violation alerts
- Payment confirmations
- Score updates

### 6. **Database Layer** (`src/database/`)

MongoDB integration with Pydantic models.

**Collections:**
- `users` - User accounts
- `vehicles` - Registered vehicles
- `violations` - Parking violations
- `warnings` - Predictive warnings
- `payments` - Payment records
- `traffic_impact` - Congestion analytics
- `cameras` - Camera locations
- `detection_logs` - All detections

---

## 💻 Installation

### Prerequisites

- **macOS** (MacBook Pro M2)
- **Python 3.8+**
- **MongoDB** installed via Homebrew
- **Git**

### Step 1: Clone Repository

Already done! You're in: `/Users/ranidupromod/Projects/intelligent-traffic-management-system`

### Step 2: Install MongoDB

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community
```

### Step 3: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Copy example .env
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Step 6: (Optional) Firebase Setup

If you want push notifications:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Download service account JSON
4. Save as `config/firebase-serviceaccount.json`
5. Update `.env` with path

---

## 🚀 Running the System

### Quick Start (All Services)

```bash
./run_all.sh
```

This starts:
- FastAPI Backend (port 8000)
- Authority Dashboard (port 8501)
- Driver Mobile App (port 8502)

### Access Points

| Service | URL |
|---------|-----|
| 🔌 API Server | http://localhost:8000 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |
| 🚔 Authority Dashboard | http://localhost:8501 |
| 📱 Driver Mobile App | http://localhost:8502 |

### Stop All Services

```bash
./stop_all.sh
```

### Run Individually

**API Server:**
```bash
cd src/api
python main.py
```

**Authority Dashboard:**
```bash
streamlit run src/dashboard/authority_dashboard.py --server.port 8501
```

**Driver App:**
```bash
streamlit run src/dashboard/driver_mobile_app.py --server.port 8502
```

---

## ✨ Features

### For Authorities (Dashboard)

#### 1. Live Monitoring
- Real-time violation count
- Active camera status
- Live detection feed
- 24-hour trend chart

#### 2. Violation Management
- Complete violation list with filters
- Evidence images/videos
- Delete incorrect detections
- Edit violation details
- Export to CSV

#### 3. Traffic Impact Analytics
- Vehicles affected count
- Total delay calculation
- Congestion heat maps
- Hourly violation patterns
- Vehicle type breakdown

#### 4. Warning System
- All warnings issued
- Response rate tracking
- Success rate metrics
- Individual warning details

#### 5. Fine Breakdown
- Base fine calculation
- Duration factors
- Impact multipliers
- Detailed reasoning
- Total/paid/unpaid summary

#### 6. Historical Logs
- Date range filtering
- Violation records
- Summary statistics
- Exportable data

#### 7. Admin Functions
- Camera management (add/remove)
- Bulk delete operations
- CSV export
- System settings

### For Drivers (Mobile App)

#### 1. Safety Score Dashboard
- **100-point scoring system**
- Score badge (Excellent/Good/Average/Poor)
- Score breakdown
- 30-day trend chart
- Tips for improvement

#### 2. Real-Time Warnings
- **Predictive alerts BEFORE violations** (NOVELTY)
- Active warning list
- Quick response button
- Warning history
- Success tracking

#### 3. Vehicle Management
- Register multiple vehicles
- View vehicle details
- Violation count per vehicle
- Easy add/remove

#### 4. Violation History
- All violations with details
- Status (paid/pending)
- Fine amounts
- Evidence images
- Pay directly from list

#### 5. Payment Center
- Multiple payment methods:
  - Credit/Debit Card
  - EZ Cash
  - Bank Transfer
  - Online Banking
- Payment history
- Transaction records
- Receipt generation

#### 6. Profile Management
- Personal information
- Account statistics
- Member since date
- Edit profile

---

## 📡 API Documentation

### Authentication

**Register:**
```http
POST /auth/register
Content-Type: application/json

{
  "username": "driver1",
  "email": "driver@example.com",
  "password": "secure123",
  "full_name": "John Doe",
  "phone": "+94771234567",
  "role": "driver"
}
```

**Login:**
```http
POST /auth/login
Content-Type: application/json

{
  "username": "driver1",
  "password": "secure123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": "507f1f77bcf86cd799439011",
  "username": "driver1",
  "role": "driver"
}
```

### Violations

**Create Violation:**
```http
POST /violations
Authorization: Bearer <token>
Content-Type: application/json

{
  "vehicle_type": "car",
  "license_plate": "ABC-1234",
  "violation_type": "illegal_parking",
  "severity": "medium",
  "fine_amount": 5000,
  "location": "Pettah Market",
  "latitude": 6.9271,
  "longitude": 79.8612,
  "confidence": 0.85
}
```

**Get All Violations:**
```http
GET /violations?status=pending&limit=50
Authorization: Bearer <token>
```

### Warnings

**Create Warning:**
```http
POST /warnings
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "507f1f77bcf86cd799439011",
  "vehicle_id": "507f191e810c19729de860ea",
  "location": "Galle Road",
  "message": "Warning: Approaching no-parking zone",
  "severity": "medium"
}
```

**Mark Warning as Responded:**
```http
PUT /warnings/{warning_id}/respond
Authorization: Bearer <token>
```

### Dashboard Analytics

**Get Dashboard Stats:**
```http
GET /dashboard/stats
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_violations": 540,
  "pending_violations": 120,
  "paid_violations": 420,
  "total_warnings": 1250,
  "warnings_heeded": 980,
  "warning_success_rate": 78.4,
  "total_fines": 2123000,
  "violations_by_type": [...],
  "violations_by_vehicle": [...],
  "violations_by_hour": [...]
}
```

---

## 🗄️ Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "username": String,
  "email": String,
  "hashed_password": String,
  "full_name": String,
  "phone": String,
  "role": "driver" | "officer" | "admin",
  "safety_score": Number (0-100),
  "score_badge": "Excellent" | "Good" | "Average" | "Poor",
  "is_active": Boolean,
  "created_at": ISODate,
  "last_login": ISODate
}
```

### Violations Collection
```javascript
{
  "_id": ObjectId,
  "vehicle_id": ObjectId,
  "vehicle_type": String,
  "license_plate": String,
  "violation_type": String,
  "severity": "low" | "medium" | "high" | "severe",
  "fine_amount": Number,
  "location": String,
  "latitude": Number,
  "longitude": Number,
  "timestamp": ISODate,
  "image_path": String,
  "confidence": Number,
  "status": "pending" | "paid" | "disputed",
  "officer_id": ObjectId,
  "notes": String
}
```

### Warnings Collection
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "vehicle_id": ObjectId,
  "location": String,
  "warning_type": "predictive_parking",
  "message": String,
  "severity": "low" | "medium" | "high",
  "timestamp": ISODate,
  "responded": Boolean,
  "response_time": Number (seconds),
  "escalated_to_violation": Boolean,
  "violation_id": ObjectId
}
```

### Traffic Impact Collection
```javascript
{
  "_id": ObjectId,
  "violation_id": ObjectId,
  "vehicles_affected": Number,
  "congestion_level": "low" | "medium" | "high" | "severe",
  "congestion_score": Number (0-1),
  "duration_seconds": Number,
  "lane_blocked": Boolean,
  "impact_multiplier": Number,
  "estimated_delay_minutes": Number,
  "timestamp": ISODate
}
```

---

## 🧪 Testing

### Manual Testing

1. **Register a Driver:**
   - Go to http://localhost:8502
   - Click "Register"
   - Create account

2. **Add a Vehicle:**
   - Navigate to "My Vehicles"
   - Add vehicle details

3. **Create Test Violation:**
   - Use API or Authority Dashboard
   - Assign to your vehicle

4. **Check Driver App:**
   - View violation in app
   - Test payment flow

5. **Test Warnings:**
   - Create warning via API
   - Check notification in app
   - Mark as responded

### API Testing

Use Swagger UI: http://localhost:8000/docs

1. Click "Authorize"
2. Login to get token
3. Test all endpoints interactively

---

## 🐛 Troubleshooting

### MongoDB Not Starting

```bash
# Check if running
brew services list

# Restart
brew services restart mongodb-community

# Check logs
tail -f /opt/homebrew/var/log/mongodb/mongo.log
```

### Port Already in Use

```bash
# Find process on port
lsof -ti:8000  # or 8501, 8502

# Kill process
kill -9 <PID>

# Or use stop script
./stop_all.sh
```

### Dependencies Not Installing

```bash
# Upgrade pip
pip install --upgrade pip

# Try installing individually
pip install fastapi uvicorn pymongo

# Check Python version
python --version  # Should be 3.8+
```

### Firebase Notifications Not Working

This is expected if you haven't set up Firebase. The system runs in DEMO mode:
- Notifications are logged to console
- All features work except actual push notifications

To enable:
1. Set up Firebase project
2. Download service account JSON
3. Place in `config/firebase-serviceaccount.json`
4. Restart services

### Streamlit "Address already in use"

```bash
# Kill streamlit processes
pkill -f streamlit

# Or specific ports
lsof -ti:8501 | xargs kill -9
lsof -ti:8502 | xargs kill -9
```

---

## 📈 Performance Optimization

### Detection Speed

- Use `fast_detector.py` with frame sampling
- Adjust `CONFIDENCE_THRESHOLD` in .env
- Use GPU if available (CUDA)

### Database Optimization

```javascript
// Create indexes in MongoDB
db.violations.createIndex({"timestamp": -1})
db.violations.createIndex({"vehicle_id": 1})
db.violations.createIndex({"status": 1})
db.warnings.createIndex({"user_id": 1, "timestamp": -1})
```

---

## 🎯 Next Steps

### Immediate Enhancements
- [ ] License Plate Recognition (OCR)
- [ ] Real SMS notifications (Twilio)
- [ ] Email notifications
- [ ] GPS coordinates from camera locations

### Future Development
- [ ] Native mobile app (React Native)
- [ ] Live camera feed integration
- [ ] Multi-camera support
- [ ] Automated report generation
- [ ] Integration with police database

---

## 📞 Support

If you encounter issues:

1. Check logs in `logs/` directory
2. Verify MongoDB is running
3. Ensure all dependencies are installed
4. Check `.env` configuration

---

## 🎉 Success!

Your system is now fully operational with:

✅ FastAPI Backend
✅ Authority Dashboard
✅ Driver Mobile App
✅ MongoDB Database
✅ Firebase Notifications (Optional)
✅ YOLOv8 Detection
✅ Real-time Analytics
✅ Safety Score System
✅ Predictive Warnings

---


---

