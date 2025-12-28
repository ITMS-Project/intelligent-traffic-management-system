#!/bin/bash
# Activate virtual environment
source venv/bin/activate

# Navigate to backend
cd backend

# Run the server
echo "🚀 Starting Backend Server..."
python3 -m uvicorn app.main:app --reload --port 8000
