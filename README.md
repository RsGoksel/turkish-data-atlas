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

**345 kaynak** · 286 Hugging Face + 59 GitHub / kurum / web · doğrulama 2026-08-16

## Neden bir liste daha

Mevcut listeler kartın iddia ettiği sayıyı kopyalıyor. Buradaki her rakam ölçüldü:

- **Boyutlar** Hugging Face `datasets-server` `/size` ucundan geldi, kart beyanından değil.
- **Her bağlantı istendi.** Ölü olan üç HF deposu ve beş dış kaynak listeye girmedi.
- **Çokdilli korpuslar işaretli.** Boyutları tüm dillerin boyutudur. Bu ayrım yapılmazsa
  toplam 158 TB görünüyor; gerçekten tek-dilli Türkçe veri **4,29 TB** (129 set).
- **Lisans duruşu** her satırda: ticari kullanıma açık (161), ticari-olmayan (33),
  doğrulanamadı (151).

## Kapsam

| kategori | kayıt |
|---|---:|
| Konuşma (ASR, TTS) | 133 |
| Metin / LLM | 198 |
| Görüntü (OCR, VQA) | 14 |

Görüntü tarafı şu an ince ve büyük ölçüde OCR ağırlıklı. Katkıya en açık bölüm orası.

## Veri

Katalogun tamamı tek dosyada: [`datasets.json`](datasets.json). Sayfa onu render eder,
dolayısıyla yeni bir veri seti eklemek bir JSON kaydı eklemek demektir.

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
