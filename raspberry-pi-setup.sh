#!/bin/sh

# Update and cleanup system
sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y

# Install additional essential packages
sudo apt install -y build-essential git

# Install Grove
cd ~
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .

# Reboot now
sudo reboot now
