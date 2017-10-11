@echo off
setlocal ENABLEEXTENSIONS
echo VMware Get macOS Tools 2.1.1
echo =============================
echo (c) Dave Parsons 2015-17

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

echo Getting VMware Tools...
gettools.exe
xcopy /F /Y .\tools\darwin*.* "%InstallPath%"

popd

echo Finished!
