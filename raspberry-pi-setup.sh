#!/bin/sh

# Update and cleanup system
sudo apt update -y
sudo apt upgade -y
sudo apt dist-upgade -y
sudo apt autoremove -y

# Install node v16
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g npm

# Install additional essential packages
sudo apt install -y build-essential git

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ${USER}

# Install docker-compose
sudo apt-get install -y libffi-dev libssl-dev
sudo apt install -y python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose

# Install Respeaker
cd ~
git clone https://github.com/HinTak/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh

# Install Grove
cd ~
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .

# Reboot now
sudo reboot now
