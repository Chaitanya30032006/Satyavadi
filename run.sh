#!/bin/bash

echo "Starting TruthGuard Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo ""
echo "Starting Flask server..."
echo "Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py

