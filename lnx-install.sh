#!/bin/bash
set -e

echo "Unlocker 3.0.2 for VMware Workstation"
echo "====================================="
echo "(c) Dave Parsons 2011-18"

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
cp -v /usr/lib/vmware/bin/vmware-vmx ./backup/
cp -v /usr/lib/vmware/bin/vmware-vmx-debug ./backup/
cp -v /usr/lib/vmware/bin/vmware-vmx-stats ./backup/
if [ -d /usr/lib/vmware/lib/libvmwarebase.so.0/ ]; then
    cp -v /usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0 ./backup/
elif [ -d /usr/lib/vmware/lib/libvmwarebase.so/ ]; then
    cp -v /usr/lib/vmware/lib/libvmwarebase.so/libvmwarebase.so ./backup/
fi

echo Patching...
python3 ./unlocker.py

echo Getting VMware Tools...
python3 ./gettools.py
cp ./tools/darwin*.* /usr/lib/vmware/isoimages/

echo Finished!

