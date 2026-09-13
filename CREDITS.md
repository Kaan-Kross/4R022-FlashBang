# Credits & Acknowledgments / Teşekkürler

**[Türkçe](#türkçe) | [English](#english)**

---

## Türkçe

4R022 FlashBang, aşağıdaki kaynaklar ve araçlar olmadan mümkün
olmazdı. Bu içerikleri sağlayan/geliştiren herkese teşekkür ederiz.

### Ses Efektleri

- **Fırlatma sesi** — *"Throwing Flashbang Sound Effect (CS:GO) —
  made with Voicemod"*. [Voicemod](https://www.voicemod.net/) ile
  işlenmiş bir ses efekti kullanılmıştır.

**Patlama ses havuzu** (bkz. `core/sound_pool.py` — tam şans/rarity
tablosu için README'ye bakın) — internette yaygın olarak paylaşılan,
tek bir üreticiye net şekilde atfedilemeyen meme/ses klipleridir; yine
de kaynağı olan herkese teşekkür ederiz:

- **Flashbang** (×2, "Common" kademe) — gerçek flashbang/stun grenade
  ses efektleri.
- **AK-47**, **Alarm**, **Metal Boru** ("Uncommon" kademe) — yaygın
  silah/uyarı sesi klipleri.
- **Meme Patlaması**, **Roblox Oof** ("Rare" kademe) — internet
  meme kültüründen tanıdık efektler (Roblox'un klasik "oof" ölüm sesi
  dahil).
- **What Is Love**, **Max Verstappen Telsiz** ("Epic" kademe) —
  sırasıyla Haddaway'in *"What Is Love"* şarkısına dayanan meme kesiti
  ve Formula 1 pilotu Max Verstappen'in ikonikleşmiş takım telsizi
  anına gönderme yapan bir ses klibi.
- **Whopper Reklamı**, **Asansör Müziği**, **Gizemli Ton**
  ("Legendary" kademe) — Burger King "Whopper" reklamına dayanan bir
  bas-boost edit, jenerik asansör müziği ve kaynağı belirsiz kısa bir
  ton klibi.

Tüm ses dosyaları uygulamaya entegre edilmeden önce (baştaki/sondaki
sessiz boşlukları kaldırmak amacıyla, gerekli olanlarda) kırpılmış ve
yeniden kodlanmıştır; özgün içerik ve telif hakları kendi
sahiplerine/kaynaklarına aittir. Bu ses klipleri yalnızca eğlence
amaçlı, ticari olmayan bir bağlamda kullanılmaktadır.

### Görseller

- **Flashbang (stun grenade) referans görseli** — uygulamanın ana
  ekranında kullanılan stok/referans ürün fotoğrafı, yalnızca arayüz
  amaçlı kullanılmıştır.
- **4R022 marka logosu** — Kaan Kross / 4R022 için özel olarak
  üretilmiştir; tüm platform uygulama ikonları bu logodan türetilmiştir.

### Kullanılan Açık Kaynak Araçlar ve Kütüphaneler

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** —
  arayüz, çoklu ortam (ses) ve pencere yönetimi.
- **[PyInstaller](https://pyinstaller.org/)** — tek dosyalık
  yürütülebilir paketleme.
- **[FFmpeg](https://ffmpeg.org/)** — geliştirme sürecinde ses
  dosyalarının sessiz bölümlerinin tespiti ve kırpılması için
  kullanılmıştır; PyQt6'nın çoklu ortam arka ucu olarak da görev
  yapar.
- **Python** ve geniş açık kaynak ekosistemi.

### Özel Teşekkür

Bu projeyi test eden, geri bildirim veren ve fikir katkısında bulunan
herkese; ayrıca kullandığımız ve projeye yüklediğimiz tüm ses ve
görsel varlıkların özgün üreticilerine içtenlikle teşekkür ederiz.
Bu materyaller olmasaydı proje bu haliyle var olamazdı.

---

## English

4R022 FlashBang would not have been possible without the following
resources and tools. Thank you to everyone who provided or built
them.

### Sound Effects

- **Throw sound** — *"Throwing Flashbang Sound Effect (CS:GO) — made
  with Voicemod"*. A sound effect processed with
  [Voicemod](https://www.voicemod.net/).

**Explosion sound pool** (see `core/sound_pool.py` — full rarity/odds
table in the README) — these are widely circulated internet meme/sound
clips with no single clearly attributable creator; we're grateful to
whoever originated each one nonetheless:

- **Flashbang** (×2, "Common" tier) — genuine flashbang/stun grenade
  sound effects.
- **AK-47**, **Alarm**, **Metal Pipe** ("Uncommon" tier) — familiar
  weapon/warning sound clips.
- **Meme Explosion**, **Roblox Oof** ("Rare" tier) — recognizable
  internet meme-culture effects, including Roblox's classic "oof"
  death sound.
- **What Is Love**, **Max Verstappen Radio** ("Epic" tier) — a meme
  edit based on Haddaway's *"What Is Love"*, and a sound clip
  referencing Formula 1 driver Max Verstappen's famous team radio
  moment, respectively.
- **Whopper Ad**, **Elevator Music**, **Mystery Tone** ("Legendary"
  tier) — a bass-boosted edit of a Burger King "Whopper" ad, generic
  elevator music, and a short tone clip of unclear origin.

All sound files were trimmed and re-encoded where needed before being
bundled with the app (to remove leading/trailing silence); original
content and copyrights belong to their respective owners/sources.
These clips are used purely for entertainment, in a non-commercial
context.

### Images

- **Flashbang (stun grenade) reference image** — a stock/reference
  product photo used in the app's main screen for UI purposes only.
- **4R022 brand logo** — custom-made for Kaan Kross / 4R022; all
  platform app icons are derived from it.

### Open-Source Tools & Libraries Used

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** —
  UI, multimedia (audio), and window management.
- **[PyInstaller](https://pyinstaller.org/)** — onefile executable
  packaging.
- **[FFmpeg](https://ffmpeg.org/)** — used during development to
  detect and trim silence in the sound assets; also powers PyQt6's
  multimedia backend at runtime.
- **Python** and its broader open-source ecosystem.

### Special Thanks

Thank you to everyone who tested this project, gave feedback, or
contributed ideas — and sincere thanks to the original creators of
every sound and image asset we used and uploaded here. This project
wouldn't exist in its current form without that work.
