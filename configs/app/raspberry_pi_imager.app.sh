# !/bin/bash
sudo pacman -S rpi-imager --noconfirm

cp /usr/share/applications/org.raspberrypi.rpi-imager.desktop ~/Desktop/org.raspberrypi.rpi-imager.desktop
sudo chmod +x ~/Desktop/org.raspberrypi.rpi-imager.desktop