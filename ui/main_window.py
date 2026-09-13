"""
4R022 FlashBang - Ana Pencere
Kaan Kross / 4R022

Çerçevesiz (native olmayan) ana uygulama penceresi. Ortada büyük bir
flashbang görseli bulunur; tıklanınca fırlatma sesi çalar, ardından
tüm monitörleri kaplayan gerçekçi beyaz bir patlama efekti ve ağırlıklı
şans (rarity) sistemiyle seçilmiş bir patlama sesi tetiklenir. Patlama
bitince hangi sesin çıktığı ve gerçek düşme oranı ekranda gösterilir.
ESC tuşu veya sağ üstteki X butonu ile uygulama kapatılabilir (patlama
sürerken kapatma devre dışı bırakılır — kullanıcı patlamanın geçmesini
beklemek zorundadır).

Frameless (non-native) main application window. A large flashbang
image sits in the center; clicking it plays the throw sound, then
triggers a realistic full-screen white flash across every monitor with
an explosion sound chosen via a weighted rarity system. Once it's over,
which sound played and its real odds are shown on screen. ESC or the
top-right X button closes the app (disabled while the flash is active
— the user must wait it out).
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QCloseEvent, QIcon, QKeyEvent, QMouseEvent, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.audio_manager import AudioManager
from core.config_manager import ConfigManager
from core.i18n import t
from core.luck_boost import LuckBoost
from core.resources import FLASHBANG_IMAGE, ICON_IMAGE, LOGO_IMAGE
from core.sound_pool import SoundEntry, format_meme_odds, get_sound_display_name, odds_percentage
from core.theme import RARITY_BADGE_ICON, build_main_stylesheet, build_result_pill_stylesheet
from ui.flash_overlay import FlashController
from ui.settings_dialog import SettingsDialog

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 660
IMAGE_MAX_SIZE = 320


class MainWindow(QWidget):
    """4R022 FlashBang uygulamasının ana (tek) penceresi."""

    def __init__(self, config: ConfigManager) -> None:
        super().__init__(None, Qt.WindowType.FramelessWindowHint)
        self.config = config
        self.luck_boost = LuckBoost(self)
        self.audio_manager = AudioManager(self, luck_boost=self.luck_boost)
        self.flash_controller = FlashController()
        self.flash_controller.on_finished = self._on_sequence_finished
        self.audio_manager.explosion_started.connect(self._on_explosion_started)
        self.audio_manager.sound_rolled.connect(self._on_sound_rolled)

        self._drag_pos: Optional[QPoint] = None
        self._sequence_active = False
        self._last_roll: Optional[SoundEntry] = None
        self._last_roll_multiplier: float = 1.0

        self.setWindowIcon(QIcon(ICON_IMAGE))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setObjectName("RootPanel")

        self._build_ui()
        self._apply_theme()
        self._retranslate()
        self._restore_position()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(14, 0, 8, 0)
        title_layout.setSpacing(8)

        logo_label = QLabel()
        logo_pixmap = QPixmap(LOGO_IMAGE)
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(
                22,
                22,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        logo_label.setPixmap(logo_pixmap)
        title_layout.addWidget(logo_label)

        brand_label = QLabel("4R022 · FLASHBANG")
        brand_label.setObjectName("BrandLabel")
        title_layout.addWidget(brand_label)
        title_layout.addStretch(1)

        gear_btn = QPushButton("⚙")
        gear_btn.setObjectName("GearButton")
        gear_btn.setFixedSize(30, 30)
        gear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gear_btn.clicked.connect(self._open_settings)
        title_layout.addWidget(gear_btn)

        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self._request_close)
        title_layout.addWidget(close_btn)

        title_bar.mousePressEvent = self._title_mouse_press
        title_bar.mouseMoveEvent = self._title_mouse_move
        self._title_bar = title_bar

        root_layout.addWidget(title_bar)

        center_area = QWidget()
        center_layout = QVBoxLayout(center_area)
        center_layout.setContentsMargins(30, 10, 30, 10)
        center_layout.setSpacing(14)
        center_layout.addStretch(1)

        title_label = QLabel("FLASHBANG")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(title_label)

        self.image_label = QLabel()
        self.image_label.setObjectName("FlashbangImage")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        pixmap = QPixmap(FLASHBANG_IMAGE)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                IMAGE_MAX_SIZE,
                IMAGE_MAX_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        self.image_label.setPixmap(pixmap)
        self.image_label.mousePressEvent = self._on_image_clicked

        image_card = QFrame()
        image_card.setObjectName("ImageCard")
        image_card_layout = QVBoxLayout(image_card)
        image_card_layout.setContentsMargins(14, 14, 14, 14)
        image_card_layout.addWidget(self.image_label)
        center_layout.addWidget(image_card, alignment=Qt.AlignmentFlag.AlignCenter)

        self.hint_label = QLabel()
        self.hint_label.setObjectName("HintLabel")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setWordWrap(True)
        center_layout.addWidget(self.hint_label)

        self.result_label = QLabel()
        self.result_label.setObjectName("ResultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        center_layout.addWidget(self.result_label)

        center_layout.addStretch(2)

        self.esc_hint_label = QLabel()
        self.esc_hint_label.setObjectName("HintLabel")
        self.esc_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.esc_hint_label)

        root_layout.addWidget(center_area)

    def _apply_theme(self) -> None:
        theme = self.config.get("theme", "dark")
        self.setStyleSheet(build_main_stylesheet(theme))

    def _retranslate(self) -> None:
        lang = self.config.get("language", "tr")
        if self._sequence_active:
            self.hint_label.setText(t("hint_pulled", lang))
        else:
            self.hint_label.setText(t("hint_click", lang))
        self.esc_hint_label.setText(t("hint_exit", lang))
        self._update_result_label()

    def _update_result_label(self) -> None:
        if self._last_roll is None:
            self.result_label.setText("")
            self.result_label.setStyleSheet("")
            return
        lang = self.config.get("language", "tr")
        theme = self.config.get("theme", "dark")
        tier = self._last_roll["tier"]
        icon = RARITY_BADGE_ICON.get(tier, "")
        text = self._format_roll_result(self._last_roll, lang, self._last_roll_multiplier)
        self.result_label.setText(f"{icon}  {text}  {icon}" if icon else text)
        self.result_label.setStyleSheet(build_result_pill_stylesheet(tier, theme))

    @staticmethod
    def _format_roll_result(entry: SoundEntry, lang: str, meme_multiplier: float = 1.0) -> str:
        if entry["category"] == "flashbang":
            odds = odds_percentage(entry, meme_multiplier)
            return t("result_flashbang", lang).format(odds=odds)
        odds = format_meme_odds(entry, meme_multiplier)
        name = get_sound_display_name(entry, lang)
        return t("result_meme", lang).format(odds=odds) + f" — {name}"

    def _restore_position(self) -> None:
        pos = self.config.get("window_pos")
        if pos and isinstance(pos, list) and len(pos) == 2 and self._is_position_visible(pos[0], pos[1]):
            self.move(pos[0], pos[1])
        else:
            self._center_on_primary_screen()

    def _is_position_visible(self, x: int, y: int) -> bool:
        """Konumun hâlâ mevcut monitörlerden birinde göründüğünü doğrular.

        Kaydedilen konum, o zamanki bir monitörde olabilir; ama kullanıcı
        o monitörü söküp taktıysa veya çözünürlük değiştiyse, pencere artık
        hiçbir ekranda görünmeyen bir noktada açılıp "kaybolabilir". Bu
        durumda ortalanmış konuma geri dönülür.

        Verifies the position still falls on one of the currently
        connected monitors. A saved position may have been valid on a
        monitor that has since been disconnected or had its resolution
        changed, which would otherwise open the window somewhere
        invisible. In that case we fall back to centering it.
        """
        probe_rect_width, probe_rect_height = 50, 50
        probe = QRect(x, y, probe_rect_width, probe_rect_height)
        for screen in QApplication.screens():
            geo = screen.availableGeometry()
            if geo.intersects(probe):
                return True
        return False

    def _center_on_primary_screen(self) -> None:
        screen = self.screen()
        if screen is not None:
            geo = screen.geometry()
            x = geo.x() + (geo.width() - WINDOW_WIDTH) // 2
            y = geo.y() + (geo.height() - WINDOW_HEIGHT) // 2
            self.move(x, y)

    # ------------------------------------------------------------- Actions

    def _on_image_clicked(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if self._sequence_active:
            return
        self._start_sequence()

    def _start_sequence(self) -> None:
        self._sequence_active = True
        self._retranslate()
        self.image_label.setCursor(Qt.CursorShape.ForbiddenCursor)
        duration_ms = self.config.get("flash_duration_ms", 3000)
        self.audio_manager.play_throw_then_explosion(duration_ms)

    def _on_explosion_started(self) -> None:
        duration_ms = self.config.get("flash_duration_ms", 3000)
        self.flash_controller.trigger(duration_ms)

    def _on_sound_rolled(self, entry: dict, meme_multiplier: float) -> None:
        self._last_roll = entry  # type: ignore[assignment]
        self._last_roll_multiplier = meme_multiplier

    def _on_sequence_finished(self) -> None:
        self._sequence_active = False
        self._retranslate()
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)

    def _open_settings(self) -> None:
        if self._sequence_active:
            return
        dialog = SettingsDialog(
            current_theme=self.config.get("theme", "dark"),
            current_duration_ms=self.config.get("flash_duration_ms", 3000),
            current_language=self.config.get("language", "tr"),
            luck_boost=self.luck_boost,
            parent=self,
        )
        dialog.settings_applied.connect(self._on_settings_applied)
        dialog.exec()

    def _on_settings_applied(self, theme: str, duration_ms: int, language: str) -> None:
        self.config.set("theme", theme)
        self.config.set("flash_duration_ms", duration_ms)
        self.config.set("language", language)
        self._apply_theme()
        self._retranslate()

    def _request_close(self) -> None:
        if self._sequence_active:
            return
        self.close()

    # --------------------------------------------------------------- Events

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            if not self._sequence_active:
                self.close()
            event.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._sequence_active:
            event.ignore()
            return
        pos = self.pos()
        self.config.set("window_pos", [pos.x(), pos.y()])
        self.audio_manager.stop_all()
        self.flash_controller.dismiss(run_callback=False)
        super().closeEvent(event)

    def _title_mouse_press(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _title_mouse_move(self, event: QMouseEvent) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
