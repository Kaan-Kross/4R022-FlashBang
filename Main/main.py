#!/usr/bin/env python3
"""
4R022 FlashBang
Kaan Kross / 4R022

Uygulama giriş noktası. Windows, macOS ve Linux üzerinde çalışır.

Application entry point. Runs on Windows, macOS, and Linux.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Proje kökünü import yoluna ekle (core/ ve ui/ paketleri bu dosyanın
# bir üst dizininde yer alır). PyInstaller ile paketlendiğinde de
# çalışmaya devam eder çünkü _MEIPASS zaten sys.path içindedir.
#
# Add the project root to the import path (the core/ and ui/ packages
# live one directory above this file). This keeps working when bundled
# with PyInstaller since _MEIPASS is already on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from core.config_manager import ConfigManager
from core.resources import ICON_IMAGE
from core.version import APP_AUTHOR, APP_DISPLAY_NAME, __version__
from ui.main_window import MainWindow


def main() -> int:
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_DISPLAY_NAME)
    app.setApplicationVersion(__version__)
    app.setOrganizationName(APP_AUTHOR)
    app.setWindowIcon(QIcon(ICON_IMAGE))
    app.setQuitOnLastWindowClosed(True)

    config = ConfigManager()
    window = MainWindow(config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
