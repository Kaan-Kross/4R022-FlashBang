"""
4R022 FlashBang - Şans Butonu (Luck Boost) Durumu
Kaan Kross / 4R022

Ayarlar penceresindeki "Şans Butonu"na basıldığında 1 dakika boyunca
meme seslerinin çıkma ihtimalini artıran, ardından 4 dakikalık bir
bekleme (cooldown) süresine giren basit bir durum makinesi.

Bu nesne MainWindow tarafından uygulamanın tüm ömrü boyunca tek bir
örnek olarak tutulur (Ayarlar penceresi her açıldığında yeniden
oluşturulmaz) — böylece pencere kapatılıp açılsa bile süre kesintisiz
işlemeye devam eder. Durum yalnızca bellekte tutulur (diske
kaydedilmez); uygulama kapatılıp açıldığında sıfırlanır.

Sistem saati değişikliklerinden etkilenmemesi için `time.monotonic()`
kullanılır (duvar saati değil).

A simple state machine for the Settings "Luck Button": pressing it
boosts meme-sound odds for 1 minute, then enters a 4-minute cooldown.

This object is kept as a single instance by MainWindow for the app's
whole lifetime (not recreated each time Settings is opened), so the
timer keeps running correctly even if the dialog is closed and
reopened. State lives in memory only (not persisted to disk); it
resets when the app restarts.

`time.monotonic()` is used (not wall-clock time) so the timer is
unaffected by system clock changes.
"""

from __future__ import annotations

import time
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

from core.sound_pool import MEME_BOOST_MULTIPLIER

BOOST_DURATION_SECONDS = 60
COOLDOWN_DURATION_SECONDS = 4 * 60


class LuckBoost(QObject):
    """Şans Butonu'nun aktif/bekleme durumunu yöneten basit durum makinesi."""

    state_changed = pyqtSignal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._boost_ends_at: Optional[float] = None
        self._cooldown_ends_at: Optional[float] = None

    def can_activate(self) -> bool:
        return not self.is_boosted() and not self.is_on_cooldown()

    def activate(self) -> bool:
        """Şansı aktive etmeye çalışır. Zaten aktifse veya bekleme
        süresindeyse hiçbir şey yapmaz ve False döner."""
        if not self.can_activate():
            return False
        now = time.monotonic()
        self._boost_ends_at = now + BOOST_DURATION_SECONDS
        self._cooldown_ends_at = self._boost_ends_at + COOLDOWN_DURATION_SECONDS
        self.state_changed.emit()
        return True

    def is_boosted(self) -> bool:
        return self._boost_ends_at is not None and time.monotonic() < self._boost_ends_at

    def is_on_cooldown(self) -> bool:
        if self.is_boosted():
            return False
        return self._cooldown_ends_at is not None and time.monotonic() < self._cooldown_ends_at

    def seconds_remaining_boost(self) -> int:
        if not self.is_boosted() or self._boost_ends_at is None:
            return 0
        return max(0, int(round(self._boost_ends_at - time.monotonic())))

    def seconds_remaining_cooldown(self) -> int:
        if not self.is_on_cooldown() or self._cooldown_ends_at is None:
            return 0
        return max(0, int(round(self._cooldown_ends_at - time.monotonic())))

    def current_meme_multiplier(self) -> float:
        return float(MEME_BOOST_MULTIPLIER) if self.is_boosted() else 1.0
