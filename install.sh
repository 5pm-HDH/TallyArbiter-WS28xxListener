#!/bin/bash

read -p "did you check config_ws281x.json before install? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then

  apt-get install python3-pip
  pip3 install rpi_ws281x
  pip3 install "python-socketio[client]"

  mkdir /root/tally

  cp tallyarbiter-ws281xlistener.py /root/tally/tallyarbiter-ws281xlistener.py
  cp config_ws281x.json /root/tally/config_ws281x.json


  read -p "Enable systemd service [y/n]" -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      cp ws281x.service /etc/systemd/system/ws281x.service
      systemctl reload-daemon
      systemctl enable ws281x.service
  fi
fi

echo "Install finished"
echo "installed to /root/tally"