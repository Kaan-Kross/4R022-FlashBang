"""
4R022 FlashBang - Ses Havuzu ve Şans (Rarity) Sistemi
Kaan Kross / 4R022

Patlama anında çalınacak ses, oyunlardaki "roll" / "loot" sistemleri
gibi ağırlıklı (weighted) rastgelelik ile seçilir. Nadirlik, DÜZ
(temiz, yuvarlak) şans skalalarına dayanır — her "rank" (kademe) kendi
sabit oranını taşır:

    Flashbang  → geri kalanın tamamı (baskın, "olağan" sonuç)
    Uncommon   → 1/100
    Rare       → 1/1.000
    Epic       → 1/10.000
    Legendary  → 1/100.000

Bu tablo, uygulama içinde patlama sonrası gösterilen "Tebrikler X/Y ...!"
mesajı için de kullanılır — meme sesleri için gösterilen kesir, gerçekte
uygulanan ağırlıktan matematiksel olarak hesaplanır (uydurma değildir).
Flashbang sonucu için (payı çok büyük ve "temiz" bir kesre indirgenemediği
için) yüzde olarak gösterilir.

Şans Butonu (bkz. core/luck_boost.py) aktifken, "meme" kategorisindeki
tüm seslerin ağırlığı MEME_BOOST_MULTIPLIER ile çarpılır.

The sound played on explosion is chosen via weighted randomness, like a
loot/roll system in games. Rarity is based on FLAT, round odds scales —
each rank carries a fixed rate:

    Flashbang  → whatever remains (the dominant, "normal" outcome)
    Uncommon   → 1/100
    Rare       → 1/1,000
    Epic       → 1/10,000
    Legendary  → 1/100,000

This table also backs the "Congrats X/Y ...!" message shown after the
explosion — for meme sounds the displayed fraction is computed from the
actual configured weight (never made up). The flashbang result is shown
as a percentage instead, since its share is the (non-round) remainder
of the pool rather than a designed clean fraction.

While the Luck Boost (see core/luck_boost.py) is active, every "meme"
sound's weight is scaled up by MEME_BOOST_MULTIPLIER.
"""

from __future__ import annotations

import math
import random
from typing import List, Tuple, TypedDict

from core.i18n import t
from core.resources import resource_path


class SoundEntry(TypedDict):
    file: str
    name_key: str  # core.i18n çeviri anahtarı (yerelleştirilmiş ses adı için)
    tier: str  # "flashbang" | "uncommon" | "rare" | "epic" | "legendary"
    category: str  # "flashbang" | "meme" — mesaj metninde kullanılan üst kategori
    weight: int


# Temiz şans skalası için ortak taban: 1.000.000 (10^6).
# Common base for the clean odds scale: 1,000,000 (10^6).
_SCALE = 1_000_000

# Rank başına DÜZ (round) oran — bkz. modül docstring'i.
_RANK_ODDS = {
    "uncommon": 100,       # 1/100
    "rare": 1_000,         # 1/1,000
    "epic": 10_000,        # 1/10,000
    "legendary": 100_000,  # 1/100,000
}

SOUND_POOL: List[SoundEntry] = [
    # --- Flashbang — baskın/olağan sonuç; ikisi de farklı ağırlıkta ---
    {"file": "loud-flashbang.mp3", "name_key": "sound_flashbang", "tier": "flashbang", "category": "flashbang", "weight": 600_000},
    {"file": "loud-flash-bang.mp3", "name_key": "sound_flashbang", "tier": "flashbang", "category": "flashbang", "weight": 367_770},

    # --- Meme: Uncommon (1/100) ---
    {"file": "ak47-loud.mp3", "name_key": "sound_ak47", "tier": "uncommon", "category": "meme", "weight": _SCALE // _RANK_ODDS["uncommon"]},
    {"file": "warning-alarm-loud-af.mp3", "name_key": "sound_alarm", "tier": "uncommon", "category": "meme", "weight": _SCALE // _RANK_ODDS["uncommon"]},
    {"file": "loud-metal-pipe-loud.mp3", "name_key": "sound_metal_pipe", "tier": "uncommon", "category": "meme", "weight": _SCALE // _RANK_ODDS["uncommon"]},

    # --- Meme: Rare (1/1.000) ---
    {"file": "explosion-meme.mp3", "name_key": "sound_meme_explosion", "tier": "rare", "category": "meme", "weight": _SCALE // _RANK_ODDS["rare"]},
    {"file": "new-oooof-sound-from-roblox.mp3", "name_key": "sound_roblox_oof", "tier": "rare", "category": "meme", "weight": _SCALE // _RANK_ODDS["rare"]},

    # --- Meme: Epic (1/10.000) ---
    {"file": "what-is-love-loud.mp3", "name_key": "sound_what_is_love", "tier": "epic", "category": "meme", "weight": _SCALE // _RANK_ODDS["epic"]},
    {"file": "tu-tu-tu-du-max-verstappen.mp3", "name_key": "sound_verstappen_radio", "tier": "epic", "category": "meme", "weight": _SCALE // _RANK_ODDS["epic"]},

    # --- Meme: Legendary (1/100.000) — en nadirler ---
    {"file": "whopper-ad-bass-boosted.mp3", "name_key": "sound_whopper_ad", "tier": "legendary", "category": "meme", "weight": _SCALE // _RANK_ODDS["legendary"]},
    {"file": "musica-elevador-short_CNEma6b.mp3", "name_key": "sound_elevator_music", "tier": "legendary", "category": "meme", "weight": _SCALE // _RANK_ODDS["legendary"]},
    {"file": "tunez-audiotrimmer.mp3", "name_key": "sound_mystery_tone", "tier": "legendary", "category": "meme", "weight": _SCALE // _RANK_ODDS["legendary"]},
]

TOTAL_WEIGHT = sum(entry["weight"] for entry in SOUND_POOL)
assert TOTAL_WEIGHT == _SCALE, (
    f"SOUND_POOL agirliklari {_SCALE} taban degerine tam oturmali (su an {TOTAL_WEIGHT})"
)

# Şans Butonu aktifken meme seslerinin ağırlığı bu kadar katlanır.
# While the Luck Button is active, meme sound weights are multiplied by this.
MEME_BOOST_MULTIPLIER = 10


def get_sound_display_name(entry: SoundEntry, lang: str) -> str:
    """Sesin, seçilen dile göre yerelleştirilmiş görünen adını döndürür."""
    return t(entry["name_key"], lang)


def get_sound_path(entry: SoundEntry) -> str:
    return resource_path(f"assets/sounds/{entry['file']}")


def _effective_weights(meme_multiplier: float = 1.0) -> Tuple[List[float], float]:
    weights = [
        entry["weight"] * (meme_multiplier if entry["category"] == "meme" else 1.0)
        for entry in SOUND_POOL
    ]
    return weights, sum(weights)


def roll_sound(meme_multiplier: float = 1.0) -> SoundEntry:
    """Ağırlıklara göre rastgele bir ses seçer (oyunlardaki 'loot roll' gibi).

    meme_multiplier > 1.0 iken (Şans Butonu aktif), meme sesleri orantılı
    olarak daha olası hale gelir; flashbang ağırlıkları değişmez.
    """
    weights, _ = _effective_weights(meme_multiplier)
    return random.choices(SOUND_POOL, weights=weights, k=1)[0]


def odds_fraction(entry: SoundEntry, meme_multiplier: float = 1.0) -> str:
    """Meme sesleri için: GERÇEKTE uygulanan (varsa şans artırımı dahil)
    düşme oranını sadeleştirilmiş, temiz bir kesir olarak döndürür
    (ör. '1/100'). Rank tasarımı gereği bu her zaman düz bir sayıdır."""
    weights, total = _effective_weights(meme_multiplier)
    index = SOUND_POOL.index(entry)
    weight = weights[index]

    scale = 1000
    weight_i = round(weight * scale)
    total_i = round(total * scale)
    divisor = math.gcd(weight_i, total_i) or 1
    numerator = weight_i // divisor
    denominator = total_i // divisor
    return f"{numerator}/{denominator}"


def odds_percentage(entry: SoundEntry, meme_multiplier: float = 1.0) -> str:
    """Flashbang sonucu için: havuzun geri kalanını temsil eden, temiz bir
    kesre indirgenemeyen payı, okunaklı bir yüzde olarak döndürür (ör. '%60')."""
    weights, total = _effective_weights(meme_multiplier)
    index = SOUND_POOL.index(entry)
    weight = weights[index]
    percentage = (weight / total) * 100 if total else 0.0
    return f"%{percentage:.1f}".rstrip("0").rstrip(".")


_MAX_CLEAN_DENOMINATOR = 100_000


def format_meme_odds(entry: SoundEntry, meme_multiplier: float = 1.0) -> str:
    """Meme sesleri için ekranda gösterilecek oranı seçer: normalde temiz
    bir kesir (ör. '1/1000'). Ancak Şans Butonu aktifken payda artık
    'düz' bir sayı olmayabilir (ör. 10000/129007) — bu durumda okunabilir
    bir yüzdeye düşer.

    For meme sounds, picks the odds string to display: normally a clean
    fraction (e.g. '1/1000'). But while the Luck Button is active the
    denominator may no longer be a round number (e.g. 10000/129007) — in
    that case it falls back to a readable percentage instead.
    """
    fraction = odds_fraction(entry, meme_multiplier)
    denominator = int(fraction.split("/")[1])
    if denominator > _MAX_CLEAN_DENOMINATOR:
        return odds_percentage(entry, meme_multiplier)
    return fraction
