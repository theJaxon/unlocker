from __future__ import print_function

import shutil
import dumpsmc
import unlocker


def main():
    # Test Windows patching
    shutil.copyfile('./samples/windows/wks12/vmware-vmx.exe', './tests/windows/wks12/vmware-vmx.exe')
    unlocker.patchsmc('./tests/windows/wks12/vmware-vmx.exe', False)
    dumpsmc.dumpsmc('./tests/windows/wks12/vmware-vmx.exe')
    unlocker.patchbase('./tests/windows/wks12/vmware-vmx.exe')
    shutil.copyfile('./samples/windows/wks14/vmware-vmx.exe', './tests/windows/wks12/vmware-vmx.exe')
    dumpsmc.dumpsmc('./tests/windows/wks14/vmware-vmx.exe')
    unlocker.patchsmc('./tests/windows/wks14/vmware-vmx.exe', False)
    unlocker.patchbase('./tests/windows/wks14/vmware-vmx.exe')
    shutil.copyfile('./samples/windows/wks12/vmwarebase.dll', './tests/windows/wks12/vmwarebase.dll')
    unlocker.patchbase('./tests/windows/wks12/vmwarebase.dll')
    shutil.copyfile('./samples/windows/wks14/vmwarebase.dll', './tests/windows/wks14/vmwarebase.dll')
    unlocker.patchbase('./tests/windows/wks14/vmwarebase.dll')

    # Test Linux patching
    shutil.copyfile('./samples/linux/wks12/vmware-vmx', './tests/linux/wks12/vmware-vmx')
    dumpsmc.dumpsmc('./tests/linux/wks12/vmware-vmx')
    unlocker.patchsmc('./tests/linux/wks12/vmware-vmx', True)
    unlocker.patchbase('./tests/linux/wks12/vmware-vmx')
    shutil.copyfile('./samples/linux/wks14/vmware-vmx', './tests/linux/wks14/vmware-vmx')
    dumpsmc.dumpsmc('./tests/linux/wks14/vmware-vmx')
    unlocker.patchsmc('./tests/linux/wks14/vmware-vmx', True)
    unlocker.patchbase('./tests/linux/wks14/vmware-vmx')
    shutil.copyfile('./samples/linux/wks12/libvmwarebase.so', './tests/linux/wks12/libvmwarebase.so')
    unlocker.patchbase('./tests/linux/wks12/libvmwarebase.so')
    shutil.copyfile('./samples/linux/wks14/libvmwarebase.so', './tests/linux/wks14/libvmwarebase.so')
    unlocker.patchbase('./tests/linux/wks14/libvmwarebase.so')

    # Test macOS patching
    shutil.copyfile('./samples/macos/fus8/vmware-vmx', './tests/macos/fus8/vmware-vmx')
    unlocker.patchsmc('./tests/macos/fus8/vmware-vmx', False)
    shutil.copyfile('./samples/macos/fus10/vmware-vmx', './tests/macos/fus10/vmware-vmx')
    unlocker.patchsmc('./tests/macos/fus10/vmware-vmx', False)

    # Test ESXi patching
    shutil.copyfile('./samples/esxi/esxi600/vmx', './tests/esxi/esxi600/vmx')
    dumpsmc.dumpsmc('./tests/esxi/esxi600/vmx')
    unlocker.patchsmc('./tests/esxi/esxi600/vmx', True)
    unlocker.patchbase('./tests/esxi/esxi600/vmx')
    shutil.copyfile('./samples/esxi/esxi650/vmx', './tests/esxi/esxi650/vmx')
    dumpsmc.dumpsmc('./tests/esxi/esxi650/vmx')
    unlocker.patchsmc('./tests/esxi/esxi650/vmx', True)
    unlocker.patchbase('./tests/esxi/esxi650/vmx')
    shutil.copyfile('./samples/esxi/esxi600/libvmkctl.so', './tests/esxi/esxi600/libvmkctl.so')
    unlocker.patchvmkctl('./tests/esxi/esxi600/libvmkctl.so')
    shutil.copyfile('./samples/esxi/esxi650/lib/libvmkctl.so', './tests/esxi/esxi650/lib/libvmkctl.so')
    unlocker.patchvmkctl('./tests/esxi/esxi650/lib/libvmkctl.so')
    shutil.copyfile('./samples/esxi/esxi650/lib64/libvmkctl.so', './tests/esxi/esxi650/lib64/libvmkctl.so')
    unlocker.patchvmkctl('./tests/esxi/esxi650/lib64/libvmkctl.so')
    shutil.copyfile('./samples/esxi/esxi650/config.xml', './tests/esxi/esxi650/config.xml')


if __name__ == '__main__':
    main()
