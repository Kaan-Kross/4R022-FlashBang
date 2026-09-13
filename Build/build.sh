#!/usr/bin/env bash
# ============================================================
# 4R022 FlashBang - macOS / Linux Otomatik Derleme
# Kaan Kross / 4R022
#
# Bu betiği çalıştırmanız yeterlidir — başka hiçbir dosyaya
# ihtiyaç duymaz. Sırasıyla:
#   1) Build/.venv altında izole bir sanal ortam oluşturur
#      (sistem Python'ınıza dokunmaz),
#   2) gerekli bağımlılıkları (PyQt6, PyInstaller) o ortama kurar,
#   3) PyInstaller ile tek-dosya bir yürütülebilir üretir,
#   4) sonucu Build/dist_packages/ altına sürümlü bir ZIP olarak
#      paketler.
#
# Just run this script — it needs no other file. It will:
#   1) create an isolated virtual environment under Build/.venv
#      (never touches your system Python),
#   2) install the required dependencies (PyQt6, PyInstaller)
#      into it,
#   3) build a onefile executable with PyInstaller,
#   4) package the result as a versioned ZIP under
#      Build/dist_packages/.
#
# Kullanım / Usage:
#   chmod +x Build/build.sh   (yalnızca ilk seferde / first time only)
#   ./Build/build.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

VENV_DIR="Build/.venv"
SPEC_FILE="Build/4R022_FlashBang.spec"
# ONEMLI: "build" ismini KULLANMAYIN — Windows (NTFS) ve varsayilan
# macOS (APFS) dosya sistemleri buyuk/kucuk harf duyarsizdir, yani
# "build" ve "Build" AYNI klasor olarak gorulur. Asagidaki temizlik
# adimi bu klasoru silseydi, projenin gercek "Build/" klasorunu
# (bu betiğin kendisi dahil) silerdi.
#
# IMPORTANT: do NOT use the name "build" — Windows (NTFS) and default
# macOS (APFS) filesystems are case-INsensitive, so "build" and
# "Build" resolve to the SAME folder. If the cleanup step below
# deleted this, it would delete the project's actual "Build/" folder
# (including this very script).
DIST_DIR="dist"
WORK_DIR="_pyi_workcache"
PACKAGES_DIR="Build/dist_packages"
APP_NAME="4R022FlashBang"

echo ""
echo "=== 4R022 FlashBang - macOS/Linux Derleme ==="
echo ""

# ---------------------------------------------------------------- Python
PYTHON_BIN=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON_BIN="$candidate"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "[HATA] Python bulunamadi. Lutfen Python 3.10 veya ustunu kurun."
    echo "[ERROR] Python not found. Please install Python 3.10 or newer."
    exit 1
fi

# ------------------------------------------------------------- Sanal ortam
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Sanal ortam olusturuluyor / Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    echo "[1/4] Mevcut sanal ortam kullaniliyor / Reusing existing virtual environment..."
fi

VENV_PY="$VENV_DIR/bin/python"
if [ ! -x "$VENV_PY" ]; then
    VENV_PY="$VENV_DIR/Scripts/python.exe"
fi

# ------------------------------------------------------------ Bagimliliklar
echo ""
echo "[2/4] Bagimliliklar kuruluyor / Installing dependencies..."
"$VENV_PY" -m pip install --upgrade pip >/dev/null
"$VENV_PY" -m pip install -r "requirements.txt" -r "Build/requirements-build.txt"

# ------------------------------------------------------------------- Derle
echo ""
echo "[3/4] Uygulama PyInstaller ile derleniyor / Building with PyInstaller..."
rm -rf "$DIST_DIR" "$WORK_DIR"
"$VENV_PY" -m PyInstaller "$SPEC_FILE" --noconfirm --clean --distpath "$DIST_DIR" --workpath "$WORK_DIR"

# ---------------------------------------------------------------- Paketle
echo ""
echo "[4/4] Paketleniyor / Packaging..."

VERSION="$("$VENV_PY" -c "import sys; sys.path.insert(0, '.'); from core.version import __version__; print(__version__)")"

case "$(uname -s)" in
    Darwin*) PLATFORM_TAG="macos" ;;
    Linux*)  PLATFORM_TAG="linux" ;;
    *)       PLATFORM_TAG="unknown" ;;
esac

mkdir -p "$PACKAGES_DIR"
ZIP_NAME="4R022-FlashBang-v${VERSION}-${PLATFORM_TAG}.zip"
ZIP_PATH="$PACKAGES_DIR/$ZIP_NAME"
rm -f "$ZIP_PATH"

if [ "$PLATFORM_TAG" = "macos" ] && [ -d "$DIST_DIR/${APP_NAME}.app" ]; then
    BUILD_OUTPUT="$DIST_DIR/${APP_NAME}.app"
else
    BUILD_OUTPUT="$DIST_DIR/${APP_NAME}"
fi

if [ ! -e "$BUILD_OUTPUT" ]; then
    echo "[HATA] Beklenen derleme ciktisi bulunamadi: $BUILD_OUTPUT"
    echo "[ERROR] Expected build output not found: $BUILD_OUTPUT"
    exit 1
fi

if command -v zip >/dev/null 2>&1; then
    (cd "$DIST_DIR" && zip -rq "../$ZIP_PATH" "$(basename "$BUILD_OUTPUT")")
    echo ""
    echo "=== Tamamlandi! Paket: $ZIP_PATH ==="
    echo "=== Done! Package: $ZIP_PATH ==="
else
    echo "[UYARI] 'zip' komutu bulunamadi, otomatik paketleme atlaniyor."
    echo "[WARNING] 'zip' command not found, skipping automatic packaging."
    echo "Derlenen dosya burada / The built output is here: $BUILD_OUTPUT"
fi
echo ""
