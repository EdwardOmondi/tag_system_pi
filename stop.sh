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