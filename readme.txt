Mac OS X Unlocker for VMware V2.0
=================================

1. Introduction
---------------

Unlocker 2 is designed for Workstation 11, Player 7 and Fusion 7.

If you are using an earlier product please continue using Unlocker 1 

Version 2 has been tested against:

* Workstation 11 on Windows and Linux
* Player 7 on Windows and Linux
* Fusion 7 on Mavericks and Yosemite
* (Currently is does not work on ESXi 6.0)

The patch code carries out the following modifications dependent on the product
being patched:

* Fix vmware-vmx and derivatives to allow Mac OS X to boot
* Fix vmwarebase .dll or .so to allow Apple to be selected during VM creation
* A copy of the latest VMware Tools for OS X is included

Note that not all products recognise the darwin.iso via install tools menu item.
You will have to manually mount the darwin.iso for example on Workstation and Player.

The vmwarebase code does not need to be patched on OS X so you will see a
message on those systems telling you that it will not be patched.

In all cases make sure VMware is not running, and any background guests have
been shutdown.

The code is now Python as it makes the Unlocker easier to run and maintain on ESXi.
There are some challenges to write the code as ESXi has a subset of Python 2.7 which
constrains some modules that can be used.

2. Prerequisites
----------------

The code requires Python 2.7 to work. Most Linux distros and OS X ship with a compatible
Python interpreter and should work without requiring any additional software.

Windows has a packaged version of the Python script using PyInstaller, and so does not
require Python to be installed.

3. Limitations
--------------

The Unlocker currently does not work on ESXi 6.

Work continues to find solutions to the limitations.

4. Windows
----------
On Windows you will need to either run cmd.exe as Administrator or using
Explorer right click on the command file and select "Run as administrator".

win-install.cmd   - patches VMware
win-uninstall.cmd - restores VMware

5. Linux
---------
On Linux you will need to be either root or use sudo to run the scripts.

You may need to ensure the Linux scripts have execute permissions
by running chmod +x against the 2 files.

lnx-install.sh   - patches VMware
lnx-uninstall.sh - restores VMware

6. Mac OS X
-----------
On Mac OS X you will need to be either root or use sudo to run the scripts.
This is really only needed if you want to use client versions of Mac OS X.

You may need to ensure the OS X scripts have execute permissions
by running chmod +x against the 2 files.

osx-install.sh   - patches VMware
osx-uninstall.sh - restores VMware


7. Notes
--------

+-----------------------------------------------------------------------------+
| IMPORTANT:                                                                  |
| ==========                                                                  |
|                                                                             |
| If you create a new VM using version 11 hardware VMware will stop and       |
| create a core dump.There are two options to work around this issue:         |
|                                                                             |
| 1. Change the VM to be HW 10 - this does not affect performance.            |
| 2. Edit the VMX file and add:                                               |
|    smc.version = "0"                                                        |
|                                                                             |
+-----------------------------------------------------------------------------+

To remove the check for server versions for OS X Leopard and Snow Leopard 
(10.5 and 10.6) you must use a replacement EFI firwmare module from the firmware
folder.

If you are using a 32-bit installation of OS X:

1. Copy efi32-srvr.rom to guest folder.
2. Edit the vmx file and add:
	efi32.filename = "efi32-srvr.rom"

If you are using a 64-bit installation of OS X:

1. Copy efi64-srvr.rom to guest folder.
2. Edit the vmx file and add:
	efi64.filename = "efi64-srvr.rom"

8. Thanks
---------

Thanks to Zenith432 for originally building the C++ unlocker and Mac Son of Knife
(MSoK) for all the testing and support.


History
-------
12/12/14 2.0.0 - First release
13/13/14 2.0.1 - Removed need for Python for Windows
13/13/14 2.0.2 - darwin.iso was missing from zip file
02/01/15 2.0.3 - Added EFI firmware files to remove Server check
               - Refactored Python code
07/01/15 2.0.4 - Added View USB Service to Windows batch files
               - Fixed broken GOS Table patching on Linux

(c) 2011-2015 Dave Parsons