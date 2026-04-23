"""Regression tests for Claude stdout shape normalization in run_stepwise.

Claude `-p --output-format json` emits either a single top-level result dict
OR a list of stream events (when `--json-schema` is combined with tool use).
The three parsers the orchestrator relies on must handle both shapes. These
tests pin that behavior.

Run: `python3 skills/stepwise/scripts/test_run_stepwise.py`
"""

import json
import sys
import unittest
from pathlib import Path

# Import the module under test without executing argparse.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_stepwise as rs  # noqa: E402


# A minimal result event mirroring the real shape captured from a critic run
# with tool use: the orchestrator only needs type=result + session_id +
# structured_output. Other fields exist in production but are irrelevant here.
_RESULT_EVENT = {
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327",
    "stop_reason": "end_turn",
    "structured_output": {
        "step_n": 2,
        "verdict": "pass",
        "checks": [
            {
                "name": "artifact_exists",
                "status": "pass",
                "evidence": "file exists and header matches",
            }
        ],
        "summary": "Step 2 produced outline.md with the expected header.",
    },
}

# A list-shape payload: several non-result events preceded by one result.
_STREAM_EVENTS = [
    {"type": "system", "subtype": "init", "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "..."}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "..."}]}},
    _RESULT_EVENT,
]


def _stdout_from(obj) -> str:
    """Simulate subprocess stdout: Claude's last line holds the JSON payload."""
    return "\n".join(["(prior lifecycle noise)", json.dumps(obj)])


class ExtractClaudeResultEvent(unittest.TestCase):
    def test_dict_passthrough(self):
        self.assertIs(rs._extract_claude_result_event(_RESULT_EVENT), _RESULT_EVENT)

    def test_list_finds_result_event(self):
        got = rs._extract_claude_result_event(_STREAM_EVENTS)
        self.assertIs(got, _RESULT_EVENT)

    def test_list_with_noise_after_result(self):
        # Defensive: if non-result events follow the result, we still find it.
        noisy = _STREAM_EVENTS + [{"type": "meta", "note": "extra"}]
        got = rs._extract_claude_result_event(noisy)
        self.assertIs(got, _RESULT_EVENT)

    def test_list_with_no_result_returns_none(self):
        self.assertIsNone(
            rs._extract_claude_result_event([{"type": "system"}, {"type": "assistant"}])
        )

    def test_garbage_returns_none(self):
        self.assertIsNone(rs._extract_claude_result_event(None))
        self.assertIsNone(rs._extract_claude_result_event("unexpected"))
        self.assertIsNone(rs._extract_claude_result_event(42))


class ParseClaudeSessionId(unittest.TestCase):
    def test_dict_shape(self):
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_RESULT_EVENT)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_list_shape_regression(self):
        """Before the fix, a list payload crashed in `.get('session_id')`.
        After the fix, we extract the session id from the embedded result
        event."""
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_STREAM_EVENTS)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_missing_session_id(self):
        dict_without = {"type": "result", "subtype": "success"}
        self.assertIsNone(rs._parse_claude_session_id(_stdout_from(dict_without)))

    def test_invalid_json(self):
        self.assertIsNone(rs._parse_claude_session_id("not json at all"))


class ParseClaudeFinalJson(unittest.TestCase):
    def test_dict_shape_returns_dict(self):
        got = rs._parse_claude_final_json(_stdout_from(_RESULT_EVENT))
        self.assertIsInstance(got, dict)
        self.assertEqual(got.get("type"), "result")

    def test_list_shape_returns_extracted_event(self):
        """Before the fix, callers expected a dict but got the raw list.
        After the fix, we return the extracted result event."""
        got = rs._parse_claude_final_json(_stdout_from(_STREAM_EVENTS))
        self.assertIsInstance(got, dict)
        self.assertEqual(got.get("session_id"), "aa86534c-57f3-4b99-8f34-c48821a3f327")


class ExtractVerdictFromFinal(unittest.TestCase):
    def test_dict_final(self):
        verdict = rs._extract_verdict_from_final(_RESULT_EVENT)
        self.assertIsInstance(verdict, dict)
        self.assertEqual(verdict.get("verdict"), "pass")

    def test_list_final_regression(self):
        """Before the fix, cmd_critic_spawn crashed here on list payloads."""
        verdict = rs._extract_verdict_from_final(_STREAM_EVENTS)
        self.assertIsInstance(verdict, dict)
        self.assertEqual(verdict.get("verdict"), "pass")
        self.assertEqual(verdict.get("step_n"), 2)

    def test_missing_structured_output(self):
        # Result event without structured_output → None, not a crash.
        ev = {"type": "result", "session_id": "x"}
        self.assertIsNone(rs._extract_verdict_from_final(ev))

    def test_no_result_event(self):
        self.assertIsNone(rs._extract_verdict_from_final([{"type": "system"}]))


if __name__ == "__main__":
    unittest.main()
