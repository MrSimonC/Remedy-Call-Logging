# -*- mode: python -*-

block_cipher = None
data_files = Tree(r'C:\Python35\Lib\site-packages\requests', prefix='requests')
collect_files = [('IEDriverServer.exe', r'C:\Users\nbf1707\Desktop\IEDriverServer.exe', 'DATA')]
collect_files += [('settings.cfg', 'settings.cfg', 'DATA')]

a = Analysis(['remedy.py'],
             pathex=['C:\\simon files\\compilation zone\\Remedy Call Logging'],
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
          data_files,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Remedy',
          debug=False,
          strip=False,
          upx=True,
          icon='remedy.ico',
          console=True )
coll = COLLECT(exe,
			collect_files,
            upx=True,
			name='remedy')
			