# -*- mode: python -*-
a = Analysis(['D:\\vmware\\unlocker\\unlocker.py'],
             pathex=['D:\\PyInstaller-2.1\\unlocker'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='unlocker.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
