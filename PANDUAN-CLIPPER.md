# ✂️ Panduan Clipper — Buat Uang

Clipper memotong video panjang (podcast, live streaming, webinar) menjadi beberapa **klip pendek vertikal bersubtitle** untuk TikTok, Reels, dan Shorts.

```
Video panjang ──► Transkripsi (Whisper) ──► Pilih momen (AI / manual) ──► Potong + ubah ke 9:16 ──► Subtitle ──► Klip siap upload
```

---

## ⚠️ Hak Cipta — Baca Dulu

Gunakan Clipper **hanya untuk**:
- video **milikmu sendiri**, atau
- video yang **pemiliknya sudah memberi izin**, misalnya order clipping dari kreator, program clipper resmi, atau konten berlisensi Creative Commons yang mengizinkan modifikasi.

Memotong video orang lain tanpa izin bisa berakibat:
- **YouTube Content ID:** pemilik bisa mengambil pendapatan iklan klipmu, memblokir video, atau mengajukan takedown yang berujung **copyright strike**. Tiga strike membuat **channel dihapus**.
- **Monetisasi ditolak:** YouTube Partner Program bisa menolak channel yang isinya mayoritas potongan video orang lain ("reused content").
- **TikTok / Instagram / Facebook:** tidak ada bagi hasil seperti Content ID. Klip biasanya di-mute, diturunkan, atau akun kena pelanggaran.

**Tips untuk order dari kreator:** simpan bukti izin (chat atau kontrak), dan cantumkan kredit ke channel asli di deskripsi klip.

Mengunduh dari YouTube juga diatur oleh ketentuan layanan YouTube. Unduh hanya video yang memang boleh kamu pakai.

---

## 1. Persiapan

Clipper sudah ikut terpasang lewat `pip install -r requirements.txt` (termasuk `yt-dlp` untuk link YouTube). Untuk **mode AI** dan **subtitle**, pasang juga Whisper:

```bash
pip install -r requirements-whisper.txt
```

Tanpa Whisper, Clipper tetap bisa dipakai dengan **timestamp manual tanpa subtitle**.

**LLM untuk mode AI** memakai pengaturan di halaman utama (LLM Provider + API Key). Semua pilihan gratis di [PANDUAN-GRATIS-DAN-KUALITAS.md](PANDUAN-GRATIS-DAN-KUALITAS.md#3-cara-gratis-mendapatkan-naskah) bisa dipakai, **kecuali** cara copy-paste, karena di sini AI perlu membaca transkrip secara otomatis.

---

## 2. Cara Pakai

1. Jalankan WebUI (`webui.bat` / `sh webui.sh`).
2. Di sidebar kiri, buka halaman **Clipper**.
3. **Sumber video**, pilih salah satu:

   | Pilihan | Kapan dipakai |
   |---------|---------------|
   | **Link YouTube** | Tempel link video. Video diunduh otomatis (pilih kualitas 1080p/720p/480p). |
   | **File lokal (path)** | **Untuk video besar.** Tempel lokasi file, misalnya `D:\Podcast\episode-01.mp4`. File dibaca langsung dari lokasinya, tidak diunggah. Di Windows: tahan **Shift**, klik kanan file → **Copy as path**, lalu tempel (tanda kutipnya tidak masalah). |
   | **Upload** | Hanya untuk file kecil (maks. 200 MB). |

4. **Pilih momen:**
   - **AI pilih otomatis:** atur jumlah klip (1–10) dan durasi per klip (misalnya 20–60 detik). AI membaca transkrip lalu memilih momen dengan hook kuat, fakta menarik, tips jelas, atau momen lucu/emosional. Batas klip otomatis digeser ke awal/akhir kalimat supaya tidak terpotong di tengah kata.
   - **Timestamp manual:** tulis satu klip per baris. Cocok kalau kreator sudah menentukan momennya.
     ```
     12:30 - 13:15 Tips hemat listrik
     1:02:10 - 1:03:00 Cerita lucu
     ```
5. **Format & subtitle:** pilih rasio (9:16, 1:1, 16:9), lalu aktifkan subtitle dan atur font, ukuran, posisi, dan warna.
6. Klik **✂️ Buat Klip**. Hasilnya bisa diputar dan diunduh langsung, dan tersimpan di `storage/clips/<id>/`.

---

## 3. Yang Perlu Diketahui

### Kecepatan
Bagian paling lama adalah **transkripsi Whisper**. Di CPU, model default `large-v3` bisa memakan waktu lebih lama dari durasi videonya sendiri. Pilihan:
- Ganti `model_size` di bagian `[whisper]` pada `config.toml` ke `"medium"` atau `"small"`. Jauh lebih cepat, sedikit kurang akurat.
- Punya GPU NVIDIA? Set `device = "cuda"` dan `compute_type = "float16"`.
- Pakai **timestamp manual tanpa subtitle**, yang tidak butuh transkripsi sama sekali.

### Rasio 9:16 memotong bagian tengah
Video landscape dipotong **di tengah frame**. Ini cocok untuk podcast satu kamera dengan pembicara di tengah, tapi kurang pas kalau dua orang duduk di kiri dan kanan. Untuk kasus itu, pilih **16:9** (video diberi bingkai hitam) atau **1:1**. Fitur mengikuti wajah pembicara belum ada.

### Link YouTube gagal diunduh
YouTube sering mengubah sistemnya. Kalau unduhan gagal, perbarui yt-dlp:
```bash
pip install -U yt-dlp
```
Video privat, video dengan batas usia, atau video yang butuh login bisa tetap gagal. Unduh manual, lalu pakai **File lokal (path)**.

### Transkrip sangat panjang
Untuk video sangat panjang, transkrip dibagi menjadi beberapa bagian sebelum dikirim ke AI, lalu kandidat terbaik dari semua bagian digabung berdasarkan skor. Model lokal kecil (Ollama) dengan konteks pendek bisa menghasilkan pilihan yang kurang bagus. Kalau begitu, pakai Gemini atau model yang lebih besar.

### Menjalankan lewat Docker
Di dalam container, **File lokal (path)** hanya bisa membaca file di dalam folder repo (dipasang sebagai `/MoneyPrinterTurbo`). Taruh video di folder `storage/` lalu tulis path seperti `/MoneyPrinterTurbo/storage/episode-01.mp4`.

---

## 4. Checklist Sebelum Upload Klip

- [ ] Ada izin dari pemilik video (atau videonya milikmu sendiri)
- [ ] Kredit ke channel asli dicantumkan di deskripsi
- [ ] Klip dimulai dengan hook dan berakhir di poin yang selesai
- [ ] Subtitle sinkron dan tidak menutupi wajah
- [ ] Pembicara tidak terpotong di frame 9:16
