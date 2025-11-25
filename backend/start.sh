#!/bin/bash

# Band Music Backend - Simple Startup Script

echo "🎵 Starting Band Music Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Activate virtual environment and start server
source venv/bin/activate
echo "✅ Virtual environment activated"
echo "🚀 Starting Uvicorn server on http://localhost:8000"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
