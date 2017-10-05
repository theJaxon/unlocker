#!/bin/sh
set -e
#set -x

echo VMware Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-17

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo Uninstalling local.sh
cp /etc/rc.local.d/.#local.sh /etc/rc.local.d/local.sh
python esxi-config.py delete
backup.sh 0
echo Success - please now restart the server!
