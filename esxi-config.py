#!/usr/bin/env python
"""
This is a simple method to modify the hostd XML file
Not using XML on ESXi Python as it does not preserve
formatting or comments.

(This could be sed but cannot find a suitable regex.)

"""
from __future__ import print_function


def main():
    vmsvc = '    <vmsvc>\n'
    sandbox = '      <useVmxSandbox>false</useVmxSandbox>\n'

    with open('/etc/vmware/hostd/config.xml', 'r+') as f:
        data = f.readlines()
        i = data.index(vmsvc)
        try:
            j = data.index(sandbox)
        except ValueError:
            j = 0

        # Simple toggle on or off depending if found
        if j == 0:
            data.insert(i+1, sandbox)
        else:
            del data[j]

        # Rewrite the config.xml file
        f.seek(0)
        f.write(''.join(data))
        f.truncate()
        f.close()

if __name__ == '__main__':
    main()
