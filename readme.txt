macOS Unlocker V3.0 for VMware Workstation
==========================================

+-----------------------------------------------------------------------------+
| IMPORTANT:                                                                  |
| ==========                                                                  |
|                                                                             |
| Always uninstall the previous version of the Unlocker before using a new    |
| version. Failure to do this could render VMware unusable.                   |
|                                                                             |
+-----------------------------------------------------------------------------+

1. Introduction
---------------

Unlocker 3 is designed for VMware Workstation 11-15 and Player 7-15.

If you are using an earlier product please continue using Unlocker 1.

Version 3 has been tested against:

* Workstation 11/12/14/15 on Windows and Linux
* Workstation Player 7/12/14/15 on Windows and Linux

The patch code carries out the following modifications dependent on the product
being patched:

* Fix vmware-vmx and derivatives to allow macOS to boot
* Fix vmwarebase .dll or .so to allow Apple to be selected during VM creation
* Download a copy of the latest VMware Tools for macOS

Note that not all products recognise the darwin.iso via install tools menu item.
You will have to manually mount the darwin.iso for example on Workstation 11 and Player 7.

In all cases make sure VMware is not running, and any background guests have
been shutdown.

The code is written in Python.

2. Prerequisites
----------------

The code requires Python 2.7 to work. Most Linux distros ship with a compatible
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
| If you create a new VM VMware may stop and create a core dump.              |
| There are two options to work around this issue:                            |
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
lnx-update-tools.sh - retrieves latest macOS guest tools
   
6. Thanks
---------

Thanks to Zenith432 for originally building the C++ unlocker and Mac Son of Knife
(MSoK) for all the testing and support.

Thanks also to Sam B for finding the solution for ESXi 6 and helping me with
debugging expertise. Sam also wrote the code for patching ESXi ELF files and
modified the unlocker code to run on Python 3 in the ESXi 6.5 environment.


History
-------
27/09/18 3.0.0 - First release
02/10/18 3.0.1 - Fixed gettools.py to work with Python 3 and correctly download darwinPre15.iso
10/10/18 3.0.2 - Fixed false positives from anti-virus software with Windows executables
               - Allow Python 2 and 3 to run the Python code from Bash scripts


(c) 2011-2018 Dave Parsons