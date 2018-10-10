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

echo Restoring files...
cp -v ./backup/vmware-vmx  /usr/lib/vmware/bin/
cp -v ./backup/vmware-vmx-debug /usr/lib/vmware/bin/
cp -v ./backup/vmware-vmx-stats /usr/lib/vmware/bin/
if [ -d /usr/lib/vmware/lib/libvmwarebase.so.0/ ]; then
    cp -v ./backup/libvmwarebase.so.0 /usr/lib/vmware/lib/libvmwarebase.so.0/
elif [ -d /usr/lib/vmware/lib/libvmwarebase.so/ ]; then
    cp -v ./backup/libvmwarebase.so /usr/lib/vmware/lib/libvmwarebase.so/
fi

echo Removing backup files...
rm -rf ./backup
rm -rf ./tools
rm -f /usr/lib/vmware/isoimages/darwin*.*

echo Finished!
