#!/bin/bash


echo -e "[Wallpaper] Loading..."

if [ -e get-pip.py ]
then
    echo
else
    wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py 
    python3 get-pip.py # install pip
    python3 -m pip install --user virtualenv # install venv
fi


python3 -m virtualenv venv # creating venv
venv/bin/pip3 install -r requirements/linux_requirements.txt # installing requirements
echo -e "\n[Wallpaper] The program must be in tray"
venv/bin/python3 src/main.pyw
