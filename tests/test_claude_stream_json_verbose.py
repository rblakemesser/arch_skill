import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

STREAM_JSON_DOCS = [
    "skills/agent-delegate/references/model-and-invocation.md",
    "skills/fresh-consult/references/model-and-invocation.md",
    "skills/model-consensus/references/model-and-invocation.md",
    "skills/stepwise/references/session-resume.md",
]


class ClaudeStreamJsonVerboseDoctrineTests(unittest.TestCase):
    def test_stream_json_command_doctrine_mentions_verbose_near_every_use(self):
        for relpath in STREAM_JSON_DOCS:
            body = (REPO_ROOT / relpath).read_text(encoding="utf-8")
            start = 0
            while True:
                idx = body.find("--output-format stream-json", start)
                if idx == -1:
                    break
                window = body[max(0, idx - 100):idx + 300]
                with self.subTest(relpath=relpath, offset=idx):
                    self.assertIn("--verbose", window)
                start = idx + 1


if __name__ == "__main__":
    unittest.main()
