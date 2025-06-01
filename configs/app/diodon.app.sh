#!/bin/bash
sudo pacman -S python-markupsafe --overwrite '*' --noconfirm
sudo pacman -S meson ninja base-devel gtk3 glib2 libayatana-appindicator zeitgeist gobject-introspection --noconfirm
curl https://codeload.github.com/diodon-dev/diodon/tar.gz/refs/tags/1.13.0 -o src.tar.gz
tar -xzf src.tar.gz
cd diodon-1.13.0
mkdir build
cd build
meson .. --prefix=/usr
ninja
sudo ninja install
cd ../..
sudo rm -R diodon-1.13.0
sudo rm -R src.tar.gz
echo /usr/local/lib | sudo tee /etc/ld.so.conf.d/usr-local.conf
ldconfig

sudo mkdir -p ~/.config/autostart/
sudo tee ~/.config/autostart/diodon.desktop > /dev/null <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=Diodon
Icon=diodon
NotShowIn=KDE;
Exec=diodon %u
Terminal=false
Categories=GTK;GNOME;Utility;
StartupNotify=false
MimeType=x-scheme-handler/clipboard;
EOF