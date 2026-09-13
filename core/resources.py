"""
4R022 FlashBang - Kaynak Yolu Yardımcısı
Kaan Kross / 4R022

PyInstaller ile tek dosya (--onefile) paketlendiğinde varlıklar geçici
bir dizine (_MEIPASS) çıkarılır. Bu modül, geliştirme ortamında ve
paketlenmiş halde aynı şekilde çalışan yol çözümlemesi sağlar.

When bundled with PyInstaller (--onefile), assets are extracted to a
temporary directory (_MEIPASS). This module resolves paths correctly
both in development and in the packaged executable.
"""

from __future__ import annotations

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """Geliştirme ve PyInstaller ortamlarında doğru mutlak yolu döndürür."""
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path is None:
        # core/ dizininden proje köküne çık
        base_path = Path(__file__).resolve().parent.parent
    else:
        base_path = Path(base_path)
    return str(base_path / relative_path)


ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"

FLASHBANG_IMAGE = resource_path(f"{IMAGES_DIR}/flashbang.jpeg")
LOGO_IMAGE = resource_path(f"{IMAGES_DIR}/logo.png")
ICON_IMAGE = resource_path(f"{IMAGES_DIR}/icon.png")
ICON_ICO = resource_path(f"{IMAGES_DIR}/icon.ico")
ICON_ICNS = resource_path(f"{IMAGES_DIR}/icon.icns")

THROW_SOUND = resource_path(f"{SOUNDS_DIR}/throw.mp3")

# Patlama sesi havuzu (şans/rarity sistemi) artık core/sound_pool.py içinde.
# The explosion sound pool (rarity/loot system) now lives in core/sound_pool.py.
