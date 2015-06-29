#!/bin/sh
set -e

echo VMware Unlocker 2.0.6
echo ===============================
echo Copyright: Dave Parsons 2011-15

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Copy patch to local.sh
echo Installing local.sh 
cp local-template.sh local.sh
cat unlocker.py >> local.sh
echo END >> local.sh
echo /etc/init.d/hostd restart >> local.sh
chmod +x local.sh
cp local.sh /etc/rc.local.d/local.sh
echo Success - please now restart the server!
