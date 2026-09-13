"""
4R022 FlashBang - Hakkımızda Penceresi
Kaan Kross / 4R022

Çerçevesiz, marka logosunu ön plana çıkaran "Hakkımızda" diyaloğu.
Sürüm numarası, geliştirici bilgisi ve uygulama/şans sistemi hakkında
kısa bir açıklama gösterir. Kapatma yalnızca başlık çubuğundaki tek
"×" butonuyla yapılır (önceki sürümde yanlışlıkla hem başlıkta hem
altta iki ayrı kapatma butonu vardı — bu, ikincisi kaldırılarak
düzeltildi).

Frameless "About" dialog that prominently features the brand logo.
Shows the version number, developer credit, and a short description of
the app and its luck/rarity system. Closing is done via the single "×"
button in the title bar only (a previous version mistakenly had two
separate close buttons — one in the title bar and one at the bottom —
this was fixed by removing the latter).
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.i18n import t
from core.resources import LOGO_IMAGE
from core.theme import build_dialog_stylesheet, get_theme_colors
from core.version import APP_AUTHOR, APP_DISPLAY_NAME, __version__

LOGO_DISPLAY_SIZE = 88
LOGO_FRAME_SIZE = 108


class AboutDialog(QDialog):
    """Marka logosu, sürüm ve geliştirici bilgisini gösteren çerçevesiz diyalog."""

    def __init__(self, language: str, theme: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setFixedSize(380, 460)
        self.setObjectName("SettingsRoot")

        self._drag_pos: Optional[QPoint] = None
        self._lang = language
        self._theme = theme

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---------------------------------------------------------- title bar
        title_bar = QWidget()
        title_bar.setObjectName("DialogTitleBar")
        title_bar.setFixedHeight(34)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(14, 0, 8, 0)

        title_label = QLabel(t("about_title", self._lang))
        title_label.setObjectName("SettingsTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)

        # Tek kapatma butonu — bilerek yalnızca burada. Aşağıda ikinci bir
        # "Kapat" butonu YOK (bkz. modül docstring'i).
        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        title_layout.addWidget(close_btn)

        title_bar.mousePressEvent = self._title_mouse_press
        title_bar.mouseMoveEvent = self._title_mouse_move

        outer.addWidget(title_bar)

        # -------------------------------------------------------------- body
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(26, 22, 26, 22)
        body_layout.setSpacing(4)

        logo_frame = QFrame()
        logo_frame.setObjectName("LogoFrame")
        logo_frame.setFixedSize(LOGO_FRAME_SIZE, LOGO_FRAME_SIZE)
        logo_frame_layout = QVBoxLayout(logo_frame)
        logo_frame_layout.setContentsMargins(0, 0, 0, 0)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(LOGO_IMAGE)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                LOGO_DISPLAY_SIZE,
                LOGO_DISPLAY_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        logo_label.setPixmap(pixmap)
        logo_frame_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        body_layout.addWidget(logo_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        body_layout.addSpacing(12)

        name_label = QLabel(APP_DISPLAY_NAME)
        name_label.setObjectName("TitleLabel")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body_layout.addWidget(name_label)

        version_badge = QLabel(f"{t('about_version_label', self._lang)} {__version__}")
        version_badge.setObjectName("VersionBadge")
        version_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body_layout.addWidget(version_badge, alignment=Qt.AlignmentFlag.AlignCenter)

        body_layout.addSpacing(8)

        developer_row = QLabel(f"{t('about_developer_label', self._lang)}: {APP_AUTHOR}")
        developer_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        developer_row.setObjectName("HintLabel")
        body_layout.addWidget(developer_row)

        body_layout.addSpacing(14)

        description_label = QLabel(t("about_description", self._lang))
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        body_layout.addWidget(description_label)

        body_layout.addStretch(1)

        outer.addWidget(body)

        self.setStyleSheet(build_dialog_stylesheet(theme) + self._extra_stylesheet())

    def _extra_stylesheet(self) -> str:
        c = get_theme_colors(self._theme)
        return f"""
        QFrame#LogoFrame {{
            background-color: {c['card']};
            border: 2px solid {c['gold']};
            border-radius: {LOGO_FRAME_SIZE // 2}px;
        }}
        QLabel#VersionBadge {{
            color: {c['gold']};
            background-color: {c['card']};
            border: 1px solid {c['gold']};
            border-radius: 9px;
            padding: 2px 10px;
            font-size: 11px;
            font-weight: 700;
        }}
        """

    def _title_mouse_press(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _title_mouse_move(self, event: QMouseEvent) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
