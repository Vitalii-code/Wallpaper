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

if [ -e venv ]
then
    echo
else
    python3 -m virtualenv -q venv # creating venv
fi



venv/bin/pip3 install -q -r requirements/linux_requirements.txt # installing requirements
venv/bin/python3 src/main.pyw $@
