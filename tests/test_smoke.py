"""Headless duman testi (smoke test) - CI/geliştirme sırasında kullanılır."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest

from core.config_manager import ConfigManager
from ui.main_window import MainWindow
from ui.settings_dialog import SettingsDialog

app = QApplication(sys.argv)
config = ConfigManager()
config.set("flash_duration_ms", 1200)
window = MainWindow(config)
window.show()
app.processEvents()

print("Ekranlar / screens:", app.screens())
window.grab().save("/tmp/01_main_window.png")
print("Ana pencere görüntüsü kaydedildi.")

# Ayarlar diyaloğunu test et (non-modal test için exec yerine manuel aç/kapat)
dlg = SettingsDialog(config.get("theme"), config.get("flash_duration_ms"), config.get("language"), window.luck_boost, window)
dlg.show()
app.processEvents()
dlg.grab().save("/tmp/02_settings_dialog.png")
assert "✕" in dlg.cancel_btn.text() and "✓" in dlg.save_btn.text(), "Kaydet/Iptal butonlarinda sembol yok!"
dlg.theme_combo.setCurrentIndex(1)
app.processEvents()
dlg.grab().save("/tmp/03_settings_dialog_light.png")

# Dil degistirme testi - 4 dilin de patlamadan cikmadigindan emin ol
from core.i18n import SUPPORTED_LANGUAGES

for i, code in enumerate(SUPPORTED_LANGUAGES):
    dlg.language_combo.setCurrentIndex(i)
    app.processEvents()
    print(f"dil={code} baslik={dlg.title_label.text()!r} kaydet={dlg.save_btn.text()!r}")
    dlg.grab().save(f"/tmp/lang_{code}.png")

dlg.language_combo.setCurrentIndex(0)  # tr'ye geri don
app.processEvents()
dlg.close()
print("Ayarlar penceresi ve dil secenekleri test edildi.")

# Hakkımızda diyaloğu testi
from ui.about_dialog import AboutDialog

about = AboutDialog("tr", config.get("theme"), window)
about.show()
app.processEvents()
about.grab().save("/tmp/05_about_dialog.png")
assert not hasattr(about, "close_btn"), "Hakkımızda penceresinde hâlâ ikinci bir kapatma butonu (close_btn) var!"
about.close()
app.processEvents()
print("Hakkımızda penceresi test edildi (tek kapatma butonu dogrulandi).")

# Şans Butonu (Luck Boost) testi
print("\n--- Sans Butonu testi ---")
print("Baslangicta can_activate:", window.luck_boost.can_activate())
assert window.luck_boost.can_activate(), "Baslangicta sans butonu aktif edilebilir olmali!"

dlg2 = SettingsDialog(config.get("theme"), config.get("flash_duration_ms"), "tr", window.luck_boost, window)
dlg2.show()
app.processEvents()
assert dlg2.luck_button.isEnabled(), "Sans butonu baslangicta etkin olmali!"
QTest.mouseClick(dlg2.luck_button, Qt.MouseButton.LeftButton)
app.processEvents()
print("Aktivasyon sonrasi boosted:", window.luck_boost.is_boosted())
assert window.luck_boost.is_boosted(), "Sans butonu tiklandiktan sonra boost aktif olmali!"
assert not dlg2.luck_button.isEnabled(), "Aktifken buton devre disi olmali!"
print("Buton metni (aktif):", dlg2.luck_button.text())
dlg2.close()
app.processEvents()

# Boost aktifken tetiklenen patlamanin gercek carpanla roll yaptigini dogrula
from core.sound_pool import MEME_BOOST_MULTIPLIER

assert window.luck_boost.current_meme_multiplier() == float(MEME_BOOST_MULTIPLIER), "Multiplier yanlis!"
print("Sans Butonu testi basarili.")

# Ana pencerenin canli (yeniden baslatmadan) dil guncellemesi testi
window._on_settings_applied("dark", 1200, "ru")
app.processEvents()
print("Ana pencere RU sonrasi hint:", window.hint_label.text())
assert window.hint_label.text() == "Нажмите на изображение, чтобы выдернуть чеку", "RU hint metni guncellenmedi!"
window._on_settings_applied("dark", 1200, "tr")
app.processEvents()
print("Ana pencere TR'ye geri donduruldu, hint:", window.hint_label.text())

# Flashbang görseline tıklama simülasyonu
QTest.mouseClick(window.image_label, Qt.MouseButton.LeftButton)
app.processEvents()
print("Tıklama tetiklendi, sequence_active =", window._sequence_active)


def check_after_throw():
    print("throw sonrası, sequence_active =", window._sequence_active)
    print("flash_controller aktif mi:", window.flash_controller.is_active())


def check_mid_flash():
    print("patlama ortası, overlay sayisi:", len(window.flash_controller._overlays))
    if window.flash_controller._overlays:
        window.flash_controller._overlays[0].grab().save("/tmp/04_flash_overlay.png")
        print("Flash overlay görüntüsü kaydedildi.")
    # ESC bu sirada calismamali (beklemek zorunlu)
    # Not: pencere yoneticisi olmayan headless ortamda QTest.keyClick focus
    # bekleyip kilitlenebiliyor; mantigi dogrudan cagirarak test ediyoruz.
    from PyQt6.QtGui import QKeyEvent

    esc_event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier)
    window.keyPressEvent(esc_event)
    app.processEvents()
    print("Flash sirasinda ESC denendi, pencere hala acik mi:", window.isVisible())


def check_after_finish():
    print("Sequence bitti mi:", not window._sequence_active)
    print("Overlay kapandi mi:", not window.flash_controller.is_active())
    print("Son roll sonucu:", window._last_roll)
    print("Roll sirasindaki multiplier (boost aktifti, MEME_BOOST_MULTIPLIER olmali):", window._last_roll_multiplier)
    print("hint_label (her zaman tiklama talimati olmali):", window.hint_label.text())
    print("result_label (roll sonucunu icermeli, renkli):", window.result_label.text())
    print("result_label stylesheet:", window.result_label.styleSheet())
    assert window._last_roll is not None, "Roll sonucu kaydedilmedi!"
    assert window.hint_label.text() == "Fitili çekmek için görsele tıkla", "hint_label roll sonrasi da tiklama talimatini gostermeli!"
    assert window.result_label.text() != "", "Roll sonrasi result_label bos kaldi!"
    assert "color:" in window.result_label.styleSheet(), "result_label renklendirilmemis!"
    assert "border" in window.result_label.styleSheet(), "result_label 'epic' cerceve/pill stiline sahip degil!"
    from core.sound_pool import MEME_BOOST_MULTIPLIER
    assert window._last_roll_multiplier == float(MEME_BOOST_MULTIPLIER), "Boost aktifken roll multiplier MEME_BOOST_MULTIPLIER olmali!"
    window.close()
    app.processEvents()
    print("Pencere kapatildi, isVisible:", window.isVisible())
    app.quit()


heartbeat = QTimer()
heartbeat.timeout.connect(lambda: print("heartbeat", time.time(), flush=True))
heartbeat.start(200)

QTimer.singleShot(600, check_after_throw)
QTimer.singleShot(1800, check_mid_flash)
QTimer.singleShot(3600, check_after_finish)
QTimer.singleShot(4200, app.quit)

sys.exit(app.exec())
