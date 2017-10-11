#!/bin/bash
set -e

echo VMware Unlocker 2.1.1
echo ===============================
echo Copyright: Dave Parsons 2011-17

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Creating backup folder...
rm -rf ./backup
mkdir -p "./backup"
cp -v /Applications/VMware\ Fusion.app/Contents/Library/vmware-vmx ./backup/
cp -v /Applications/VMware\ Fusion.app/Contents/Library/vmware-vmx-debug ./backup/
cp -v /Applications/VMware\ Fusion.app/Contents/Library/vmware-vmx-stats ./backup/
cp -v /Applications/VMware\ Fusion.app/Contents/Frameworks/libvmwarebase.dylib ./backup/

echo Patching...
python ./unlocker.py

echo Finished!
