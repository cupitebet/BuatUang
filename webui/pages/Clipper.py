import os
import sys

import streamlit as st

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.config import config  # noqa: E402
from app.models.schema import VideoAspect, VideoParams  # noqa: E402
from app.services import clipper  # noqa: E402
from app.utils import utils  # noqa: E402

st.set_page_config(page_title="Clipper - Buat Uang", page_icon="✂️", layout="wide")
st.title("✂️ Clipper")
st.caption("Potong video panjang (podcast, live, webinar) jadi klip pendek vertikal bersubtitle.")

st.warning(
    "**Hak cipta:** gunakan hanya untuk video milikmu sendiri atau video yang pemiliknya sudah "
    "memberi izin (misalnya order clipping dari kreator). Memotong video orang lain tanpa izin bisa "
    "berujung klaim, video diturunkan, *copyright strike*, sampai channel dihapus. "
    "Detail: `PANDUAN-CLIPPER.md`."
)

ASPECTS = {
    "9:16 Vertikal (TikTok/Reels/Shorts)": VideoAspect.portrait,
    "1:1 Kotak": VideoAspect.square,
    "16:9 Landscape": VideoAspect.landscape,
}
POSITIONS = {"Bawah": "bottom", "Tengah-bawah": "custom", "Tengah": "center", "Atas": "top"}

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.subheader("1. Sumber video")
        source_type = st.radio(
            "Ambil video dari",
            ["Link YouTube", "File lokal (path)", "Upload (file kecil)"],
            horizontal=True,
        )
        youtube_url = local_path = uploaded = None
        max_height = 1080
        if source_type == "Link YouTube":
            youtube_url = st.text_input("Link YouTube", placeholder="https://www.youtube.com/watch?v=...")
            max_height = st.selectbox("Kualitas maksimal", [1080, 720, 480], index=0, format_func=lambda h: f"{h}p")
        elif source_type == "File lokal (path)":
            local_path = st.text_input(
                "Lokasi file di komputer ini",
                placeholder=r"D:\Podcast\episode-01.mp4  atau  /home/saya/video.mp4",
                help="File dibaca langsung dari lokasinya, tidak diunggah atau disalin. "
                     "Di Windows: klik kanan file sambil tahan Shift → 'Copy as path', lalu tempel di sini.",
            )
        else:
            uploaded = st.file_uploader("Pilih video", type=["mp4", "mov", "mkv", "webm", "avi"])
            st.caption("Maksimal 200 MB. Untuk video besar, pakai pilihan **File lokal (path)** supaya tidak perlu upload.")

    with st.container(border=True):
        st.subheader("2. Pilih momen")
        mode = st.radio("Cara memilih momen", ["AI pilih otomatis", "Timestamp manual"], horizontal=True)
        manual_ranges = ""
        count, min_sec, max_sec = 3, 20, 60
        if mode == "AI pilih otomatis":
            st.caption(
                "AI membaca transkrip lalu memilih momen paling menarik. Memakai LLM yang diatur di "
                f"halaman utama (sekarang: **{config.app.get('llm_provider', '-')}**)."
            )
            count = st.slider("Jumlah klip", 1, 10, 3)
            min_sec, max_sec = st.slider("Durasi per klip (detik)", 10, 180, (20, 60))
        else:
            manual_ranges = st.text_area(
                "Satu klip per baris: mulai - selesai judul (opsional)",
                placeholder="12:30 - 13:15 Tips hemat listrik\n1:02:10 - 1:03:00 Cerita lucu",
                height=150,
            )

with right:
    with st.container(border=True):
        st.subheader("3. Format & subtitle")
        aspect = ASPECTS[st.selectbox("Rasio", list(ASPECTS))]
        if aspect == VideoAspect.portrait:
            st.caption("Video landscape dipotong di bagian tengah. Pastikan pembicara ada di tengah frame.")
        with_subtitles = st.checkbox("Tambahkan subtitle", value=True,
                                     help="Butuh Whisper: pip install -r requirements-whisper.txt")
        style = VideoParams(video_subject="clip")
        if with_subtitles:
            fonts = sorted(f for f in os.listdir(utils.font_dir()) if f.lower().endswith((".ttf", ".ttc", ".otf")))
            default_font = fonts.index("NotoSans-Bold.ttf") if "NotoSans-Bold.ttf" in fonts else 0
            c1, c2 = st.columns(2)
            style.font_name = c1.selectbox("Font", fonts, index=default_font) if fonts else ""
            style.font_size = c2.slider("Ukuran font", 30, 100, 64)
            style.subtitle_position = POSITIONS[c1.selectbox("Posisi", list(POSITIONS), index=1)]
            style.custom_position = 75.0
            style.text_fore_color = c2.color_picker("Warna teks", "#FFFFFF")
            style.stroke_width = 2.0

    start = st.button("✂️ Buat Klip", type="primary", use_container_width=True)


def resolve_source(job_dir: str, progress) -> str:
    if source_type == "Link YouTube":
        if not youtube_url:
            raise clipper.ClipperError("isi link YouTube dulu")
        return clipper.download_youtube(youtube_url, job_dir, max_height, progress)
    if source_type == "File lokal (path)":
        path = (local_path or "").strip().strip('"').strip("'")
        if not path:
            raise clipper.ClipperError("isi lokasi file dulu")
        if not os.path.isfile(path):
            raise clipper.ClipperError(f"file tidak ditemukan: {path}")
        return path
    if not uploaded:
        raise clipper.ClipperError("pilih file video dulu")
    path = os.path.join(job_dir, "source" + os.path.splitext(uploaded.name)[1].lower())
    with open(path, "wb") as f:
        while chunk := uploaded.read(8 * 1024 * 1024):
            f.write(chunk)
    return path


if start:
    bar = st.progress(0.0, text="menyiapkan...")

    def progress(stage: str, fraction: float):
        bar.progress(min(max(fraction, 0.0), 1.0), text=stage)

    job_dir = clipper.new_job_dir()
    try:
        source = resolve_source(job_dir, progress)
        st.session_state["clip_results"] = clipper.make_clips(
            source, job_dir, count=count, min_sec=min_sec, max_sec=max_sec, aspect=aspect,
            with_subtitles=with_subtitles, manual_ranges=manual_ranges, style=style, progress=progress,
        )
        st.session_state["clip_dir"] = job_dir
    except (clipper.ClipperError, ValueError) as e:
        bar.empty()
        st.error(f"Gagal: {e}")

results = st.session_state.get("clip_results") or []
if results:
    st.success(f"{len(results)} klip selesai. Tersimpan di: `{st.session_state.get('clip_dir')}`")
    cols = st.columns(min(3, len(results)))
    for i, r in enumerate(results):
        with cols[i % len(cols)]:
            st.markdown(f"**{i + 1}. {r.title or 'Klip'}**  \n"
                        f"{clipper.format_time(r.start)} – {clipper.format_time(r.end)} "
                        f"({r.end - r.start:.0f} detik)")
            st.video(r.path)
            with open(r.path, "rb") as f:
                st.download_button("Download", f, file_name=os.path.basename(r.path),
                                   mime="video/mp4", key=f"dl-{r.path}")
