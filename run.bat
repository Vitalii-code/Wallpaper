@echo off
echo [Wallpaper] Loading...



@IF Not Defined python (
	echo Python is not installed
	
	
	set /p ask="Do you want to install Python? [Yes, No]:"
	if "%ask%" == "Yes"{
		echo Installing Python...
		[CmdletBinding()] Param(
			$pythonVersion = "3.10.7"
			$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion.exe"
			$pythonDownloadPath = 'C:\Tools\python-$pythonVersion.exe'
			$pythonInstallDir = "C:\Tools\Python$pythonVersion"
		)

		(New-Object Net.WebClient).DownloadFile($pythonUrl, $pythonDownloadPath)
		& $pythonDownloadPath /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=$pythonInstallDir
		if ($LASTEXITCODE -ne 0) {
			throw "The python installer at '$pythonDownloadPath' exited with error code '$LASTEXITCODE'"
		}

		[Environment]::SetEnvironmentVariable("PATH", "${env:path};${pythonInstallDir}", "Machine")
	
		}
		
) Else (
	echo Python is installed
)



python -m venv venv
venv\Scripts\pip.exe install -r requirements\windows_requirements.txt
start venv\Scripts\pythonw.exe src\main.pyw


