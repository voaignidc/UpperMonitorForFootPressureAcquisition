# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.\\ui', 'D:\\Python\\pyqt\\foot_release'],
             binaries=[],
             datas=[],
             hiddenimports=['ui.adminDataBase', 'ui.serialPort', 'ui.userInput', 'ui.currentTime', 'ui.signIn', 'ui.convert', 'ui.currentTime', 'ui.createTxt','ui.pressureAnalysis'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)
