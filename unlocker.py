"""
The MIT License (MIT)

Copyright (c) 2014 Dave Parsons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

vSMC Header Structure
Offset  Length  struct Type Description
----------------------------------------
0x00/00 0x08/08 Q      ptr  Offset to key table
0x08/08 0x04/4  I      int  Number of private keys
0x0C/12 0x04/4  I      int  Number of public keys

vSMC Key Data Structure
Offset  Length  struct Type Description
----------------------------------------
0x00/00 0x04/04 4s     int  Key name (byte reversed e.g. #KEY is YEK#)
0x04/04 0x01/01 B      byte Length of returned data
0x05/05 0x04/04 4s     int  Data type (byte reversed e.g. ui32 is 23iu)
0x09/09 0x01/01 B      byte Flag R/W
0x0A/10 0x06/06 6x     byte Padding
0x10/16 0x08/08 Q      ptr  Internal VMware routine
0x18/24 0x30/48 48B    byte Data
"""

import optparse
import os
import sys
import struct

# Setup imports depending on whether IronPython or CPython
if sys.platform == 'win32' \
        or sys.platform == 'cli':
    from _winreg import *


def rot13(s):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    trans = chars[26:] + chars[:26]
    rot_char = lambda c: trans[chars.find(c)] if chars.find(c) > -1 else c
    return ''.join(rot_char(c) for c in s)


def bytetohex(bytestr):
    return ''.join(['%02X ' % ord(x) for x in bytestr]).strip()


def printkey(i, smc_key, smc_data):
    print str(i).zfill(3)  \
    + ' ' + smc_key[0][::-1] \
    + ' ' + str(smc_key[1]).zfill(2) \
    + ' ' + smc_key[2][::-1].replace('\x00', ' ') \
    + ' ' + '{0:#0{1}x}'.format(smc_key[3],4) \
    + ' ' + hex(smc_key[4]) \
    + ' ' + bytetohex(smc_data)


def patchkeys(f, key):

    # Setup struct pack string
    key_pack = '=4sB4sB6xQ'

    # Do Until OSK1 read
    i = 0
    while True:

        #  Read key into struct str and data byte str
        offset = key + (i * 72)
        f.seek(offset)
        smc_key = struct.unpack(key_pack, f.read(24))
        smc_data = f.read(smc_key[1])

        # Reset pointer to beginning of key entry
        f.seek(offset)

        if smc_key[0] == 'SKL+':
            # Use the +LKS data routine for OSK0/1
            smc_new_memptr = smc_key[4]
            print '+LKS Key: '
            printkey(i, smc_key, smc_data)

        elif smc_key[0] == '0KSO':
            # Write new data routine pointer from +LKS
            print 'OSK0 Key Before:'
            printkey(i, smc_key, smc_data)
            f.seek(offset)
            f.write(struct.pack(key_pack, smc_key[0], smc_key[1], smc_key[2], smc_key[3], smc_new_memptr))
            f.flush()

            # Write new data for key
            f.seek(offset + 24)
            smc_new_data = rot13('bheuneqjbexolgurfrjbeqfthneqrqcy')
            f.write(smc_new_data)
            f.flush()

            # Re-read and print key
            f.seek(offset)
            smc_key = struct.unpack(key_pack, f.read(24))
            smc_data = f.read(smc_key[1])
            print 'OSK0 Key After:'
            printkey(i, smc_key, smc_data)

        elif smc_key[0] == '1KSO':
            # Write new data routine pointer from +LKS
            print 'OSK1 Key Before:'
            printkey(i, smc_key, smc_data)
            f.seek(offset)
            f.write(struct.pack(key_pack, smc_key[0], smc_key[1], smc_key[2], smc_key[3], smc_new_memptr))
            f.flush()

            # Write new data for key
            f.seek(offset + 24)
            smc_new_data = rot13('rnfrqbagfgrny(p)NccyrPbzchgreVap')
            f.write(smc_new_data)
            f.flush()

            # Re-read and print key
            f.seek(offset)
            smc_key = struct.unpack(key_pack, f.read(24))
            smc_data = f.read(smc_key[1])
            print 'OSK1 Key After:'
            printkey(i, smc_key, smc_data)

            # Finished so get out of loop
            break

        else:
            pass

        i += 1


def patchsmc(name):

    with open(name, 'r+b') as f:

        # Read file into string variable
        vmx = f.read()

        print 'File: ' + name

        # Setup hex string for vSMC headers
        # These are the private and public key counts
        smc_header_v0 = '\xF2\x00\x00\x00\xF0\x00\x00\x00'
        smc_header_v1 = '\xB4\x01\x00\x00\xB0\x01\x00\x00'

        # Setup hex string for #KEY key
        key_key = '\x59\x45\x4B\x23\x04\x32\x33\x69\x75'

        # Setup hex string for $Adr key
        adr_key = '\x72\x64\x41\x24\x04\x32\x33\x69\x75'

        # Find the vSMC headers
        smc_header_v0_offset = vmx.find(smc_header_v0) - 8
        smc_header_v1_offset = vmx.find(smc_header_v1) - 8

        # Find '#KEY' keys
        smc_key0 = vmx.find(key_key)
        smc_key1 = vmx.rfind(key_key)

        # Find '$Adr' key only V1 table
        smc_adr = vmx.find(adr_key)

        # Read the vSMC version 0 header
        f.seek(smc_header_v0_offset)
        appleSMCTableV0 = struct.unpack('=QII', f.read(16))

        # Read the vSMC version 1 header
        f.seek(smc_header_v1_offset)
        appleSMCTableV1 = struct.unpack('=QII', f.read(16))

        # Print vSMC0 tables and keys
        print 'appleSMCTableV0 (smc.version = "0")'
        print 'appleSMCTableV0 Address      : ' + hex(smc_header_v0_offset)
        print 'appleSMCTableV0 Private Key #: 0xF2'
        print 'appleSMCTableV0 Public Key  #: 0xF0'

        if (smc_adr - smc_key0) != 72:
            print 'appleSMCTableV0 Table        : ' + hex(smc_key0)
            patchkeys(f, smc_key0)
        elif (smc_adr - smc_key1) != 72:
            print 'appleSMCTableV0 Table        : ' + hex(smc_key1)
            patchkeys(f, smc_key1)
        else:
            print 'appleSMCTableV0 Error        : ' \
                  + hex((appleSMCTableV0[0] - data_offset) - smc_key0) + ' ' \
                  + hex((appleSMCTableV0[0] - data_offset) - smc_key1)

        print

        # Print vSMC1 tables and keys
        print 'appleSMCTableV1 (smc.version = "1")'
        print 'appleSMCTableV1 Address      : ' + hex(smc_header_v1_offset)
        print 'appleSMCTableV1 Private Key #: 0x01B0'
        print 'appleSMCTableV1 Public Key  #: 0x01B4'

        if (smc_adr - smc_key0) == 72:
            print 'appleSMCTableV1 Table        : ' + hex(smc_key0)
            patchkeys(f, smc_key0)
        elif (smc_adr - smc_key1) == 72:
            print 'appleSMCTableV1 Table        : ' + hex(smc_key1)
            patchkeys(f, smc_key1)
        else:
            print 'appleSMCTableV1 Error        : ' \
                  + hex((appleSMCTableV1[0] - data_offset) - smc_key0) + ' ' \
                  + hex((appleSMCTableV1[0] - data_offset) - smc_key1)

        print

        # Tidy up
        f.flush()
        f.close()

def patchbase(name):

    # Patch file
    print 'GOS Patching: ' + name
    f = open(name, 'r+b')

    # Entry to search for in GOS table
    darwin = (
        '\x10\x00\x00\x00\x10\x00\x00\x00'
        '\x02\x00\x00\x00\x00\x00\x00\x00'
        '\x00\x00\x00\x00\x00\x00\x00\x00'
        '\x00\x00\x00\x00\x00\x00\x00\x00'
        '\xBE'
    )

    # Read file into string variable
    base = f.read()

    # Loop thorugh each entry and set top bit
    # 0xBE --> 0xBF
    offset = 0
    while offset < len(base):
        offset = base.find(darwin, offset)
        if offset == -1:
            break
        f.seek(offset + 32)
        flag = f.read(1)
        if flag == '\xBE':
            f.seek(offset + 32)
            f.write('\xBF')
            print 'GOS Patched flag @: ' + hex(offset)
        else:
            print 'GOS Unknown flag @: ' + hex(offset) + '/' + hex(flag)

        offset += 33

    # # Tidy up
    f.flush()
    f.close()
    print 'GOS Patched: ' + name


def main():

    # Work around absent Platform module on VMkernel
    if os.name == 'nt' or os.name == 'cli':
        osname = 'windows'
    else:
        osname = os.uname()[0].lower()

    # Setup default paths
    if osname == 'darwin':
        vmx_path = '/Applications/VMware Fusion.app/Contents/Library/'
        vmx = vmx_path + 'vmware-vmx'
        vmx_debug = vmx_path + 'vmware-vmx-debug'
        vmx_stats = vmx_path + 'vmware-vmx-stats'
        vmwarebase = ''

    elif osname == 'linux':
        vmx_path = '/usr/lib/vmware/bin/'
        vmx = vmx_path + 'vmware-vmx'
        vmx_debug = vmx_path + 'vmware-vmx-debug'
        vmx_stats = vmx_path + 'vmware-vmx-stats'
        vmwarebase = '/usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0'

    elif osname == 'vmkernel':
        vmx_path = '/unlocker/'
        vmx = vmx_path + 'vmx'
        vmx_debug = vmx_path + 'vmx-debug'
        vmx_stats = vmx_path + 'vmx-stats'
        vmwarebase = ''

    elif osname == 'windows':
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, r'SOFTWARE\Wow6432Node\VMware, Inc.\VMware Workstation')
        vmwarebase_path = QueryValueEx(key, 'InstallPath')[0]
        vmx_path = QueryValueEx(key, 'InstallPath64')[0]
        vmx = vmx_path + 'vmware-vmx.exe'
        vmx_debug = vmx_path + 'vmware-vmx-debug.exe'
        vmx_stats = vmx_path + 'vmware-vmx-stats.exe'
        vmwarebase = vmwarebase_path + 'vmwarebase.dll'

    else:
        print('Unknown Operating System: ' + osname)
        return

    #  Patch the vmx executables skipping stats version for Player
    patchsmc(vmx)
    patchsmc(vmx_debug)
    try:
        patchsmc(vmx_stats)
    except IOError:
        pass

    # Patch vmwarebase for Workstation and Player
    # Not required on Fusion or ESXi as table already has correct flags
    if vmwarebase != '':
        patchbase(vmwarebase)
    else:
        print 'Patching vmwarebase is not required on this system'


if __name__ == '__main__':
    main()
