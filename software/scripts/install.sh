#!/bin/bash

set echo off

echo "Installing cueServer."

if [ "$EUID" -ne 0 ]
  then echo "Please re-run the install scrhipt as root."
  exit
fi

apt-get update
apt install python3 -y
pip install pyserial websocket-client

exit