# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\src\\pdf_compress.py'],
             pathex=['C:\\Users\\zhangyi\\PycharmProjects\\compressor\\pdf_build'],
             binaries=[('..\\resource\\gswin64.exe', 'bin'), ('..\\resource\\gswin64c.exe', 'bin'),
                    ('..\\resource\\gsdll64.dll', 'bin'), ('..\\resource\\gsdll64.lib', 'bin')],
             datas=[],
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
          name='pdf_compress',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='..\\resource\\bear.ico')
