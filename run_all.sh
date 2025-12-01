#!/bin/bash

# Intelligent Traffic Management System - Startup Script
# This script starts all components of the system

echo "🚀 Starting Intelligent Traffic Management System..."
echo "=================================================="

# Colors for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if MongoDB is running
echo -e "${YELLOW}Checking MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${YELLOW}Starting MongoDB...${NC}"
    brew services start mongodb-community
    sleep 3
else
    echo -e "${GREEN}✅ MongoDB is already running${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Create logs directory
mkdir -p logs
LOG_DIR=$(pwd)/logs


# Clear old log files
rm -f logs/*.log logs/pids.txt

echo ""
echo "=================================================="
echo -e "${GREEN}Starting all services...${NC}"
echo "=================================================="
echo ""

# Start FastAPI Backend
echo -e "${GREEN}🔌 Starting FastAPI Backend on port 8000...${NC}"
cd src/api && python main.py > "$LOG_DIR/api.log" 2>&1 &
API_PID=$!
echo -e "${GREEN}   API PID: $API_PID${NC}"


sleep 2

# Start Authority Dashboard
echo -e "${GREEN}🚔 Starting Authority Dashboard on port 8501...${NC}"
streamlit run src/dashboard/app_with_video.py --server.port 8501 > "$LOG_DIR/authority_dashboard.log" 2>&1 &
DASHBOARD_PID=$!
echo -e "${GREEN}   Dashboard PID: $DASHBOARD_PID${NC}"

sleep 2

# Start Mobile Driver App
echo -e "${GREEN}📱 Starting Driver Mobile App on port 8502...${NC}"
streamlit run src/dashboard/user_app_enhanced.py --server.port 8502 > "$LOG_DIR/driver_app.log" 2>&1 &
MOBILE_PID=$!
echo -e "${GREEN}   Mobile App PID: $MOBILE_PID${NC}"

sleep 3

echo ""
echo "=================================================="
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo "=================================================="
echo ""
echo "Access your applications:"
echo ""
echo "  🔌 API Server:           http://localhost:8000"
echo "  📖 API Documentation:    http://localhost:8000/docs"
echo "  🚔 Authority Dashboard:  http://localhost:8501"
echo "  📱 Driver Mobile App:    http://localhost:8502"
echo ""
echo "=================================================="
echo ""
echo "Process IDs:"
echo "  API:       $API_PID"
echo "  Dashboard: $DASHBOARD_PID"
echo "  Mobile:    $MOBILE_PID"
echo ""
echo "To stop all services, run:"
echo "  ./stop_all.sh"
echo ""
echo "Or manually kill processes:"
echo "  kill $API_PID $DASHBOARD_PID $MOBILE_PID"
echo ""
echo "Logs are available in the logs/ directory"
echo ""
echo "=================================================="


# Save PIDs to file for easy stopping
echo "$API_PID" > "$LOG_DIR/pids.txt"
echo "$DASHBOARD_PID" >> "$LOG_DIR/pids.txt"
echo "$MOBILE_PID" >> "$LOG_DIR/pids.txt"

# Keep script running
wait
