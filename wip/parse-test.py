#!/usr/bin/env python
from __future__ import print_function
import sys
import xml.etree.ElementTree as ET


def main():
    dom = ET.ElementTree(file='./samples/config.xml')

    vmsvcpath = './/plugins//vmsvc'
    sandboxpath = './/plugins//vmsvc//useVmxSandbox'

    vmsvc = ET.ElementTree.find(dom, vmsvcpath)
    sandbox = ET.ElementTree.find(dom, sandboxpath)

    if vmsvc is None:
        print('ESXi Config - config.xml is corrupt')
        return False
    else:
        if sandbox is None:
            sandbox = ET.Element('useVmxSandbox')
            sandbox.text = 'false'
            vmsvc.append(sandbox)

        sandbox = ET.ElementTree.find(dom, sandboxpath)
        if sys.argv[1] == 'off':
            sandbox.text = 'false'
        elif sys.argv[1] == 'on':
            sandbox.text = 'true'
        else:
            print('ESXi Config - Error no or incorrect paramter passed')
            return False

        dom.write('./samples/output.xml')
        return True


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.exit(1)
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
