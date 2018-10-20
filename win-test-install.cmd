@echo off
setlocal ENABLEEXTENSIONS
echo.
echo Unlocker 3.0.2 for VMware Workstation
echo =====================================
echo (c) Dave Parsons 2011-18
echo.
echo Set encoding parameters...
chcp 850

net session >NUL 2>&1
if %errorlevel% neq 0 (
    echo Administrator privileges required!
    exit /b
)

echo.
set KeyName="HKLM\SOFTWARE\Wow6432Node\VMware, Inc.\VMware Player"
:: delims is a TAB followed by a space
for /F "tokens=2* delims=	 " %%A in ('REG QUERY %KeyName% /v InstallPath') do set InstallPath=%%B
echo VMware is installed at: %InstallPath%
for /F "tokens=2* delims=	 " %%A in ('REG QUERY %KeyName% /v ProductVersion') do set ProductVersion=%%B
echo VMware product version: %ProductVersion%

pushd %~dp0

echo.
echo Stopping VMware services...
net stop vmware-view-usbd > NUL 2>&1
net stop VMwareHostd > NUL 2>&1
net stop VMAuthdService > NUL 2>&1
net stop VMUSBArbService > NUL 2>&1
taskkill /F /IM vmware-tray.exe > NUL 2>&1

echo.
echo Backing up files...
rd /s /q .\backup > NUL 2>&1
mkdir .\backup
mkdir .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx.exe" .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx-debug.exe" .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx-stats.exe" .\backup\x64
xcopy /F /Y "%InstallPath%vmwarebase.dll" .\backup\

echo.
echo Patching...
python unlocker.py

echo.
echo Getting VMware Tools...
python gettools.py
xcopy /F /Y .\tools\darwin*.* "%InstallPath%"

echo.
echo Starting VMware services...
net start VMUSBArbService > NUL 2>&1
net start VMAuthdService > NUL 2>&1
net start VMwareHostd > NUL 2>&1
net start vmware-view-usbd > NUL 2>&1

popd
echo.
echo Finished!
