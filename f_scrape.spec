# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['f_scrape.py'],
             pathex=['C:\\Users\\kulka'],
             binaries=[],
             datas=[("C:\\Users\\kulka\\anaconda3\\Lib\\site-packages\\branca\\*.json","branca"),
         ("C:\\Users\\kulka\\anaconda3\\Lib\\site-packages\\branca\\templates","templates"),
         ("C:\\Users\\kulka\\anaconda3\\Lib\\site-packages\\folium\\templates","templates"),],
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
          name='f_scrape',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
