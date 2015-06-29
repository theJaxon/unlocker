#!/bin/bash
set -e

echo VMware Unlocker 2.0.6
echo ===============================
echo Copyright: Dave Parsons 2011-15

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Restoring files...
cp -v ./backup/vmware-vmx /Applications/VMware\ Fusion.app/Contents/Library
cp -v ./backup/vmware-vmx-debug /Applications/VMware\ Fusion.app/Contents/Library
cp -v ./backup/vmware-vmx-stats /Applications/VMware\ Fusion.app/Contents/Library
cp -v ./backup/libvmwarebase.dylib /Applications/VMware\ Fusion.app/Contents/Frameworks/

echo Removing backup files...
rm -rf ./backup

echo Finished!
