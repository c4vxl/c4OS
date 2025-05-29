#!/bin/bash
python build.py

sudo rm /usr/bin/c4osinstall
sudo rm /usr/bin/installer
sudo rm -R /usr/bin/c4OSInstaller

sudo mkdir -p /usr/bin/c4OSInstaller

sudo pacman -S tk webkit2gtk dosfstools --noconfirm
pip install qtpy PyGObject customtkinter flask pywebview requests PyQt5 PyQtWebEngine --break-system-packages


sudo tee /usr/bin/c4OSInstaller/wrapper_py > /dev/null <<EOF
#!/bin/bash
cd /usr/bin/c4OSInstaller/
python3 /usr/bin/c4OSInstaller/installer.py "\$@"
EOF
sudo tee /usr/bin/c4OSInstaller/wrapper_sh > /dev/null <<EOF
#!/bin/bash
cd /usr/bin/c4OSInstaller/
bash /usr/bin/c4OSInstaller/installer.sh "\$@"
EOF

sudo cp installer.py /usr/bin/c4OSInstaller/installer.py
sudo cp installer.sh /usr/bin/c4OSInstaller/installer.sh
sudo cp -R configs /usr/bin/c4OSInstaller/configs
sudo cp -R programs /usr/bin/c4OSInstaller/programs

sudo ln -s /usr/bin/c4OSInstaller/wrapper_py /usr/bin/installer
sudo chmod 777 /usr/bin/installer
sudo ln -s /usr/bin/c4OSInstaller/wrapper_sh /usr/bin/c4osinstall
sudo chmod 777 /usr/bin/c4osinstall