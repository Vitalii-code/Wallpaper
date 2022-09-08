#!/bin/bash

echo -e "[Wallpaper] Loading..."
python3 -m venv venv
venv/bin/pip3 install -r requirements/linux_requirements.txt
echo -e "\n[Wallpaper] The program must be in tray"
venv/bin/python3 src/main.pyw &


