@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: 4R022 FlashBang - Windows Otomatik Derleme
:: Kaan Kross / 4R022
::
:: Bu betiğe çift tıklamanız yeterlidir — başka hiçbir dosyaya
:: ihtiyaç duymaz. Sırasıyla:
::   1) Build\.venv altında izole bir sanal ortam oluşturur
::      (sistem Python'ınıza dokunmaz),
::   2) gerekli bağımlılıkları (PyQt6, PyInstaller) o ortama kurar,
::   3) PyInstaller ile tek-dosya bir .exe üretir,
::   4) sonucu Build\dist_packages\ altına sürümlü bir ZIP olarak
::      paketler (PowerShell Compress-Archive ile).
::
:: Just double-click this file — it needs no other file. It will:
::   1) create an isolated virtual environment under Build\.venv
::      (never touches your system Python),
::   2) install the required dependencies (PyQt6, PyInstaller)
::      into it,
::   3) build a onefile .exe with PyInstaller,
::   4) package the result as a versioned ZIP under
::      Build\dist_packages\ (via PowerShell Compress-Archive).
:: ============================================================

cd /d "%~dp0\.."

set VENV_DIR=Build\.venv
set SPEC_FILE=Build\4R022_FlashBang.spec
:: ONEMLI: "build" ismini KULLANMAYIN — Windows'ta (NTFS) dosya sistemi
:: buyuk/kucuk harf duyarsizdir, yani "build" ve "Build" AYNI klasor
:: olarak gorulur. Asagidaki temizlik adimi bu klasoru silseydi,
:: projenin gercek "Build\" klasorunu (bu betiğin kendisi dahil) silerdi
:: ve calisan komut dosyasi kendi altindan silindigi icin cmd.exe
:: aniden kapanirdi.
::
:: IMPORTANT: do NOT use the name "build" — Windows (NTFS) is
:: case-INsensitive, so "build" and "Build" resolve to the SAME
:: folder. If the cleanup step below deleted this, it would delete the
:: project's actual "Build\" folder (including this very script), and
:: cmd.exe would abruptly terminate since its running script vanished.
set DIST_DIR=dist
set WORK_DIR=_pyi_workcache
set PACKAGES_DIR=Build\dist_packages
set APP_NAME=4R022FlashBang

echo.
echo === 4R022 FlashBang - Windows Derleme ===
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [HATA] Python bulunamadi. Lutfen https://python.org adresinden
    echo Python 3.10 veya ustunu kurup PATH'e ekleyin ^(kurulumda
    echo "Add python.exe to PATH" secenegini isaretleyin^).
    echo [ERROR] Python not found. Please install Python 3.10+ from
    echo https://python.org and check "Add python.exe to PATH" during setup.
    if not defined CI pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [1/4] Sanal ortam olusturuluyor / Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [HATA] Sanal ortam olusturulamadi.
        if not defined CI pause
        exit /b 1
    )
) else (
    echo [1/4] Mevcut sanal ortam kullaniliyor / Reusing existing virtual environment...
)

set VENV_PY=%VENV_DIR%\Scripts\python.exe

echo.
echo [2/4] Bagimliliklar kuruluyor / Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip >nul
"%VENV_PY%" -m pip install -r "requirements.txt" -r "Build\requirements-build.txt"
if errorlevel 1 (
    echo [HATA] Bagimlilik kurulumu basarisiz oldu.
    if not defined CI pause
    exit /b 1
)

echo.
echo [3/4] Uygulama PyInstaller ile derleniyor / Building with PyInstaller...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%WORK_DIR%" rmdir /s /q "%WORK_DIR%"
"%VENV_PY%" -m PyInstaller "%SPEC_FILE%" --noconfirm --clean --distpath "%DIST_DIR%" --workpath "%WORK_DIR%"
if errorlevel 1 (
    echo [HATA] Derleme basarisiz oldu.
    if not defined CI pause
    exit /b 1
)

echo.
echo [4/4] Paketleniyor / Packaging...

for /f "delims=" %%V in ('"%VENV_PY%" -c "import sys; sys.path.insert(0, '.'); from core.version import __version__; print(__version__)"') do set VERSION=%%V

if not exist "%PACKAGES_DIR%" mkdir "%PACKAGES_DIR%"
set ZIP_NAME=4R022-FlashBang-v%VERSION%-windows.zip
set ZIP_PATH=%PACKAGES_DIR%\%ZIP_NAME%
if exist "%ZIP_PATH%" del /q "%ZIP_PATH%"

if not exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo [HATA] Beklenen derleme ciktisi bulunamadi: %DIST_DIR%\%APP_NAME%.exe
    echo [ERROR] Expected build output not found: %DIST_DIR%\%APP_NAME%.exe
    if not defined CI pause
    exit /b 1
)

powershell -NoProfile -Command "Compress-Archive -Path '%DIST_DIR%\%APP_NAME%.exe' -DestinationPath '%ZIP_PATH%' -Force"
if errorlevel 1 (
    echo [UYARI] ZIP paketleme basarisiz oldu. Derlenen .exe burada: %DIST_DIR%\%APP_NAME%.exe
    echo [WARNING] ZIP packaging failed. The built .exe is here: %DIST_DIR%\%APP_NAME%.exe
    if not defined CI pause
    exit /b 0
)

echo.
echo === Tamamlandi! Paket: %ZIP_PATH% ===
echo === Done! Package: %ZIP_PATH% ===
echo.
if not defined CI pause
