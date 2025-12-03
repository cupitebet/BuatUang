# 📖 Panduan Lengkap untuk Pemula - Buat Uang

**Panduan ini dibuat khusus untuk pemula yang ingin membuat video otomatis dengan AI, tanpa perlu pengetahuan teknis yang mendalam.**

> **Buat Uang** adalah generator video otomatis berbasis AI (MoneyPrinterTurbo) yang sudah dilokalisasi untuk Indonesia.

---

## 📋 Daftar Isi

1. [Apa itu MoneyPrinterTurbo?](#apa-itu-moneyprinterturbo)
2. [Spesifikasi Komputer](#spesifikasi-komputer)
3. [Alat dan Bahan yang Dibutuhkan](#alat-dan-bahan-yang-dibutuhkan)
4. [Cara Install - Step by Step](#cara-install-step-by-step)
5. [Cara Menggunakan](#cara-menggunakan)
6. [Troubleshooting](#troubleshooting)
7. [FAQ - Pertanyaan Umum](#faq-pertanyaan-umum)

---

## 🎯 Apa itu Buat Uang?

**Buat Uang** adalah aplikasi yang bisa membuat video pendek secara otomatis dengan bantuan AI. Aplikasi ini berbasis MoneyPrinterTurbo yang sudah dilokalisasi untuk Indonesia dengan panduan lengkap dalam Bahasa Indonesia.

### Cara Kerjanya:
```
Anda → Berikan Topik → AI Proses → Video Jadi!
```

**Contoh:**
- Input: "Manfaat Olahraga"
- Output: Video 60 detik dengan narasi, gambar, subtitle, dan musik!

### Untuk Apa?
- ✅ Konten TikTok, Instagram Reels, YouTube Shorts
- ✅ Video promosi produk
- ✅ Video edukasi
- ✅ Video motivasi
- ✅ Dan lain-lain!

---

## 💻 Spesifikasi Komputer

### Spesifikasi Minimum (Budget)

| Komponen | Minimum | Rekomendasi |
|----------|---------|-------------|
| **Processor** | Intel Core i3 / AMD Ryzen 3 (4 core) | Intel Core i5 / AMD Ryzen 5 |
| **RAM** | 4 GB | 8 GB atau lebih |
| **Storage** | 10 GB tersedia | 20 GB SSD |
| **Internet** | Koneksi stabil | Min. 5 Mbps |
| **GPU** | Tidak wajib | Bonus untuk proses lebih cepat |
| **OS** | Windows 10/11, MacOS 11+, Linux | Windows 10/11 (paling mudah) |

### Contoh Laptop yang Cocok:
- **Budget (3-5 juta)**: ASUS VivoBook, Lenovo IdeaPad 3, HP 14s
- **Mid-range (5-8 juta)**: Acer Swift 3, ASUS ZenBook, Lenovo Yoga
- **High-end (8 juta+)**: MacBook Air M1, ASUS ROG, Dell XPS

**Catatan:** Laptop/PC kantor biasa umumnya sudah cukup!

---

## 🛠️ Alat dan Bahan yang Dibutuhkan

### 1. Software yang Harus Diinstall

#### A. Python 3.11 (Gratis)
**Apa itu?** Bahasa pemrograman yang dibutuhkan aplikasi ini.

**Download:**
- Windows: https://www.python.org/downloads/
- **⚠️ SANGAT PENTING untuk Windows: Download versi 64-bit!**
  - Klik "Download Python 3.11.x"
  - Pilih: `Windows installer (64-bit)` atau file `python-3.11.x-amd64.exe`
  - JANGAN download versi 32-bit!
- **PENTING**: Saat install, centang "Add Python to PATH"!

**Cara Cek Sudah Terinstall:**
```bash
# Buka Command Prompt (Windows) atau Terminal (Mac/Linux)
python --version
# Harus muncul: Python 3.11.x

# Cek 64-bit (PENTING untuk Windows!)
python -c "import platform; print(platform.architecture())"
# Harus muncul: ('64bit', ...) ✅
# Jika muncul ('32bit', ...) → Install ulang Python 64-bit!
```

**❌ Jika Dapat Error saat Install Dependencies:**
Lihat: [SOLUSI-ERROR-WINDOWS.md](SOLUSI-ERROR-WINDOWS.md)

#### B. Git (Gratis)
**Apa itu?** Tool untuk download source code dari internet.

**Download:**
- Windows: https://git-scm.com/download/win
- Mac: Sudah built-in atau `brew install git`
- Linux: `sudo apt install git`

#### C. ImageMagick (Gratis)
**Apa itu?** Tool untuk membuat subtitle di video.

**Download Windows:**
1. Kunjungi: https://imagemagick.org/script/download.php
2. Pilih: `ImageMagick-7.1.1-32-Q16-x64-static.exe` (HARUS yang static!)
3. Install ke lokasi default
4. JANGAN ubah path instalasi!

**Download Mac:**
```bash
brew install imagemagick
```

**Download Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install imagemagick

# CentOS/Fedora
sudo yum install ImageMagick
```

---

### 2. API Keys (Beberapa Gratis, Beberapa Bayar)

#### A. Pexels API Key ⭐ **WAJIB & GRATIS**

**Untuk Apa?** Download video/gambar material berkualitas HD.

**Cara Daftar:**
1. Buka: https://www.pexels.com/
2. Klik "Sign Up" (pojok kanan atas)
3. Daftar dengan email (atau Google/Facebook)
4. Setelah login, buka: https://www.pexels.com/api/
5. Klik "Get Started" atau "Generate API Key"
6. Copy API Key yang muncul
7. Simpan di notepad!

**Biaya:** 100% GRATIS! (200 request per jam)

---

#### B. LLM Provider ⭐ **WAJIB (Ada Gratis & Bayar)**

**Untuk Apa?** AI yang membuat naskah video.

**Pilihan Provider:**

##### Option 1: DeepSeek (Recommended untuk Indonesia) 💰 Murah
- **Harga:** $0.14 per 1 juta token (super murah!)
- **Trial:** Dapat kredit gratis saat daftar
- **Cara Daftar:**
  1. Buka: https://platform.deepseek.com/
  2. Sign up dengan email
  3. Verify email
  4. Ke "API Keys"
  5. Generate API key
  6. Copy dan simpan!

##### Option 2: Google Gemini 🆓 Gratis (Limited)
- **Harga:** GRATIS (ada limit per hari)
- **Cara Daftar:**
  1. Buka: https://makersuite.google.com/app/apikey
  2. Login dengan Google account
  3. Klik "Create API Key"
  4. Copy dan simpan!

##### Option 3: OpenAI 💰 Bayar (Kualitas Terbaik)
- **Harga:** Pay as you go (sekitar $2-5 untuk 100 video)
- **Cara Daftar:**
  1. Buka: https://platform.openai.com/
  2. Sign up
  3. Top up minimal $5
  4. Generate API key

**Rekomendasi untuk Pemula:**
- Mulai dengan **Google Gemini** (gratis untuk testing)
- Kalau mau kualitas bagus: **DeepSeek** (murah)
- Kalau budget besar: **OpenAI** (terbaik)

---

### 3. Optional (Tidak Wajib)

#### Azure Speech API
- Untuk suara yang lebih natural
- Ada free tier: 500,000 karakter per bulan
- Daftar: https://azure.microsoft.com/free/

---

## 📥 Cara Install - Step by Step

### Langkah 1: Install Software Prerequisites

**1. Install Python 3.11**
```bash
# Download dari: https://www.python.org/downloads/
# PENTING: Centang "Add Python to PATH" saat install!
```

**2. Install Git**
```bash
# Download dari: https://git-scm.com/
```

**3. Install ImageMagick**
```bash
# Download dari: https://imagemagick.org/script/download.php
# Pilih versi "static"
```

---

### Langkah 2: Download MoneyPrinterTurbo

**Buka Command Prompt (Windows) atau Terminal (Mac/Linux)**

```bash
# 1. Pindah ke folder Downloads (atau folder lain yang Anda inginkan)
cd Downloads

# 2. Download Buat Uang source code
git clone https://github.com/cupitebet/BuatUang.git

# 3. Masuk ke folder
cd BuatUang
```

---

### Langkah 3: Install Dependencies Python

```bash
# 1. Buat virtual environment (opsional tapi recommended)
python -m venv venv

# 2. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install semua library yang dibutuhkan (proses ini 5-10 menit)
pip install -r requirements.txt
```

**Tunggu sampai selesai!** Akan download 100+ packages.

---

### Langkah 4: Setup Konfigurasi

```bash
# 1. Copy file contoh konfigurasi
cp config.example.toml config.toml

# 2. Edit file config.toml
# Windows: notepad config.toml
# Mac: open -a TextEdit config.toml
# Linux: nano config.toml
```

**Isi yang WAJIB diubah:**

```toml
# 1. Masukkan Pexels API Key
pexels_api_keys = ["PASTE_API_KEY_PEXELS_DISINI"]

# 2. Pilih LLM Provider (pilih salah satu)
llm_provider = "gemini"  # atau "deepseek" atau "openai"

# 3. Isi API Key sesuai provider yang dipilih

# Jika pakai Google Gemini:
gemini_api_key = "PASTE_API_KEY_GEMINI_DISINI"

# Jika pakai DeepSeek:
deepseek_api_key = "PASTE_API_KEY_DEEPSEEK_DISINI"

# Jika pakai OpenAI:
openai_api_key = "PASTE_API_KEY_OPENAI_DISINI"
```

**Simpan file!**

---

### Langkah 5: Test Instalasi

```bash
# Cek apakah config berhasil
python -c "from app.config import config; print('✅ Config OK!')"
```

Jika muncul "✅ Config OK!" berarti instalasi berhasil!

---

## 🎬 Cara Menggunakan

### Metode 1: Web Interface (Paling Mudah untuk Pemula)

**1. Jalankan Web UI:**

```bash
# Windows
webui.bat

# Mac/Linux
sh webui.sh
```

**2. Buka Browser:**

Otomatis akan terbuka browser ke: http://localhost:8501

**3. Isi Form:**

| Field | Isi | Contoh |
|-------|-----|--------|
| **Video Subject** | Topik video | "Manfaat Olahraga untuk Kesehatan" |
| **Language** | Bahasa narasi | Indonesian (id-ID) |
| **Voice** | Pilih suara | id-ID-ArdiNeural (pria) atau id-ID-GadisNeural (wanita) |
| **Video Aspect** | Ukuran video | 9:16 (vertical untuk TikTok) atau 16:9 (horizontal untuk YouTube) |
| **Paragraph Number** | Jumlah paragraf | 2-3 untuk video 30-60 detik |
| **Enable Subtitle** | Subtitle | ON (recommended) |

**4. Klik "Generate Video"**

**5. Tunggu 5-15 menit**

Proses:
```
[1/5] Generating script... ⏳
[2/5] Finding video materials... 🎬
[3/5] Generating voice... 🎙️
[4/5] Generating subtitles... 📝
[5/5] Composing final video... 🎥
✅ Done!
```

**6. Download Video**

Klik tombol download setelah selesai!

---

### Metode 2: Command Line (Untuk yang Lebih Advanced)

```bash
# Jalankan API server
python main.py

# Buka browser ke: http://localhost:8080/docs
# Gunakan Swagger UI untuk test API
```

---

## 🐛 Troubleshooting

### ⚠️ ERROR WINDOWS: "Could not find a version that satisfies the requirement onnxruntime"

**Penyebab:** Python yang terinstall adalah versi 32-bit (harus 64-bit)

**Solusi Lengkap:** 📖 **[Baca SOLUSI-ERROR-WINDOWS.md](SOLUSI-ERROR-WINDOWS.md)**

**Quick Fix:**
1. Uninstall Python 32-bit
2. Download Python 64-bit: https://www.python.org/downloads/
   - Pilih file: `python-3.11.x-amd64.exe`
3. Install dengan centang "Add Python to PATH"
4. Cek: `python -c "import platform; print(platform.architecture())"`
   - Harus: `('64bit', ...)` ✅
5. Install ulang: `pip install -r requirements.txt`

---

### Problem 1: "Python not found"

**Solusi:**
```bash
# Cek apakah Python terinstall
python --version

# Jika tidak ketemu, install Python dan centang "Add to PATH"
```

---

### Problem 2: "ImageMagick not found"

**Solusi:**
```bash
# Download ImageMagick versi STATIC
# Install ke lokasi default
# Edit config.toml:
imagemagick_path = "C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"
```

---

### Problem 3: "No ffmpeg found"

**Solusi:**
```bash
# Download ffmpeg dari: https://www.gyan.dev/ffmpeg/builds/
# Extract file
# Edit config.toml:
ffmpeg_path = "C:\\path\\to\\ffmpeg.exe"
```

---

### Problem 4: "API Key Invalid"

**Solusi:**
1. Cek API key sudah benar (tidak ada spasi)
2. Cek format: `api_key = "xxxxxxx"` (pakai tanda kutip)
3. Cek API key masih aktif di dashboard provider

---

### Problem 5: "Video Generation Failed"

**Solusi:**
1. Cek koneksi internet
2. Cek API key masih punya quota
3. Cek log error di terminal
4. Coba topik video yang lebih sederhana

---

## ❓ FAQ - Pertanyaan Umum

### Q1: Berapa biaya untuk membuat 1 video?

**A:** Tergantung provider LLM:
- **Google Gemini (gratis):** Rp 0
- **DeepSeek:** ~Rp 50-100 per video
- **OpenAI:** ~Rp 200-500 per video
- **Pexels (video material):** GRATIS selamanya!

---

### Q2: Berapa lama proses generate 1 video?

**A:** 5-15 menit tergantung:
- Panjang video (paragraph number)
- Kecepatan internet
- Spesifikasi komputer

---

### Q3: Apakah bisa generate video dalam bahasa Indonesia?

**A:** ✅ YES! Sudah support penuh:
- Voice Indonesia: `id-ID-ArdiNeural` (pria), `id-ID-GadisNeural` (wanita)
- Script dalam bahasa Indonesia
- Subtitle bahasa Indonesia

---

### Q4: Apakah video yang dihasilkan bisa langsung diupload?

**A:** ✅ YES!
- Video HD quality (1080p)
- Format MP4
- Siap upload ke TikTok, Instagram, YouTube
- Bebas royalti (material dari Pexels)

---

### Q5: Apakah bisa kustomisasi video?

**A:** ✅ YES! Bisa custom:
- ✅ Naskah video (tulis sendiri)
- ✅ Video material (pakai video lokal)
- ✅ Background music (pakai musik sendiri)
- ✅ Font subtitle
- ✅ Warna subtitle
- ✅ Posisi subtitle

---

### Q6: Apakah legal untuk monetisasi?

**A:** ✅ YES!
- Video material dari Pexels/Pixabay: bebas royalti
- Voice dari Edge TTS: boleh digunakan komersial
- Script dari AI: Anda yang punya hak cipta

**Catatan:** Cek terms & conditions masing-masing platform tempat upload.

---

### Q7: Apakah perlu coding untuk pakai ini?

**A:** ❌ TIDAK!
- Pakai Web UI (no coding)
- Tinggal klik-klik
- Isi form
- Generate!

---

### Q8: Berapa video maksimal per hari?

**A:** Tergantung limit API:
- **Pexels:** 200 request/jam (bisa ratusan video)
- **Google Gemini:** ~50-100 video/hari (gratis)
- **DeepSeek/OpenAI:** Unlimited (bayar per usage)

---

### Q9: Apakah bisa batch generate banyak video sekaligus?

**A:** ✅ YES!
- Set "Video Count" di Web UI
- Aplikasi akan generate beberapa variasi
- Pilih yang terbaik

---

### Q10: Apakah data aman?

**A:** ✅ YES!
- Semua proses di komputer Anda
- API key tersimpan lokal
- Video tersimpan lokal
- Tidak ada upload ke server pihak ketiga

---

## 🎓 Tips untuk Pemula

### 1. Mulai dengan Topik Sederhana
```
✅ Good: "5 Manfaat Minum Air Putih"
❌ Too complex: "Analisis Mendalam Geopolitik Asia Tenggara"
```

### 2. Test dengan Video Pendek Dulu
```
Paragraph: 2-3 (sekitar 30-60 detik)
Durasi pendek = proses cepat = testing cepat
```

### 3. Pakai Voice Preview
```
Di Web UI ada tombol "Preview Voice"
Test dulu sebelum generate video!
```

### 4. Save API Key di Tempat Aman
```
Jangan share API key ke siapapun!
Simpan di password manager
```

### 5. Join Community
```
- GitHub Issues: https://github.com/harry0703/MoneyPrinterTurbo/issues
- Tanya jawab dengan pengguna lain
- Share hasil video Anda!
```

---

## 🚀 Next Steps

Setelah instalasi berhasil:

1. ✅ **Generate video pertama** dengan topik sederhana
2. ✅ **Eksperimen** dengan berbagai voice dan setting
3. ✅ **Upload** ke TikTok/Instagram/YouTube
4. ✅ **Analisa** mana yang paling engaging
5. ✅ **Iterate** dan improve!

---

## 📞 Butuh Bantuan?

- 📖 **Dokumentasi Lengkap:** Baca [SETUP-ID.md](SETUP-ID.md)
- 🐛 **Report Bug:** https://github.com/harry0703/MoneyPrinterTurbo/issues
- 💬 **Diskusi:** GitHub Discussions
- 📧 **Email:** Lihat di repository

---

## 🎉 Selamat Mencoba!

Sekarang Anda siap membuat video otomatis dengan AI!

**Remember:**
- 🎯 Start small, think big
- 💪 Practice makes perfect
- 🚀 Consistency is key
- 🎨 Be creative!

**Happy video making! 🎬✨**

---

*Dibuat dengan ❤️ untuk komunitas Indonesia*
