"""
4R022 FlashBang - Ses Yöneticisi
Kaan Kross / 4R022

Sıralama: fırlatma sesi (throw.mp3) tam olarak çalar, bitince ağırlıklı
şans (rarity) sistemiyle seçilen bir patlama sesi (bkz. core/sound_pool.py)
en yüksek seviyede çalınır. Patlama sesi, ayarlanan patlama (flash)
süresinden kısa ise otomatik olarak baştan tekrar oynatılarak süreyi
doldurur (otomatik uzatma).

Otomatik uzatma (loop) hassas zamanlama ile yapılır: ses dosyasının
gerçek süresi öğrenilir öğrenilmez, "tam bittiği an" yeniden başlaması
için kendi QTimer'ımızla önceden zamanlanır. Yalnızca Qt'nin
EndOfMedia sinyaline güvenmek (backend'e göre birkaç yüz milisaniyeye
kadar gecikebiliyor) sesler arasında fark edilir bir boşluk
bırakabiliyordu; bu artık yalnızca süre bilgisi zamanında gelmezse
devreye giren bir yedek yöntem olarak kullanılır.

Sequence: the throw sound plays fully; once finished, an explosion
sound is chosen via a weighted rarity system (see core/sound_pool.py)
and plays at maximum volume. If the explosion sound is shorter than
the configured flash duration, it is automatically looped from the
start to fill the remaining time.

The loop restart is precisely timed: as soon as the real duration of
the loaded sound is known, we schedule our own QTimer to restart it
exactly as it finishes. Relying solely on Qt's EndOfMedia signal (which
can lag by a couple hundred milliseconds depending on the backend) left
a perceptible gap between repeats; that signal is now only used as a
fallback if duration info doesn't arrive in time.

Not: Kasıtlı olarak ses seviyesinde tekrarlı/hızlı setVolume() çağrılarıyla
bir "fade-out" YAPILMAZ. Bazı sistemlerde (ses aygıtı bulunamayan, PulseAudio/
PipeWire servisine bağlanamayan veya ses sürücüsü arızalı ortamlarda) art arda
hızlı setVolume() çağrıları Qt Multimedia/FFmpeg ses arka ucunda kilitlenmeye
(deadlock) yol açabiliyor — bu, geliştirme sırasında Xvfb ortamında
doğrulanmış gerçek bir sorundur. Bunun yerine patlama sesi, ayarlanan süre
dolduğunda tek seferde temiz bir şekilde durdurulur. Görsel patlama zaten
kendi (renk tabanlı, sese dokunmayan) sönüş animasyonuna sahiptir.

Note: audio fade-out via rapid repeated setVolume() calls is deliberately
NOT used. On some systems (no audio device present, PulseAudio/PipeWire
unreachable, or a broken audio driver) rapid successive setVolume() calls
can deadlock the Qt Multimedia/FFmpeg audio backend — verified during
development in a headless Xvfb environment. Instead, the explosion sound
is cleanly hard-stopped once the configured duration elapses. The visual
flash already has its own (color-based, audio-independent) fade-out.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QObject, QTimer, QUrl, pyqtSignal
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

from core.resources import THROW_SOUND
from core.sound_pool import SoundEntry, get_sound_path, roll_sound

if TYPE_CHECKING:
    from core.luck_boost import LuckBoost


class AudioManager(QObject):
    """Fırlatma + patlama ses dizisini yöneten, süreye göre hassas
    zamanlamayla otomatik uzatma (loop) yapan ses yöneticisi."""

    throw_finished = pyqtSignal()
    explosion_started = pyqtSignal()
    sound_rolled = pyqtSignal(dict, float)  # secilen SoundEntry, roll anindaki meme carpani
    sequence_finished = pyqtSignal()

    def __init__(self, parent: Optional[QObject] = None, luck_boost: Optional["LuckBoost"] = None) -> None:
        super().__init__(parent)
        self._luck_boost = luck_boost

        self._throw_player = QMediaPlayer(self)
        self._throw_output = QAudioOutput(self)
        self._throw_player.setAudioOutput(self._throw_output)
        self._throw_output.setVolume(1.0)
        self._throw_player.mediaStatusChanged.connect(self._on_throw_status)

        self._boom_player = QMediaPlayer(self)
        self._boom_output = QAudioOutput(self)
        self._boom_player.setAudioOutput(self._boom_output)
        self._boom_output.setVolume(1.0)
        self._boom_player.mediaStatusChanged.connect(self._on_boom_status)
        self._boom_player.durationChanged.connect(self._on_boom_duration_changed)

        self._elapsed_timer = QTimer(self)
        self._elapsed_timer.setSingleShot(True)
        self._elapsed_timer.timeout.connect(self._stop_boom_sequence)

        self._loop_timer = QTimer(self)
        self._loop_timer.setSingleShot(True)
        self._loop_timer.timeout.connect(self._restart_boom_loop)

        self._target_duration_ms = 0
        self._boom_active = False
        self._boom_duration_ms: Optional[int] = None
        self._master_volume = 1.0

    def set_master_volume(self, volume: float) -> None:
        self._master_volume = max(0.0, min(1.0, volume))
        self._throw_output.setVolume(self._master_volume)
        self._boom_output.setVolume(self._master_volume)

    def stop_all(self) -> None:
        self._elapsed_timer.stop()
        self._loop_timer.stop()
        self._boom_active = False
        self._throw_player.stop()
        self._boom_player.stop()

    def play_throw_then_explosion(self, flash_duration_ms: int) -> None:
        """Fırlatma sesini oynatır; bittiğinde patlama dizisini başlatır."""
        self._target_duration_ms = max(200, flash_duration_ms)
        self._throw_player.setSource(QUrl.fromLocalFile(THROW_SOUND))
        self._throw_player.setPosition(0)
        self._throw_player.play()

    def _on_throw_status(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self._throw_player.stop()
            self.throw_finished.emit()
            self._start_explosion()

    def _start_explosion(self) -> None:
        meme_multiplier = self._luck_boost.current_meme_multiplier() if self._luck_boost else 1.0
        entry: SoundEntry = roll_sound(meme_multiplier)
        sound_path = get_sound_path(entry)
        self._boom_duration_ms = None
        self._loop_timer.stop()
        self._boom_output.setVolume(self._master_volume)
        self._boom_player.setSource(QUrl.fromLocalFile(sound_path))
        self._boom_player.setPosition(0)
        self._boom_player.play()
        self._boom_active = True
        self.sound_rolled.emit(entry, meme_multiplier)
        self.explosion_started.emit()
        self._elapsed_timer.start(self._target_duration_ms)

    def _on_boom_duration_changed(self, duration_ms: int) -> None:
        # Ses dosyasinin gercek suresi (ms) - kesin zamanli tekrar icin kullanilir.
        # Bu sinyal play() cagrisindan bir miktar sonra (metadata okunduktan
        # sonra) gelebilir; o ana kadar gecen calma suresini (position())
        # hesaba katmazsak, tekrar tam bitisten daha GEC tetiklenir ve
        # aradaki bosluk sorunu geri doner. Bu yuzden kalan sureyi
        # (duration - position) kullanarak zamanliyoruz.
        self._boom_duration_ms = duration_ms if duration_ms and duration_ms > 0 else None
        if self._boom_active and self._boom_duration_ms:
            elapsed = max(0, self._boom_player.position())
            remaining = max(10, self._boom_duration_ms - elapsed)
            self._loop_timer.start(remaining)

    def _restart_boom_loop(self) -> None:
        if not self._boom_active:
            return
        self._boom_player.setPosition(0)
        self._boom_player.play()
        if self._boom_duration_ms:
            self._loop_timer.start(self._boom_duration_ms)

    def _on_boom_status(self, status: QMediaPlayer.MediaStatus) -> None:
        # Yedek yontem: sure bilgisi zamaninda gelmediyse EndOfMedia'da tekrar baslat.
        # Sure bilinen normal durumda _loop_timer zaten daha once tetiklenmis olur.
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self._boom_active:
            if self._boom_duration_ms is None:
                self._boom_player.setPosition(0)
                self._boom_player.play()

    def _stop_boom_sequence(self) -> None:
        self._boom_active = False
        self._loop_timer.stop()
        self._boom_player.stop()
        self.sequence_finished.emit()
