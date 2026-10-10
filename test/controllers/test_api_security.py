import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.asgi import app  # noqa: E402
from app.config import config  # noqa: E402
from app.utils import utils  # noqa: E402


class TestApiSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.saved_key = config.app.get("api_key", "")
        config.app["api_key"] = ""
        self.task_id = "test-security-task"
        self.task_path = os.path.join(utils.task_dir(), self.task_id)
        os.makedirs(self.task_path, exist_ok=True)
        with open(os.path.join(self.task_path, "final-1.mp4"), "wb") as f:
            f.write(b"0123456789")
        self.outside = tempfile.mkdtemp()

    def tearDown(self):
        config.app["api_key"] = self.saved_key
        shutil.rmtree(self.task_path, ignore_errors=True)
        shutil.rmtree(self.outside, ignore_errors=True)

    def test_download_and_stream_reject_paths_outside_tasks_dir(self):
        for url in (
            "/api/v1/download//etc/passwd",
            "/api/v1/download/..%2F..%2Fconfig.example.toml",
            "/api/v1/stream/..%2F..%2Fconfig.example.toml",
            "/api/v1/stream//etc/passwd",
        ):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 404, url)
            self.assertNotIn("root:", r.text)
            self.assertNotIn("[app]", r.text)

    def test_download_and_stream_still_serve_task_files(self):
        r = self.client.get(f"/api/v1/download/{self.task_id}/final-1.mp4")
        self.assertEqual((r.status_code, r.content), (200, b"0123456789"))
        r = self.client.get(f"/api/v1/stream/{self.task_id}/final-1.mp4", headers={"Range": "bytes=2-5"})
        self.assertEqual((r.status_code, r.content), (206, b"2345"))
        r = self.client.get(f"/api/v1/stream/{self.task_id}/final-1.mp4", headers={"Range": "bytes=-3"})
        self.assertEqual((r.status_code, r.content), (206, b"789"))
        r = self.client.get(f"/api/v1/stream/{self.task_id}/final-1.mp4", headers={"Range": "bytes=-10000"})
        self.assertEqual((r.status_code, r.content), (206, b"0123456789"))
        r = self.client.get(f"/api/v1/stream/{self.task_id}/final-1.mp4", headers={"Range": "bytes=abc"})
        self.assertEqual(r.status_code, 416)

    def test_bgm_upload_cannot_write_outside_song_dir(self):
        target = os.path.join(self.outside, "evil.mp3")
        r = self.client.post("/api/v1/musics", files={"file": (f"../../../../../../..{target}", b"x")})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(os.path.exists(target))
        saved = r.json()["data"]["file"]
        self.assertEqual(os.path.dirname(saved), utils.song_dir())
        os.remove(saved)

        r = self.client.post("/api/v1/musics", files={"file": ("../../x/notmp3", b"x")})
        self.assertEqual(r.status_code, 400)

    def test_api_key_enforced_when_configured(self):
        config.app["api_key"] = "s3cret"
        self.assertEqual(self.client.get("/api/v1/tasks").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/tasks", headers={"x-api-key": "wrong"}).status_code, 401)
        self.assertEqual(self.client.get("/api/v1/tasks", headers={"x-api-key": "s3cret"}).status_code, 200)
        self.assertEqual(self.client.post("/api/v1/scripts", json={}).status_code, 401)

    def test_api_open_when_no_key_configured(self):
        self.assertEqual(self.client.get("/api/v1/tasks").status_code, 200)


if __name__ == "__main__":
    unittest.main()
