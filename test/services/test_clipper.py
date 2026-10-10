import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from moviepy import VideoFileClip  # noqa: E402
from moviepy.config import FFMPEG_BINARY  # noqa: E402

from app.models.schema import VideoAspect  # noqa: E402
from app.services import clipper  # noqa: E402
from app.services.clipper import ClipperError, Highlight  # noqa: E402

# transkrip tiruan: kalimat 5 detik dari 0 sampai 60 detik
ITEMS = [{"msg": f"Kalimat {i}", "start_time": i * 5.0, "end_time": i * 5.0 + 4.5} for i in range(12)]


def make_video(path, seconds=60, size="1280x720"):
    subprocess.run([FFMPEG_BINARY, "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", f"testsrc=size={size}:rate=30:duration={seconds}",
                    "-f", "lavfi", "-i", f"sine=frequency=300:duration={seconds}",
                    "-shortest", "-c:v", "libx264", "-c:a", "aac", path], check=True)


class TestParsing(unittest.TestCase):
    def test_parse_time(self):
        self.assertEqual(clipper.parse_time("1:02:03.5"), 3723.5)
        self.assertEqual(clipper.parse_time("02:03"), 123)
        self.assertEqual(clipper.parse_time("90,5"), 90.5)
        for bad in ("", "1:2:3:4", "abc", "1:-2"):
            with self.assertRaises(ValueError):
                clipper.parse_time(bad)

    def test_parse_manual_ranges(self):
        hs = clipper.parse_manual_ranges("# komentar\n00:10 - 00:40 Tips hemat\n\n1:00:00–1:00:30\n")
        self.assertEqual([(h.start, h.end, h.title) for h in hs], [(10, 40, "Tips hemat"), (3600, 3630, "")])
        with self.assertRaises(ValueError):
            clipper.parse_manual_ranges("00:40 - 00:10")
        with self.assertRaises(ValueError):
            clipper.parse_manual_ranges("mulai menit 10")


class TestHighlightSelection(unittest.TestCase):
    def test_llm_response_is_parsed_from_noisy_text(self):
        reply = 'Berikut hasilnya: [{"start": 1, "end": 30, "title": "A", "score": 9}, {"start": "x"}]'
        with mock.patch.object(clipper.llm, "_generate_response", return_value=reply):
            hs = clipper.select_highlights(ITEMS, 3, 15, 60)
        self.assertEqual([(h.start, h.end, h.title, h.score) for h in hs], [(1, 30, "A", 9)])

    def test_llm_error_is_raised(self):
        with mock.patch.object(clipper.llm, "_generate_response", return_value="Error: kuota habis"):
            with self.assertRaisesRegex(ClipperError, "kuota habis"):
                clipper.select_highlights(ITEMS, 3, 15, 60)

    def test_long_transcript_is_split_into_chunks(self):
        reply = json.dumps([{"start": 0, "end": 20, "title": "x", "score": 5}])
        with mock.patch.object(clipper, "TRANSCRIPT_CHUNK_CHARS", 60), \
                mock.patch.object(clipper.llm, "_generate_response", return_value=reply) as gen:
            clipper.select_highlights(ITEMS, 2, 15, 60)
        self.assertGreater(gen.call_count, 1)

    def test_normalize_snaps_fits_and_removes_overlap(self):
        hs = [
            Highlight(7, 23, "tengah kalimat", 6),      # -> 5..24.5 (snap ke kalimat)
            Highlight(10, 50, "tumpang tindih", 9),     # skor tertinggi, dipotong ke maks 30 dtk
            Highlight(52, 54, "terlalu pendek", 4),     # diperpanjang ke min 15 dtk, mentok di akhir video (60)
            Highlight(70, 80, "di luar video", 10),
        ]
        out = clipper.normalize_highlights(hs, ITEMS, total=60, count=5, min_sec=15, max_sec=30)
        self.assertEqual([(h.title, h.start, h.end) for h in out],
                         [("tumpang tindih", 10.0, 39.5), ("terlalu pendek", 50.0, 60.0)])
        for h in out:
            self.assertLessEqual(h.duration, 30)

    def test_subtitles_for_range_shifts_times(self):
        subs = clipper.subtitles_for_range(ITEMS, 12, 22)
        self.assertEqual([(s["msg"], s["start_time"], s["end_time"]) for s in subs],
                         [("Kalimat 2", 0, 2.5), ("Kalimat 3", 3, 7.5), ("Kalimat 4", 8, 10)])


class TestClipRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.mkdtemp()
        cls.src = os.path.join(cls.work, "podcast.mp4")
        make_video(cls.src)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.work, ignore_errors=True)

    def test_cut_clip_all_aspects_keep_audio(self):
        for aspect, size in ((VideoAspect.portrait, [1080, 1920]), (VideoAspect.square, [1080, 1080]),
                             (VideoAspect.landscape, [1920, 1080])):
            out = os.path.join(self.work, f"cut-{aspect.name}.mp4")
            clipper.cut_clip(self.src, 5, 15, out, aspect)
            c = VideoFileClip(out)
            self.assertEqual(list(c.size), size)
            self.assertAlmostEqual(c.duration, 10, delta=0.2)
            self.assertIsNotNone(c.audio)
            c.close()

    def test_ai_mode_with_subtitles(self):
        out_dir = os.path.join(self.work, "ai")
        reply = json.dumps([{"start": 3, "end": 22, "title": "Momen A", "score": 8},
                            {"start": 31, "end": 48, "title": "Momen B", "score": 7}])
        with mock.patch.object(clipper.subtitle, "transcribe", return_value=ITEMS), \
                mock.patch.object(clipper.llm, "_generate_response", return_value=reply):
            results = clipper.make_clips(self.src, out_dir, count=2, min_sec=10, max_sec=30)
        self.assertEqual([(r.title, r.start, r.end) for r in results],
                         [("Momen A", 0.0, 24.5), ("Momen B", 30.0, 49.5)])
        for r in results:
            c = VideoFileClip(r.path)
            self.assertEqual(list(c.size), [1080, 1920])
            self.assertAlmostEqual(c.duration, r.end - r.start, delta=0.3)
            self.assertIsNotNone(c.audio)
            c.close()
            self.assertTrue(r.subtitles)
        self.assertFalse([f for f in os.listdir(out_dir) if f.endswith("-raw.mp4")])

    def test_manual_mode_without_subtitles_needs_no_whisper(self):
        out_dir = os.path.join(self.work, "manual")
        with mock.patch.object(clipper.subtitle, "transcribe", side_effect=AssertionError("tidak dipanggil")):
            results = clipper.make_clips(self.src, out_dir, with_subtitles=False,
                                         manual_ranges="00:05 - 00:12 Intro\n00:40 - 01:30 Penutup")
        self.assertEqual([(r.start, r.end) for r in results], [(5, 12), (40, 60)])
        self.assertTrue(all(os.path.isfile(r.path) for r in results))

    def test_ai_mode_without_whisper_explains_install(self):
        with mock.patch.object(clipper.subtitle, "transcribe", return_value=None):
            with self.assertRaisesRegex(ClipperError, "requirements-whisper"):
                clipper.make_clips(self.src, os.path.join(self.work, "nowhisper"))


class TestYoutubeDownload(unittest.TestCase):
    def test_rejects_non_youtube_links(self):
        for url in ("https://example.com/v.mp4", "file:///etc/passwd", "youtube.com/watch?v=x"):
            with self.assertRaises(ClipperError):
                clipper.download_youtube(url, tempfile.gettempdir())

    def test_downloads_with_expected_options(self):
        out_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, out_dir, True)
        target = os.path.join(out_dir, "source.mp4")

        class FakeYDL:
            def __init__(self, opts):
                FakeYDL.opts = opts

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def extract_info(self, url, download):
                open(target, "wb").close()
                return {"ext": "webm"}

            def prepare_filename(self, info):
                return os.path.join(out_dir, "source.webm")

        with mock.patch("yt_dlp.YoutubeDL", FakeYDL):
            path = clipper.download_youtube("https://youtu.be/abc123", out_dir, max_height=720)
        self.assertEqual(path, target)
        self.assertIn("height<=720", FakeYDL.opts["format"])
        self.assertTrue(FakeYDL.opts["noplaylist"])
        self.assertEqual(FakeYDL.opts["merge_output_format"], "mp4")


if __name__ == "__main__":
    unittest.main()
