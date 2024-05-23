#!/bin/bash

# Variables
USERNAME=$1  # Get username from command line argument
REPO_URL="https://github.com/EdwardOmondi/tag_system_pi.git"
BASE_DIR="/home/$USERNAME"
REPO_DIR="$BASE_DIR/tag_system_pi"

echo "Setting up the system for $USERNAME"

# Update and upgrade system
sudo apt update
sudo apt upgrade -y
echo "System updated and upgraded"

# Install required packages
sudo apt install -y python3-dev python3-pip python3-venv nginx
echo "Required packages installed"

# Clone the repository
cd $BASE_DIR
git clone $REPO_URL
echo "Repository cloned"

# Install Python packages
cd $REPO_DIR
pip install -r requirements.txt --break-system-packages
echo "Python packages installed"

# Setup nginx
sudo sed -i 's|location / {|location / {\n\ttry_files $uri $uri/ /index.html;\n|' /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl enable nginx
sudo service nginx restart
sudo chown -R www-data:$USERNAME /var/www/html/
sudo chmod -R 770 /var/www/html/
echo "Nginx setup complete"

# Setup systemd service
echo "[Unit]
Description=Connect to scanner on Boot
After=network.target

[Service]
ExecStart=/usr/bin/python $REPO_DIR/tagserver.py
WorkingDirectory=$REPO_DIR
StandardOutput=$REPO_DIR/tagscan.log
StandardError=$REPO_DIR/tagscan_error.log
Restart=always
User=$USERNAME

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/tagscan.service
echo "Systemd service created"

sudo systemctl daemon-reload
sudo systemctl enable tagscan.service
echo "Service enabled"

# Create log files
touch $REPO_DIR/tagscan.log
touch $REPO_DIR/tagscan_error.log

# Start the service
sudo systemctl start tagscan.service
echo "Service started"

echo "System setup complete"