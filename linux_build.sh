#!/bin/bash

pyinstaller src/main.pyw --clean --onefile --name Wallpaper --icon icons/ico.ico
cp -r icons/ dist/icons/
