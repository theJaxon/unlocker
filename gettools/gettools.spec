# -*- mode: python -*-
a = Analysis(['D:\\vmware\\unlocker\\gettools.py'],
             pathex=['D:\\PyInstaller-2.1\\gettools'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gettools.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
