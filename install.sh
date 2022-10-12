#!/bin/sh

CURRENT_DIRECTORY=`pwd`

#################################################
#              Raspberry Pi Setup               #
#################################################
# Update and cleanup system
sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y

#################################################
#                  Git basics                   #
#################################################
sudo apt-get install -y \
    build-essential \
    git

#################################################
#              Python requirements              #
#################################################
sudo apt-get install -y \
    python-pil \
    python-twisted \
    python-dateutil \
    python-autobahn \
    python-serial

#################################################
#               Install gstreamer               #
#################################################
sudo apt-get install -y \
    gstreamer1.0-good \
    gstreamer1.0-plugins-good \
    gstreamer1.0-alsa \
    gstreamer1.0-tools

#################################################
#                  Install VLC                  #
#################################################
sudo apt-get install -y \
    vlc

#################################################
#                    Camera                     #
#################################################
sudo sed -i "/^exit 0$/ i modprobe bcm2835-v4l2" /etc/rc.local

#################################################
#              Python dependencies              #
#################################################
pip3 install configparser
pip3 install twisted
pip3 install python-vlc

#################################################
#               Respeaker Drivers               #
#################################################
cd ~
git clone https://github.com/HinTak/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh

#################################################
#              Grove Sensor Drivers             #
#################################################
cd ~
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .

#################################################
#            Create lullaby song path           #
#################################################
sudo mkdir /mnt/lullaby-songs
# This mounts the network folder with the lullaby songs to the created path.
sudo echo "//192.168.178.21/theatre/music/Lullaby-List /mnt/lullaby-songs cifs guest,_netdev 0 0" >> /etc/fstab

#################################################
#            Install systemd service            #
#################################################
cd ${CURRENT_DIRECTORY}
sudo cp baby-monitor.service /lib/systemd/system/
sudo systemctl enable baby-monitor.service
sudo systemctl start baby-monitor.service

echo "Please reboot your raspberry pi now!"
