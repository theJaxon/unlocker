# -*- mode: python -*-
a = Analysis(['D:\\vmware\\unlocker\\dumpsmc.py'],
             pathex=['D:\\PyInstaller-2.1\\dumpsmc'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dumpsmc.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
