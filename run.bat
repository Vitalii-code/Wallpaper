@echo off
echo "[Wallpaper] Loading..."

python -m venv venv
venv\Scripts\pip.exe install -r requirements\windows_requirements.txt
start venv\Scripts\pythonw.exe src\main.pyw


