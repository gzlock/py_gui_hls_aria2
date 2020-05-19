# -*- mode: python ; coding: utf-8 -*-

from sys import platform

binaries=[]

if platform == 'win32':
    path = 'Z:\\'
    icon = 'icon.ico'
    binaries.append(('./binary/win', './binary/win'))
else:
    path = '/Users/lock/Desktop/python_hls_aria2'
    icon = 'icon.icns'
    binaries.append(('./binary/darwin', './binary/darwin'))

block_cipher = None


a = Analysis(['main.py'],
             pathex=[path],
             binaries=binaries,
             datas=[
                ('icon.ico', '.'),
                ('icon.icns', '.'),
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
          [],
          exclude_binaries=True,
          name='main',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
app = BUNDLE(coll,
             name='main.app',
             icon='icon.icns',
             bundle_identifier='com.gzlock.hls_recorder')
