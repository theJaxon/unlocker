#!/bin/sh
set -e
#set -x

echo VMware Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Copy patch to local.sh
echo Installing local.sh
chmod +x local.sh
cp local.sh /etc/rc.local.d/local.sh
python esxi-config.py insert
backup.sh 0
echo Success - please now restart the server!
