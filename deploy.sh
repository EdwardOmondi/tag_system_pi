#!/bin/bash

cd ~/tag_system_pi/
echo "'removing old browser files... \n'"
sudo rm -rf /var/www/html/assets*  /var/www/html/favicon*  /var/www/html/index*  /var/www/html/main*  /var/www/html/styles*  /var/www/html/polyfills*
echo "'copying new files... \n'"
sudo cp browser.zip /var/www/html/
echo "'moving to new directory... \n'"
cd /var/www/html/
echo "'unzipping files... \n'"
sudo unzip browser.zip
echo "'moving new files... \n'"
sudo cp -r browser/* /var/www/html/
echo "'removing excess files... \n'"
sudo rm -rf browser*
echo "'restarting web server... \n'"
sudo service nginx restart
echo "'Done! \n'"
cd ~/tag_system_pi/