# -*- mode: python ; coding: utf-8 -*-
"""
4R022 FlashBang - PyInstaller Spec Dosyası
Kaan Kross / 4R022

Tek bir spec dosyasıyla Windows, macOS ve Linux için tek-dosya (onefile)
yürütülebilir üretir. Platforma göre doğru ikon otomatik seçilir.

A single spec file producing a onefile executable for Windows, macOS, and
Linux. The correct icon is chosen automatically based on the platform.

Kullanım / Usage (proje kökünden / from the project root):
    pyinstaller Build/4R022_FlashBang.spec --noconfirm
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(SPECPATH).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.version import APP_DISPLAY_NAME, __version__  # noqa: E402

block_cipher = None

datas = [
    (str(PROJECT_ROOT / "assets" / "images"), "assets/images"),
    (str(PROJECT_ROOT / "assets" / "sounds"), "assets/sounds"),
]

if sys.platform.startswith("win"):
    icon_path = str(PROJECT_ROOT / "assets" / "images" / "icon.ico")
elif sys.platform == "darwin":
    icon_path = str(PROJECT_ROOT / "assets" / "images" / "icon.icns")
else:
    icon_path = str(PROJECT_ROOT / "assets" / "images" / "icon.png")

a = Analysis(
    [str(PROJECT_ROOT / "Main" / "main.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "PyQt6.QtMultimedia",
        "PyQt6.QtMultimediaWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_DISPLAY_NAME.replace(" ", ""),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name=f"{APP_DISPLAY_NAME}.app",
        icon=icon_path,
        bundle_identifier="com.4r022.flashbang",
        info_plist={
            "CFBundleName": APP_DISPLAY_NAME,
            "CFBundleDisplayName": APP_DISPLAY_NAME,
            "CFBundleShortVersionString": __version__,
            "NSHighResolutionCapable": True,
            "LSUIElement": False,
        },
    )
