#!/bin/bash

# Stop all services

echo "🛑 Stopping all services..."

if [ -f "logs/pids.txt" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping process $pid..."
            kill $pid
        fi
    done < logs/pids.txt
    rm logs/pids.txt
    echo "✅ All services stopped"
else
    echo "⚠️  No PID file found. Stopping by port..."

    # Kill processes on specific ports
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:8501 | xargs kill -9 2>/dev/null
    lsof -ti:8502 | xargs kill -9 2>/dev/null

    echo "✅ Services stopped"
fi
