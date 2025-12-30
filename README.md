# Intelligent Traffic Management System

A specialized AI-powered system designed to detect parking violations, read license plates, and manage driver scores using computer vision.

![System Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%7C%20YOLOv8%20%7C%20EasyOCR-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)

## � System Capabilities

*   **🚗 Vehicle Detection & Tracking**: Real-time YOLOv8 tracking of cars, trucks, and buses.
*   **🅿️ Parking Violation Detection**: Automatically identifies vehicles parked in restricted red zones (Warning @ 5s, Violation @ 15s).
*   **🔍 License Plate Recognition (ALPR)**: Custom-trained model to detect and read license plates.
*   **📊 Driver Scoring**: Tracks violations per vehicle and maintains a 100-point driver score system.
*   **🔊 Audio Warnings**: Automated voice alerts for violators (TTS).
*   **📄 Evidence Capture**: Logs violations and captures evidence in a local database.

## 🏗️ Project Structure

The project follows a clean, backend-centric architecture:

```
Intelligent-Traffic-Management-System/
├── backend/
│   ├── app/
│   │   ├── api/            # API Endpoints (video, parking, scoring)
│   │   ├── core/           # Configuration & Database
│   │   ├── services/       # AI Logic (Detection, OCR, Parking, TTS)
│   │   ├── static/         # Web Interface (Dashboard)
│   │   └── main.py         # Application Entry Point
│   ├── data/               # Persistent Data
│   │   ├── its.db          # SQLite Database
│   │   └── videos/         # Video Recordings
│   ├── models/             # AI Models
│   │   ├── yolov8n.pt      # Vehicle Detection
│   │   └── best_plate.pt   # License Plate Detection
│   ├── scripts/            # Helper Scripts
│   └── requirements.txt    # Dependencies
├── .venv/                  # Virtual Environment
└── .vscode/                # VS Code Settings
```

## 🚀 Quick Start Guide

### 1. Prerequisites
*   Python 3.10 or 3.11
*   VS Code (Recommended)
*   Virtual Environment (venv)

### 2. Setup (First Time)
Open a terminal in the project root:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Running the System
You can run the system directly from VS Code using **Run and Debug > "Run Traffic System API"**.

Or via terminal:

```bash
cd backend
../.venv/bin/uvicorn app.main:app --reload --port 8000
```

### 4. Access the Dashboard
Once running, open your browser:

*   **🎥 Live Detection Feed**: [http://127.0.0.1:8000/detect](http://127.0.0.1:8000/detect)
*   **📄 API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧩 How It Works

1.  **Ingestion**: Reads video feed (webcam or file).
2.  **Detection**: YOLOv8 detects vehicles and defines their bounding boxes.
3.  **Parking Logic**: Checks if a vehicle's center point stays inside a "No Parking Zone" (defined in `detection.py`) for >5 seconds.
4.  **Plate Recognition**: If a violation is imminent, the system crops the vehicle, detects the plate, and uses EasyOCR to read the text.
5.  **Action**:
    *   **Audio**: Plays a TTS warning.
    *   **Database**: Records the violation in `its.db`.
    *   **Scoring**: Deducts points from the driver's score.

## 🛠️ Configuration
Adjust settings in `backend/app/core/config.py`:
*   `PARKING_WARNING_SECONDS`: Time before warning (default: 5s)
*   `PARKING_VIOLATION_SECONDS`: Time before fine (default: 15s)
*   `OCR_ENABLED`: Toggle license plate reading

## � Models
*   **Vehicles**: `backend/models/yolov8n.pt` (Auto-downloaded if missing)
*   **Plates**: `backend/models/best_plate.pt` (Custom trained)

## 📝 License
This project is for educational and demonstration purposes.

<!-- Updated on 2025-12-16 09:04:00 -->
<!-- Updated on 2025-12-17 09:37:00 -->
<!-- Updated on 2025-12-17 16:28:00 -->
<!-- Updated on 2025-12-17 13:52:00 -->
<!-- Updated on 2025-12-17 17:56:00 -->
<!-- Updated on 2025-12-17 18:53:00 -->
<!-- Updated on 2025-12-17 12:18:00 -->
<!-- Updated on 2025-12-17 10:32:00 -->
<!-- Updated on 2025-12-18 19:34:00 -->
<!-- Updated on 2025-12-18 19:10:00 -->
<!-- Updated on 2025-12-18 13:52:00 -->
<!-- Updated on 2025-12-18 14:01:00 -->
<!-- Updated on 2025-12-18 20:31:00 -->
<!-- Updated on 2025-12-18 19:25:00 -->
<!-- Updated on 2025-12-19 14:04:00 -->
<!-- Updated on 2025-12-19 11:50:00 -->
<!-- Updated on 2025-12-19 10:48:00 -->
<!-- Updated on 2025-12-19 13:53:00 -->
<!-- Updated on 2025-12-19 10:38:00 -->
<!-- Updated on 2025-12-19 10:09:00 -->
<!-- Updated on 2025-12-19 14:35:00 -->
<!-- Updated on 2025-12-20 18:30:00 -->
<!-- Updated on 2025-12-20 16:57:00 -->
<!-- Updated on 2025-12-20 20:56:00 -->
<!-- Updated on 2025-12-20 18:50:00 -->
<!-- Updated on 2025-12-20 11:03:00 -->
<!-- Updated on 2025-12-20 19:02:00 -->
<!-- Updated on 2025-12-21 13:28:00 -->
<!-- Updated on 2025-12-21 20:08:00 -->
<!-- Updated on 2025-12-21 15:16:00 -->
<!-- Updated on 2025-12-21 09:58:00 -->
<!-- Updated on 2025-12-21 10:53:00 -->
<!-- Updated on 2025-12-22 15:41:00 -->
<!-- Updated on 2025-12-22 20:33:00 -->
<!-- Updated on 2025-12-22 18:54:00 -->
<!-- Updated on 2025-12-22 14:57:00 -->
<!-- Updated on 2025-12-22 12:52:00 -->
<!-- Updated on 2025-12-22 14:05:00 -->
<!-- Updated on 2025-12-23 09:46:00 -->
<!-- Updated on 2025-12-23 20:53:00 -->
<!-- Updated on 2025-12-23 13:15:00 -->
<!-- Updated on 2025-12-23 16:12:00 -->
<!-- Updated on 2025-12-23 13:28:00 -->
<!-- Updated on 2025-12-23 17:01:00 -->
<!-- Updated on 2025-12-23 09:18:00 -->
<!-- Updated on 2025-12-24 15:05:00 -->
<!-- Updated on 2025-12-24 10:35:00 -->
<!-- Updated on 2025-12-24 10:54:00 -->
<!-- Updated on 2025-12-24 17:10:00 -->
<!-- Updated on 2025-12-24 13:11:00 -->
<!-- Updated on 2025-12-24 19:27:00 -->
<!-- Updated on 2025-12-25 11:29:00 -->
<!-- Updated on 2025-12-25 18:25:00 -->
<!-- Updated on 2025-12-25 19:09:00 -->
<!-- Updated on 2025-12-25 17:41:00 -->
<!-- Updated on 2025-12-25 17:54:00 -->
<!-- Updated on 2025-12-25 20:32:00 -->
<!-- Updated on 2025-12-26 14:30:00 -->
<!-- Updated on 2025-12-26 11:09:00 -->
<!-- Updated on 2025-12-26 20:15:00 -->
<!-- Updated on 2025-12-26 12:24:00 -->
<!-- Updated on 2025-12-26 15:00:00 -->
<!-- Updated on 2025-12-26 15:42:00 -->
<!-- Updated on 2025-12-26 13:12:00 -->
<!-- Updated on 2025-12-27 09:30:00 -->
<!-- Updated on 2025-12-27 10:19:00 -->
<!-- Updated on 2025-12-27 15:09:00 -->
<!-- Updated on 2025-12-27 20:12:00 -->
<!-- Updated on 2025-12-28 09:48:00 -->
<!-- Updated on 2025-12-28 16:18:00 -->
<!-- Updated on 2025-12-28 18:45:00 -->
<!-- Updated on 2025-12-28 10:53:00 -->
<!-- Updated on 2025-12-28 17:45:00 -->
<!-- Updated on 2025-12-28 15:15:00 -->
<!-- Updated on 2025-12-29 19:55:00 -->
<!-- Updated on 2025-12-29 14:35:00 -->
<!-- Updated on 2025-12-29 10:31:00 -->
<!-- Updated on 2025-12-29 09:50:00 -->
<!-- Updated on 2025-12-29 09:22:00 -->
<!-- Updated on 2025-12-29 15:50:00 -->
<!-- Updated on 2025-12-29 17:20:00 -->
<!-- Updated on 2025-12-30 12:08:00 -->
<!-- Updated on 2025-12-30 12:19:00 -->
<!-- Updated on 2025-12-30 09:07:00 -->
<!-- Updated on 2025-12-30 17:07:00 -->
<!-- Updated on 2025-12-30 13:27:00 -->
<!-- Updated on 2025-12-30 19:45:00 -->
<!-- Updated on 2025-12-31 19:41:00 -->
<!-- Updated on 2025-12-31 10:49:00 -->
<!-- Updated on 2025-12-31 13:45:00 -->
<!-- Updated on 2025-12-31 20:38:00 -->
<!-- Updated on 2025-12-31 09:35:00 -->
<!-- Updated on 2025-12-31 16:58:00 -->
<!-- Updated on 2025-12-31 10:30:00 -->
<!-- Updated on 2026-01-01 18:30:00 -->
<!-- Updated on 2026-01-01 13:08:00 -->
<!-- Updated on 2026-01-01 18:45:00 -->
<!-- Updated on 2026-01-01 10:54:00 -->
<!-- Updated on 2026-01-01 14:29:00 -->
<!-- Updated on 2026-01-02 11:08:00 -->
<!-- Updated on 2026-01-02 14:33:00 -->
<!-- Updated on 2026-01-02 16:04:00 -->
<!-- Updated on 2026-01-02 09:42:00 -->
<!-- Updated on 2026-01-02 14:32:00 -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- update -->
<!-- Update detection region of interest coordinates -->
<!-- Update utility helper functions -->
<!-- Fix race condition in thread management -->
<!-- Update output video resolution settings -->
<!-- Update project metadata and versioning -->
<!-- Update unit tests for scoring engine -->
<!-- Refactor directory structure for scalability -->
<!-- Fix memory leak in frame buffer -->
<!-- Update environment variable parsing -->
<!-- Update monitoring dashboard layout -->
<!-- Update license plate recognition regex -->
<!-- Improve mobile responsiveness of monitor -->
<!-- Improve text-to-speech warning clarity -->
<!-- Cleanup temporary cache files -->
<!-- Refactor alert generation logic -->
<!-- Optimize variable naming for readability -->
<!-- Add validation for vehicle plate input strings -->
<!-- Optimize image processing pipeline speed -->
<!-- Optimize database connection pool configuration -->
<!-- Refactor parking duration calculation logic -->
<!-- Reformat code according to PEP8 standards -->
<!-- Handle edge case where vehicle stays stationary -->
<!-- Improve exception handling in main loop -->
<!-- Add retry mechanism for database writes -->
<!-- Clean up logging statements in detection service -->
<!-- Tune YOLO confidence levels for night time -->
<!-- Enhance dashboard load time efficiency -->
<!-- Fix minor typo in code comments -->
<!-- Remove deprecated function calls -->
<!-- Refactor main execution entry point -->
<!-- Add debug logs for tracking persistence -->
<!-- Update API documentation in README -->
<!-- Add comments to complex algorithm sections -->
<!-- Update detection model weights path -->
<!-- Fix bug in API response format -->
<!-- Update unit tests for scoring engine -->
<!-- Update project metadata and versioning -->
<!-- Optimize CPU usage during idle times -->
<!-- Update output video resolution settings -->
<!-- Update utility helper functions -->
<!-- Improve error handling in video stream processing -->
<!-- Fix issue with timestamp synchronization -->
<!-- Refactor directory structure for scalability -->
<!-- Update alert sound generated files -->
<!-- Reformat code according to PEP8 standards -->
<!-- Refactor parking duration calculation logic -->
<!-- Optimize variable naming for readability -->
<!-- Add retry mechanism for database writes -->