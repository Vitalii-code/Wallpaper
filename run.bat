@echo off
setlocal enabledelayedexpansion
echo [Wallpaper] Loading...

@REM for /f %%i in ('python -V') do set VARIABLE=%%i

if not exist "python\" (
	echo [Wallpaper] Python is not installed
	SET /p "ASK=[Wallpaper] Do you want to install Python? [y, n]:"
	if "!ASK!" == "y" (
		echo [Wallpaper] Python is installing...
		powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip', 'python.zip')" < NUL
		md python
		tar -xf python.zip -C python
		del python.zip
		(
			echo python39.zip
			echo .
			echo import site
		)>>"python\python39._pth"

		powershell -Command "(New-Object Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', 'python\get-pip.py')" < NUL
		python\python.exe python\get-pip.py
		

		@REM powershell -Command "Invoke-WebRequest http://www.example.com/package.zip -OutFile package.zip"		
		@REM Powershell.exe -ExecutionPolicy Bypass -File src\python-install.ps1 
		echo [Wallpaper] Python is installed
	)
)

@REM python -m venv venv
@REM venv\Scripts\pip.exe install -r requirements\windows_requirements.txt
@REM start venv\Scripts\pythonw.exe src\main.pyw

python\Scripts\pip.exe install -r requirements\windows_requirements.txt
start python\pythonw.exe src\main.pyw

echo [Wallpaper] The program must be in tray

@REM pause
@REM endlocal
@REM exit/B
