"""
The MIT License (MIT)

Copyright (c) 2014-2015 Dave Parsons & Sam Bingner

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

import os
import sys
import struct
import subprocess

if sys.version_info < (2, 7):
    sys.stderr.write('You need Python 2.7 or later\n')
    sys.exit(1)

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


def printkey(i, offset, smc_key, smc_data):
    print str(i + 1).zfill(3) \
          + ' ' + hex(offset) \
          + ' ' + smc_key[0][::-1] \
          + ' ' + str(smc_key[1]).zfill(2) \
          + ' ' + smc_key[2][::-1].replace('\x00', ' ') \
          + ' ' + '{0:#0{1}x}'.format(smc_key[3], 4) \
          + ' ' + hex(smc_key[4]) \
          + ' ' + bytetohex(smc_data)


E_CLASS64 = 2
E_SHT_RELA = 4


def patchELF(f, oldOffset, newOffset):
    f.seek(0)
    magic = f.read(4)
    if not magic == b'\x7fELF':
        raise Exception('Magic number does not match')

    ei_class = struct.unpack('=B', f.read(1))[0]
    if ei_class != E_CLASS64:
        raise Exception('Not 64bit elf header: ' + ei_class)

    f.seek(40)
    e_shoff = struct.unpack('=Q', f.read(8))[0]
    f.seek(58)
    e_shentsize = struct.unpack('=H', f.read(2))[0]
    e_shnum = struct.unpack('=H', f.read(2))[0]
    e_shstrndx = struct.unpack('=H', f.read(2))[0]

    # print 'e_shoff: 0x{:x} e_shentsize: 0x{:x} e_shnum:0x{:x} e_shstrndx:0x{:x}'.format(e_shoff, e_shentsize, e_shnum, e_shstrndx)

    for i in range(0, e_shnum):
        f.seek(e_shoff + i * e_shentsize)
        e_sh = struct.unpack('=LLQQQQLLQQ', f.read(e_shentsize))
        e_sh_name = e_sh[0]
        e_sh_type = e_sh[1]
        e_sh_offset = e_sh[4]
        e_sh_size = e_sh[5]
        e_sh_entsize = e_sh[9]
        if e_sh_type == E_SHT_RELA:
            e_sh_nument = e_sh_size / e_sh_entsize
            # print 'RELA at 0x{:x} with {:d} entries'.format(e_sh_offset, e_sh_nument)
            for j in range(0, e_sh_nument):
                f.seek(e_sh_offset + e_sh_entsize * j)
                rela = struct.unpack('=QQq', f.read(e_sh_entsize))
                r_offset = rela[0]
                r_info = rela[1]
                r_addend = rela[2]
                if r_addend == oldOffset:
                    r_addend = newOffset
                    f.seek(e_sh_offset + e_sh_entsize * j)
                    f.write(struct.pack('=QQq', r_offset, r_info, r_addend))
                    print 'Relocation modified at: ' + hex(e_sh_offset + e_sh_entsize * j)


def patchkeys(f, vmx, key, osname):
    # Setup struct pack string
    key_pack = '=4sB4sB6xQ'
    smc_old_memptr = 0
    smc_new_memptr = 0

    # Do Until OSK1 read
    i = 0
    while True:

        # Read key into struct str and data byte str
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
            printkey(i, offset, smc_key, smc_data)

        elif smc_key[0] == '0KSO':
            # Write new data routine pointer from +LKS
            print 'OSK0 Key Before:'
            printkey(i, offset, smc_key, smc_data)
            smc_old_memptr = smc_key[4]
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
            printkey(i, offset, smc_key, smc_data)

        elif smc_key[0] == '1KSO':
            # Write new data routine pointer from +LKS
            print 'OSK1 Key Before:'
            printkey(i, offset, smc_key, smc_data)
            smc_old_memptr = smc_key[4]
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
            printkey(i, offset, smc_key, smc_data)

            # Finished so get out of loop
            break

        else:
            pass

        i += 1
    return smc_old_memptr, smc_new_memptr


def patchsmc(name, osname, sharedobj):
    with open(name, 'r+b') as f:

        smc_old_memptr = 0
        smc_new_memptr = 0

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

        # Print vSMC0 tables and keys
        print 'appleSMCTableV0 (smc.version = "0")'
        print 'appleSMCTableV0 Address      : ' + hex(smc_header_v0_offset)
        print 'appleSMCTableV0 Private Key #: 0xF2/242'
        print 'appleSMCTableV0 Public Key  #: 0xF0/240'

        if (smc_adr - smc_key0) != 72:
            print 'appleSMCTableV0 Table        : ' + hex(smc_key0)
            smc_old_memptr, smc_new_memptr = patchkeys(f, vmx, smc_key0, osname)
        elif (smc_adr - smc_key1) != 72:
            print 'appleSMCTableV0 Table        : ' + hex(smc_key1)
            smc_old_memptr, smc_new_memptr = patchkeys(f, vmx, smc_key1, osname)

        print

        # Print vSMC1 tables and keys
        print 'appleSMCTableV1 (smc.version = "1")'
        print 'appleSMCTableV1 Address      : ' + hex(smc_header_v1_offset)
        print 'appleSMCTableV1 Private Key #: 0x01B4/436'
        print 'appleSMCTableV1 Public Key  #: 0x01B0/432'

        if (smc_adr - smc_key0) == 72:
            print 'appleSMCTableV1 Table        : ' + hex(smc_key0)
            smc_old_memptr, smc_new_memptr = patchkeys(f, vmx, smc_key0, osname)
        elif (smc_adr - smc_key1) == 72:
            print 'appleSMCTableV1 Table        : ' + hex(smc_key1)
            smc_old_memptr, smc_new_memptr = patchkeys(f, vmx, smc_key1, osname)

        print

        # Find matching RELA record in .rela.dyn in ESXi ELF files
        # This is temporary code until proper ELF parsing written
        if sharedobj:
            print 'Modifying RELA records from: ' + hex(smc_old_memptr) + ' to ' + hex(smc_new_memptr)
            patchELF(f, smc_old_memptr, smc_new_memptr)

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
            print 'GOS Unknown flag @: ' + hex(offset) + '/' + hex(int(flag))

        offset += 33

    # Tidy up
    f.flush()
    f.close()
    print 'GOS Patched: ' + name


def patchvmkctl(name):
    # Patch file
    print 'smcPresent Patching: ' + name
    f = open(name, 'r+b')

    # Read file into string variable
    vmkctl = f.read()
    applesmc = vmkctl.find('applesmc')
    f.seek(applesmc)
    f.write('vmkernel')

    # Tidy up
    f.flush()
    f.close()
    print 'smcPresent Patched: ' + name


def main():
    # Work around absent Platform module on VMkernel
    if os.name == 'nt' or os.name == 'cli':
        osname = 'windows'
    else:
        osname = os.uname()[0].lower()

    vmx_so = False

    # Setup default paths
    if osname == 'darwin':
        vmx_path = '/Applications/VMware Fusion.app/Contents/Library/'
        vmx = vmx_path + 'vmware-vmx'
        vmx_debug = vmx_path + 'vmware-vmx-debug'
        vmx_stats = vmx_path + 'vmware-vmx-stats'
        vmwarebase = ''
        libvmkctl = ''

    elif osname == 'linux':
        vmx_path = '/usr/lib/vmware/bin/'
        vmx = vmx_path + 'vmware-vmx'
        vmx_debug = vmx_path + 'vmware-vmx-debug'
        vmx_stats = vmx_path + 'vmware-vmx-stats'
        vmx_version = subprocess.check_output(["vmplayer", "-v"])
        if vmx_version.startswith('VMware Player 12'):
            vmx_so = True
            vmwarebase = '/usr/lib/vmware/lib/libvmwarebase.so/libvmwarebase.so'
        else:
            vmwarebase = '/usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0'
        libvmkctl = ''

    elif osname == 'vmkernel':
        vmx_path = '/unlocker/'
        vmx = vmx_path + 'vmx'
        vmx_debug = vmx_path + 'vmx-debug'
        vmx_stats = vmx_path + 'vmx-stats'
        vmx_so = True
        vmwarebase = ''
        libvmkctl = vmx_path + 'libvmkctl.so'

    elif osname == 'windows':
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, r'SOFTWARE\Wow6432Node\VMware, Inc.\VMware Workstation')
        vmwarebase_path = QueryValueEx(key, 'InstallPath')[0]
        vmx_path = QueryValueEx(key, 'InstallPath64')[0]
        vmx = vmx_path + 'vmware-vmx.exe'
        vmx_debug = vmx_path + 'vmware-vmx-debug.exe'
        vmx_stats = vmx_path + 'vmware-vmx-stats.exe'
        vmwarebase = vmwarebase_path + 'vmwarebase.dll'
        libvmkctl = ''

    else:
        print('Unknown Operating System: ' + osname)
        return

    # Patch the vmx executables skipping stats version for Player
    patchsmc(vmx, osname, vmx_so)
    patchsmc(vmx_debug, osname, vmx_so)
    try:
        patchsmc(vmx_stats, osname, vmx_so)
    except IOError:
        pass

    # Patch vmwarebase for Workstation and Player
    # Not required on Fusion or ESXi as table already has correct flags
    if vmwarebase != '':
        patchbase(vmwarebase)
    else:
        print 'Patching vmwarebase is not required on this system'

    if osname == 'vmkernel':
        patchvmkctl(libvmkctl)


if __name__ == '__main__':
    main()
