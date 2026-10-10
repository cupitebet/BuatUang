import shutil
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.config import config  # noqa: E402
from app.models import const  # noqa: E402
from app.services import state as sm  # noqa: E402
from app.services import task as tm  # noqa: E402
from app.utils import utils  # noqa: E402

TASK_ID = "test-subtitle-failure"


class TestSubtitleFailure(unittest.TestCase):
    def setUp(self):
        self.saved = config.app.get("subtitle_provider")
        self.params = SimpleNamespace(subtitle_enabled=True)
        sm.state.update_task(TASK_ID)

    def tearDown(self):
        config.app["subtitle_provider"] = self.saved
        sm.state.delete_task(TASK_ID)
        shutil.rmtree(utils.task_dir(TASK_ID), ignore_errors=True)

    def test_whisper_unavailable_fails_task_instead_of_zero_length_subtitles(self):
        config.app["subtitle_provider"] = "whisper"
        with mock.patch.object(tm.subtitle, "create", return_value=None), \
                mock.patch.object(tm.subtitle, "correct") as correct:
            self.assertIsNone(tm.generate_subtitle(TASK_ID, self.params, "Halo. Dunia.", None, "a.mp3"))
        correct.assert_not_called()
        self.assertEqual(sm.state.get_task(TASK_ID)["state"], const.TASK_STATE_FAILED)

    def test_failed_whisper_fallback_keeps_video_without_subtitles(self):
        config.app["subtitle_provider"] = "edge"
        with mock.patch.object(tm.voice, "create_subtitle"), \
                mock.patch.object(tm.subtitle, "create", return_value=None), \
                mock.patch.object(tm.subtitle, "correct") as correct:
            self.assertEqual(tm.generate_subtitle(TASK_ID, self.params, "Halo.", None, "a.mp3"), "")
        correct.assert_not_called()
        self.assertNotEqual(sm.state.get_task(TASK_ID)["state"], const.TASK_STATE_FAILED)


if __name__ == "__main__":
    unittest.main()
