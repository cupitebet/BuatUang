# 💸 Panduan Biaya & Kualitas Video — Buat Uang

Panduan ini menjawab tiga pertanyaan:

1. **Apakah Buat Uang bisa dipakai 100% gratis?** Bisa.
2. **Apakah langganan ChatGPT Plus / Claude Pro / Gemini bisa dipakai sebagai pengganti kredit API?** Tidak secara langsung, tapi tetap bisa dimanfaatkan (lihat [Opsi A](#opsi-a--naskah-dari-langganan-chatgptclaudegemini-copy-paste)).
3. **Seberapa bagus video hasil versi gratis?** Layak dan rapi, tapi generik. Detail dan cara meningkatkannya ada di bawah.

---

## Daftar Isi

1. [Komponen Video & Biayanya](#1-komponen-video--biayanya)
2. [Kenapa Langganan Chat AI Tidak Bisa Dipakai sebagai API](#2-kenapa-langganan-chat-ai-tidak-bisa-dipakai-sebagai-api)
3. [Cara Gratis Mendapatkan Naskah](#3-cara-gratis-mendapatkan-naskah)
   - [Opsi A — Naskah dari langganan (copy-paste)](#opsi-a--naskah-dari-langganan-chatgptclaudegemini-copy-paste)
   - [Opsi B — Ollama (AI di komputer sendiri)](#opsi-b--ollama-ai-di-komputer-sendiri)
   - [Opsi C — Gemini API free tier](#opsi-c--gemini-api-free-tier)
   - [Opsi D — Berbayar tapi murah](#opsi-d--berbayar-tapi-murah-otomatis-penuh)
   - [Yang harus dihindari: g4f](#yang-harus-dihindari-g4f)
4. [Ekspektasi Kualitas Versi Gratis](#4-ekspektasi-kualitas-versi-gratis)
5. [Cara Meningkatkan Kualitas Tanpa Biaya](#5-cara-meningkatkan-kualitas-tanpa-biaya)
6. [Upgrade Berbayar yang Paling Terasa](#6-upgrade-berbayar-yang-paling-terasa)
7. [Monetisasi & Aturan Platform](#7-monetisasi--aturan-platform)
8. [Checklist Sebelum Upload](#8-checklist-sebelum-upload)

---

## 1. Komponen Video & Biayanya

Satu video Buat Uang dibuat dari lima bagian. Hanya bagian pertama yang memakai AI teks (LLM).

| # | Komponen | Sumber bawaan | Biaya |
|---|----------|---------------|-------|
| 1 | **Naskah + kata kunci klip** | LLM (OpenAI, DeepSeek, Gemini, Ollama, dll.) | Gratis s/d berbayar, tergantung pilihan di [§3](#3-cara-gratis-mendapatkan-naskah) |
| 2 | **Klip video** | Pexels / Pixabay | **Gratis** (perlu API key gratis dari Pexels) |
| 3 | **Suara narasi** | Edge TTS | **Gratis**, tanpa API key |
| 4 | **Subtitle** | Dibuat dari data suara (mode `edge`) | **Gratis** |
| 5 | **Musik latar** | File `.mp3` milikmu di `resource/songs/` | **Gratis** (pakai musik bebas royalti) |

Artinya: kalau bagian naskah memakai salah satu cara gratis di bawah, **seluruh video bisa dibuat tanpa biaya sama sekali**.

---

## 2. Kenapa Langganan Chat AI Tidak Bisa Dipakai sebagai API

Langganan seperti **ChatGPT Plus, Claude Pro, atau Gemini Advanced** memberi akses ke **aplikasi chat** (web/HP). Aplikasi lain seperti Buat Uang butuh **API**, yaitu jalur akses untuk program, yang dijual dan ditagih **terpisah** dari langganan, biasanya per pemakaian (token).

| | Langganan chat | API |
|---|---|---|
| Dipakai oleh | Kamu, lewat chat | Program/aplikasi |
| Cara bayar | Bulanan tetap | Per pemakaian (kredit) |
| Bisa dipakai Buat Uang secara otomatis? | ❌ Tidak | ✅ Ya |

Jadi API key **tidak bisa** diambil dari langganan. Tapi langganan tetap berguna: kamu bisa membuat naskahnya di chat lalu menempelkannya ke Buat Uang ([Opsi A](#opsi-a--naskah-dari-langganan-chatgptclaudegemini-copy-paste)). Kualitas naskahnya **sama** dengan versi API, karena modelnya sama.

---

## 3. Cara Gratis Mendapatkan Naskah

### Opsi A — Naskah dari langganan ChatGPT/Claude/Gemini (copy-paste)

**Cocok untuk:** yang sudah berlangganan chat AI, atau mau memakai versi gratis aplikasi chat tersebut.
**Biaya:** Rp 0 tambahan. **Kualitas naskah:** terbaik.

Aplikasi **tidak memanggil AI sama sekali** jika kolom **Video Script** *dan* **Video Keywords** sudah terisi. Kalau salah satu kosong, AI tetap dipanggil untuk mengisinya.

**Langkah:**

1. Buka ChatGPT / Claude / Gemini, lalu kirim prompt ini (ganti topiknya):

   ```text
   Buatkan naskah narasi video pendek (TikTok/Reels) berdurasi sekitar 45-60 detik
   tentang: [TOPIK KAMU].

   Aturan:
   - Bahasa Indonesia santai, kalimat pendek, 2 paragraf.
   - Kalimat pertama harus jadi "hook" yang bikin orang berhenti scroll.
   - Tanpa judul, tanpa emoji, tanpa tanda **, tanpa label seperti "Narator:".
   - Setiap kalimat diakhiri titik (penting untuk subtitle).

   Setelah naskah, tulis juga 5 kata kunci BAHASA INGGRIS untuk mencari klip video stok
   yang cocok dengan isi naskah. Setiap kata kunci 2-4 kata, deskriptif secara visual
   (contoh: "woman jogging sunrise park"), dipisahkan koma, dalam satu baris.
   ```

2. Buka WebUI Buat Uang (`webui.bat` / `sh webui.sh`).
3. Tempel **naskah** ke kolom **Video Script**.
4. Tempel **kata kunci** ke kolom **Video Keywords**. Pisahkan dengan **koma**, bahasa Inggris saja.
5. **Jangan** klik tombol *Generate Video Script and Keywords*, karena tombol itu memanggil AI.
6. Atur suara, subtitle, dan musik, lalu klik **Generate Video**.

> Kolom **LLM Provider / API Key** boleh dibiarkan kosong kalau kamu selalu memakai cara ini.

### Opsi B — Ollama (AI di komputer sendiri)

**Cocok untuk:** yang mau otomatis penuh tanpa biaya dan punya PC cukup kuat.
**Biaya:** Rp 0 (hanya listrik). **Kualitas naskah:** cukup; bahasa Indonesianya di bawah ChatGPT/Claude.

**Kebutuhan:** RAM minimal sekitar **8 GB** untuk model ukuran ~7B, 16 GB lebih nyaman. GPU tidak wajib, tapi tanpa GPU prosesnya lebih lambat.

**Langkah:**

1. Unduh dan instal Ollama dari https://ollama.com.
2. Unduh satu model. Pilih model yang mendukung banyak bahasa, misalnya keluarga Qwen atau Gemma. Lihat pilihan terbaru di https://ollama.com/library, lalu jalankan:
   ```bash
   ollama pull qwen2.5:7b
   ollama list            # pastikan nama model muncul
   ```
3. Di WebUI, bagian **LLM Settings**, isi:

   | Kolom | Isi |
   |-------|-----|
   | LLM Provider | `Ollama` |
   | API Key | Isi apa saja, misalnya `123` |
   | Base Url | `http://localhost:11434/v1` |
   | Model Name | Nama persis dari `ollama list`, misalnya `qwen2.5:7b` |

   Atau langsung di `config.toml`:
   ```toml
   llm_provider = "ollama"
   ollama_base_url = "http://localhost:11434/v1"
   ollama_model_name = "qwen2.5:7b"
   ```
4. **Kalau Buat Uang dijalankan lewat Docker** (`docker compose up`), isi Base Url dengan `http://host.docker.internal:11434/v1`. `docker-compose.yml` repo ini sudah memetakan nama itu ke komputer host.
   - **Docker Desktop (Windows/Mac):** langsung jalan.
   - **Docker di Linux:** Ollama secara default hanya menerima koneksi dari `127.0.0.1`, jadi container tidak bisa menjangkaunya. Jalankan Ollama dengan `OLLAMA_HOST=0.0.0.0` (untuk service systemd: `sudo systemctl edit ollama`, tambahkan `Environment="OLLAMA_HOST=0.0.0.0"`, lalu `sudo systemctl restart ollama`). Setelah itu port 11434 terbuka ke jaringan. Kalau server bisa diakses dari internet, **izinkan port itu hanya dari jaringan Docker**, misalnya dengan UFW (urutan perintah penting, aturan `allow` harus lebih dulu):
     ```bash
     sudo ufw allow from 172.16.0.0/12 to any port 11434
     sudo ufw deny 11434
     ```
   - **Menjalankan dengan `docker run` (bukan compose):** tambahkan `--add-host=host.docker.internal:host-gateway`.
5. Klik *Generate Video Script and Keywords* untuk menguji. Kalau naskahnya kurang bagus, edit langsung di kolom sebelum klik **Generate Video**.

### Opsi C — Gemini API free tier

**Cocok untuk:** yang mau otomatis penuh tanpa memasang apa pun.
**Biaya:** Rp 0 selama masih dalam kuota gratis harian. **Kualitas naskah:** bagus.

1. Buka https://aistudio.google.com, login dengan akun Google, lalu buat **API key**.
2. Di WebUI, **LLM Settings**:

   | Kolom | Isi |
   |-------|-----|
   | LLM Provider | `Gemini` |
   | API Key | API key dari AI Studio |
   | Model Name | `gemini-flash-latest` |

   Alias `gemini-flash-latest` otomatis mengikuti model Flash terbaru, jadi tidak perlu diganti setiap kali Google memensiunkan model.

> ⚠️ **Batas kuota gratis bisa berubah sewaktu-waktu** dan diatur per menit/per hari. Cek batas terbarunya di AI Studio. Untuk beberapa video per hari biasanya cukup. Data yang dikirim lewat tier gratis juga bisa dipakai Google untuk meningkatkan layanannya, jadi jangan kirim informasi pribadi atau rahasia.

### Opsi D — Berbayar tapi murah (otomatis penuh)

Kalau mau otomatis tanpa batas kuota, **DeepSeek** termasuk API paling murah. Satu naskah pendek hanya butuh sedikit token, sehingga biayanya per video sangat kecil. Cek harga terbaru di https://platform.deepseek.com.

```toml
llm_provider = "deepseek"
deepseek_api_key = "API_KEY_KAMU"
deepseek_model_name = "deepseek-chat"
```

### Yang harus dihindari: g4f

`g4f` (GPT4Free) memakai akses tidak resmi ke situs chat AI. **Jangan dipakai:**
- Melanggar ketentuan layanan penyedia AI, sehingga akun atau IP bisa diblokir.
- Versi di aplikasi ini **sudah tidak berfungsi** (error *"No provider found"*).
- Tidak stabil dan bisa berhenti kapan saja.

---

## 4. Ekspektasi Kualitas Versi Gratis

Penilaian jujur per komponen:

| Komponen | Kualitas | Catatan |
|----------|----------|---------|
| **Naskah** | ✅ Bagus | Lewat Opsi A atau C, modelnya sama dengan versi berbayar |
| **Klip video (Pexels)** | 🟡 Cukup | Tajam (HD) dan bebas royalti, tapi stok umum. Klip dipilih berdasarkan **kata kunci**, bukan per kalimat, jadi sering kurang nyambung dengan kalimat yang sedang dibacakan |
| **Suara (Edge TTS)** | 🟡 Cukup | Jelas dan natural untuk ukuran gratis (`id-ID-ArdiNeural` pria, `id-ID-GadisNeural` wanita), tapi **datar dan kurang emosi**. Penonton cepat mengenali ini suara AI |
| **Subtitle** | ✅ Baik | Rapi dengan gaya standar. Font bawaan **Noto Sans Bold** mendukung huruf Latin (Indonesia/Inggris), tapi tidak mendukung huruf Mandarin/Jepang/Korea |
| **Musik latar** | Tergantung kamu | Folder `resource/songs/` kosong secara default. Tanpa lagu, video dibuat tanpa musik |

**Kesimpulan:** hasilnya **layak upload dan rapi**, cocok untuk konten edukasi, fakta, tips, atau motivasi dengan gaya "faceless". Tapi tanpa sentuhan tambahan, videonya terasa **generik** dan mirip ribuan video template lain.

---

## 5. Cara Meningkatkan Kualitas Tanpa Biaya

Faktor yang paling menentukan kualitas **tidak ada hubungannya dengan bayar atau gratis**:

### 5.1 Hook di 3 detik pertama
Kalimat pertama menentukan apakah penonton bertahan. Bandingkan:
- ❌ "Olahraga memiliki banyak manfaat bagi kesehatan."
- ✅ "Cuma 10 menit jalan kaki bisa bikin mood kamu naik seharian. Ini alasannya."

### 5.2 Isi kata kunci klip sendiri, dengan spesifik
Ini cara termudah membuat klip lebih nyambung.
- ❌ `olahraga, kesehatan`
- ✅ `woman jogging sunrise park, healthy breakfast table, man stretching home, running shoes close up`

Kata kunci harus bahasa Inggris, menggambarkan **apa yang terlihat**, dan dipisahkan koma.

### 5.3 Atur durasi klip
**Clip Duration** (durasi maksimal per klip) 2–3 detik membuat video terasa lebih dinamis untuk TikTok/Reels. 4–5 detik lebih santai.

### 5.4 Pilih dan atur suara
- Coba kedua suara Indonesia dengan tombol **Play Voice** sebelum generate.
- Set **Speech Rate** ke 1.1 atau 1.2 agar narasi tidak terdengar lambat.

### 5.5 Musik latar
- Taruh 5–10 lagu bebas royalti di `resource/songs/` (YouTube Audio Library, Pixabay Music), lalu pilih *Random Background Music*.
- Set **Background Music Volume** ke 0.1–0.2 supaya musik tidak menenggelamkan suara narasi.

### 5.6 Campur dengan footage sendiri
Pilih **Video Source → Local file** untuk mengunggah video atau foto milikmu sendiri: produk, lokasi, layar HP, tangan sedang mengerjakan sesuatu. Footage asli langsung membuat video terasa berbeda dari template.

### 5.7 Selalu tinjau sebelum upload
Tonton hasilnya sampai habis. Kalau ada klip yang aneh, ganti kata kunci lalu generate ulang. Atau set **Number of Videos Generated Simultaneously** ke 2–3, lalu pilih hasil terbaik.

---

## 6. Upgrade Berbayar yang Paling Terasa

Kalau nanti mau menambah budget, urutan dampaknya dari yang paling terasa:

1. **Suara.** Suara AI yang lebih ekspresif (misalnya suara Azure yang sudah didukung aplikasi ini, atau layanan voice AI lain), **atau rekam suaramu sendiri**. Ini perubahan paling terasa bagi penonton.
2. **Footage.** Rekaman sendiri atau stok premium yang lebih spesifik.
3. **Naskah otomatis.** Ini paling kecil dampaknya, karena Opsi A sudah memberi kualitas terbaik.

---

## 7. Monetisasi & Aturan Platform

- **YouTube dan platform lain memperketat aturan** terhadap konten yang diproduksi massal, berulang, dan minim nilai tambah. Video berupa klip stok + suara AI + template yang sama, dibuat dalam jumlah banyak, **berisiko tidak lolos monetisasi** walaupun tetap boleh diunggah. Baca kebijakan monetisasi terbaru di masing-masing platform.
- **Gunakan Buat Uang sebagai alat bantu produksi, bukan pabrik konten.** Tambahkan sudut pandangmu sendiri, informasi yang benar-benar berguna, dan footage atau suara asli.
- **Lisensi suara Edge TTS:** suara bawaan gratis ini diambil dari layanan baca-teks browser Microsoft Edge secara tidak resmi, dan **tidak ada lisensi komersial yang jelas**. Untuk channel yang dimonetisasi, opsi yang aman secara lisensi adalah **Azure Speech** (berbayar, sudah didukung aplikasi ini lewat pilihan *TTS Provider*) atau rekaman suaramu sendiri.
- **Hak cipta naskah AI:** status hak cipta teks buatan AI masih diperdebatkan. Edit dan tambahkan isi sendiri supaya karyanya jelas milikmu.
- **Hak cipta musik:** musik berhak cipta (misalnya lagu populer) bisa membuat video kena klaim, di-mute, atau diturunkan. Pakai musik bebas royalti.
- **Klip Pexels/Pixabay** bebas dipakai, termasuk komersial, sesuai lisensi masing-masing, tapi tetap tidak boleh dijual ulang sebagai klip mentah.
- **Cek fakta.** AI bisa salah. Untuk konten kesehatan, keuangan, atau hukum, pastikan isi naskah benar sebelum dipublikasikan.

---

## 8. Checklist Sebelum Upload

- [ ] Kalimat pertama adalah hook yang kuat
- [ ] Fakta dalam naskah sudah dicek
- [ ] Klip video nyambung dengan isi narasi
- [ ] Suara jelas, kecepatan pas, musik tidak terlalu keras
- [ ] Subtitle terbaca dan tidak menutupi bagian penting video
- [ ] Musik latar bebas royalti
- [ ] Ada nilai tambah dari kamu (sudut pandang, footage, atau suara asli)

---

**Lihat juga:** [README-id.md](README-id.md) · [PANDUAN-PEMULA.md](PANDUAN-PEMULA.md) · [SETUP-ID.md](SETUP-ID.md)
