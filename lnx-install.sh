#!/bin/bash
set -e

echo VMware Unlocker 2.0.4
echo ===============================
echo Copyright: Dave Parsons 2011-15

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
cp -v /usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0 ./backup/

echo Patching...
python2 ./vmxsmc.py

cp ./tools/darwin.* /usr/lib/vmware/isoimages/

echo Finished!

