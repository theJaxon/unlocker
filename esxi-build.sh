#!/bin/sh
set -e
#set -x

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Copy patch to local.sh
rm -fv local.sh
cp local-prefix.sh local.sh
cat unlocker.py >> local.sh
cat local-suffix.sh >> local.sh
chmod +x local.sh
