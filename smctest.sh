#!/bin/sh
vim-cmd hostsvc/hosthardware | grep smcPresent | cut -d ',' -f 1 | sed 's/^[ \t]*//'
