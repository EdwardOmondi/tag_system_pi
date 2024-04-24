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