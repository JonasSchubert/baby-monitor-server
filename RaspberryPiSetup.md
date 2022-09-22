# Raspberry Pi Setup

## Update

```bash
sudo apt update
sudo apt upgade

sudo apt dist-upgade

sudo apt autoremove
```

## Install Node 16.x & NPM

```bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -

sudo apt install nodejs

sudo npm install -g npm
```

```bash
sudo apt install build-essential
```

## Install Git

```bash
sudo apt install git
```

## Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh
```

Add your user to the Docker group:

```bash
sudo usermod -aG docker ${USER}
```

## Install docker-compose

```bash
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip

sudo pip3 install docker-compose
```

## Activate camera

```bash
sudo raspi-config
```

> Activate I2C

## Respeaker

> Do NOT use the official repository as this does not work on latest build

```bash
git clone https://github.com/HinTak/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
sudo reboot now
```

## Grove

### Base

- https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/#installation

### Temperature & Humidity Sensor (SHT31) 

- https://wiki.seeedstudio.com/Grove-TempAndHumi_Sensor-SHT31/
- https://github.com/Seeed-Studio/Grove_SHT31_Temp_Humi_Sensor
