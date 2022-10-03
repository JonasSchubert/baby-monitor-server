#!/bin/sh

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

#################################################
#            Install systemd service            #
#################################################
sudo cp baby-monitor.service /lib/systemd/system/
sudo systemctl enable baby-monitor.service
sudo systemctl start baby-monitor.service
