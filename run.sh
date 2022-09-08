#!/bin/bash

python3 -m venv venv
venv/bin/pip3 install -r linux_requirements.txt
echo -e "\n The program must be in tray"
venv/bin/python3 main.pyw


