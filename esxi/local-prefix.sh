#!/bin/sh
set -e
set -x

echo VMware ESXi 6.x Unlocker 2.1.0
echo ===============================
echo Copyright: Dave Parsons 2011-17

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Exit if boot option specified
if bootOption -o | grep -q 'nounlocker'; then
    logger -t unlocker disabled via nounlocker boot option
    exit 0
fi

# Make sure working files are removed
if [ -d /unlocker ]; then
	logger -t unlocker Removing current patches
	rm -rfv /unlocker
fi

# Create new RAM disk and map to /unlocker
logger -t unlocker Creating RAM disk
mkdir /unlocker
localcli system visorfs ramdisk add -m 200 -M 200 -n unlocker -p 0755 -t /unlocker
logger -t unlocker Stopping hostd daemon
/etc/init.d/hostd stop

# Copy the vmx files
logger -t unlocker Copying vmx files
mkdir /unlocker/bin
cp /bin/vmx /unlocker/bin/
cp /bin/vmx-debug /unlocker/bin/
cp /bin/vmx-stats /unlocker/bin/

# Setup symlink from /bin
logger -t unlocker Setup vmx sym links
rm -fv /bin/vmx
ln -s /unlocker/bin/vmx /bin/vmx
rm -fv /bin/vmx-debug
ln -s /unlocker/bin/vmx-debug /bin/vmx-debug
rm -fv /bin/vmx-stats
ln -s /unlocker/bin/vmx-stats /bin/vmx-stats

# Copy the libvmkctl.so files
logger -t unlocker Copying 32-bit lib files
mkdir /unlocker/lib
cp /lib/libvmkctl.so /unlocker/lib/
logger -t unlocker Setup 32-bit lib sym links
rm -fv /lib/libvmkctl.so
ln -s /unlocker/lib/libvmkctl.so /lib/libvmkctl.so
if [ -f /lib64/libvmkctl.so ]; then
    logger -t unlocker Copying 64-bit lib files
    mkdir /unlocker/lib64
    cp /lib64/libvmkctl.so /unlocker/lib64/
    logger -t unlocker Setup 64-bit lib sym links
    rm -fv /lib64/libvmkctl.so
    ln -s /unlocker/lib64/libvmkctl.so /lib64/libvmkctl.so
fi

# Patch the vmx files
logger -t unlocker Patching vmx files
python <<END
