#!/bin/sh
grep -il \(c\)AppleComputerInc /bin/vmx*
vim-cmd hostsvc/hosthardware | grep smcPresent | cut -d ',' -f 1 | sed 's/^[ \t]*//'
grep useVmxSandbox /etc/vmware/hostd/config.xml | sed 's/^[ \t]*//'
