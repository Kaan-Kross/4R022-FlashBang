"""
4R022 FlashBang - Yerelleştirme (i18n)
Kaan Kross / 4R022

Desteklenen diller: Türkçe (tr), İngilizce (en), Lehçe (pl), Rusça (ru).
Arayüzdeki tüm metinler bu modül üzerinden çözümlenir; dil ayarı
değiştiğinde arayüz yeniden çizilmeden (restart gerekmeden) güncellenir.

Supported languages: Turkish (tr), English (en), Polish (pl), Russian (ru).
All UI text is resolved through this module; when the language setting
changes, the UI updates live without requiring a restart.
"""

from __future__ import annotations

SUPPORTED_LANGUAGES = ["tr", "en", "pl", "ru"]
DEFAULT_LANGUAGE = "tr"

LANGUAGE_NATIVE_NAMES = {
    "tr": "Türkçe",
    "en": "English",
    "pl": "Polski",
    "ru": "Русский",
}

_TRANSLATIONS = {
    "hint_click": {
        "tr": "Fitili çekmek için görsele tıkla",
        "en": "Click the image to pull the pin",
        "pl": "Kliknij obraz, aby wyciągnąć zawleczkę",
        "ru": "Нажмите на изображение, чтобы выдернуть чеку",
    },
    "hint_pulled": {
        "tr": "Fitil çekildi...",
        "en": "Pin pulled...",
        "pl": "Zawleczka wyciągnięta...",
        "ru": "Чека выдернута...",
    },
    "hint_exit": {
        "tr": "ESC veya × ile çıkış",
        "en": "Press ESC or × to exit",
        "pl": "Naciśnij ESC lub × aby wyjść",
        "ru": "Нажмите ESC или ×, чтобы выйти",
    },
    "settings_title": {
        "tr": "AYARLAR",
        "en": "SETTINGS",
        "pl": "USTAWIENIA",
        "ru": "НАСТРОЙКИ",
    },
    "theme_label": {
        "tr": "Ana Tema Rengi (Arkaplan)",
        "en": "Main Theme Color (Background)",
        "pl": "Główny kolor motywu (Tło)",
        "ru": "Основной цвет темы (Фон)",
    },
    "theme_dark": {
        "tr": "Koyu (Siyah)",
        "en": "Dark (Black)",
        "pl": "Ciemny (Czarny)",
        "ru": "Тёмная (Чёрный)",
    },
    "theme_light": {
        "tr": "Açık (Beyaz)",
        "en": "Light (White)",
        "pl": "Jasny (Biały)",
        "ru": "Светлая (Белый)",
    },
    "duration_label": {
        "tr": "Patlama (Flash) Süresi",
        "en": "Flash Duration",
        "pl": "Czas trwania flasha",
        "ru": "Длительность вспышки",
    },
    "duration_unit_suffix": {
        "tr": "sn",
        "en": "s",
        "pl": "s",
        "ru": "с",
    },
    "duration_hint": {
        "tr": "Not: Patlama sesi bu süreden kısa ise otomatik olarak\nbaştan tekrar oynatılarak süre doldurulur.",
        "en": "Note: if the explosion sound is shorter than this\nduration, it automatically loops to fill the time.",
        "pl": "Uwaga: jeśli dźwięk wybuchu jest krótszy niż ten czas,\nzostanie automatycznie powtórzony, aby go wypełnić.",
        "ru": "Примечание: если звук взрыва короче этого времени,\nон будет автоматически повторён для заполнения.",
    },
    "language_label": {
        "tr": "Dil",
        "en": "Language",
        "pl": "Język",
        "ru": "Язык",
    },
    "btn_cancel": {
        "tr": "İptal",
        "en": "Cancel",
        "pl": "Anuluj",
        "ru": "Отмена",
    },
    "btn_save": {
        "tr": "Kaydet",
        "en": "Save",
        "pl": "Zapisz",
        "ru": "Сохранить",
    },
    "result_flashbang": {
        "tr": "Tebrikler — {odds} Patlaması!",
        "en": "Congrats — {odds} Explosion!",
        "pl": "Gratulacje — {odds} Wybuch!",
        "ru": "Поздравляем — {odds} Взрыв!",
    },
    "result_meme": {
        "tr": "Tebrikler — {odds} Rastgele Meme!",
        "en": "Congrats — {odds} Random Meme!",
        "pl": "Gratulacje — {odds} Losowe Meme!",
        "ru": "Поздравляем — {odds} Случайный Мем!",
    },
    "luck_section_title": {
        "tr": "Şans Sistemi",
        "en": "Luck System",
        "pl": "System Szczęścia",
        "ru": "Система Удачи",
    },
    "luck_button_ready": {
        "tr": "🍀 Şansını Dene!",
        "en": "🍀 Try Your Luck!",
        "pl": "🍀 Spróbuj Szczęścia!",
        "ru": "🍀 Испытать Удачу!",
    },
    "luck_button_active": {
        "tr": "🍀 Aktif — {seconds} sn kaldı",
        "en": "🍀 Active — {seconds}s left",
        "pl": "🍀 Aktywne — pozostało {seconds}s",
        "ru": "🍀 Активно — осталось {seconds}с",
    },
    "luck_button_cooldown": {
        "tr": "⏳ Bekleme Süresi — {mm}:{ss}",
        "en": "⏳ Cooldown — {mm}:{ss}",
        "pl": "⏳ Odnowienie — {mm}:{ss}",
        "ru": "⏳ Перезарядка — {mm}:{ss}",
    },
    "luck_hint": {
        "tr": "1 dakika boyunca meme seslerinin çıkma ihtimali 10 kat artar. "
              "Kullanımdan sonra 4 dakikalık bir bekleme süresi başlar.",
        "en": "For 1 minute, meme sounds become 10× more likely to appear. "
              "A 4-minute cooldown starts once it ends.",
        "pl": "Przez 1 minutę dźwięki meme mają 10 razy większą szansę na "
              "pojawienie się. Po zakończeniu rozpoczyna się 4-minutowe "
              "odnowienie.",
        "ru": "В течение 1 минуты звуки мемов появляются в 10 раз чаще. "
              "После окончания начинается 4-минутная перезарядка.",
    },
    "about_button": {
        "tr": "ℹ Hakkımızda",
        "en": "ℹ About",
        "pl": "ℹ O nas",
        "ru": "ℹ О нас",
    },
    "about_title": {
        "tr": "HAKKIMIZDA",
        "en": "ABOUT",
        "pl": "O NAS",
        "ru": "О НАС",
    },
    "about_version_label": {
        "tr": "Sürüm",
        "en": "Version",
        "pl": "Wersja",
        "ru": "Версия",
    },
    "about_developer_label": {
        "tr": "Geliştirici",
        "en": "Developer",
        "pl": "Deweloper",
        "ru": "Разработчик",
    },
    "about_description": {
        "tr": "4R022 FlashBang, tıklandığında tüm ekranlarınızı kaplayan "
              "gerçekçi bir flashbang efekti oynatan, eğlence amaçlı bir "
              "masaüstü uygulamasıdır.\n\n"
              "Patlama sesi, oyunlardaki şans (loot) sistemlerine benzer "
              "şekilde seçilir: gerçek flashbang sesleri en olası "
              "sonuçtur, ama nadiren çeşitli \"meme\" sesleri de "
              "çıkabilir — her sesin kendine özgü bir düşme oranı "
              "vardır. Ayarlar'daki Şans Butonu, bir dakikalığına meme "
              "seslerinin çıkma ihtimalini geçici olarak artırır.",
        "en": "4R022 FlashBang is a fun desktop app that plays a "
              "realistic flashbang effect covering all your screens "
              "when clicked.\n\n"
              "The explosion sound is chosen like a loot system in "
              "games: genuine flashbang sounds are the most likely "
              "outcome, but rare \"meme\" sounds can occasionally "
              "appear too — every sound has its own unique odds. The "
              "Luck Button in Settings temporarily boosts the odds of "
              "meme sounds for one minute.",
        "pl": "4R022 FlashBang to zabawna aplikacja desktopowa, która "
              "po kliknięciu odtwarza realistyczny efekt flashbanga na "
              "wszystkich ekranach.\n\n"
              "Dźwięk wybuchu jest losowany jak w systemie loot w "
              "grach: prawdziwe dźwięki flashbanga są najbardziej "
              "prawdopodobne, ale czasem mogą pojawić się rzadkie "
              "dźwięki \"meme\" — każdy dźwięk ma swoją unikalną szansę. "
              "Przycisk Szczęścia w Ustawieniach tymczasowo zwiększa "
              "szansę na dźwięki meme na jedną minutę.",
        "ru": "4R022 FlashBang — это весёлое настольное приложение, "
              "которое при нажатии воспроизводит реалистичный эффект "
              "флешбанга на всех экранах.\n\n"
              "Звук взрыва выбирается как в игровой системе добычи: "
              "настоящие звуки флешбанга наиболее вероятны, но иногда "
              "могут появиться редкие звуки «мемов» — у каждого звука "
              "свой уникальный шанс выпадения. Кнопка удачи в "
              "настройках временно повышает шанс на звуки мемов на "
              "одну минуту.",
    },
    "btn_close": {
        "tr": "Kapat",
        "en": "Close",
        "pl": "Zamknij",
        "ru": "Закрыть",
    },
    # --- Ses adları (core/sound_pool.py tarafından kullanılır) ---
    # --- Sound names (used by core/sound_pool.py) ---
    "sound_flashbang": {
        "tr": "Flashbang",
        "en": "Flashbang",
        "pl": "Flashbang",
        "ru": "Флешбанг",
    },
    "sound_ak47": {
        "tr": "AK-47",
        "en": "AK-47",
        "pl": "AK-47",
        "ru": "АК-47",
    },
    "sound_alarm": {
        "tr": "Alarm",
        "en": "Alarm",
        "pl": "Alarm",
        "ru": "Сигнализация",
    },
    "sound_metal_pipe": {
        "tr": "Metal Boru",
        "en": "Metal Pipe",
        "pl": "Metalowa Rura",
        "ru": "Металлическая Труба",
    },
    "sound_meme_explosion": {
        "tr": "Meme Patlaması",
        "en": "Meme Explosion",
        "pl": "Wybuch Meme",
        "ru": "Мем-взрыв",
    },
    "sound_roblox_oof": {
        "tr": "Roblox Oof",
        "en": "Roblox Oof",
        "pl": "Roblox Oof",
        "ru": "Roblox Oof",
    },
    "sound_what_is_love": {
        "tr": "What Is Love",
        "en": "What Is Love",
        "pl": "What Is Love",
        "ru": "What Is Love",
    },
    "sound_verstappen_radio": {
        "tr": "Max Verstappen Telsizi",
        "en": "Max Verstappen Radio",
        "pl": "Radio Max Verstappena",
        "ru": "Рация Макса Ферстаппена",
    },
    "sound_whopper_ad": {
        "tr": "Whopper Reklamı",
        "en": "Whopper Ad",
        "pl": "Reklama Whoppera",
        "ru": "Реклама Whopper",
    },
    "sound_elevator_music": {
        "tr": "Asansör Müziği",
        "en": "Elevator Music",
        "pl": "Muzyka Windowa",
        "ru": "Лифтовая Музыка",
    },
    "sound_mystery_tone": {
        "tr": "Gizemli Ton",
        "en": "Mystery Tone",
        "pl": "Tajemniczy Ton",
        "ru": "Таинственный Тон",
    },
    # --- Nadirlik rank adları (sonuç mesajlarında/README'de kullanılabilir) ---
    # --- Rarity rank names ---
    "rank_uncommon": {
        "tr": "Az Bulunur",
        "en": "Uncommon",
        "pl": "Niepospolity",
        "ru": "Необычный",
    },
    "rank_rare": {
        "tr": "Nadir",
        "en": "Rare",
        "pl": "Rzadki",
        "ru": "Редкий",
    },
    "rank_epic": {
        "tr": "Epik",
        "en": "Epic",
        "pl": "Epicki",
        "ru": "Эпический",
    },
    "rank_legendary": {
        "tr": "Efsanevi",
        "en": "Legendary",
        "pl": "Legendarny",
        "ru": "Легендарный",
    },
}


def t(key: str, lang: str) -> str:
    """Verilen anahtar için, belirtilen dilde çeviri döndürür.

    Bilinmeyen dil ya da anahtar durumunda İngilizce'ye, o da yoksa
    anahtarın kendisine düşer (asla patlamaz).
    """
    entry = _TRANSLATIONS.get(key)
    if entry is None:
        return key
    if lang in entry:
        return entry[lang]
    return entry.get("en", key)


def normalize_language(lang: str) -> str:
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
