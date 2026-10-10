# 🚀 Panduan Setup Buat Uang

Dokumentasi lengkap setup dan penggunaan **Buat Uang** (Generator Video Otomatis dengan AI) untuk pemula.

> Berbasis MoneyPrinterTurbo

---

## ✅ Kebutuhan & Konfigurasi yang Disarankan

### Kebutuhan
- **Python 3.11** (64-bit). Versi yang lebih baru belum tentu didukung semua paket.
- `pip install -r requirements.txt`. **ImageMagick tidak perlu diinstal.**
- Opsional, hanya untuk subtitle mode whisper: `pip install -r requirements-whisper.txt`

### Konfigurasi Awal (gratis)
- **Pexels API key** (gratis): wajib, untuk klip video
- **Naskah:** copy-paste dari ChatGPT/Claude, **Ollama**, atau **Gemini free tier**. Lihat **[PANDUAN-GRATIS-DAN-KUALITAS.md](PANDUAN-GRATIS-DAN-KUALITAS.md)**
- **Voice/TTS:** Edge TTS (gratis)
- **Subtitle:** `edge` (gratis)

---

## 📋 Cara Menjalankan Aplikasi

### 1️⃣ Jalankan API Server

```bash
python main.py
```

Setelah jalan, API akan tersedia di:
- **Docs**: http://127.0.0.1:8080/docs
- **Alternative Docs**: http://127.0.0.1:8080/redoc

### 2️⃣ Jalankan Web UI

#### Windows:
```bash
webui.bat
```

#### Linux/MacOS:
```bash
sh webui.sh
```

Web UI akan otomatis terbuka di browser di: http://localhost:8501

---

## 🎬 Cara Membuat Video Pertama

### Via Web UI (Recommended untuk Pemula)

1. **Buka Web UI**: http://localhost:8501
2. **Isi Form**:
   - **Video Subject**: Contoh: "Manfaat Olahraga untuk Kesehatan"
   - **Language**: Pilih "Indonesian" atau "English"
   - **Video Size**: Pilih 9:16 (vertical) atau 16:9 (horizontal)
   - **Voice**: Pilih suara yang diinginkan
3. **Klik Generate Video**
4. **Tunggu proses** (~5-10 menit untuk video pendek)
5. **Download video** yang sudah jadi

### Via API

**POST** ke `http://127.0.0.1:8080/api/v1/video/generate`

Body (JSON):
```json
{
  "video_subject": "Manfaat Olahraga untuk Kesehatan",
  "video_language": "id-ID",
  "paragraph_number": 3,
  "video_aspect": "9:16",
  "voice_name": "id-ID-ArdiNeural"
}
```

---

## 🔧 Troubleshooting

### Error: "No ffmpeg exe could be found"

**Solusi**:
1. Download ffmpeg dari: https://www.gyan.dev/ffmpeg/builds/
2. Extract file
3. Edit `config.toml`:
```toml
ffmpeg_path = "C:\\path\\to\\ffmpeg.exe"  # Windows
# atau
ffmpeg_path = "/usr/local/bin/ffmpeg"     # Linux/Mac
```

### ImageMagick

Tidak perlu diinstal. Versi ini (moviepy 2.x) merender subtitle dengan Pillow.

### Error: "LLM API Error"

Kalau masih memakai **g4f**, ganti provider: g4f sudah tidak berfungsi (error *"No provider found"*) dan melanggar ketentuan layanan penyedia AI. Pilihan gratis ada di [PANDUAN-GRATIS-DAN-KUALITAS.md](PANDUAN-GRATIS-DAN-KUALITAS.md#3-cara-gratis-mendapatkan-naskah). Pilihan berbayar:

1. **Pakai DeepSeek** (Recommended):
   - Daftar: https://platform.deepseek.com/
   - Get API key
   - Edit `config.toml`:
   ```toml
   llm_provider = "deepseek"
   deepseek_api_key = "YOUR_API_KEY"
   ```

2. **Pakai Moonshot**:
   - Daftar: https://platform.moonshot.cn/
   - Get API key
   - Edit `config.toml`:
   ```toml
   llm_provider = "moonshot"
   moonshot_api_key = "YOUR_API_KEY"
   ```

### Error: Pexels API Rate Limit

Jika muncul rate limit error, tambahkan lebih banyak API keys:

```toml
pexels_api_keys = [
    "KEY_1",
    "KEY_2",
    "KEY_3"
]
```

Setiap akun Pexels bisa generate 1 API key gratis.

---

## 🎙️ Daftar Voice Indonesia

Voice Indonesia yang bisa digunakan:

| Voice Name | Gender | Gaya |
|------------|--------|------|
| `id-ID-ArdiNeural` | Male | Natural |
| `id-ID-GadisNeural` | Female | Natural |

Untuk voice lengkap, lihat: `docs/voice-list.txt`

---

## 🌟 Tips & Trik

### 1. Buat Video Berkualitas Tinggi
- Gunakan topik yang **spesifik dan jelas**
- Pilih voice yang **sesuai dengan mood** video
- Test dengan **paragraph_number kecil** (1-2) dulu
- Gunakan **subtitle** untuk engagement lebih baik

### 2. Hemat Waktu
- Gunakan **batch generation** untuk buat banyak video sekaligus
- Gunakan **local materials** untuk video yang sering dipakai

### 3. Optimasi Kualitas
- **Naskah gratis** lewat copy-paste dari ChatGPT/Claude kualitasnya sudah terbaik; DeepSeek API murah kalau mau otomatis penuh
- **Edge TTS** cukup bagus → Upgrade ke Azure Speech untuk suara lebih natural dan berlisensi komersial
- **Edge subtitle** cepat → Pakai Whisper untuk subtitle lebih akurat

---

## 📚 Resource Tambahan

### Video Material Sources (Gratis)
- Pexels: https://www.pexels.com/
- Pixabay: https://pixabay.com/

### Font untuk Subtitle
Terletak di: `resource/fonts/`
Bisa tambahkan font sendiri (TTF/OTF).

### Background Music
Terletak di: `resource/songs/`
Bisa tambahkan musik sendiri (MP3).

### Test Files
Contoh test ada di folder: `test/`

---

## 🐛 Melaporkan Bug

Jika menemukan bug atau error:
1. Cek dulu di: https://github.com/harry0703/MoneyPrinterTurbo/issues
2. Jika belum ada, buat issue baru dengan detail:
   - Error message lengkap
   - Config yang digunakan
   - Step untuk reproduce

---

## 📝 Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

---

## 🎉 Selamat!

Setup selesai! Anda sekarang bisa mulai membuat video otomatis dengan AI.

**Next Steps**:
1. Jalankan Web UI: `sh webui.sh` atau `webui.bat`
2. Buat video pertama dengan topik sederhana
3. Eksperimen dengan berbagai voice dan settings
4. Share hasil video Anda!

Happy video making! 🎬✨
