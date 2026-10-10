"""Clipper: potong video panjang (podcast, live, webinar) menjadi klip pendek vertikal.

Alur: transkripsi (Whisper) -> pilih momen (LLM atau timestamp manual) -> potong + ubah rasio
(ffmpeg) -> subtitle (renderer yang sama dengan video biasa).
"""

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Callable

from loguru import logger
from moviepy import VideoFileClip
from moviepy.config import FFMPEG_BINARY

from app.models.schema import VideoAspect, VideoParams
from app.services import llm, subtitle
from app.services import video as video_service
from app.utils import utils

# Batas karakter transkrip per panggilan LLM; transkrip yang lebih panjang dipecah per bagian.
TRANSCRIPT_CHUNK_CHARS = 30000

WHISPER_HINT = (
    "Whisper belum terpasang. Jalankan: pip install -r requirements-whisper.txt "
    "(dibutuhkan untuk mode AI dan untuk subtitle)."
)


class ClipperError(Exception):
    pass


@dataclass
class Highlight:
    start: float
    end: float
    title: str = ""
    score: float = 0.0

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class ClipResult:
    path: str
    start: float
    end: float
    title: str = ""
    subtitles: list[dict] = field(default_factory=list)


def parse_time(value: str) -> float:
    """'1:02:03.5', '02:03', '123', '1.5' -> detik."""
    value = value.strip().replace(",", ".")
    if not value:
        raise ValueError("waktu kosong")
    parts = value.split(":")
    if len(parts) > 3:
        raise ValueError(f"format waktu tidak dikenal: {value}")
    seconds = 0.0
    for part in parts:
        if not re.fullmatch(r"\d+(\.\d+)?", part):
            raise ValueError(f"format waktu tidak dikenal: {value}")
        seconds = seconds * 60 + float(part)
    return seconds


def format_time(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def parse_manual_ranges(text: str) -> list[Highlight]:
    """Satu klip per baris: `mulai - selesai [judul]`, misalnya `12:30 - 13:15 Tips hemat`."""
    highlights = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([\d:.,]+)\s*[-–—]\s*([\d:.,]+)\s*(.*)$", line)
        if not m:
            raise ValueError(f"baris {line_no}: tulis seperti '12:30 - 13:15 judul', bukan '{line}'")
        start, end = parse_time(m.group(1)), parse_time(m.group(2))
        if end <= start:
            raise ValueError(f"baris {line_no}: waktu selesai harus setelah waktu mulai")
        highlights.append(Highlight(start=start, end=end, title=m.group(3).strip()))
    return highlights


def probe_duration(path: str) -> float:
    clip = VideoFileClip(path)
    try:
        return float(clip.duration)
    finally:
        clip.close()


def _transcript_chunks(items: list[dict], max_chars: int) -> list[str]:
    chunks, current, size = [], [], 0
    for it in items:
        line = f"[{it['start_time']:.1f}-{it['end_time']:.1f}] {it['msg']}"
        if current and size + len(line) > max_chars:
            chunks.append("\n".join(current))
            current, size = [], 0
        current.append(line)
        size += len(line) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks


def _prompt(transcript: str, count: int, min_sec: int, max_sec: int) -> str:
    return f"""
# Role: Short-form video editor

## Goal
Pick the {count} best moments from this transcript to cut into standalone vertical clips
(TikTok / Reels / Shorts).

## Rules
1. Each moment must be between {min_sec} and {max_sec} seconds long.
2. Each moment must make sense on its own: it starts at the beginning of a thought and ends
   after a complete point, punchline, or answer. Prefer strong hooks, surprising facts,
   clear advice, emotional or funny moments.
3. Moments must not overlap.
4. "start" and "end" are seconds, taken from the [start-end] markers in the transcript.
5. "title" is a short catchy title in the same language as the transcript.
6. "score" is 1-10: how likely the clip is to keep viewers watching.
7. Return ONLY a JSON array, no markdown, no explanation:
[{{"start": 12.0, "end": 58.5, "title": "...", "score": 8}}]

## Transcript
{transcript}
""".strip()


def _parse_llm_highlights(response: str) -> list[Highlight]:
    if not response or response.startswith("Error: "):
        raise ClipperError(f"AI gagal memilih momen: {response or 'respons kosong'}")
    match = re.search(r"\[.*\]", response, re.S)
    if not match:
        raise ClipperError("AI tidak mengembalikan daftar momen dalam format JSON")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ClipperError(f"jawaban AI bukan JSON yang valid: {e}") from e
    highlights = []
    for item in data if isinstance(data, list) else []:
        try:
            highlights.append(Highlight(
                start=float(item["start"]), end=float(item["end"]),
                title=str(item.get("title", "")).strip(), score=float(item.get("score", 0) or 0),
            ))
        except (KeyError, TypeError, ValueError):
            continue
    return highlights


def select_highlights(items: list[dict], count: int, min_sec: int, max_sec: int) -> list[Highlight]:
    """Minta LLM memilih momen terbaik; transkrip panjang dipecah lalu kandidat digabung per skor."""
    if not items:
        raise ClipperError("transkrip kosong: tidak ada ucapan yang terdeteksi di video")
    candidates = []
    chunks = _transcript_chunks(items, TRANSCRIPT_CHUNK_CHARS)
    for i, chunk in enumerate(chunks, start=1):
        logger.info(f"asking AI for highlights, part {i}/{len(chunks)}")
        candidates += _parse_llm_highlights(
            llm._generate_response(_prompt(chunk, count, min_sec, max_sec))
        )
    if not candidates:
        raise ClipperError("AI tidak menemukan momen yang cocok")
    return candidates


def _snap_to_sentences(h: Highlight, items: list[dict]) -> Highlight:
    """Geser batas ke awal/akhir kalimat agar klip tidak terpotong di tengah kata."""
    inside = [it for it in items if it["end_time"] > h.start and it["start_time"] < h.end]
    if not inside:
        return h
    return Highlight(start=inside[0]["start_time"], end=inside[-1]["end_time"], title=h.title, score=h.score)


def _fit_length(h: Highlight, items: list[dict], min_sec: float, max_sec: float, total: float) -> Highlight:
    start, end = h.start, h.end
    if end - start > max_sec:
        sentence_ends = [it["end_time"] for it in items if start < it["end_time"] <= start + max_sec]
        end = max(sentence_ends) if sentence_ends and max(sentence_ends) - start >= min_sec else start + max_sec
    if end - start < min_sec:
        following = [it["end_time"] for it in items if it["end_time"] > end and it["end_time"] - start <= max_sec]
        end = next((e for e in following if e - start >= min_sec), start + min_sec)
    end = min(end, total)
    return Highlight(start=start, end=end, title=h.title, score=h.score)


def normalize_highlights(highlights: list[Highlight], items: list[dict], total: float, count: int,
                         min_sec: float, max_sec: float, snap: bool = True) -> list[Highlight]:
    """Rapikan saran AI: batas kalimat, panjang min/max, dalam durasi video, tanpa tumpang tindih."""
    cleaned = []
    for h in highlights:
        h = Highlight(max(0.0, h.start), min(total, h.end), h.title, h.score)
        if h.end <= h.start:
            continue
        if snap and items:
            h = _snap_to_sentences(h, items)
            h = _fit_length(h, items, min_sec, max_sec, total)
        if h.duration >= 1:
            cleaned.append(h)

    chosen = []
    for h in sorted(cleaned, key=lambda x: (-x.score, x.start)):
        if all(h.end <= c.start or h.start >= c.end for c in chosen):
            chosen.append(h)
        if len(chosen) >= count:
            break
    return sorted(chosen, key=lambda x: x.start)


_ASPECT_FILTERS = {
    # crop tengah ke 9:16 lalu skala; nilai dalam '...' agar koma di min() tidak memecah filter
    VideoAspect.portrait: "crop=w='min(iw,ih*9/16)':h='min(ih,iw*16/9)',scale=1080:1920,setsar=1",
    VideoAspect.square: "crop=w='min(iw,ih)':h='min(iw,ih)',scale=1080:1080,setsar=1",
    VideoAspect.landscape: (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"
    ),
}


def cut_clip(source: str, start: float, end: float, output: str,
             aspect: VideoAspect = VideoAspect.portrait) -> None:
    """Potong [start, end] dan ubah ke rasio target. Di-encode ulang agar potongan tepat di detiknya."""
    cmd = [
        FFMPEG_BINARY, "-y", "-loglevel", "error",
        "-ss", f"{start:.3f}", "-i", source, "-t", f"{end - start:.3f}",
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", _ASPECT_FILTERS[VideoAspect(aspect)],
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
        output,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise ClipperError(f"ffmpeg gagal memotong klip: {e.stderr.strip()}") from e


def subtitles_for_range(items: list[dict], start: float, end: float) -> list[dict]:
    """Ambil kalimat dalam [start, end] dan geser waktunya agar mulai dari 0."""
    shifted = []
    for it in items:
        s, e = max(it["start_time"], start), min(it["end_time"], end)
        if e > s:
            shifted.append({"msg": it["msg"], "start_time": s - start, "end_time": e - start})
    return shifted


def make_clips(
    source: str,
    output_dir: str,
    count: int = 3,
    min_sec: int = 20,
    max_sec: int = 60,
    aspect: VideoAspect = VideoAspect.portrait,
    with_subtitles: bool = True,
    manual_ranges: str = "",
    style: VideoParams | None = None,
    progress: Callable[[str, float], None] | None = None,
) -> list[ClipResult]:
    """Buat klip dari `source`. Mode manual dipakai jika `manual_ranges` diisi, selain itu mode AI."""
    def report(stage: str, fraction: float):
        logger.info(f"clipper: {stage}")
        if progress:
            progress(stage, fraction)

    if not os.path.isfile(source):
        raise ClipperError(f"file video tidak ditemukan: {source}")
    count = max(1, min(int(count), 10))
    min_sec, max_sec = sorted((max(5, int(min_sec)), max(5, int(max_sec))))
    os.makedirs(output_dir, exist_ok=True)
    total = probe_duration(source)

    manual = parse_manual_ranges(manual_ranges) if manual_ranges.strip() else []
    items: list[dict] = []
    if not manual or with_subtitles:
        report("transkripsi audio dengan Whisper (bisa lama untuk video panjang)", 0.05)
        transcript = subtitle.transcribe(source)
        if transcript is None:
            raise ClipperError(WHISPER_HINT)
        items = transcript

    if manual:
        highlights = normalize_highlights(manual, items, total, len(manual), 1, total, snap=False)
    else:
        report("AI memilih momen terbaik", 0.35)
        highlights = normalize_highlights(
            select_highlights(items, count, min_sec, max_sec), items, total, count, min_sec, max_sec
        )
    if not highlights:
        raise ClipperError("tidak ada momen valid untuk dipotong (cek durasi video dan rentang waktu)")

    style = style or VideoParams(video_subject="clip")
    style = style.model_copy(update={"video_aspect": VideoAspect(aspect), "bgm_type": "",
                                     "voice_volume": 1.0, "subtitle_enabled": True})
    results = []
    for i, h in enumerate(highlights, start=1):
        report(f"membuat klip {i}/{len(highlights)} ({format_time(h.start)} - {format_time(h.end)})",
               0.4 + 0.6 * (i - 1) / len(highlights))
        raw = os.path.join(output_dir, f"clip-{i:02d}-raw.mp4")
        final = os.path.join(output_dir, f"clip-{i:02d}.mp4")
        cut_clip(source, h.start, h.end, raw, aspect)

        clip_subs = subtitles_for_range(items, h.start, h.end) if with_subtitles else []
        if clip_subs:
            srt = os.path.join(output_dir, f"clip-{i:02d}.srt")
            subtitle.write_srt(clip_subs, srt)
            video_service.generate_video(raw, raw, srt, final, style)
            os.remove(raw)
        else:
            os.replace(raw, final)
        results.append(ClipResult(path=final, start=h.start, end=h.end, title=h.title, subtitles=clip_subs))

    report("selesai", 1.0)
    return results


def new_job_dir() -> str:
    return utils.storage_dir(os.path.join("clips", utils.get_uuid()), create=True)


YOUTUBE_URL = re.compile(r"^https?://(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", re.I)


def download_youtube(url: str, output_dir: str, max_height: int = 1080,
                     progress: Callable[[str, float], None] | None = None) -> str:
    """Unduh video YouTube (maks. `max_height`p) ke output_dir sebagai mp4. Return path file."""
    url = url.strip()
    if not YOUTUBE_URL.match(url):
        raise ClipperError("link harus berupa link YouTube (youtube.com atau youtu.be)")
    try:
        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError
    except ImportError as e:
        raise ClipperError("yt-dlp belum terpasang. Jalankan: pip install -r requirements.txt") from e

    def hook(d):
        if progress and d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                progress("mengunduh video dari YouTube", min(d.get("downloaded_bytes", 0) / total, 1.0))

    opts = {
        "format": f"bv*[height<={max_height}]+ba/b[height<={max_height}]/b",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "source.%(ext)s"),
        "ffmpeg_location": FFMPEG_BINARY,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [hook],
    }
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
    except DownloadError as e:
        raise ClipperError(
            f"gagal mengunduh dari YouTube: {e}. Coba perbarui yt-dlp: pip install -U yt-dlp"
        ) from e
    # setelah merge, ekstensi akhir bisa berbeda dari yang dilaporkan prepare_filename
    mp4 = os.path.splitext(path)[0] + ".mp4"
    if os.path.isfile(mp4):
        return mp4
    if os.path.isfile(path):
        return path
    raise ClipperError("unduhan selesai tetapi file video tidak ditemukan")
