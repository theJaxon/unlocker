#!/bin/sh
set -e
set -x

echo VMware ESXi 6.x Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

/etc/init.d/hostd status
/etc/init.d/hostd stop

vmkramdisk /bootbank/unlocker.vgz

sed -i 's/applesmc/vmkernel/g' /lib/libvmkctl.so
if [ -f /lib64/libvmkctl.so ]; then
    sed -i 's/applesmc/vmkernel/g' /lib64/libvmkctl.so
fi

/etc/init.d/hostd start
/etc/init.d/hostd status
