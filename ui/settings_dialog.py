"""
4R022 FlashBang - Ayarlar Penceresi
Kaan Kross / 4R022

Çerçevesiz (native olmayan) ayarlar penceresi: tema seçimi, patlama
süresi, dil ayarı (Türkçe / English / Polski / Русский), Şans Butonu
(meme seslerinin çıkma ihtimalini 1 dakikalığına artırır) ve başlık
çubuğundaki "ℹ" simgesi üzerinden Hakkımızda penceresine erişim.
Ayarlar, her biri simgeli bir başlığa sahip ayrı "kart" panellerinde
gruplanır (Dil & Görünüm / Patlama Süresi / Şans Sistemi) — daha
profesyonel, taranabilir bir görünüm için. Tema ve dil değişiklikleri
pencere içinde anında (kaydetmeden) önizlenir. Sürükle-taşı için özel
başlık alanı ve X kapatma butonu içerir.

Frameless (non-native) settings window: theme selection, flash duration,
language setting (Turkish / English / Polish / Russian), a Luck Button
(temporarily boosts meme-sound odds for 1 minute), and access to the
About dialog via an "ℹ" icon in the title bar. Settings are grouped into
separate "card" panels, each with an icon heading (Language & Appearance
/ Flash Duration / Luck System), for a more professional, scannable
look. Theme and language changes are previewed live inside the dialog
before saving. Includes a custom title area for drag-to-move and an X
close button.
"""

from __future__ import annotations

from typing import Optional, Tuple

from PyQt6.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from core.config_manager import MAX_FLASH_DURATION_MS, MIN_FLASH_DURATION_MS
from core.i18n import LANGUAGE_NATIVE_NAMES, SUPPORTED_LANGUAGES, t
from core.luck_boost import LuckBoost
from core.theme import build_dialog_stylesheet, build_luck_button_stylesheet
from ui.about_dialog import AboutDialog

_COUNTDOWN_REFRESH_MS = 500


def _make_card() -> Tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("SectionCard")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 12, 14, 14)
    layout.setSpacing(8)
    return card, layout


class SettingsDialog(QDialog):
    """Tema, patlama süresi, dil ve şans sistemi ayarlarını yönetmek için
    çerçevesiz diyalog."""

    settings_applied = pyqtSignal(str, int, str)  # theme, flash_duration_ms, language

    def __init__(
        self,
        current_theme: str,
        current_duration_ms: int,
        current_language: str,
        luck_boost: LuckBoost,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setFixedSize(390, 640)
        self.setObjectName("SettingsRoot")

        self._drag_pos: Optional[QPoint] = None
        self._theme = current_theme
        self._lang = current_language
        self._luck_boost = luck_boost
        self._luck_state: Optional[str] = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---------------------------------------------------------- title bar
        title_bar = QWidget()
        title_bar.setObjectName("DialogTitleBar")
        title_bar.setFixedHeight(34)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(14, 0, 8, 0)
        title_layout.setSpacing(6)

        self.title_label = QLabel()
        self.title_label.setObjectName("SettingsTitle")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch(1)

        self.about_icon_btn = QPushButton("ℹ")
        self.about_icon_btn.setObjectName("IconButton")
        self.about_icon_btn.setFixedSize(26, 26)
        self.about_icon_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_icon_btn.clicked.connect(self._open_about)
        title_layout.addWidget(self.about_icon_btn)

        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        title_layout.addWidget(close_btn)

        title_bar.mousePressEvent = self._title_mouse_press
        title_bar.mouseMoveEvent = self._title_mouse_move

        outer.addWidget(title_bar)

        # -------------------------------------------------------------- body
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(18, 16, 18, 18)
        body_layout.setSpacing(14)

        # ----- Kart 1: Dil & Görünüm / Language & Appearance -----
        appearance_card, appearance_layout = _make_card()

        self.language_heading = QLabel()
        self.language_heading.setObjectName("SectionHeading")
        appearance_layout.addWidget(self.language_heading)

        self.language_combo = QComboBox()
        for code in SUPPORTED_LANGUAGES:
            self.language_combo.addItem(LANGUAGE_NATIVE_NAMES[code], code)
        idx = SUPPORTED_LANGUAGES.index(current_language) if current_language in SUPPORTED_LANGUAGES else 0
        self.language_combo.setCurrentIndex(idx)
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        appearance_layout.addWidget(self.language_combo)

        appearance_layout.addSpacing(4)

        self.theme_heading = QLabel()
        self.theme_heading.setObjectName("SectionHeading")
        appearance_layout.addWidget(self.theme_heading)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("", "dark")
        self.theme_combo.addItem("", "light")
        idx = 0 if current_theme == "dark" else 1
        self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        appearance_layout.addWidget(self.theme_combo)

        body_layout.addWidget(appearance_card)

        # ----- Kart 2: Patlama Süresi / Flash Duration -----
        duration_card, duration_layout = _make_card()

        duration_label_row = QHBoxLayout()
        self.duration_heading = QLabel()
        self.duration_heading.setObjectName("SectionHeading")
        self.duration_value_label = QLabel()
        duration_label_row.addWidget(self.duration_heading)
        duration_label_row.addStretch(1)
        duration_label_row.addWidget(self.duration_value_label)
        duration_layout.addLayout(duration_label_row)

        self.duration_slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_slider.setMinimum(MIN_FLASH_DURATION_MS)
        self.duration_slider.setMaximum(MAX_FLASH_DURATION_MS)
        self.duration_slider.setSingleStep(100)
        self.duration_slider.setPageStep(500)
        self.duration_slider.setValue(current_duration_ms)
        self.duration_slider.valueChanged.connect(self._on_duration_changed)
        duration_layout.addWidget(self.duration_slider)

        self.duration_hint = QLabel()
        self.duration_hint.setWordWrap(True)
        self.duration_hint.setObjectName("HintLabel")
        duration_layout.addWidget(self.duration_hint)

        body_layout.addWidget(duration_card)

        # ----- Kart 3: Şans Sistemi / Luck System -----
        luck_card, luck_layout = _make_card()

        self.luck_section_title = QLabel()
        self.luck_section_title.setObjectName("SectionHeading")
        luck_layout.addWidget(self.luck_section_title)

        self.luck_button = QPushButton()
        self.luck_button.setObjectName("LuckButton")
        self.luck_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.luck_button.setFixedHeight(44)
        self.luck_button.clicked.connect(self._on_luck_button_clicked)
        luck_layout.addWidget(self.luck_button)

        self.luck_hint = QLabel()
        self.luck_hint.setWordWrap(True)
        self.luck_hint.setObjectName("HintLabel")
        luck_layout.addWidget(self.luck_hint)

        body_layout.addWidget(luck_card)

        body_layout.addStretch(1)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        self.cancel_btn = QPushButton()
        self.cancel_btn.setObjectName("SecondaryButton")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn = QPushButton()
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self._on_save)
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.save_btn)
        body_layout.addLayout(button_row)

        outer.addWidget(body)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(_COUNTDOWN_REFRESH_MS)
        self._countdown_timer.timeout.connect(self._refresh_luck_button)
        self._countdown_timer.start()
        self.finished.connect(self._countdown_timer.stop)

        self._retranslate()
        self._apply_stylesheet()
        self._refresh_luck_button()

    # -------------------------------------------------------------- helpers

    def _format_duration(self, ms: int) -> str:
        unit = t("duration_unit_suffix", self._lang)
        return f"{ms / 1000:.1f} {unit}"

    def _retranslate(self) -> None:
        self.setWindowTitle(t("settings_title", self._lang))
        self.title_label.setText(t("settings_title", self._lang))
        self.language_heading.setText(f"🌐  {t('language_label', self._lang)}")
        self.theme_heading.setText(f"🎨  {t('theme_label', self._lang)}")
        self.theme_combo.setItemText(0, t("theme_dark", self._lang))
        self.theme_combo.setItemText(1, t("theme_light", self._lang))
        self.duration_heading.setText(f"⏱️  {t('duration_label', self._lang)}")
        self.duration_value_label.setText(self._format_duration(self.duration_slider.value()))
        self.duration_hint.setText(t("duration_hint", self._lang))
        self.luck_section_title.setText(f"🍀  {t('luck_section_title', self._lang)}")
        self.luck_hint.setText(t("luck_hint", self._lang))
        self.about_icon_btn.setToolTip(t("about_button", self._lang))
        self.cancel_btn.setText(f"✕  {t('btn_cancel', self._lang)}")
        self.save_btn.setText(f"✓  {t('btn_save', self._lang)}")
        self._refresh_luck_button()

    def _apply_stylesheet(self) -> None:
        self.setStyleSheet(build_dialog_stylesheet(self._theme))
        self._luck_state = None  # tema degisince buton stilini de yeniden uygula
        self._refresh_luck_button()

    def _refresh_luck_button(self) -> None:
        if self._luck_boost.is_boosted():
            state = "active"
            seconds = self._luck_boost.seconds_remaining_boost()
            self.luck_button.setText(t("luck_button_active", self._lang).format(seconds=seconds))
            self.luck_button.setEnabled(False)
        elif self._luck_boost.is_on_cooldown():
            state = "cooldown"
            remaining = self._luck_boost.seconds_remaining_cooldown()
            mm, ss = divmod(remaining, 60)
            self.luck_button.setText(
                t("luck_button_cooldown", self._lang).format(mm=mm, ss=f"{ss:02d}")
            )
            self.luck_button.setEnabled(False)
        else:
            state = "ready"
            self.luck_button.setText(t("luck_button_ready", self._lang))
            self.luck_button.setEnabled(True)

        if state != self._luck_state:
            self.luck_button.setStyleSheet(build_luck_button_stylesheet(self._theme, state))
            self._luck_state = state

    # -------------------------------------------------------------- signals

    def _on_duration_changed(self, value: int) -> None:
        self.duration_value_label.setText(self._format_duration(value))

    def _on_theme_changed(self, _index: int) -> None:
        self._theme = self.theme_combo.currentData()
        self._apply_stylesheet()

    def _on_language_changed(self, _index: int) -> None:
        self._lang = self.language_combo.currentData()
        self._retranslate()

    def _on_luck_button_clicked(self) -> None:
        self._luck_boost.activate()
        self._refresh_luck_button()

    def _open_about(self) -> None:
        dialog = AboutDialog(language=self._lang, theme=self._theme, parent=self)
        dialog.exec()

    def _on_save(self) -> None:
        theme = self.theme_combo.currentData()
        duration_ms = self.duration_slider.value()
        language = self.language_combo.currentData()
        self.settings_applied.emit(theme, duration_ms, language)
        self.accept()

    # --------------------------------------------------------------- dragging

    def _title_mouse_press(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _title_mouse_move(self, event) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
