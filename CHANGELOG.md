# Changelog

Bu projedeki tüm önemli değişiklikler bu dosyada belgelenir.
Format [Keep a Changelog](https://keepachangelog.com/) temel alınarak
hazırlanmıştır ve bu proje [Semantic Versioning](https://semver.org/)
kullanır.

All notable changes to this project are documented in this file. The
format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

**[Türkçe](#türkçe) | [English](#english)**

---

## Türkçe

### [1.50V] - 2026-09-09

#### Eklendi
- Ses adları artık **yerelleştirilmiş** — ör. "Max Verstappen Telsizi"
  yalnızca Türkçe'de görünür, İngilizce'de "Max Verstappen Radio",
  Lehçe'de "Radio Max Verstappena", Rusça'da "Рация Макса Ферстаппена"
  olarak gösterilir. Tüm ses adları artık `core/i18n.py` üzerinden 4
  dilde de çevrilidir.
- **Ayrı, nadirliğe göre renklenen sonuç satırı**: Görsele tıklama
  talimatı ("Fitili çekmek için görsele tıkla") artık her zaman
  ekranda kalıyor; patlama sonucu ("Tebrikler — ...!") bunun ayrı bir
  satırında, nadirliğe göre renklenerek (Flashbang=gri, Az
  Bulunur=yeşil, Nadir=mavi, Epik=mor, Efsanevi=altın) gösteriliyor.
- `core/theme.py` içine `get_rarity_color()` ve Şans Butonu için
  duruma göre (hazır/aktif/bekleme) gradyanlı stil üreten
  `build_luck_button_stylesheet()` eklendi.
- Ayarlar penceresinde görsel iyileştirmeler: Hakkımızda erişimi artık
  başlık çubuğunda küçük bir **ℹ** simge butonu (tam genişlikte bir
  buton yerine); Şans Butonu artık duruma göre renk değiştiren
  (bordo → yeşil → gri) gradyanlı bir buton; bölümler arasına ince
  ayırıcı çizgiler eklendi.
- **Tüm arayüz "epic"/profesyonel bir tasarıma yeniden kavuşturuldu**:
  Ayarlar penceresindeki her bölüm (Dil & Görünüm / Patlama Süresi /
  Şans Sistemi) artık simgeli başlıklara sahip, ayrı "kart" panellerinde
  gruplanıyor; ana pencere ve diyaloglarda ince gradyanlı arkaplanlar,
  görsel etrafında kart çerçevesi, Hakkımızda'da altın çerçeveli dairesel
  logo ve bir sürüm rozeti eklendi.
- **Butonlara sembol eklendi** ki buton oldukları daha net anlaşılsın:
  Kaydet (✓), İptal (✕) metin butonlarına simge eklendi; dişli (⚙),
  kapatma (×) ve Hakkımızda (ℹ) simge butonları artık her zaman (yalnızca
  üzerine gelindiğinde değil) görünür bir daire çerçeveye sahip.
- Patlama sonucu mesajı artık çok daha vurgulu: nadirliğe göre renkli,
  kenarlıklı bir "rozet" (pill) içinde, daha büyük/kalın yazı tipiyle ve
  nadirliğe göre değişen bir kutlama simgesiyle (💥/✨/🌟/💫/👑) gösteriliyor.

#### Düzeltildi
- **Hakkımızda penceresinde iki ayrı kapatma butonu vardı** (başlık
  çubuğundaki "×" ve alttaki "Kapat" butonu) — kafa karıştırıcıydı;
  alttaki buton kaldırıldı, kapatma artık yalnızca başlık çubuğundaki
  tek "×" ile yapılıyor.

#### Değiştirildi
- **Şans/nadirlik sistemi tamamen "düz" (yuvarlak) oranlara geçirildi**:
  Az Bulunur = 1/100, Nadir = 1/1.000, Epik = 1/10.000, Efsanevi =
  1/100.000 — her rank kendi sabit oranını taşıyor (önceki, her sesin
  benzersiz ama "çirkin" bir kesre sahip olduğu sistemin yerine).
  Flashbang sesleri artık havuzun geri kalanını (~%97) temsil ediyor
  ve ekranda temiz bir kesre indirgenemediği için yüzde olarak
  gösteriliyor (ör. `%60`).
- Şans Butonu çarpanı 4'ten **10'a**, bekleme (cooldown) süresi 5
  dakikadan **4 dakikaya** çekildi.
- Sürüm numarası formatı `1.50V` olarak değiştirildi (4R022'nin diğer
  uygulamalarındaki `X.YV` kuralına uyumlu).

---

### [1.4.0] - 2026-09-08

#### Eklendi
- **Şans Butonu**: Ayarlar penceresinde, tıklandığında 1 dakika
  boyunca aktif olan, ardından 5 dakikalık bir bekleme (cooldown)
  süresine giren yeni bir sistem. Aktifken meme seslerinin ağırlığı
  4 katına çıkar (flashbang ağırlıkları değişmez), böylece nadir meme
  seslerinin çıkma ihtimali geçici olarak artar. Buton, kalan
  süreyi/bekleme zamanını canlı olarak gösterir.
- Yeni `core/luck_boost.py` modülü — sistem saatinden bağımsız
  (`time.monotonic()` tabanlı) durum makinesi.
- **Hakkımızda penceresi**: Ayarlar'dan erişilebilen yeni bir pencere;
  4R022 logosu, uygulama sürümü, geliştirici bilgisi ve uygulama ile
  şans sistemi hakkında kısa bir açıklama içerir (4 dilin tamamında).
- Ana pencerenin başlık çubuğuna küçük bir 4R022 logosu eklendi —
  logo artık pencere ikonu, Hakkımızda penceresi, başlık çubuğu ve
  README'de olmak üzere uygulamanın birden çok yerinde görünüyor.
- README'ye Windows/macOS'un eski uygulama ikonlarını önbellekte
  tutabileceğine (icon cache) dair bir not eklendi.

#### Değiştirildi
- **Ses havuzundaki HER ses artık tekil bir ağırlığa sahip** — iki
  flashbang sesi dahil, hiçbir iki ses birbiriyle tam olarak aynı
  düşme oranına sahip değil (`core/sound_pool.py`, toplam ağırlık artık
  122). Bu, "her patlamanın ve her meme sesinin kendi nadirliği olsun,
  hepsi aynı şansta olmasın" isteğini tam olarak karşılıyor.
- `roll_sound()` ve `odds_fraction()` artık isteğe bağlı bir
  `meme_multiplier` parametresi kabul ediyor (Şans Butonu tarafından
  kullanılıyor); ekranda gösterilen oran, roll anında gerçekten
  uygulanan çarpanı yansıtıyor.

#### Düzeltildi
- Ayarlar penceresindeki Şans Butonu metni Rusça'da buton genişliğini
  aşıp kırpılıyordu; buton metni kısaltıldı, süre/aktivasyon detayı
  zaten var olan alt açıklama metnine bırakıldı.

---

### [1.3.0] - 2026-09-07

#### Eklendi
- **Ses şans (loot/rarity) sistemi**: Patlama sesi artık oyunlardaki
  "roll" mekaniklerine benzer, ağırlıklı bir rastgelelik tablosuyla
  seçiliyor. 2 gerçek flashbang sesi (birleşik ~%50 şans) ve 5 nadirlik
  kademesine (Uncommon/Rare/Epic/Legendary) yayılmış 10 meme sesi
  (1/12 ile 1/40 arası). Patlama bitince ekranın altında gerçek düşme
  oranını gösteren bir sonuç mesajı beliriyor (ör. *"Tebrikler — 1/12
  Rastgele Meme! — Alarm"*), 4 dilin tamamında.
- Yeni `core/sound_pool.py` modülü — ses havuzu tanımı, ağırlıklı
  seçim (`roll_sound`) ve gerçek oran hesaplama (`odds_fraction`).
- README'ye tam "Ses Havuzu ve Şanslar" tablosu ve bir ses seviyesi
  uyarısı eklendi.

#### Değiştirildi
- Eski 2 patlama sesi tamamen kaldırıldı; yerine kullanıcı tarafından
  sağlanan 12 yeni ses eklendi (2 flashbang + 10 meme sesi). Gerekli
  olanların baştaki/sondaki sessiz boşlukları `ffmpeg` ile kırpıldı.
- `CREDITS.md` yeni ses havuzunu yansıtacak şekilde güncellendi.

#### Düzeltildi
- **Kritik build hatası:** `Build/build.bat` ve `Build/build.sh`,
  PyInstaller'ın geçici çalışma klasörü için `"build"` (küçük harf)
  adını kullanıyordu. Windows (NTFS) ve varsayılan macOS (APFS) dosya
  sistemleri büyük/küçük harf duyarsız olduğundan, bu klasör işletim
  sistemi tarafından projenin gerçek `Build/` klasörüyle (script'in
  kendisini içeren klasör) **aynı klasör** olarak görülüyordu.
  Betiğin başındaki temizlik adımı bu yüzden `Build/` klasörünün
  tamamını — betiğin kendisi dahil — siliyor, bu da çalışan komut
  dosyasının aniden sonlanmasına yol açıyordu. Çalışma klasörünün adı
  artık `_pyi_workcache` — hiçbir mevcut klasörle çakışmıyor.
- **Ses döngü zamanlama hassasiyeti:** `durationChanged` sinyali
  geldiğinde o ana kadar geçen çalma süresi (`position()`) hesaba
  katılmıyordu; bu da uzun gecikmelerde bir sonraki döngünün olması
  gerekenden geç başlamasına (fark edilir bir boşluğa) yol açabiliyordu.
  Artık kalan süre (`süre - geçen süre`) üzerinden hassas şekilde
  zamanlanıyor.
- **Pencere konumu ekran dışında kalma sorunu:** Kaydedilen pencere
  konumu, bir monitör söküldükten/çözünürlük değiştikten sonra artık
  hiçbir ekranda görünmeyebiliyordu (pencere "kayboluyordu"). Şimdi
  açılışta konumun hâlâ görünür bir ekranda olup olmadığı doğrulanıyor;
  değilse pencere otomatik olarak ortalanıyor.

---

### [1.2.0] - 2026-09-07

#### Eklendi
- Resmi 4R022 marka logosu projeye entegre edildi; tüm platform
  ikonları (`.ico`, `.icns`, `.png`) bu logodan yeniden üretildi.
- `LICENSE.md`, `CHANGELOG.md` ve `CREDITS.md` — profesyonel,
  GitHub'a uygun belgeler.
- `Main/` klasörü — uygulama giriş noktası artık `Main/main.py`
  altında, proje kökü daha düzenli.

#### Değiştirildi
- **Ses düzeltmesi:** Yüklenen ses dosyalarındaki baştaki boşluk/sessizlik
  (özellikle bir patlama sesinde ~1 saniyeye varan) `ffmpeg` ile tespit
  edilip kesildi; patlama artık gecikmeden başlıyor.
- **Döngü zamanlaması:** Patlama sesi, ayarlanan süreden kısa kaldığında
  artık kendi hassas zamanlayıcımızla, sesin gerçek süresine göre "tam
  bittiği an" yeniden başlıyor (önceden yalnızca Qt'nin EndOfMedia
  sinyaline bağlıydı, bu da fark edilir bir boşluğa yol açabiliyordu).
- **Görsel patlama efekti geliştirildi:** Açılış titreşimi artık çok
  aşamalı (anlık sıcak tonlu aşırı pozlama + kısa, hafif rastgele
  zamanlamalı strob), sönüş ise beyazdan sıcak "after-image" tonuna,
  oradan kül grisine ve siyaha yumuşak geçişli (ease/smoothstep) bir
  eğriyle gerçekleşiyor — gerçek bir flashbang sonrası göz kamaşması
  hissine daha yakın.
- **Build sistemi sadeleştirildi:** Ayrı bir `build.py` dosyasına artık
  gerek yok — tüm derleme/paketleme mantığı doğrudan `Build/build.bat`
  (Windows) ve `Build/build.sh` (macOS/Linux) içine taşındı. Her ikisi
  de kendi izole sanal ortamını (`Build/.venv`) hâlâ otomatik kurar.
- Sürüm numarası `1.2.0`'a yükseltildi.

#### Kaldırıldı
- `Build/build.py` (işlevi doğrudan `.bat`/`.sh` betiklerine taşındı).
- Build bağımlılıklarından `Pillow` (yalnızca ikon üretimi için
  kullanılıyordu; ikonlar artık statik varlık olarak depoda hazır).

---

### [1.1.0] - 2026-09-06

#### Eklendi
- **4 dil desteği**: Türkçe, English, Polski, Русский. Ayarlar
  penceresinden anında (yeniden başlatmadan) değiştirilebilir.
- `core/i18n.py` — merkezi çeviri modülü.
- Windows (`build.bat`) ve macOS/Linux (`build.sh`) için tek adımlı,
  otomatik (izole sanal ortam kuran) derleme betikleri.
- GitHub Actions iş akışı — 3 platform için otomatik derleme.

#### Değiştirildi
- Ayarlar penceresi dil, tema ve süre değişikliklerini anlık önizler.

---

### [1.0.0] - 2026-09-06

#### Eklendi
- İlk sürüm: PyQt6 tabanlı, Windows/macOS/Linux destekli flashbang
  efekti uygulaması.
- Ortada büyük flashbang görseli; tıklanınca fırlatma sesi → rastgele
  patlama sesi + tüm monitörleri kaplayan tam beyaz patlama efekti.
- Ayarlar: koyu/açık tema (yalnızca arkaplanı etkiler), patlama süresi
  (otomatik ses uzatma/loop ile).
- Çerçevesiz özel pencere tasarımı, ESC/× ile kapatma (patlama
  sırasında devre dışı).
- PyInstaller ile tek-dosya paketleme desteği.

#### Düzeltildi
- **Kritik ses kilitlenmesi (deadlock):** Ses fade-out'u için kullanılan
  hızlı, art arda `setVolume()` çağrılarının, ses aygıtı bulunamayan
  veya PulseAudio/PipeWire'a bağlanamayan sistemlerde Qt Multimedia/
  FFmpeg ses arka ucunu tamamen kilitlediği tespit edildi ve
  kaldırıldı; patlama sesi artık temiz bir şekilde duruyor.

---

## English

### [1.50V] - 2026-09-09

#### Added
- Sound names are now **localized** — e.g. "Max Verstappen Telsizi"
  only shows in Turkish, becoming "Max Verstappen Radio" in English,
  "Radio Max Verstappena" in Polish, "Рация Макса Ферстаппена" in
  Russian. All sound names are now translated across all 4 languages
  via `core/i18n.py`.
- **A separate, rarity-colored result line**: the click instruction
  ("Click the image to pull the pin") now always stays on screen; the
  explosion result ("Congrats — ...!") appears on its own line below
  it, colored by rarity (Flashbang=gray, Uncommon=green, Rare=blue,
  Epic=purple, Legendary=gold).
- Added `get_rarity_color()` and a state-aware (ready/active/cooldown)
  gradient stylesheet builder `build_luck_button_stylesheet()` to
  `core/theme.py`.
- Visual improvements to the Settings dialog: the About dialog is now
  reached via a small **ℹ** icon button in the title bar (instead of a
  full-width button); the Luck Button is now a gradient button that
  changes color by state (bordeaux → green → gray); thin section
  dividers were added between groups.
- **The entire UI was redesigned for an "epic"/professional look**:
  each Settings section (Language & Appearance / Flash Duration / Luck
  System) is now grouped into its own icon-headed "card" panel; the
  main window and dialogs gained subtle gradient backgrounds, a card
  frame around the image, a gold-ringed circular logo and a version
  badge in the About dialog.
- **Symbols were added to buttons** so they read clearly as buttons:
  Save (✓) and Cancel (✕) now show icons; the gear (⚙), close (×), and
  About (ℹ) icon buttons now always show a visible circular outline
  (not just on hover).
- The explosion result message is now much more emphasized: a
  rarity-colored, bordered "pill" badge, larger/bolder text, and a
  rarity-scaled celebration icon (💥/✨/🌟/💫/👑).

#### Fixed
- **The About dialog had two separate close buttons** (the title bar
  "×" and a bottom "Close" button) — confusing and redundant; the
  bottom button was removed, leaving only the single "×" in the title
  bar.

#### Changed
- **The rarity system now uses fully flat (round) odds**: Uncommon =
  1/100, Rare = 1/1,000, Epic = 1/10,000, Legendary = 1/100,000 — each
  rank carries a fixed rate (replacing the previous system where every
  sound had a unique but "unclean" fraction). Flashbang sounds now
  represent the pool's remainder (~97%) and are shown as a percentage
  on screen since that share can't be reduced to a clean fraction
  (e.g. `%60`).
- The Luck Button's multiplier went from 4 to **10**, and its cooldown
  from 5 minutes to **4 minutes**.
- The version number format changed to `1.50V` (matching the `X.YV`
  convention used by 4R022's other apps).

---

### [1.4.0] - 2026-09-08

#### Added
- **Luck Button**: a new system in Settings — clicking it activates a
  1-minute boost, followed by a 5-minute cooldown. While active, every
  meme sound's weight is multiplied by 4 (flashbang weights are
  untouched), temporarily raising the odds of rare meme sounds. The
  button shows the remaining time/cooldown live.
- New `core/luck_boost.py` module — a state machine based on
  `time.monotonic()`, independent of the system clock.
- **About dialog**: a new window accessible from Settings; shows the
  4R022 logo, app version, developer credit, and a short description
  of the app and its luck system (in all 4 languages).
- A small 4R022 logo was added to the main window's title bar — the
  logo now appears in multiple places across the app (window icon,
  About dialog, title bar) and the README.
- Added a README note about Windows/macOS potentially caching old app
  icons (icon cache).

#### Changed
- **Every sound in the pool now has a unique weight** — including the
  two flashbang sounds; no two sounds share the exact same odds
  (`core/sound_pool.py`, total weight is now 122). This fully satisfies
  the request that "every explosion and every meme sound has its own
  rarity, not all equal odds."
- `roll_sound()` and `odds_fraction()` now accept an optional
  `meme_multiplier` parameter (used by the Luck Button); the odds shown
  on screen reflect the multiplier that was actually applied at roll
  time.

#### Fixed
- The Luck Button's label overflowed its button width in Russian; the
  label was shortened, with the duration/activation detail left to the
  hint text below it (which already stated it).

---

### [1.3.0] - 2026-09-07

#### Added
- **Sound loot/rarity system**: the explosion sound is now chosen via
  a weighted-odds table, similar to "roll" mechanics in games. 2
  genuine flashbang sounds (~50% combined chance) and 10 meme sounds
  spread across 4 rarity tiers (Uncommon/Rare/Epic/Legendary, from
  1-in-12 down to 1-in-40). Once the flash ends, a result message
  appears at the bottom of the window showing the real odds (e.g.
  *"Congrats — 1/12 Random Meme! — Alarm"*), in all 4 languages.
- New `core/sound_pool.py` module — the sound pool definition, weighted
  selection (`roll_sound`), and real-odds computation (`odds_fraction`).
- A full "Sound Pool & Odds" table and a volume warning added to the
  README.

#### Changed
- The old 2 explosion sounds were fully removed and replaced with 12
  user-provided sounds (2 flashbang + 10 meme sounds). Leading/trailing
  silence was trimmed with `ffmpeg` where needed.
- `CREDITS.md` updated to reflect the new sound pool.

#### Fixed
- **Critical build bug:** `Build/build.bat` and `Build/build.sh` used
  `"build"` (lowercase) as PyInstaller's temporary work directory name.
  Since Windows (NTFS) and default macOS (APFS) filesystems are
  case-insensitive, the OS treated this as the **same folder** as the
  project's actual `Build/` directory (which contains the scripts
  themselves). The cleanup step at the start of the script therefore
  deleted the entire `Build/` folder — including the running script —
  causing the command window to terminate abruptly. The work directory
  is now named `_pyi_workcache`, which doesn't collide with anything.
- **Audio loop timing precision:** the elapsed playback time
  (`position()`) wasn't accounted for when the `durationChanged` signal
  arrived, which could make the next loop iteration start later than
  it should on longer delays (a perceptible gap). It's now scheduled
  precisely from the remaining time (`duration - elapsed`).
- **Window position could end up off-screen:** a saved window position
  could point nowhere visible after a monitor was disconnected or its
  resolution changed (the window would appear to "vanish"). On
  startup, the position is now checked against currently connected
  screens and re-centered automatically if it's no longer visible.

---

### [1.2.0] - 2026-09-07

#### Added
- The official 4R022 brand logo is now integrated into the project;
  all platform icons (`.ico`, `.icns`, `.png`) were regenerated from
  it.
- `LICENSE.md`, `CHANGELOG.md`, and `CREDITS.md` — professional,
  GitHub-friendly documentation.
- `Main/` folder — the entry point now lives at `Main/main.py`,
  keeping the project root cleaner.

#### Changed
- **Audio fix:** leading dead air in the uploaded sound files
  (up to ~1 second on one explosion sound) was detected and trimmed
  with `ffmpeg`; the explosion now starts without delay.
- **Loop timing:** when the explosion sound is shorter than the
  configured duration, it now restarts using our own precisely-timed
  scheduler based on the sound's real duration, right as it finishes
  (previously it relied solely on Qt's EndOfMedia signal, which could
  leave a perceptible gap).
- **Improved visual flash effect:** the opening flicker is now
  multi-stage (an instant warm-toned overexposure pulse plus a brief,
  lightly randomized strobe), and the fade-out eases from white
  through a warm "after-image" tone, into ash-grey, and finally black
  — closer to the flash-blindness feeling after a real flashbang.
- **Simplified build system:** a separate `build.py` file is no longer
  needed — all build/packaging logic now lives directly inside
  `Build/build.bat` (Windows) and `Build/build.sh` (macOS/Linux). Both
  still automatically set up their own isolated virtual environment
  (`Build/.venv`).
- Version bumped to `1.2.0`.

#### Removed
- `Build/build.py` (its logic moved directly into the `.bat`/`.sh`
  scripts).
- `Pillow` from build dependencies (it was only used for one-time icon
  generation; icons now ship as static assets in the repo).

---

### [1.1.0] - 2026-09-06

#### Added
- **4-language support**: Turkish, English, Polish, Russian.
  Switchable instantly from Settings, no restart needed.
- `core/i18n.py` — the central translation module.
- One-step, automated build scripts for Windows (`build.bat`) and
  macOS/Linux (`build.sh`), each setting up its own isolated virtual
  environment.
- GitHub Actions workflow — automated builds for all 3 platforms.

#### Changed
- The Settings dialog now live-previews language, theme, and duration
  changes.

---

### [1.0.0] - 2026-09-06

#### Added
- Initial release: a PyQt6-based flashbang effect app supporting
  Windows, macOS, and Linux.
- A large flashbang image in the center; clicking it plays a throw
  sound → a randomly chosen explosion sound plus a full-white flash
  covering every connected monitor.
- Settings: dark/light theme (background only), configurable flash
  duration (with automatic audio loop/extend).
- Custom frameless window design, closable via ESC/× (disabled during
  the flash).
- PyInstaller-based onefile packaging support.

#### Fixed
- **Critical audio deadlock:** rapid, repeated `setVolume()` calls used
  for an audio fade-out were found to completely hang the Qt
  Multimedia/FFmpeg audio backend on systems with no audio device or
  an unreachable PulseAudio/PipeWire service; this was removed, and
  the explosion sound now stops cleanly instead.
