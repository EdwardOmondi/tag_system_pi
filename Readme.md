# Kidsquad Raspberry Pi RFID Reader Setup

## Introduction

This repository houses the code for the tag raspberry pi system

## Equipment List

- Raspberry Pi
- FissaiD RFID Reader Writer
- Internet connection (WiFi/Ethernet)

## Initial Setup

clone the code into the base directory

```bash
cd ~/
git  clone https://github.com/EdwardOmondi/tag_system_pi.git
```

### Locale Setup

```bash
sudo nano /etc/default/locale
```

then paste the following content

```txt
LC_CTYPE="en_GB.UTF-8"
LC_ALL="en_GB.UTF-8"
LANG=en_GB.UTF-8
```

and then continue

## Installing the Required Packages

1. Run the following two commands on your Raspberry Pi to update it and ensure it is running the latest version of all the software.

```bash
sudo apt update
sudo apt upgrade
```

2. Then run the following command on your Raspberry Pi to install all of the required packages needed for the scripts

```bash
sudo apt install python3-dev python3-pip python3-venv
```

Before running any command, ensure you are in the right directory. (This is after cloning the repository)

```bash
cd ~/tag_system_pi
```

## Installing the Packages

5. Run the following command to install all the required packages

```bash
pip install -r requirements.txt --break-system-packages
```

> optional start

## Running the scripts

Before running either script, ensure you are in the right directory, and you are using the virtual environment stored within it

```bash
cd ~/tag_system_pi
source env/bin/activate
```

> optional end

## Serving the UI

### nginx setup

The application runs on the browser so we first setup NGINX to serve it.
Run the commands below

```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/default
```

add the information below in the first `location / { }` area

```bash
    location / {
        try_files $uri $uri/ /index.html;
    }
```

Test your Nginx configuration:

```bash
sudo nginx -t
```

then restart nginx for the changes to take effect

```bash
sudo systemctl enable nginx
sudo service nginx restart
sudo chown -R www-data:[username] /var/www/html/
sudo chmod -R 770 /var/www/html/
cd ~/tag_system_pi
```
### Setup the Browser

Run the commands below to setup the UI

```bash
cd ~/tag_system_pi/
sudo cp browser.zip /var/www/html/
cd /var/www/html/
sudo unzip browser.zip
sudo cp -r browser/* /var/www/html/
sudo rm -rf browser*
sudo service nginx restart
cd ~/tag_system_pi/
```
All done!

To open the application, go to [http://[username].local](http://[username].local) in your browser. Replace `[username]` with the pi username

## Automatic starting when booted up

To have your script start up automatically every time the Raspberry Pi boots up, you can use systemd, which is a system and service manager for Linux. Here's how you can create a systemd service for your script:

1. Create a systemd service unit file for your script. You can do this by creating a new file ending with `.service` in the `/etc/systemd/system/` directory. For example:

```bash
sudo nano /etc/systemd/system/tagscan.service
```

2. Add the following content to the file:

```txt
[Unit]
Description=Connect to scanner on Boot
After=network.target

[Service]
ExecStart=/usr/bin/python /home/[username]/tag_system_pi/tagserver.py
WorkingDirectory=/home/[username]/tag_system_pi
StandardOutput=/home/[username]/tag_system_pi/tagscan.log
StandardError=/home/[username]/tag_system_pi/tagscan_error.log
Restart=always
User=[username]

[Install]
WantedBy=multi-user.target
```

Replace `username` with your username.

3. Save the file and exit the text editor. `Ctrl+X`, then `Y` then `Enter`.

4. Reload systemd to read the new service file:

```bash
sudo systemctl daemon-reload
```

5. Enable the service to start at boot:

```bash
sudo systemctl enable tagscan.service
```

6. Start the service:
   > Create the output files first by running the commands below remembering to replace username with your username

```bash
touch /home/[username]/tag_system_pi/tagscan.log
touch /home/[username]/tag_system_pi/tagscan_error.log
```

```bash
sudo systemctl start tagscan.service
```

Now, your script should start automatically every time the Raspberry Pi boots up. You can also manually start, stop, and check the status of the service using `systemctl`. For example:

- To stop the service: `sudo systemctl stop tagscan.service`
- To check the status of the service: `sudo systemctl status tagscan.service`
- To view the output: `journalctl -u tagscan.service -f`. To quit, press `q`.

## Replacing the videos

> **_ONLY DO THIS IF YOU WANT TO REPLACE VIDEOS. THIS IS NOT AN INITIAL STEP_**

The videos playing are in `.mp4` format.
The title of the normal video **MUST ALWAYS BE** `video1.mp4`
and the title of the success video **MUST ALWAYS BE** `video2.mp4`

To change the video,

1. Add them to the same directory as the tag application. You can copy the new video into the tag directory using a flashdrive or download it from the cloud
2. Ensure they are named correctly as instructed above
3. run the commands

```bash
cd ~/tag_system_pi
sudo rm -rf /var/www/html/assets/video?.mp4
sudo mv video?.mp4 /var/www/html/assets/
sudo service nginx restart
```

## Opening the website via the terminal

To open the website via the terminal,run the following command in the terminal

```bash
DISPLAY=:0 chromium-browser --start-fullscreen --incognito http://0.0.0.0/read &
```

## Connect UI to the scanning program
If the UI is not connected to the scanning program, you will see a red dot on the header bar (for large screens) or the navigation menu (for small  screens).
To  reconnect it back to the scanning program,go to the `home` page and enter  the address below into the input field and click  connect
```url
ws://localhost:8765
```
