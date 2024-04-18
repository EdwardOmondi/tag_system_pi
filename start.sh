#!/bin/bash

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
}

# Function to stop a process
stop_process() {
    pkill -f "$1"
}

# Check if HTTP server is running
if is_process_running "python3 -m http.server"; then
    echo "Stopping HTTP server..."
    stop_process "python3 -m http.server"
fi

# Check if WebSocket server is running
if is_process_running "python wspi.py"; then
    echo "Stopping WebSocket server..."
    stop_process "python wspi.py"
fi

# Start HTTP server in the background and redirect output to a log file
echo "Starting HTTP server..."
python3 -m http.server > http_server.log &

# Start WebSocket server in the background and redirect output to a log file
echo "Starting WebSocket server..."
python wspi.py > ws.log &

# Open the application in the default web browser
xdg-open http://localhost:8000
chromium-browser http://localhost:8000
midori http://localhost:8000

