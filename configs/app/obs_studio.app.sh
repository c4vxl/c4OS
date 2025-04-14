# !/bin/bash
sudo pacman -S libfdk-aac libva-intel-driver libva-mesa-driver luajit sndio qrcodegencpp-cmake v4l2loopback-dkms pipewire --noconfirm
yay -S obs-studio --noconfirm
cp /usr/share/applications/com.obsproject.Studio.desktop ~/Desktop/com.obsproject.Studio.desktop
sudo chmod +x ~/Desktop/com.obsproject.Studio.desktop