#!/bin/sh
set -e
set -x

echo VMware ESXi 6.x Unlocker 2.0.6
echo ===============================
echo Copyright: Dave Parsons 2011-15

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure working files are removed
if [ -d /unlocker ]; then
	logger -t unlocker Removing current patches
	rm -rfv /unlocker
fi

# Create new RAM disk and map to /unlocker
logger -t unlocker Creating RAM disk
mkdir /unlocker
localcli system visorfs ramdisk add -m 100 -M 100 -n unlocker -p 0755 -t /unlocker

# Copy the vmx files
logger -t unlocker Copying vmx files
cp /bin/vmx /unlocker/
cp /bin/vmx-debug /unlocker/
cp /bin/vmx-stats /unlocker/

# Setup symlink from /bin
logger -t unlocker Setup sym links
rm -fv /bin/vmx
ln -s /unlocker/vmx /bin/vmx
rm -fv /bin/vmx-debug
ln -s /unlocker/vmx-debug /bin/vmx-debug
rm -fv /bin/vmx-stats
ln -s /unlocker/vmx-stats /bin/vmx-stats

# Copy the libvmkctl.so file
cp /lib/libvmkctl.so /unlocker
rm -fv /lib/libvmkctl.so
ln -s /unlocker/libvmkctl.so /lib/libvmkctl.so

# Patch the vmx files
logger -t unlocker Patching vmx files
python <<END
