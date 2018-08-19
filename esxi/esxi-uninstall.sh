#!/bin/sh
set -e
#set -x

echo VMware Unlocker 3.0.0
echo ===============================
echo Copyright: Dave Parsons 2011-18

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo Uninstalling unlocker.tgz
BootModuleConfig.sh --verbose --remove=unlocker.tgz
echo Success - please now restart the server!
