# ⚠️ SOLUSI ERROR INSTALASI WINDOWS

## Error: "Could not find a version that satisfies the requirement onnxruntime"

### 🔍 Penyebab Error:

Error ini terjadi karena:
1. ❌ Python yang terinstall adalah versi **32-bit** (harus 64-bit)
2. ❌ Python version tidak compatible
3. ❌ pip version terlalu lama

---

## ✅ SOLUSI LENGKAP

### Solusi 1: Install Python 64-bit (RECOMMENDED)

**Step 1: Cek Python yang terinstall**

```bash
python --version
python -c "import platform; print(platform.architecture())"
```

Jika muncul `('32bit', ...)` → Anda pakai Python 32-bit ❌

**Step 2: Uninstall Python 32-bit**

1. Buka **Control Panel** → **Programs** → **Uninstall a program**
2. Cari "Python 3.11"
3. Klik kanan → **Uninstall**

**Step 3: Install Python 64-bit**

1. Download: https://www.python.org/downloads/windows/
2. Pilih: **"Windows installer (64-bit)"** ⭐ PENTING!
3. Download file: `python-3.11.x-amd64.exe`
4. Install dengan centang:
   - ✅ **"Add Python to PATH"**
   - ✅ **"Install for all users"**

**Step 4: Verify Instalasi**

```bash
python --version
python -c "import platform; print(platform.architecture())"
```

Harus muncul: `('64bit', ...)`  ✅

**Step 5: Update pip**

```bash
python -m pip install --upgrade pip
```

**Step 6: Install Dependencies**

```bash
cd MoneyPrinterTurbo
pip install -r requirements.txt
```

---

### Solusi 2: Install onnxruntime Manual (Jika Solusi 1 Tidak Berhasil)

```bash
# Update pip dulu
python -m pip install --upgrade pip

# Install onnxruntime versi stable
pip install onnxruntime==1.17.0

# Lalu install requirements
pip install -r requirements.txt
```

---

### Solusi 3: Skip Whisper (Pakai Edge TTS Saja)

Jika masih error, Anda bisa skip `faster-whisper` dan pakai `edge` untuk subtitle:

**Step 1: Edit requirements.txt**

Buka `requirements.txt` dan comment/hapus baris:
```
# faster-whisper==1.1.0  # ← Comment atau hapus baris ini
```

**Step 2: Install tanpa faster-whisper**

```bash
pip install -r requirements.txt
```

**Step 3: Edit config.toml**

Pastikan pakai `edge` untuk subtitle:
```toml
subtitle_provider = "edge"  # Jangan pakai "whisper"
```

**Catatan:** Edge TTS sudah cukup bagus untuk subtitle!

---

### Solusi 4: Install Dependencies Satu-Satu

Jika masih error, install satu-satu dependency utama:

```bash
# Install core dependencies
pip install moviepy==2.1.2
pip install streamlit==1.45.0
pip install edge_tts==6.1.19
pip install fastapi==0.115.6
pip install uvicorn==0.32.1
pip install openai==1.56.1
pip install loguru==0.7.3
pip install redis==5.2.0
pip install requests

# Skip faster-whisper jika error
# pip install faster-whisper==1.1.0

# Install LLM providers
pip install google.generativeai==0.8.3
pip install dashscope==1.20.14
```

---

## 🔍 Cek Apakah Python 32-bit atau 64-bit

### Windows:

**Method 1: Via Command Prompt**
```bash
python -c "import struct; print(struct.calcsize('P') * 8)"
```
- Output `64` = 64-bit ✅
- Output `32` = 32-bit ❌

**Method 2: Via Python Interactive**
```python
import platform
print(platform.architecture())
print(platform.machine())
```

---

## 📋 Checklist After Install

```bash
# 1. Cek Python 64-bit
python -c "import platform; print(platform.architecture())"
# Harus: ('64bit', ...)

# 2. Cek pip version
pip --version
# Harus: pip 24.x atau lebih baru

# 3. Test import core packages
python -c "import moviepy; import streamlit; import fastapi; print('✅ OK!')"

# 4. Test config load
python -c "from app.config import config; print('✅ Config OK!')"
```

---

## ⚡ Quick Fix (Jika Masih Error)

```bash
# Install versi minimal (tanpa faster-whisper)
pip install moviepy streamlit fastapi uvicorn openai edge-tts loguru

# Test run
python main.py
```

Aplikasi akan jalan, tapi **subtitle hanya pakai edge** (tidak bisa whisper).

---

## 🆘 Masih Error?

### Error: "Microsoft Visual C++ required"

**Solusi:**
1. Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install Microsoft Visual C++ Redistributable
3. Restart komputer
4. Coba install lagi

### Error: "No module named 'numpy'"

**Solusi:**
```bash
pip install numpy
pip install -r requirements.txt
```

### Error: "Cannot open include file: 'stdint.h'"

**Solusi:**
Anda butuh C++ compiler. Dua pilihan:

**Option A: Install Visual Studio Build Tools**
1. Download: https://visualstudio.microsoft.com/downloads/
2. Pilih "Build Tools for Visual Studio"
3. Install dengan pilihan "Desktop development with C++"

**Option B: Skip packages yang butuh compile**
Pakai Solusi 3 di atas (skip faster-whisper)

---

## 💡 Tips Instalasi Windows

1. ✅ **Selalu pakai Python 64-bit**
2. ✅ **Run Command Prompt as Administrator**
3. ✅ **Disable antivirus sementara saat install**
4. ✅ **Path tidak boleh ada spasi atau karakter Mandarin**
5. ✅ **Update pip ke versi terbaru**
6. ✅ **Pakai virtual environment (venv)**

---

## 🎯 Recommended Setup untuk Windows

```bash
# 1. Install Python 3.11 64-bit
# Download dari: https://www.python.org/downloads/

# 2. Buka Command Prompt as Administrator

# 3. Pindah ke folder project
cd C:\Users\YourName\Downloads\MoneyPrinterTurbo

# 4. Buat virtual environment
python -m venv venv

# 5. Aktivasi venv
venv\Scripts\activate

# 6. Update pip
python -m pip install --upgrade pip

# 7. Install dependencies
pip install -r requirements.txt

# 8. Test
python main.py
```

---

## ✅ Jika Berhasil

Anda akan melihat:
```
INFO: MoneyPrinterTurbo v1.2.6
INFO: start server, docs: http://127.0.0.1:8080/docs
```

Buka browser ke: http://localhost:8501 untuk Web UI!

---

## 📞 Butuh Bantuan Lebih?

- GitHub Issues: https://github.com/harry0703/MoneyPrinterTurbo/issues
- Cari issue dengan keyword: "onnxruntime" atau "windows install"
- Buat issue baru dengan detail:
  - Windows version
  - Python version (`python --version`)
  - Python architecture (`platform.architecture()`)
  - Full error message

---

**Good luck! 🚀**
