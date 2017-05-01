# -*- mode: python -*-

block_cipher = None
binary_files = Tree(r'C:\Python35\Lib\site-packages\requests', prefix='requests')
binary_files += [('remedy_ie.py', 'remedy_ie.py', 'BINARY')]  # have to include as starts with same name as remedy.py
data_files = [('IEDriverServer.exe', 'IEDriverServer.exe', 'DATA')]
data_files += [('settings.cfg', 'settings.cfg', 'DATA')]

a = Analysis(['remedy.py'],
             pathex=['C:\\simon_files_compilation_zone\\Remedy Call Logging'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          binary_files,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Remedy',
          debug=False,
          strip=False,
          upx=True,
          icon='remedy_icon.ico',
          console=False )
coll = COLLECT(exe,
			data_files,
            upx=True,
			name='remedy')
			