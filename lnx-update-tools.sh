#!/bin/bash
set -e

echo VMware Get OS X Tools 2.0.8
echo ===============================
echo Copyright: Dave Parsons 2011-15

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Getting VMware Tools...
python2 gettools.py
cp ./tools/darwin.* /usr/lib/vmware/isoimages/

echo Finished!

