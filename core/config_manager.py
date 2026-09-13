"""
4R022 FlashBang - Config Manager
Kaan Kross / 4R022

Kalıcı ayarları platforma özgü kullanıcı veri dizininde, atomik JSON
yazma (+ .bak yedek) yöntemiyle saklar.

Persists settings in a platform-specific user data directory using
atomic JSON writes (with a .bak backup).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

from core.i18n import DEFAULT_LANGUAGE, normalize_language

APP_NAME = "4R022FlashBang"

DEFAULT_CONFIG: Dict[str, Any] = {
    "theme": "dark",              # "dark" (siyah) veya "light" (beyaz)
    "flash_duration_ms": 3000,    # patlama (beyaz ekran) süresi, ms
    "volume": 1.0,                # 0.0 - 1.0 arası ana ses seviyesi
    "window_pos": None,           # [x, y] ya da None (ortala)
    "language": DEFAULT_LANGUAGE,  # "tr" | "en" | "pl" | "ru"
}

MIN_FLASH_DURATION_MS = 500
MAX_FLASH_DURATION_MS = 15000


def get_user_data_dir() -> Path:
    """Platforma özgü kullanıcı veri dizinini döndürür ve oluşturur."""
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        path = Path(base) / APP_NAME
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
        path = Path(base) / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


class ConfigManager:
    """Ayarları okuyup yazan, atomik yazma ve yedekleme yapan sınıf."""

    def __init__(self) -> None:
        self.config_path = get_user_data_dir() / "config.json"
        self._data: Dict[str, Any] = dict(DEFAULT_CONFIG)
        self.load()

    def load(self) -> None:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                merged = dict(DEFAULT_CONFIG)
                merged.update({k: v for k, v in loaded.items() if k in DEFAULT_CONFIG})
                self._data = merged
                self._sanitize()
                return
            except (json.JSONDecodeError, OSError):
                backup_path = self.config_path.with_suffix(".json.bak")
                if backup_path.exists():
                    try:
                        with open(backup_path, "r", encoding="utf-8") as f:
                            loaded = json.load(f)
                        merged = dict(DEFAULT_CONFIG)
                        merged.update(
                            {k: v for k, v in loaded.items() if k in DEFAULT_CONFIG}
                        )
                        self._data = merged
                        self._sanitize()
                        return
                    except (json.JSONDecodeError, OSError):
                        pass
        self._data = dict(DEFAULT_CONFIG)
        self._sanitize()

    def _sanitize(self) -> None:
        self._data["theme"] = "light" if self._data.get("theme") == "light" else "dark"
        try:
            duration = int(self._data.get("flash_duration_ms", DEFAULT_CONFIG["flash_duration_ms"]))
        except (TypeError, ValueError):
            duration = DEFAULT_CONFIG["flash_duration_ms"]
        self._data["flash_duration_ms"] = max(
            MIN_FLASH_DURATION_MS, min(MAX_FLASH_DURATION_MS, duration)
        )
        try:
            volume = float(self._data.get("volume", DEFAULT_CONFIG["volume"]))
        except (TypeError, ValueError):
            volume = DEFAULT_CONFIG["volume"]
        self._data["volume"] = max(0.0, min(1.0, volume))
        pos = self._data.get("window_pos")
        if not (isinstance(pos, list) and len(pos) == 2):
            self._data["window_pos"] = None
        self._data["language"] = normalize_language(
            self._data.get("language", DEFAULT_LANGUAGE)
        )

    def save(self) -> None:
        """Atomik yazma: geçici dosyaya yaz, eskisini .bak yap, sonra taşı."""
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(self.config_path.parent), prefix="config_", suffix=".tmp"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix(".json.bak")
                shutil.copyfile(self.config_path, backup_path)
            os.replace(tmp_path, self.config_path)
        except OSError:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        if key not in DEFAULT_CONFIG:
            raise KeyError(f"Bilinmeyen ayar anahtarı: {key}")
        self._data[key] = value
        self._sanitize()
        self.save()

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)
