"""
4R022 FlashBang - Tema ve Tasarım Sistemi
Kaan Kross / 4R022

İstenen davranış: Siyah/Beyaz tema seçimi SADECE ana pencerenin
arkaplan rengini etkiler. Marka rengi (bordo) ve altın vurgular her
iki temada da sabit kalır.

Bu modül, uygulamanın "epic"/profesyonel görünümünü sağlayan tüm QSS
(Qt Style Sheet) üretim fonksiyonlarını barındırır: gradyanlı
arkaplanlar, kart (panel) stilleri, rozet (badge) butonlar ve
nadirliğe göre renklenen "loot" rozeti.

Requested behavior: the Dark/Light theme choice ONLY affects the main
window's background color. The brand accent (bordeaux) and gold
highlight stay constant across both themes.

This module holds all the QSS (Qt Style Sheet) generation functions
behind the app's "epic"/professional look: gradient backgrounds, card
panel styles, badge buttons, and the rarity-colored loot badge.
"""

from __future__ import annotations

BORDEAUX = "#7a1f2b"
BORDEAUX_HOVER = "#9c2836"
BORDEAUX_PRESSED = "#5e1620"
GOLD = "#e8b34e"

DARK_BG_TOP = "#121014"
DARK_BG_BOTTOM = "#050506"
DARK_FG = "#f0eeee"
DARK_SUBTLE = "#a9a3a3"
DARK_BORDER = "#2c2830"
DARK_CARD = "#1a171c"

LIGHT_BG_TOP = "#ffffff"
LIGHT_BG_BOTTOM = "#eceaec"
LIGHT_FG = "#18151a"
LIGHT_SUBTLE = "#5a5560"
LIGHT_BORDER = "#dcd8dc"
LIGHT_CARD = "#f7f5f7"

# Nadirlik (rarity) rengi — klasik oyun loot renk kodlaması:
# gri/beyaz (olağan) → yeşil → mavi → mor → altın (efsanevi).
# Rarity color — classic game loot color coding:
# gray/white (common) → green → blue → purple → gold (legendary).
_RARITY_COLORS_DARK = {
    "flashbang": "#d8d8d8",
    "uncommon": "#3ddc84",
    "rare": "#4da3ff",
    "epic": "#c46ef9",
    "legendary": GOLD,
}
_RARITY_COLORS_LIGHT = {
    "flashbang": "#3a3a3a",
    "uncommon": "#1f8b4c",
    "rare": "#1d4ed8",
    "epic": "#7c1fd6",
    "legendary": "#a8730a",
}

# Nadirliğe göre "epic" bir kutlama simgesi — düşük kademeden yükseğe
# doğru gösterişi artar (klasik loot-drop hissi).
RARITY_BADGE_ICON = {
    "flashbang": "💥",
    "uncommon": "✨",
    "rare": "🌟",
    "epic": "💫",
    "legendary": "👑",
}


def get_rarity_color(tier: str, theme: str) -> str:
    """Verilen nadirlik kademesi (tier) ve tema için okunaklı bir renk döndürür."""
    palette = _RARITY_COLORS_LIGHT if theme == "light" else _RARITY_COLORS_DARK
    return palette.get(tier, palette["flashbang"])


def get_theme_colors(theme: str) -> dict:
    if theme == "light":
        return {
            "bg_top": LIGHT_BG_TOP,
            "bg_bottom": LIGHT_BG_BOTTOM,
            "fg": LIGHT_FG,
            "subtle": LIGHT_SUBTLE,
            "accent": BORDEAUX,
            "accent_hover": BORDEAUX_HOVER,
            "accent_pressed": BORDEAUX_PRESSED,
            "gold": GOLD,
            "border": LIGHT_BORDER,
            "card": LIGHT_CARD,
        }
    return {
        "bg_top": DARK_BG_TOP,
        "bg_bottom": DARK_BG_BOTTOM,
        "fg": DARK_FG,
        "subtle": DARK_SUBTLE,
        "accent": BORDEAUX,
        "accent_hover": BORDEAUX_HOVER,
        "accent_pressed": BORDEAUX_PRESSED,
        "gold": GOLD,
        "border": DARK_BORDER,
        "card": DARK_CARD,
    }


def _bg_gradient(c: dict) -> str:
    return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {c['bg_top']}, stop:1 {c['bg_bottom']})"


def build_main_stylesheet(theme: str) -> str:
    c = get_theme_colors(theme)
    bg = _bg_gradient(c)
    return f"""
    QWidget#RootPanel {{
        background: {bg};
    }}
    QWidget#TitleBar {{
        border-bottom: 1px solid {c['border']};
    }}
    QLabel#BrandLabel {{
        color: {c['accent']};
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2.5px;
    }}
    QLabel#TitleLabel {{
        color: {c['fg']};
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
    }}
    QLabel#HintLabel {{
        color: {c['subtle']};
        font-size: 11px;
    }}
    QFrame#ImageCard {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 14px;
    }}
    QPushButton#CloseButton {{
        background-color: transparent;
        color: {c['subtle']};
        border: 1px solid {c['border']};
        font-size: 14px;
        font-weight: 700;
        border-radius: 15px;
    }}
    QPushButton#CloseButton:hover {{
        background-color: {c['accent']};
        color: #ffffff;
        border-color: {c['accent']};
    }}
    QPushButton#GearButton {{
        background-color: transparent;
        color: {c['subtle']};
        border: 1px solid {c['border']};
        font-size: 15px;
        border-radius: 15px;
    }}
    QPushButton#GearButton:hover {{
        color: {c['gold']};
        border-color: {c['gold']};
    }}
    QLabel#FlashbangImage {{
        background-color: transparent;
    }}
    """


def build_result_pill_stylesheet(tier: str, theme: str) -> str:
    """Patlama sonucu rozetinin ("Tebrikler — ...!") kademeye göre
    renklenen, vurgulu "epic" görünümünü üretir — ince renkli çerçeve,
    hafif renkli arkaplan (pill) ve nadirlik rengiyle eşleşen metin."""
    color = get_rarity_color(tier, theme)
    background = "rgba(255, 255, 255, 18)" if theme == "dark" else "rgba(0, 0, 0, 10)"
    return f"""
    QLabel#ResultLabel {{
        color: {color};
        background-color: {background};
        border: 1.5px solid {color};
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.3px;
    }}
    """


def build_dialog_stylesheet(theme: str) -> str:
    c = get_theme_colors(theme)
    bg = _bg_gradient(c)
    return f"""
    QDialog, QWidget#SettingsRoot {{
        background: {bg};
        color: {c['fg']};
    }}
    QWidget#DialogTitleBar {{
        border-bottom: 1px solid {c['border']};
    }}
    QLabel {{
        color: {c['fg']};
        font-size: 12px;
    }}
    QLabel#SettingsTitle {{
        color: {c['accent']};
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 1px;
    }}
    QLabel#SectionHeading {{
        color: {c['gold']};
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }}
    QFrame#SectionCard {{
        background-color: {c['card']};
        border: 1px solid {c['border']};
        border-radius: 12px;
    }}
    QComboBox, QSlider, QSpinBox {{
        background-color: {c['bg_bottom']};
        color: {c['fg']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 5px;
    }}
    QComboBox:hover {{
        border-color: {c['accent']};
    }}
    QComboBox QAbstractItemView {{
        background-color: {c['card']};
        color: {c['fg']};
        selection-background-color: {c['accent']};
        selection-color: #ffffff;
        outline: none;
    }}
    QSlider::groove:horizontal {{
        height: 4px;
        background: {c['border']};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {c['accent']};
        width: 15px;
        height: 15px;
        margin: -6px 0;
        border-radius: 7px;
        border: 2px solid {c['gold']};
    }}
    QSlider::sub-page:horizontal {{
        background: {c['accent']};
        border-radius: 2px;
    }}
    QPushButton {{
        background-color: {c['accent']};
        color: #ffffff;
        border: none;
        border-radius: 7px;
        padding: 8px 16px;
        font-weight: 700;
        font-size: 12.5px;
    }}
    QPushButton:hover {{
        background-color: {c['accent_hover']};
    }}
    QPushButton:pressed {{
        background-color: {c['accent_pressed']};
    }}
    QPushButton#SecondaryButton {{
        background-color: transparent;
        color: {c['subtle']};
        border: 1px solid {c['border']};
    }}
    QPushButton#SecondaryButton:hover {{
        color: {c['fg']};
        border-color: {c['accent']};
    }}
    QPushButton#IconButton {{
        background-color: transparent;
        color: {c['subtle']};
        border: 1px solid {c['border']};
        border-radius: 14px;
        font-size: 13px;
        font-weight: 700;
    }}
    QPushButton#IconButton:hover {{
        color: {c['gold']};
        border-color: {c['gold']};
    }}
    QFrame#SectionDivider {{
        background-color: {c['border']};
        max-height: 1px;
        border: none;
    }}
    """


LUCK_READY_GRADIENT = (
    "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
    f"stop:0 {BORDEAUX}, stop:0.55 {BORDEAUX_HOVER}, stop:1 {BORDEAUX})"
)
LUCK_ACTIVE_GRADIENT = (
    "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
    "stop:0 #157347, stop:0.55 #3ddc84, stop:1 #157347)"
)


def build_luck_button_stylesheet(theme: str, state: str) -> str:
    """'ready' | 'active' | 'cooldown' durumuna göre Şans Butonu stilini üretir."""
    c = get_theme_colors(theme)
    if state == "active":
        return f"""
        QPushButton#LuckButton {{
            background: {LUCK_ACTIVE_GRADIENT};
            color: #ffffff;
            border: 1px solid #0f5c38;
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 800;
            font-size: 13px;
        }}
        """
    if state == "cooldown":
        return f"""
        QPushButton#LuckButton {{
            background-color: {c['card']};
            color: {c['subtle']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 700;
            font-size: 13px;
        }}
        """
    return f"""
    QPushButton#LuckButton {{
        background: {LUCK_READY_GRADIENT};
        color: #ffffff;
        border: 1px solid {c['gold']};
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 800;
        font-size: 13px;
    }}
    QPushButton#LuckButton:hover {{
        border: 1.5px solid {c['gold']};
    }}
    """
