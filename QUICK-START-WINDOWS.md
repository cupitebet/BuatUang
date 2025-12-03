# ⚡ Quick Start Windows - Buat Uang

## 🚨 LANGKAH CEPAT UNTUK WINDOWS

### Step 1: Copy Config File

```cmd
REM JANGAN pakai 'cp' di Windows! Pakai 'copy'
copy config.example.toml config.toml
```

### Step 2: Install Dependencies

```cmd
REM Install semua library yang dibutuhkan (5-10 menit)
pip install -r requirements.txt
```

**⏳ Tunggu sampai selesai!** Proses ini akan download 100+ packages.

### Step 3: Edit Config

```cmd
REM Edit dengan Notepad
notepad config.toml
```

**Isi yang WAJIB:**
```toml
# 1. Masukkan Pexels API Key
pexels_api_keys = ["PASTE_API_KEY_DISINI"]

# 2. Pilih LLM Provider
llm_provider = "gemini"  # atau "deepseek" atau "openai"

# 3. Isi API Key sesuai provider
gemini_api_key = "PASTE_GEMINI_API_KEY_DISINI"
```

Simpan file (Ctrl+S)!

### Step 4: Jalankan Aplikasi

```cmd
REM Jalankan Web UI
webui.bat
```

Browser akan terbuka otomatis ke: http://localhost:8501

---

## ❌ JIKA ERROR: "streamlit is not recognized"

**Artinya:** Dependencies belum terinstall!

**Solusi:**
```cmd
REM Cek Python terinstall
python --version

REM Cek pip terinstall
pip --version

REM Install dependencies
pip install -r requirements.txt

REM Tunggu sampai selesai, lalu coba lagi
webui.bat
```

---

## ❌ JIKA ERROR: "No module named 'uvicorn'"

**Artinya:** Dependencies belum terinstall!

**Solusi sama:**
```cmd
pip install -r requirements.txt
```

---

## ⚠️ JIKA ERROR: "onnxruntime not found"

Lihat: [SOLUSI-ERROR-WINDOWS.md](SOLUSI-ERROR-WINDOWS.md)

**Quick Fix:** Install Python 64-bit!

---

## ✅ COMMAND WINDOWS vs LINUX

| Task | Linux/Mac | Windows |
|------|-----------|---------|
| Copy file | `cp file1 file2` | `copy file1 file2` |
| List files | `ls` | `dir` |
| Clear screen | `clear` | `cls` |
| Remove file | `rm file` | `del file` |
| Path separator | `/` | `\` |

---

## 🎯 CHECKLIST

```
✅ Python 3.11 64-bit terinstall
✅ pip terinstall
✅ Config file sudah di-copy (config.toml)
✅ Dependencies sudah terinstall (pip install -r requirements.txt)
✅ API keys sudah diisi di config.toml
✅ Jalankan: webui.bat
```

---

## 🚀 ONE-LINER INSTALL

```cmd
REM Copy, install, dan jalankan
copy config.example.toml config.toml && pip install -r requirements.txt && notepad config.toml && webui.bat
```

Jangan lupa isi API keys di notepad yang terbuka!

---

Good luck! 🎉
