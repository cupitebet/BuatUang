import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.config import config  # noqa: E402
from app.services import llm  # noqa: E402


class TestGeminiProvider(unittest.TestCase):
    def setUp(self):
        self.saved = dict(config.app)
        config.app.update(llm_provider="gemini", gemini_api_key="k", gemini_model_name="gemini-flash-latest")

    def tearDown(self):
        config.app.clear()
        config.app.update(self.saved)

    def _client(self, text):
        client = mock.MagicMock()
        client.models.generate_content.return_value = SimpleNamespace(text=text)
        return client

    def test_uses_google_genai_client(self):
        client = self._client("naskah video")
        with mock.patch("google.genai.Client", return_value=client) as ctor:
            self.assertEqual(llm._generate_response("prompt"), "naskah video")
        ctor.assert_called_once_with(api_key="k")
        kwargs = client.models.generate_content.call_args.kwargs
        self.assertEqual((kwargs["model"], kwargs["contents"]), ("gemini-flash-latest", "prompt"))
        self.assertEqual(len(kwargs["config"].safety_settings), 4)

    def test_blocked_response_is_reported_as_error(self):
        with mock.patch("google.genai.Client", return_value=self._client(None)):
            self.assertTrue(llm._generate_response("prompt").startswith("Error: "))


if __name__ == "__main__":
    unittest.main()
