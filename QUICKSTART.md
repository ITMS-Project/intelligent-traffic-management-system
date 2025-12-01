# 🚀 Quick Start Guide

Get your Intelligent Traffic Management System running in **5 minutes**!

---

## Prerequisites

- MacBook Pro M2 ✅
- MongoDB installed ✅
- Python 3.8+ ✅

---

## Installation

### 1. Start MongoDB

```bash
brew services start mongodb-community
```

### 2. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

## Run the System

### Start All Services

```bash
./run_all.sh
```

### Access Your Applications

| Application | URL | Port |
|------------|-----|------|
| 🔌 **API Server** | http://localhost:8000 | 8000 |
| 📖 **API Docs** | http://localhost:8000/docs | 8000 |
| 🚔 **Authority Dashboard** | http://localhost:8501 | 8501 |
| 📱 **Driver Mobile App** | http://localhost:8502 | 8502 |

---

## First Time Setup

### 1. Create Admin Account (API)

Go to: http://localhost:8000/docs

- Click **POST /auth/register**
- Click **"Try it out"**
- Enter:
```json
{
  "username": "admin",
  "email": "admin@traffic.lk",
  "password": "admin123",
  "full_name": "Admin User",
  "phone": "+94771234567",
  "role": "admin"
}
```
- Click **Execute**

### 2. Create Driver Account (Mobile App)

Go to: http://localhost:8502

- Click **Register** tab
- Fill in details
- Click **Register**
- Login with your credentials

### 3. Add a Vehicle

In Driver App:
- Go to **🚗 My Vehicles**
- Click **Add New Vehicle**
- Enter vehicle details
- Click **Add Vehicle**

---

## Test the System

### Create a Test Violation

Go to: http://localhost:8000/docs

1. **Login first** (use your admin credentials)
2. **Copy the access token**
3. Click **Authorize** button (top right)
4. Paste token, click **Authorize**
5. Go to **POST /violations**
6. Try it out with:

```json
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

### Check the Results

- **Authority Dashboard**: http://localhost:8501
  - Should show 1 violation
  - See it in violation list

- **Driver App**: http://localhost:8502
  - Login
  - Go to **📜 Violations**
  - See your test violation

---

## Stop the System

```bash
./stop_all.sh
```

---

## Troubleshooting

### Port Already in Use?

```bash
./stop_all.sh
# Then restart
./run_all.sh
```

### MongoDB Not Running?

```bash
brew services restart mongodb-community
```

### Dependencies Error?

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## What's Next?

1. **Upload a video** in Authority Dashboard to detect violations
2. **Test warnings** by creating warnings via API
3. **Test payments** in Driver App
4. **Explore analytics** in Authority Dashboard

---

## Key Features to Test

### Authority Dashboard (Port 8501)
- ✅ Live monitoring with real-time stats
- ✅ Violation list with filters
- ✅ Traffic impact analytics
- ✅ Warning system tracking
- ✅ Fine breakdown display
- ✅ Export to CSV
- ✅ Camera management

### Driver Mobile App (Port 8502)
- ✅ Safety score (100 points)
- ✅ Real-time warnings (NOVELTY)
- ✅ Vehicle management
- ✅ Violation history
- ✅ Payment integration
- ✅ Profile management

### API Server (Port 8000)
- ✅ 40+ REST endpoints
- ✅ JWT authentication
- ✅ Real-time analytics
- ✅ Interactive docs (Swagger)

---

## Need Help?

Check the complete guide: **COMPLETE_SYSTEM_GUIDE.md**

---

