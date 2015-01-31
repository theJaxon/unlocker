import os
import shutil
import sys
import subprocess
import hashlib

print sys.path[0]

shutil.rmtree(sys.path[0] + '/backup', True)
os.mkdir(sys.path[0] + '/backup')

hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()

shutil.copy2('/Applications/VMware Fusion.app/Contents/Library/vmware-vmx', './backup/')
shutil.copy2('/Applications/VMware Fusion.app/Contents/Library/vmware-vmx-debug', './backup/')
shutil.copy2('/Applications/VMware Fusion.app/Contents/Library/vmware-vmx-stats', './backup/')

res = subprocess.check_output(['/Applications/VMware Fusion.app/Contents/Library/vmrun', 'list'],
                              stderr=subprocess.STDOUT)

if res == 'Total running VMs: 0\n':
    print 'OK'
else:
    print 'Fail'

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')
