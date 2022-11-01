@echo off
setlocal enabledelayedexpansion
echo [Wallpaper] Loading...

set version="3.9.13"
set version_code="39"
@REM set version="3.11.0"
@REM set version_code="311"


if not exist "python\" (
	echo [Wallpaper] Python is not installed
	
	echo [Wallpaper] Python is installing...
	start /WAIT /b downloader\aria2c.exe --disable-ipv6 "https://www.python.org/ftp/python/%version%/python-%version%-embed-amd64.zip" -o "python.zip" < NUL
	
	md python
	tar -xf python.zip -C python
	del python.zip
	(
		echo python%version_code%.zip
		echo .
		echo import site
	)>>"python\python%version_code%._pth"

    start /WAIT /b downloader\aria2c.exe --disable-ipv6 "https://bootstrap.pypa.io/get-pip.py" -o "python\get-pip.py" < NUL
	python\python.exe python\get-pip.py

	echo [Wallpaper] Python is installed
	
)


python\Scripts\pip.exe install -r requirements\windows_requirements.txt

start python\pythonw.exe src\main.pyw %*
