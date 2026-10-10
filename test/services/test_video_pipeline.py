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

from app.models.schema import VideoAspect, VideoConcatMode  # noqa: E402
from app.services import video as vd  # noqa: E402

resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")


class TestVideoPipeline(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.audio = os.path.join(self.work, "audio.mp3")
        subprocess.run([FFMPEG_BINARY, "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                        "sine=frequency=440:duration=8", self.audio], check=True)
        self.sources = [os.path.join(resources_dir, f"{i}.png.mp4") for i in (1, 2, 3)]

    def tearDown(self):
        shutil.rmtree(self.work, ignore_errors=True)

    def test_combine_videos_with_no_transition_mode_produces_full_video(self):
        # video_transition_mode=None adalah default di API; dulu setiap klip gagal diproses
        out = os.path.join(self.work, "combined.mp4")
        vd.combine_videos(out, self.sources, self.audio, VideoAspect.portrait,
                          VideoConcatMode.sequential, None, max_clip_duration=2, threads=2)
        clip = VideoFileClip(out)
        self.assertGreaterEqual(clip.duration, 8)
        self.assertEqual(list(clip.size), [1080, 1920])
        self.assertIsNone(clip.audio)
        clip.close()
        self.assertEqual(sorted(os.listdir(self.work)), ["audio.mp3", "combined.mp4"])

    def test_concat_without_reencode_repeats_and_handles_quotes(self):
        quoted = os.path.join(self.work, "it's.mp4")
        shutil.copy(self.sources[0], quoted)
        out = os.path.join(self.work, "out.mp4")
        vd.concat_without_reencode([quoted, quoted, quoted], out, self.work)
        clip = VideoFileClip(out)
        self.assertAlmostEqual(clip.duration, 9, delta=0.2)
        clip.close()
        self.assertFalse(os.path.exists(os.path.join(self.work, "temp-concat-list.txt")))

    def test_resolve_font_falls_back_and_blocks_traversal(self):
        self.assertTrue(vd.resolve_font("NotoSans-Bold.ttf").endswith("resource/fonts/NotoSans-Bold.ttf"))
        self.assertTrue(vd.resolve_font("Missing.ttc").endswith("NotoSans-Bold.ttf"))
        self.assertTrue(vd.resolve_font(None).endswith("NotoSans-Bold.ttf"))
        self.assertIn("resource/fonts", vd.resolve_font("../../../etc/passwd"))

    def test_random_bgm_with_empty_song_dir_returns_empty(self):
        empty = os.path.join(self.work, "songs")
        os.makedirs(empty)
        with mock.patch.object(vd.utils, "song_dir", return_value=empty):
            self.assertEqual(vd.get_bgm_file("random"), "")


if __name__ == "__main__":
    unittest.main()
