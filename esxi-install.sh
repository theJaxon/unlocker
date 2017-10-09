#!/bin/sh
set -e
#set -x

echo VMware Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-17

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

VER=$(uname -r)
if [ "$VER" == "6.0.0" ]; then
   echo "Error - ESXi 6.0.0 is not supported!"
elif [ "$VER" == "6.5.0" ]; then
    # Copy patch to local.sh
    echo Installing local.sh
    chmod +x local.sh
    cp local.sh /etc/rc.local.d/local.sh
    python esxiconfig.py on
    backup.sh 0
    echo "Success - please now restart the server!"
else
   echo "Unknown ESXi version"
fi




