#!/bin/sh
set -e
set -x

echo VMware Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Remove entry from the boot configuration file
echo Deleting unlocker.vgz from bootbank...
rm /bootbank/unlocker.vgz
rm /etc/rc.local.d/local.sh

echo Please now reboot the host system!
