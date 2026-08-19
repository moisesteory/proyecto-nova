# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

packages = ['demucs_infer', 'torch', 'soundfile', 'numpy']
datas, binaries, hiddenimports = [], [], []
for package in packages:
    try:
        d, b, h = collect_all(package)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

hiddenimports += ['demucs_infer', 'demucs_infer.pretrained', 'demucs_infer.apply', 'demucs_infer.audio']


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SeparadorMusica',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
