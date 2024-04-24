#!/bin/bash

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
}

# Function to stop a process
stop_process() {
    pkill -f "$1"
}

# Check if reader is connected
if is_process_running "python wspi3.py"; then
    echo "Disconnecting reader..."
    stop_process "python wspi3.py"
fi

# Connect to reader in the background
cd ~/tag_system_pi
echo "Installing requirements..."
pip install -r requirements.txt
echo "Starting WebSocket server..."
nohup python wspi3.py > wspi3.out 2>&1  </dev/null &

