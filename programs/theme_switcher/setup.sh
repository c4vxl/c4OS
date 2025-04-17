#!/bin/bash

sudo rm /usr/bin/themes
sudo rm -R /usr/bin/c4themes

sudo pacman -S tk --noconfirm
pip install qtpy PyGObject customtkinter flask pywebview requests --break-system-packages
sudo mkdir /usr/bin/c4themes

sudo tee /usr/bin/c4themes/wrapper > /dev/null <<EOF
#!/bin/bash
python3 /usr/bin/c4themes/index.py "\$@"
EOF
sudo cp index.py /usr/bin/c4themes/index.py

# sudo cd /usr/bin/c4themes

sudo ln -s /usr/bin/c4themes/wrapper /usr/bin/themes
sudo chmod 777 /usr/bin/themes

sudo tee /usr/share/applications/themes.desktop > /dev/null <<EOF
[Desktop Entry]
Name=Themes
Comment=Select a Theme.
Exec=themes
Terminal=False
Type=Application
Categories=Development
StartupWMClass=Code
EOF