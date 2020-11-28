#!/bin/bash

read -p "Check config_ws281x.json before install! " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then

  apt-get install python3-pip
  pip3 install rpi_ws281x
  pip3 install "python-socketio[client]"

  adduser --disabled-password --disabled-login --gecos "" tally
  usermod -a -G users,dialout,dip,input,gpio tally
  mkdir /home/tally/bin

  cp tallyarbiter-ws281xlistener.py /home/tally/bin/tallyarbiter-ws281xlistener.py
  cp config_ws281x.json home/tally/bin/config_ws281x.json

  chown -R tally /home/tally/bin

  read -p "Enable systemd service " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      cp ws281x.service /etc/systemd/system/ws281x.service
      systemctl enable ws281x.service
  fi




fi

echo "Install finished"
echo "installed to /home/tally/bin/"