#!/bin/sh
set -e
set -x

echo VMware ESXi 6.x Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

/etc/init.d/hostd status
/etc/init.d/hostd stop
vmkramdisk /bootbank/unlocker.vgz
/etc/init.d/hostd start
/etc/init.d/hostd status
