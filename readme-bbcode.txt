[u][b]Mac OS X Unlocker for VMware V2.0[/b][/u]


[u]1. Introduction[/u]

Unlocker 2 is designed for Workstation 11, Player 7, ESXi 6 and Fusion 7.

If you are using an earlier product please continue using Unlocker 1

Version 2 has been tested against:
[LIST]
[*]Workstation 11/12 Pro on Windows and Linux[/*]
[*]Player 7 & Workstation Player 12 on Windows and Linux[/*]
[*]Fusion 7/8 on Mavericks and Yosemite[/*]
[*]ESXi 6.0[/*]
[/LIST]
The patch code carries out the following modifications dependent on the product
being patched:
[LIST]
[*]Fix vmware-vmx and derivatives to allow Mac OS X to boot[/*]
[*]Fix vmwarebase .dll or .so to allow Apple to be selected during VM creation[/*]
[*]Fix libvmkctl.so on ESXi 6 to allow use with vCenter[/*]
[*]A copy of the latest VMware Tools for OS X is included[/*]
[/LIST]
Note that not all products recognise the darwin.iso via install tools menu item.
You will have to manually mount the darwin.iso for example on Workstation and Player.

The vmwarebase code does not need to be patched on OS X or ESXi so you will see a
message on those systems telling you that it will not be patched.

In all cases make sure VMware is not running, and any background guests have
been shutdown.

The code is now Python as it makes the Unlocker easier to run and maintain on ESXi.
There are some challenges to write the code as ESXi has a subset of Python 2.7 which
constrains some modules that can be used.

[u]2. Prerequisites[/u]

The code requires Python 2.7 to work. Most Linux distros, ESXi and OS X ship with a compatible
Python interpreter and should work without requiring any additional software.

Windows has a packaged version of the Python script using PyInstaller, and so does not
require Python to be installed.

[u]3. Limitations[/u]

If you are using VMware Player or Workstation on Windows you may get a core dump.

Latest Linux and ESXi products are OK and do not show this problem.

[color=#ff0000][u][b] IMPORTANT:[/b][/u]

 If you create a new VM using version 11 hardware VMware will stop and 
 create a core dump.There are two options to work around this issue:

 1. Change the VM to be HW 10 - this does not affect performance.
 2. Edit the VMX file and add: [/color]
 
[code=auto:0] smc.version = "0" |[/code]
 

To remove the check for server versions for OS X Leopard and Snow Leopard
(10.5 and 10.6) you must use a replacement EFI firwmare module from the firmware
folder.

If you are using a 32-bit installation of OS X:

1. Copy efi32-srvr.rom to guest folder.
2. Edit the vmx file and add:
 
[code=auto:0]efi32.filename = "efi32-srvr.rom"[/code]
 
If you are using a 64-bit installation of OS X:

1. Copy efi64-srvr.rom to guest folder.
2. Edit the vmx file and add:
 
[code=auto:0]efi64.filename = "efi64-srvr.rom"[/code]
 
[u]4. Windows[/u]

On Windows you will need to either run cmd.exe as Administrator or using
Explorer right click on the command file and select "Run as administrator".

win-install.cmd - patches VMware
win-uninstall.cmd - restores VMware

[u]5. Linux[/u]

On Linux you will need to be either root or use sudo to run the scripts.

You may need to ensure the Linux scripts have execute permissions
by running chmod +x against the 2 files.

lnx-install.sh - patches VMware
lnx-uninstall.sh - restores VMware

[u]6. Mac OS X[/u]

On Mac OS X you will need to be either root or use sudo to run the scripts.
This is really only needed if you want to use client versions of Mac OS X.

You may need to ensure the OS X scripts have execute permissions
by running chmod +x against the 2 files.

osx-install.sh - patches VMware
osx-uninstall.sh - restores VMware

[u]7. ESXi[/u]

You will need to transfer the zip file to the ESXi host either using vSphere client or SCP.

Once uploaded you will need to either use the ESXi support console or use SSH to
run the commands. Use the unzip command to extract the files.

[color=#ff0000][b]<<< WARNING: use a datastore volume to run the scripts >>>[/b][/color]

Please note that you will need to reboot the host for the patches to become active.
The patcher is embbedded in a shell script local.sh which is run at boot from /etc/rc.local.d.

You may need to ensure the ESXi scripts have execute permissions
by running chmod +x against the 2 files.

esxi-install.sh - patches VMware
esxi-uninstall.sh - restores VMware

Note:
1. Any changes you have made to local.sh will be lost. If you have made changes to
that file, you will need to merge them into the supplied local.sh file.
2. The unlocker runs at boot time to patch the relevant files and it now survives
an upgrade or patch to ESXi as local.sh is part of the persisted local state.

[u]8. Thanks[/u]

Thanks to Zenith432 for originally building the C++ unlocker and Mac Son of Knife
(MSoK) for all the testing and support.

Thanks also to Sam B for finding the solution for ESXi 6 and helping me with
debugging expertise. Sam also wrote the code for patching ESXi ELF files.


[u]History[/u]

12/12/14 2.0.0
[LIST]
[*]First release[/*]
[/LIST]
13/13/14 2.0.1
[LIST]
[*]Removed need for Python for Windows[/*]
[/LIST]
13/13/14 2.0.2
[LIST]
[*]darwin.iso was missing from zip file[/*]
[/LIST]
02/01/15 2.0.3
[LIST]
[*]Added EFI firmware files to remove Server check[/*]
[*]Refactored Python code[/*]
[/LIST]
07/01/15 2.0.4
[LIST]
[*]Added View USB Service to Windows batch files[/*]
[*]Fixed broken GOS Table patching on Linux[/*]
[/LIST]
18/06/15 2.0.5
[LIST]
[*]ESXi 6 working[/*]
[*]Latest tools from Fusion 7.1.2[/*]
[/LIST]
20/06/15 2.0.6
[LIST]
[*]ESXi 6 patch for smcPresent vCenter compatibility[/*]
[/LIST]
16/09/15 2.0.7
[LIST]
[*]Workstation 12 on Linux fixes[/*]
[/LIST]
[/LIST]
16/09/15 2.0.8
[LIST]
[*]Player 12 on Linux fixes[/*]
[/LIST]
(c) 2011-2015 Dave Parsons