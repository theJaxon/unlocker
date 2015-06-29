#!/bin/sh
set -e

echo VMware Unlocker 2.0.6
echo ===============================
echo Copyright: Dave Parsons 2011-15

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo Uninstalling local.sh 
cp /etc/rc.local.d/.#local.sh /etc/rc.local.d/local.sh
echo Success - please now restart the server!
