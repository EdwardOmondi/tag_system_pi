#!/bin/bash

# Start HTTP server in the background and redirect output to a log file
python3 -m http.server > http_server.log &

# Start WebSocket server in the background and redirect output to a log file
python wspi.py > ws.log &

# Open the application in the default web browser
xdg-open http://localhost:8000

