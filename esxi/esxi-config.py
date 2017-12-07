#!/usr/bin/env python
"""
This is a simple method to modify the hostd XML file
Not using XML on ESXi Python as it does not preserve
formatting or comments.

(This could be sed but cannot find a suitable regex.)

"""
from __future__ import print_function
import sys


def testline(line, test):
    sline = line.lstrip()
    if sline == test:
        return True
    else:
        return False


def main():
    vmsvc = '<vmsvc>\n'
    sandbox = '<useVmxSandbox>false</useVmxSandbox>\n'

    with open('/etc/vmware/hostd/config.xml', 'r+') as f:
        data = f.readlines()

        # Search for the relevant XML tags
        i = 0
        vmsvcindex = 0
        sandboxindex = 0
        for line in data:

            if testline(line, vmsvc):
                vmsvcindex = i

            if testline(line, sandbox):
                sandboxindex = i

            # print(line, end='')
            i += 1

        # Simple toggle on or off depending if found
        if sandboxindex != 0 and sys.argv[1] == 'off':
            print('Removing useVmxSandbox')
            del data[sandboxindex]
        elif sandboxindex == 0 and sys.argv[1] == 'on':
            print('Adding useVmxSandbox')
            pad = len(data[vmsvcindex + 1]) - len(data[vmsvcindex + 1].lstrip())
            data.insert(vmsvcindex + 1, (" " * pad) + sandbox)
        else:
            pass

        # Rewrite the config.xml file
        f.seek(0)
        f.write(''.join(data))
        f.truncate()
        f.close()


if __name__ == '__main__':
    main()
