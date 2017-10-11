@echo off
setlocal ENABLEEXTENSIONS
echo VMware Unlocker 2.1.1
echo ========================
echo (c) Dave Parsons 2011-17

net session >NUL 2>&1
if %errorlevel% neq 0 (
    echo Administrator privileges required! 
    exit
)

pushd %~dp0

set KeyName="HKLM\SOFTWARE\Wow6432Node\VMware, Inc.\VMware Workstation"
:: delims is a TAB followed by a space
for /F "tokens=2* delims=	 " %%A in ('REG QUERY %KeyName% /v InstallPath') do set InstallPath=%%B
echo VMware is installed at: %InstallPath%

echo Stopping VMware services...
net stop vmware-view-usbd > NUL 2>&1
net stop VMwareHostd > NUL 2>&1
net stop VMAuthdService > NUL 2>&1
net stop VMUSBArbService > NUL 2>&1
taskkill /F /IM vmware-tray.exe > NUL 2>&1

echo Backing up files...
rd /s /q .\backup > NUL 2>&1
mkdir .\backup
mkdir .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx.exe" .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx-debug.exe" .\backup\x64
xcopy /F /Y "%InstallPath%x64\vmware-vmx-stats.exe" .\backup\x64
xcopy /F /Y "%InstallPath%vmwarebase.dll" .\backup\

echo Patching...
unlocker.exe

echo Getting VMware Tools...
gettools.exe
xcopy /F /Y .\tools\darwin*.* "%InstallPath%"

echo Starting VMware services...
net start VMUSBArbService > NUL 2>&1
net start VMAuthdService > NUL 2>&1
net start VMwareHostd > NUL 2>&1
net start vmware-view-usbd > NUL 2>&1

popd

echo Finished!
