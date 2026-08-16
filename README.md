---
title: Turkish Data Atlas
emoji: 🧭
colorFrom: blue
colorTo: gray
sdk: static
app_file: index.html
pinned: false
license: mit
---

# Turkish Data Atlas

Türkçe konuşma, görüntü ve metin veri setlerinin tek yerden, **doğrulanmış** dizini.
A single verified index of Turkish speech, vision and text datasets.

**v1 — 116 kaynak · 1,29 TB** · doğrulama 2026-08-16

| sürüm | kayıt | dili Türkçe beyan edilmiş | konuşma | metin / LLM | görüntü |
|---|---:|---:|---:|---:|---:|
| **v1** | **116** | **1,29 TB** | 52 | 52 | 12 |
| v2 | 226 | 1,76 TB | 107 | 107 | 12 |
| v3 | 336 | 1,78 TB | 143 | 181 | 12 |

Sonraki sürümü açmak: `python tools/release.py --stage 2`

## Hacim üç kovaya ayrılır

Bu ayrım katalogun asıl işi. Tek bir "toplam TB" rakamı yanıltıcı olur:

| kova | set | hacim |
|---|---:|---:|
| dili yalnızca `tr` beyan edilmiş | 70 | **1,78 TB** |
| dil beyanı hiç olmayan | 54 | 0,39 TB |
| çokdilli, Türkçe içeren | 122 | 153 TB — *tüm dillerin*, Türkçe payı ayrıştırılamıyor |

Dili beyan edilmiş Türkçe veri 1,78 TB. Ham toplam 155 TB görünür, ama o hacmin
neredeyse tamamı FineWeb2, HPLT, CulturaX gibi çokdilli korpuslardır ve Türkçe payı
bu setlerden ayrıştırılamaz.

Ayrıca dili Türkçe içermediği doğrulanan 9 kayıt katalogdan çıkarıldı — aralarında
2,12 TB'lık `MLCommons/peoples_speech` (İngilizce) ve `facebook/voxpopuli` (16 AB dili,
Türkçe yok) vardı. Bunlar Türkçe kataloglarında dolaşıyordu.

## Neden bir liste daha

Mevcut listeler kartın iddia ettiği sayıyı kopyalıyor. Buradaki her rakam ölçüldü:

- **Boyutlar** Hugging Face `datasets-server` `/size` ucundan geldi, kart beyanından değil.
- **Her bağlantı istendi.** Ölü olan üç HF deposu ve beş dış kaynak listeye girmedi.
- **Çokdilli korpuslar işaretli.** Boyutları tüm dillerin boyutudur. Bu ayrım yapılmazsa
  toplam 158 TB görünüyor; gerçekten tek-dilli Türkçe veri **4,29 TB** (129 set).
- **Lisans duruşu** her satırda: ticari kullanıma açık (161), ticari-olmayan (33),
  doğrulanamadı (151).

## Kapsam

Doğrulanmış toplam **345 kaynak** — 286 Hugging Face deposu, 59 GitHub / kurum / web
kaynağı. Sayfada o an yayında olan bölüm gösterilir; tümü `datasets.full.json` içindedir.

Görüntü tarafı ince ve büyük ölçüde OCR ağırlıklı. Katkıya en açık bölüm orası, ve v3
yalnızca mevcut kayıtları açmakla kalmayıp o boşluğu doldurmayı hedefliyor.

## Veri

İki dosya var. [`datasets.full.json`](datasets.full.json) doğrulanmış katalogun tamamını
tutar ve hiç küçülmez; her kayıtta bir `release` alanı vardır.
[`datasets.json`](datasets.json) ise sayfanın okuduğu, o anki sürüme kadar açılmış olan
alt kümedir ve `tools/release.py` tarafından üretilir. Yeni bir veri seti eklemek, tam
dosyaya bir JSON kaydı eklemek demektir.

Her kayıt: `id · url · host · modality · task · desc · license · posture · bytes · rows ·
downloads · multilingual · n_langs · verified`.

## Katkı

Eksik ya da bayat bir satır için
[GitHub'da PR açın](https://github.com/RsGoksel/turkish-data-atlas). Yeni kayıtta
en azından bağlantı ve modality gerekir; boyut ve lisans bir sonraki doğrulama turunda
API'den çekilir.

## Lisans

Katalogun kendisi MIT. Listelenen veri setlerinin lisansları kendilerine aittir ve
`license` sütununda gösterilir; ticari kullanımdan önce kaynağın kendi kartını okuyun.

[Kadir Göksel Gündüz](https://gokselgunduz.com/) · ITU Energy Institute
