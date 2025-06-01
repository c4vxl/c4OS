# !/bin/bash
yay -S jetbrains-toolbox --noconfirm
cp /usr/share/applications/jetbrains-toolbox.desktop ~/Desktop/jetbrains-toolbox.desktop
sudo chmod +x ~/Desktop/jetbrains-toolbox.desktop
sudo mkdir -p ~/.config/autostart/
sudo cp /usr/share/applications/jetbrains-toolbox.desktop ~/.config/autostart/jetbrains-toolbox.desktop
sudo chmod 777 ~/.config/autostart/jetbrains-toolbox.desktop