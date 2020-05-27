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
             pathex=[
                '/Users/lock/Desktop/py_gui_hls_aria2',
                '/Users/lock/Desktop/py_gui_hls_aria2/venv/lib/python3.7/site-packages',
             ],
             binaries=binaries,
             datas=[
                ('./icon.ico', '.'),
                ('./icon.icns', '.'),
             ],
             hiddenimports=[
                'pkg_resources.py2_warn',
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                'FixTK',
                'tcl',
                'tk',
                ],
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
             bundle_identifier='com.github.gzlock.py_gui_hls_aria2')
