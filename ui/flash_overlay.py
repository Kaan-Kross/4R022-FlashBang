"""
4R022 FlashBang - Patlama Kaplama Penceresi
Kaan Kross / 4R022

Her monitör için tam ekran, çerçevesiz, en üstte kalan, saf beyaz bir
kaplama penceresi. Gerçekçi görünmesi için çok aşamalı bir "flicker"
(titreşim — ilk anlık aşırı pozlama, ardından kısa bir strob efekti)
ile açılır, ayarlanan süre boyunca tam beyaz kalır ve sonda; gerçek bir
flashbang sonrası göz kamaşmasını anımsatan, sıcak tondan siyaha yumuşak
geçişli (ease) bir "after-image" sönüşüyle kapanır. Fare imleci
gizlenir. Süre dolana kadar kapatılamaz (kullanıcı beklemek zorunda).

Not: Titreşim ve sönüş efektleri kasıtlı olarak saf renk değişimiyle
(QGraphicsOpacityEffect KULLANILMADAN) yapılır. Alfa/opaklık efektleri
pencere yöneticisinde compositing gerektirir ve compositor olmayan
ortamlarda (bazı Linux masaüstleri, headless test ortamları) donmaya
yol açabilir. Renk tabanlı yaklaşım tüm platformlarda sorunsuz çalışır.

A fullscreen, frameless, always-on-top pure-white overlay window for
each monitor. Opens with a multi-stage flicker (an instant overexposure
pulse followed by a brief strobe), holds full white for the configured
duration, then closes with an eased "after-image" fade — warm tones
fading to black, similar to the flash-blindness recovery after a real
flashbang. The mouse cursor is hidden. It cannot be dismissed early —
the user must wait it out, matching the spec.

Note: the flicker/fade effects are implemented via plain color changes
(no QGraphicsOpacityEffect) intentionally. Alpha/opacity effects need
window-manager compositing and can hang on environments without a
compositor (some Linux desktops, headless test setups). The color-based
approach works reliably everywhere.
"""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QApplication, QWidget

# Açılış titreşimi: (gecikme_ms, arkaplan_rengi) çiftleri.
# Aşama 1 (0-40ms): anlık, sıcak tonlu aşırı pozlama (kameranın patlamayı
#                   "yakması" gibi) — tüm monitörlerde birebir aynı anda.
# Aşama 2 (40-230ms): kısa, düzensiz bir strob/titreşim (gerçek bir flash
#                   patlamasının ilk milisaniyelerindeki dengesizliği taklit
#                   eder) — her pencerede birkaç ms'lik rastgele sapmayla,
#                   tekdüze/robotik görünmesin diye.
# Aşama 3: tam, kararlı beyaz.
_FLICKER_BASE_SEQUENCE = [
    (0, "#ffffff"),
    (16, "#fff2d9"),   # sıcak aşırı pozlama tonu
    (38, "#ffffff"),
    (64, "#9c9c9c"),   # kısa "shutter" düşüşü
    (88, "#ffffff"),
    (118, "#efe3c8"),  # ikinci sıcak titreşim
    (148, "#ffffff"),
    (182, "#c7c7c7"),
    (212, "#ffffff"),
]
_FLICKER_JITTER_MAX_MS = 6  # yalnizca ilk (0ms) adim haric, gerceklik icin kucuk rastgele sapma

FADE_OUT_MS = 480
FADE_STEPS = 16

# Sönüş sırasında renk anahtar kareleri (t: 0.0 → 1.0):
# saf beyaz → sıcak/soluk "after-image" tonu → koyu kül grisi → siyah.
# Gerçek bir flashbang sonrası göz kamaşmasının geçiş hissini taklit eder.
_FADE_KEYFRAMES: List[Tuple[float, Tuple[int, int, int]]] = [
    (0.0, (255, 255, 255)),
    (0.30, (247, 226, 189)),
    (0.65, (86, 74, 66)),
    (1.0, (0, 0, 0)),
]


def _smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def _lerp_keyframes(t: float) -> str:
    t = _smoothstep(max(0.0, min(1.0, t)))
    for (t0, c0), (t1, c1) in zip(_FADE_KEYFRAMES, _FADE_KEYFRAMES[1:]):
        if t0 <= t <= t1:
            span = (t1 - t0) or 1.0
            local_t = (t - t0) / span
            r = round(c0[0] + (c1[0] - c0[0]) * local_t)
            g = round(c0[1] + (c1[1] - c0[1]) * local_t)
            b = round(c0[2] + (c1[2] - c0[2]) * local_t)
            return f"#{r:02x}{g:02x}{b:02x}"
    last = _FADE_KEYFRAMES[-1][1]
    return f"#{last[0]:02x}{last[1]:02x}{last[2]:02x}"


class FlashOverlay(QWidget):
    """Tek bir monitörü kaplayan saf beyaz patlama penceresi."""

    def __init__(self, screen: QScreen) -> None:
        super().__init__(
            None,
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)
        self._set_bg("#ffffff")
        self.setCursor(Qt.CursorShape.BlankCursor)

        self.setGeometry(screen.geometry())

        self._flicker_timers: List[QTimer] = []
        self._fade_timer: Optional[QTimer] = None
        self._fade_step_count = 0

    def _set_bg(self, hex_color: str) -> None:
        self.setStyleSheet(f"background-color: {hex_color};")

    def show_on_screen(self) -> None:
        self.showFullScreen()
        self._run_flicker()

    def _run_flicker(self) -> None:
        for index, (delay, color) in enumerate(_FLICKER_BASE_SEQUENCE):
            # İlk kare (0ms, saf beyaz) tüm monitörlerde birebir aynı anda
            # tetiklenmeli; yalnızca sonraki titreşim adımlarına küçük bir
            # rastgele sapma eklenir (robotik değil, doğal görünmesi için).
            jitter = 0 if index == 0 else random.randint(-_FLICKER_JITTER_MAX_MS, _FLICKER_JITTER_MAX_MS)
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda c=color: self._set_bg(c))
            timer.start(max(0, delay + jitter))
            self._flicker_timers.append(timer)

    def begin_fade_out(self, on_complete) -> None:
        self._fade_step_count = 0
        interval = max(1, FADE_OUT_MS // FADE_STEPS)

        self._fade_timer = QTimer(self)
        self._fade_timer.setInterval(interval)

        def _step():
            self._fade_step_count += 1
            self._set_bg(_lerp_keyframes(self._fade_step_count / FADE_STEPS))
            if self._fade_step_count >= FADE_STEPS:
                self._fade_timer.stop()
                on_complete()

        self._fade_timer.timeout.connect(_step)
        self._fade_timer.start()


class FlashController:
    """Tüm monitörlerdeki kaplama pencerelerini eş zamanlı yöneten denetleyici."""

    def __init__(self) -> None:
        self._overlays: List[FlashOverlay] = []
        self._duration_timer: Optional[QTimer] = None
        self.on_finished = None  # dışarıdan atanan callback

    def trigger(self, duration_ms: int) -> None:
        self.dismiss(run_callback=False)
        screens = QApplication.screens()
        for screen in screens:
            overlay = FlashOverlay(screen)
            overlay.show_on_screen()
            self._overlays.append(overlay)

        hold_ms = max(0, duration_ms - FADE_OUT_MS)
        self._duration_timer = QTimer()
        self._duration_timer.setSingleShot(True)
        self._duration_timer.timeout.connect(self._start_fade_out)
        self._duration_timer.start(hold_ms)

    def _start_fade_out(self) -> None:
        if not self._overlays:
            return
        state = {"remaining": len(self._overlays)}

        def _one_done():
            state["remaining"] -= 1
            if state["remaining"] <= 0:
                self._close_all()

        for overlay in self._overlays:
            overlay.begin_fade_out(_one_done)

    def _close_all(self) -> None:
        for overlay in self._overlays:
            overlay.close()
        self._overlays = []
        if self.on_finished is not None:
            self.on_finished()

    def dismiss(self, run_callback: bool = True) -> None:
        if self._duration_timer is not None:
            self._duration_timer.stop()
            self._duration_timer = None
        for overlay in self._overlays:
            overlay.close()
        self._overlays = []
        if run_callback and self.on_finished is not None:
            self.on_finished()

    def is_active(self) -> bool:
        return len(self._overlays) > 0
