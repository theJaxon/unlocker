macOS Unlocker for VMware V2.1
==============================

+-----------------------------------------------------------------------------+
| IMPORTANT:                                                                  |
| ==========                                                                  |
|                                                                             |
| Always uninstall the previous version of the Unlocker before using a new    |
| version. Failure to do this could render VMware unusable.                  |
|                                                                             |
+-----------------------------------------------------------------------------+

1. Introduction
---------------

Unlocker 2 is designed for Workstation 11/12/14, Player 7/12/14, 
and Fusion 7/8/10.

If you are using an earlier product please continue using Unlocker 1.

Version 2 has been tested against:

* Workstation 11/12/14 on Windows and Linux
* Workstation Player 7/12/14 on Windows and Linux
* Fusion 7/8/10 on macOS Sierra

The patch code carries out the following modifications dependent on the product
being patched:

* Fix vmware-vmx and derivatives to allow macOS to boot
* Fix vmwarebase .dll or .so to allow Apple to be selected during VM creation
* Download a copy of the latest VMware Tools for macOS

Note that not all products recognise the darwin.iso via install tools menu item.
You will have to manually mount the darwin.iso for example on Workstation 11 and Player 7.

The vmwarebase code does not need to be patched on macOS systems so you will see a
message on those systems telling you that it will not be patched.

In all cases make sure VMware is not running, and any background guests have
been shutdown.

The code is written in Python as it makes the Unlocker easier to run and maintain on ESXi.

2. Prerequisites
----------------

The code requires Python 2.7 to work. Most Linux distros and macOS ship with a compatible
Python interpreter and should work without requiring any additional software.

Windows Unlocker has a packaged version of the Python script using PyInstaller, 
and so does not require Python to be installed.

3. Limitations
--------------

If you are using VMware Player or Workstation on Windows you may get a core dump.

Latest Linux products are OK and do not show this problem.

+-----------------------------------------------------------------------------+
| IMPORTANT:                                                                  |
| ==========                                                                  |
|                                                                             |
| If you create a new VM using version 11, 12 or 13 hardware VMware may stop  |
| and create a core dump. There are two options to work around this issue:    |
|                                                                             |
| 1. Change the VM to be HW 10 - this does not affect performance.            |
| 2. Edit the VMX file and add:                                               |
|    smc.version = "0"                                                        |
|                                                                             |
+-----------------------------------------------------------------------------+

4. Windows
----------
On Windows you will need to either run cmd.exe as Administrator or using
Explorer right click on the command file and select "Run as administrator".

win-install.cmd   - patches VMware
win-uninstall.cmd - restores VMware
win-update-tools.cmd - retrieves latest macOS guest tools

5. Linux
---------
On Linux you will need to be either root or use sudo to run the scripts.

You may need to ensure the Linux scripts have execute permissions
by running chmod +x against the 2 files.

lnx-install.sh   - patches VMware
lnx-uninstall.sh - restores VMware
lnx-update-tools.cmd - retrieves latest macOS guest tools

6. macOS
--------
On macOS you will need to be either root or use sudo to run the scripts.
This is really only needed if you want to use client versions of macOS.

You may need to ensure the macOS scripts have execute permissions
by running chmod +x against the 2 files.

osx-install.sh   - patches VMware
osx-uninstall.sh - restores VMware

7. ESXi
-------
ESXi is no longer supported as there are too many errors on newer versions due to
VMware hardening the ESXi image.
   
8. Thanks
---------

Thanks to Zenith432 for originally building the C++ unlocker and Mac Son of Knife
(MSoK) for all the testing and support.

Thanks also to Sam B for finding the solution for ESXi 6 and helping me with
debugging expertise. Sam also wrote the code for patching ESXi ELF files and
modified the unlocker code to run on Python 3 in the ESXi 6.5 environment.


History
-------
10/10/17 2.1.0 - New version to support ESXi 6.5, Workstation/Player 14 and Fusion 10
               - Removed support for ESXi 6.0
               - Added ESXi boot option to disable unlocker (nounlocker)
11/10/17 2.1.1 - Removed all support for ESXi 6.x


(c) 2011-2017 Dave Parsons