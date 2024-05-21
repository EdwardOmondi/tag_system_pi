#!/bin/bash

cd ~/tag_system_pi/
echo "removing old browser files..."
sudo rm -rf /var/www/html/assets*  /var/www/html/favicon*  /var/www/html/index*  /var/www/html/main*  /var/www/html/styles*  /var/www/html/polyfills*
echo "copying new files..."
sudo cp browser.zip /var/www/html/
echo "moving to new directory..."
cd /var/www/html/
echo "unzipping files..."
sudo unzip browser.zip
echo "moving new files..."
sudo cp -r browser/* /var/www/html/
echo "removing excess files..."
sudo rm -rf browser*
echo "restarting web server..."
sudo service nginx restart
echo "Done!"
cd ~/tag_system_pi/