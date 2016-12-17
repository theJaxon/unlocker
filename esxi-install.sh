#!/bin/sh
set -e
set -x

echo VMware Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Ensure we run from the patcher directory
cd "`dirname $0`"

 # Create tmp folder for patching the files
echo Creating unlocker vmtar disk

# Create tmp folder for patching the files
mkdir -p tmp/bin
mkdir -p tmp/lib

cp -v /bin/vmx tmp/bin
cp -v /bin/vmx-debug tmp/bin
cp -v /bin/vmx-stats tmp/bin

# Now using sed in the local.sh script
#cp -v /lib/libvmkctl.so tmp/lib
#
#if [ -f /lib64/libvmkctl.so ]; then
#    mkdir -p tmp/lib64
#    cp -v /lib64/libvmkctl.so tmp/lib64
#fi

# Patch the files
python unlocker.py

# Create the vmtar file for ESXi kernel
#if [ -f /lib64/libvmkctl.so ]; then
#    tar cvf tmp/unlocker.tar -C tmp bin lib lib64
#else
#    tar cvf tmp/unlocker.tar -C tmp bin lib
#fi
tar cvf tmp/unlocker.tar -C tmp bin
vmtar -c tmp/unlocker.tar -v -o tmp/unlocker.vmtar
gzip tmp/unlocker.vmtar
mv tmp/unlocker.vmtar.gz tmp/unlocker.vgz

# Copy to bootbank and setup local.sh
echo Copying unlocker.vgz to bootbank...
cp tmp/unlocker.vgz /bootbank
chmod +x local.sh
cp local.sh /etc/rc.local.d/local.sh

# Clean up
#rm -rfv tmp

echo Success - please now restart the server!
