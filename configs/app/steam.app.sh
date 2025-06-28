# !/bin/bash
sudo pacman -R amdvlk lib32-amdvlk --noconfirm
sudo pacman -S vulkan-radeon lib32-vulkan-radeon steam --noconfirm

cp /usr/share/applications/steam.desktop ~/Desktop/steam.desktop/steam.desktop
sudo chmod +x ~/Desktop/steam.desktop/steam.desktop