#!/bin/bash

pyinstaller src/main.pyw --clean --onefile --name Wallpaper --icon icons/ico.ico
rm -r dist/icons/
cp -r icons/ dist/icons/
