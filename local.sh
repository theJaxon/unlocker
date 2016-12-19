#!/bin/sh
set -e
set -x

echo VMware ESXi 6.x Unlocker 2.0.9
echo ===============================
echo Copyright: Dave Parsons 2011-16

if bootOption -o | grep -q 'nounlocker'; then

    echo Unlocker disabled via boot options >> /var/log/unlocker.log

else

    echo Unlocker running >> /var/log/unlocker.log

    /etc/init.d/hostd status >> /var/log/unlocker.log
    /etc/init.d/hostd stop >> /var/log/unlocker.log

    vmkramdisk /bootbank/unlocker.vgz >> /var/log/unlocker.log

    sed -i 's/applesmc/vmkernel/g' /lib/libvmkctl.so
    if [ -f /lib64/libvmkctl.so ]; then
        sed -i 's/applesmc/vmkernel/g' /lib64/libvmkctl.so
    fi

    /etc/init.d/hostd start  >> /var/log/unlocker.log
    /etc/init.d/hostd status >> /var/log/unlocker.log

fi

exit 0
