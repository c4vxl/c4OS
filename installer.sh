#!/bin/bash
INSTALLATION_RUNTIME="runtime"
EFI=""
ROOT=""
BOOTLOADER_ID="c4OS"
HOSTNAME="c4OS"
USERNAME=""
PASSWORD=""
THEME=""
SWAP_SIZE="2G"
WIFI=""
WIFI_PW=""
DESKTOP_ENV="gnome"
NO_TOUR=false
NO_THEME_SWITCHER=false
PACKAGES="base linux linux-firmware nano sudo networkmanager bluez-utils bluez cups ghostscript neofetch grub efibootmgr git xorg git base-devel wget"
FB_SCRIPTS=""
SOFTWARE=""

for ARG in "$@"; do
  case $ARG in
    --runtime=*)
      INSTALLATION_RUNTIME="${ARG#*=}"
      ;;
    --efi=*)
      EFI="${ARG#*=}"
      ;;
    --root=*)
      ROOT="${ARG#*=}"
      ;;
    --bootloader-id=*)
      BOOTLOADER_ID="${ARG#*=}"
      ;;
    --hostname=*)
      HOSTNAME="${ARG#*=}"
      ;;
    --username=*)
      USERNAME="${ARG#*=}"
      ;;
    --password=*)
      PASSWORD="${ARG#*=}"
      ;;
    --theme=*)
      THEME="${ARG#*=}"
      ;;
    --swap=*)
      SWAP_SIZE="${ARG#*=}"
      ;;
    --wifi=*)
      WIFI="${ARG#*=}"
      ;;
    --wifi-pw=*)
      WIFI_PW="${ARG#*=}"
      ;;
    --desktop-env=*)
      DESKTOP_ENV="${ARG#*=}"
      ;;
    --packages=*)
      PACKAGES="${ARG#*=}"
      ;;
    --no-tour)
      NO_TOUR=true
      ;;
    --fbs=*)
      FB_SCRIPTS+="\n${ARG#*=}"
      ;;
    --software=*)
      SOFTWARE+="${ARG#*=}"
      SOFTWARE="${SOFTWARE//[,;]/ }"
      ;;
    --no-theme-switcher)
      NO_THEME_SWITCHER=true
      ;;
    *)

      echo ">>> Subcommand overview:"
      echo ">>> All arguments marked with a '*' are required!"
      echo "  | --runtime=<runtime_directory>         ; Path where the OS should be mounted during the installation. (Default: ./runtime)"
      echo "  | --efi=<efi_partition>         *       ; The partition for the EFI-files."
      echo "  | --root=<root_partition>       *       ; The partition where the OS should be installed."
      echo "  | --username=<username>         *       ; The username of the admin/owner of the new system."
      echo "  | --hostname=<hostname>                 ; The hostname of the new system. (Default: c4OS)"
      echo "  | --password=<password>                 ; The password for the admin/owner 's account. (Leave empty to disable password)"
      echo "  | --theme=<theme>                       ; The Theme to install (eg. c4dots/gnome_white_mar_25)."
      echo "  | --swap=<swap_size>                    ; Size of the swap file. (Default: 2G)"
      echo "  | --wifi=<wifi_network>                 ; SSID of the WIFI-Network to connect the new os to."
      echo "  | --wifi-pw=<wifi_password>             ; Password of the WIFI-Network (if needed)."
      echo "  | --desktop-env=<desktop_environment>   ; The desktop environment to use (Options: gnome, none; Default: gnome)."
      echo "  | --bootloader-id=<name>                ; The name the new OS should show up in bios. (Default: c4OS)"
      echo "  | --packages=<packages>                 ; Set the list of default packages to strap onto the installation at the beginning. (Don't touch!!!)"
      echo "  | --fbs=<shell_code>                    ; Add code to be run on first login into the system (May be passed multiple times)."
      echo "  | --software=<software>                 ; Add preinstalled software (May be passed multiple times). (Seperate by comma)"
      echo "  | --no-tour                             ; Don't show a tour at the first startup of the os."
      echo "  | --no-theme-switcher                   ; Prevents from installing the 'Theme-Switcher' app."
      exit
      ;;
  esac
done

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -z "$EFI" ] || [ -z "$ROOT" ]; then
    echo "Error: Booth '--efi' and '--root' must be specified. Try --help."
    exit
fi

if [ ! -b "$EFI" ]; then
    echo "Error: EFI-Partition '$EFI' does not exist! Try --help."
    exit
fi

if [ ! -b "$ROOT" ]; then
    echo "Error: Root-Partition '$ROOT' does not exist! Try --help."
    exit
fi

if [ "$USERNAME" == "" ]; then
    echo "Error: No username specified! Try --help."
    exit
fi


function prepare_partitions() {
    echo ">>> Preparing partitions..."
    
    echo "  | Unmounting EFI."
    umount -R "$EFI" &> /dev/null
    echo "  | Formatting EFI". &> /dev/null
    mkfs.fat -F 32 "$EFI" &> /dev/null

    echo "  | Unmounting Root."
    umount -R "$ROOT" &> /dev/null
    echo "  | Formatting Root."
    mkfs.ext4 "$ROOT" &> /dev/null
}

function prepare_env() {
    echo ">>> Preparing environment..."

    echo "  | Cleaning old runtime."
    rm -R "$INSTALLATION_RUNTIME" &> /dev/null
    mkdir -p "$INSTALLATION_RUNTIME" &> /dev/null

    echo "  | Mounting Root."
    mkdir -p "$INSTALLATION_RUNTIME" &> /dev/null
    mount "$ROOT" "$INSTALLATION_RUNTIME" &> /dev/null

    echo "  | Mounting EFI."
    mkdir -p "$INSTALLATION_RUNTIME/boot/efi" &> /dev/null
    mount "$EFI" "$INSTALLATION_RUNTIME/boot/efi" &> /dev/null
}

function execute_as_root() {
    echo "  | Executing command on installation: $1"
    arch-chroot "$INSTALLATION_RUNTIME" /bin/bash -c "$1"
}

function execute_as_user() {
    execute_as_root "printf \"$PASSWORD\n\" | sudo -u $USERNAME /bin/bash -c \"cd ~ && $1\""
}

function execute_on_first_login() {
    uuid="$(uuidgen)"
    echo "  | Creating first-login-task $uuid"
    path="/home/$USERNAME/.cache/.first_login_installer/$uuid"
    sudo mkdir -p "$INSTALLATION_RUNTIME/home/$USERNAME/.cache/.first_login_installer/"

    execute_as_root "
    if [ ! -f \"$path\" ]; then
        echo '#!/bin/bash' > \"$path\"
        echo \"$1\" >> \"$path\"
        chmod 777 \"$path\"
        echo '[[ -f ~/.is_first_login ]] && $path' >> \"/home/$USERNAME/.profile\"
    fi
    "
}

function setup_grub() {
    execute_as_root "
    grub-install --efi-directory=/boot/efi/ --bootloader-id=\"$BOOTLOADER_ID\"
    sudo pacman -S os-prober --noconfirm
    sed -i \"s/^GRUB_DISTRIBUTOR=\\\"[^\\\"]*\\\"/GRUB_DISTRIBUTOR=\\\"$BOOTLOADER_ID\\\"/\" /etc/default/grub
    sed -i 's/^#GRUB_DISABLE_OS_PROBER=.*/GRUB_DISABLE_OS_PROBER=false/' /etc/default/grub
    grub-install --efi-directory=/boot/efi/ --bootloader-id=\"$BOOTLOADER_ID\"
    grub-mkconfig -o /boot/grub/grub.cfg

    git clone "https://github.com/vinceliuice/grub2-themes.git"
    cd grub2-themes
    sudo sh ./install.sh --theme "whitesur" -b
    cd ..
    sudo rm -R grub2-themes
    "
}

function load_base() {
    echo ">>> Installing base..."
    echo "  | Installing Packages."
    pacstrap "$INSTALLATION_RUNTIME" $PACKAGES

    echo "  | Generating FS-Tab."
    genfstab -U "$INSTALLATION_RUNTIME" > "$INSTALLATION_RUNTIME/etc/fstab"

    echo "  | Enabling multilib."
    execute_as_root "sudo sed -i '/^\[multilib\]/,/Include/ s/^#//' /etc/pacman.conf"

    echo "  | Updating packages."
    execute_as_root "pacman -Sy --noconfirm && pacman -Syu --noconfirm"

    echo "  | Enabling services."
    execute_as_root "systemctl enable NetworkManager cups bluetooth"

    echo "  | Installing bootloader."
    setup_grub

    echo "  | Changing hostname."
    execute_as_root "echo \"$HOSTNAME\" > /etc/hostname"

    echo "  | Creating user."
    execute_as_root "
    sed -i 's/^# %wheel ALL=(ALL:ALL) ALL$/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
    useradd -mG wheel $USERNAME
    "

    echo "  | Installing yay."
    execute_as_root "
    pacman -S go --noconfirm
    yes \"$PASSWORD\" | sudo -S passwd -d $USERNAME
    "
    execute_as_user "
    cd /opt
    sudo -S git clone https://aur.archlinux.org/yay-bin.git
    sudo -S chown -R $(whoami):$(whoami) yay-bin
    sudo chmod 777 -R /opt/yay-bin/
    cd yay-bin
    yes | makepkg -si
    cd ..
    yes | sudo rm -R yay-bin
    yes \"$PASSWORD\" | passwd $USERNAME
    "

    echo "  | Generating swap."
    sudo sed -i '/\/swapfile\s\+none\s\+swap\s\+defaults\s\+0\s\+0/d' "$INSTALLATION_RUNTIME/etc/fstab"
    execute_as_root "
    fallocate -l $SWAP_SIZE /swapfile
    sudo swapoff -a
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo \"/swapfile none swap sw 0 0\" >> /etc/fstab
    "

    echo "  | Creating Desktop."
    execute_as_user "mkdir Desktop"
}

function load_wifi() {
    if [[ "$WIFI" != "" ]]; then
        execute_on_first_login "
        yes $PASSWORD | sudo -S nmcli device wifi connect \\\"$WIFI\\\" password \\\"$WIFI_PW\\\"
        "
    fi
}

function setup_gnome() {
    echo ">>> Installing gnome..."
    echo "  | Getting packages."
    execute_as_root "
    pacman -S gnome gdm gnome-shell gnome-terminal gnome-shell-extensions gnome-tweaks gnome-browser-connector gnome-text-editor gnome-shell-extension-desktop-icons-ng pulseaudio --noconfirm
    pacman -R gnome-tour malcontent --noconfirm
    sed -i 's/^#WaylandEnable=false$/WaylandEnable=false/' /etc/gdm/custom.conf
    systemctl enable gdm
    "

    echo "  | Configuring gnome."
    execute_as_root "
    convert -size 1x1 xc:transparent /usr/share/pixmaps/archlinux-logo.png
    rm /usr/share/pixmaps/archlinux-logo-text-dark.svg /usr/share/pixmaps/archlinux-logo-text.svg /usr/share/pixmaps/archlinux-logo.svg
    "

    execute_on_first_login "
dconf load / << EOF
$(cat configs/gnome/keybinds)
EOF
    "
}

function setup_desktop_env() {
    if [[ "$DESKTOP_ENV" == "gnome" ]]; then
        setup_gnome
    fi
}

function setup_theme() {
    if [[ "$THEME" != "" ]]; then
        echo ">>> Creating theme installation process..."
        execute_on_first_login "sleep 1 && dbus-launch \\\$(yes $PASSWORD | themes --install=$THEME)"
    fi
}

function setup_theme_switcher() {
    if [[ "$NO_THEME_SWITCHER" == "false" ]]; then
        echo ">> Installing theme switcher"
        sudo cp -R "programs/theme_switcher/" "$INSTALLATION_RUNTIME/home/$USERNAME/.theme_switcher"
        execute_as_user "
        cd .theme_switcher
        yes $PASSWORD | sudo -S sh setup.sh
        cd ..
        yes $PASSWORD | sudo -S rm -R .theme_switcher
        "
    fi
}

function prepare_tour() {
    if [[ "$NO_TOUR" == "false" ]]; then
        echo ">>> Preparing tour..."
        sudo mkdir "$INSTALLATION_RUNTIME/usr/bin/tour_src/"
        sudo cp programs/tour/tour.py "$INSTALLATION_RUNTIME/usr/bin/tour_src/"

        echo "  | Installing required packages."
        execute_as_root "sudo pacman -S python-pip --noconfirm && pip install PyGObject pywebview flask --break-system-packages"

        echo "  | Preparing wrapper."
        execute_as_root "
        echo \"#!/bin/bash\" > /usr/bin/tour_src/wrapper
        echo \"python3 /usr/bin/tour_src/tour.py \"\$@\" >/dev/null 2>&1 &\" > /usr/bin/tour_src/wrapper
        "
        sudo ln -s "/usr/bin/tour_src/wrapper" "$INSTALLATION_RUNTIME/usr/bin/tour"
        sudo chmod 777 -R "$INSTALLATION_RUNTIME/usr/bin/tour_src/"

        echo "  | Creating startup task."
        execute_on_first_login "yes $PASSWORD | sudo -S tour"
    fi
}

function install_software() {
    cp "configs/app/$1.app.sh" "$INSTALLATION_RUNTIME/home/$USERNAME/.$1.app.sh"
    execute_as_user "
    echo $PASSWORD | sudo -S -v
    sh .$1.app.sh
    rm .$1.app.sh
    "
}

function prepare_software() {
    echo ">>> Installing software..."
    for i in $SOFTWARE; do
        echo "  | Installing $i."
        install_software $i
    done
}

prepare_partitions
prepare_env
load_base
load_wifi
setup_desktop_env
prepare_tour
setup_theme
prepare_software
setup_theme_switcher

if [[ "$FB_SCRIPTS" != "" ]]; then
  execute_on_first_login $FB_SCRIPTS
fi

# Remove password if the initial password was set to ""
if [[ "$PASSWORD" == "" ]]; then
    echo ">>> Removing password..."
    execute_as_root "yes \"$PASSWORD\" | sudo -S passwd -d $USERNAME"
fi

# Enable the first-login-services
touch "$INSTALLATION_RUNTIME/home/$USERNAME/.is_first_login"
execute_on_first_login "rm .is_first_login && echo \"\" > .profile"