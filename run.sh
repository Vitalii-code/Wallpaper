#!/bin/bash


echo -e "[Wallpaper] Loading..."
python3 -m ensurepip --upgrade # install pip
python3 -m pip install virtualenv # install venv
python3 -m venv venv # creating venv
venv/bin/pip3 install -r requirements/linux_requirements.txt # installing requirements
echo -e "\n[Wallpaper] The program must be in tray"
venv/bin/python3 src/main.pyw
