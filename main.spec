# -*- mode: python ; coding: utf-8 -*-

from sys import platform

binaries=[]

if platform == 'win32':
    icon = 'icon.ico'
    binaries.append(('./binary/win', './binary/win'))
    name = 'HLS录制工具'
else:
    icon = 'icon.icns'
    binaries.append(('./binary/darwin', './binary/darwin'))
    name = 'main'

block_cipher = None


a = Analysis(['main.py'],
             pathex=['./'],
             binaries=binaries,
             datas=[
                ('./icon.ico', '.'),
                ('./icon.icns', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=name,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          debug=False,
          console=False,
          icon=icon)
app = BUNDLE(exe,
             name='HLS录制工具.app',
             icon=icon,
             bundle_identifier='me.js2.py_hls_aria2')
