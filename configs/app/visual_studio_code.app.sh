# !/bin/bash
sudo mkdir -p /usr/bin/vscode/
sudo mkdir -p /usr/share/pixmaps/
cd /usr/bin/vscode/

sudo tee /usr/share/applications/code.desktop > /dev/null <<EOF
[Desktop Entry]
Name=Visual Studio Code
Comment=Code Editing. Redefined.
Icon=/usr/share/pixmaps/vscode.png
Exec=/usr/bin/vscode/code --no-sandbox %F
Terminal=False
Type=Application
Categories=Development;IDE
StartupWMClass=Code
EOF

sudo tee /usr/bin/code > /dev/null <<EOF
#!/bin/bash
/usr/bin/vscode/code "$@" >/dev/null 2>&1 &
EOF

sudo wget -O /usr/share/pixmaps/vscode.png https://code.visualstudio.com/assets/images/code-stable.png

sudo wget -O vsc.tar.gz https://code.visualstudio.com/sha/download\?build\=stable\&os\=linux-x64
sudo tar -xvzf vsc.tar.gz --strip-components=1

cp /usr/share/applications/code.desktop ~/Desktop/code.desktop