# !/bin/bash
sudo pacman -S meson ninja gcc glib2-devel libdbusmenu-gtk3 gsettings-desktop-schemas --noconfirm
sudo pacman -S --overwrite='*' gobject-introspection --noconfirm
curl https://codeload.github.com/diodon-dev/diodon/tar.gz/refs/tags/1.13.0 -o diodon.tar.gz
tar -xvzf diodon.tar.gz
rm diodon.tar.gz
cd diodon-1.13.0
meson setup build
meson compile -C build
sudo meson install -C build
cd ..
sudo rm -R diodon-1.13.0