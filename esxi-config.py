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
    starttag = '<useVmxSandbox>'
    endtag = '</useVmxSandbox>'

    # with open('/etc/vmware/hostd/config.xml', 'r+') as f:
    with open('samples/config.xml', 'r+') as f:
        data = f.readlines()

        # Search for the relevant XML tags
        i = 0
        vmsvcindex = 0
        sandboxindex = 0
        for line in data:

            if testline(line, vmsvc):
                vmsvcindex = i

            if testline(line, starttag):
                sandboxindex = i

            # print(line, end='')
            i += 1

        # If vmsvc tag not found then file is probably corrupt
        if vmsvcindex is None:
            print('ESXi Config - config.xml is corrupt')
            return False

        # Remove the existing line if prsent
        del data[sandboxindex]

        # Now add line with correct flag
        pad = len(data[vmsvcindex + 1]) - len(data[vmsvcindex + 1].lstrip())

        if sys.argv[1] in ['on', 'off']:
            pass

        if sys.argv[1] == 'off':
            print('ESXi Config - useVmxSandbox off')
            data.insert(vmsvcindex + 1, (" " * pad) + sandboxoff)

        elif sys.argv[1] == 'on':
            print('ESXi Config - useVmxSandbox on')
            data.insert(vmsvcindex + 1, (" " * pad) + sandboxon)

        else:
            print('ESXi Config - Incorrect paramter passed')
            return False

        # Rewrite the config.xml file
        f.seek(0)
        f.write(''.join(data))
        f.truncate()
        f.close()
        return True


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.exit(1)
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
