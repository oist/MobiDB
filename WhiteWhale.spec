# -*- mode: python ; coding: utf-8 -*-
# 追記1, 3-7行目
import sys
import os
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
path = os.path.abspath(".")
block_cipher = None

a = Analysis(['main.py'],
             pathex=[path], # 追記2
             binaries=[],
             datas=[('theme.kv', 'path'), ('loading_bouningen.gif', 'path')], # 追記3
             hiddenimports=['pkg_resources.py2_warn'], # 追記4
             hookspath=[kivymd_hooks_path], # 追記5
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False) # 追記6
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

Key = ['mkl']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, Key)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)], # 追記7
          name='WhiteWhale', # 追記8
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='white.ico') # 追記9
coll = COLLECT(exe, Tree('.'),  # 追記10 以下行すべて
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='WhiteWhale')
