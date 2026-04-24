"""Regression tests for Stepwise deterministic plumbing.

Run: `python3 skills/stepwise/scripts/test_run_stepwise.py`
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_source_tags as cst  # noqa: E402
import run_stepwise as rs  # noqa: E402
import stepwise_learnings as sl  # noqa: E402


_PASS_VERDICT = {
    "step_n": 2,
    "verdict": "pass",
    "checks": [
        {
            "name": "artifact_exists",
            "status": "pass",
            "evidence": "file exists and header matches",
        }
    ],
    "observed_breach": None,
    "evidence_pointers": [],
    "contract_clauses_implicated": [],
    "summary": "Step 2 produced outline.md with the expected header.",
    "abstain_reason": None,
}

_RESULT_EVENT = {
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327",
    "stop_reason": "end_turn",
    "result": "diagnostic answer",
    "structured_output": _PASS_VERDICT,
}

_STREAM_EVENTS = [
    {"type": "system", "subtype": "init", "session_id": "aa86534c-57f3-4b99-8f34-c48821a3f327"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "..."}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "..."}]}},
    _RESULT_EVENT,
]


def _stdout_from(obj) -> str:
    return "\n".join(["(prior lifecycle noise)", json.dumps(obj)])


class ClaudeShapeParsing(unittest.TestCase):
    def test_result_event_dict_passthrough(self):
        self.assertIs(rs._extract_claude_result_event(_RESULT_EVENT), _RESULT_EVENT)

    def test_result_event_list_shape(self):
        self.assertIs(rs._extract_claude_result_event(_STREAM_EVENTS), _RESULT_EVENT)

    def test_parse_session_id_from_dict_and_list(self):
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_RESULT_EVENT)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )
        self.assertEqual(
            rs._parse_claude_session_id(_stdout_from(_STREAM_EVENTS)),
            "aa86534c-57f3-4b99-8f34-c48821a3f327",
        )

    def test_extract_verdict_from_final(self):
        self.assertEqual(rs._extract_verdict_from_final(_RESULT_EVENT), _PASS_VERDICT)
        self.assertEqual(rs._extract_verdict_from_final(_STREAM_EVENTS), _PASS_VERDICT)


class StepVerdictValidation(unittest.TestCase):
    def test_valid_observational_pass(self):
        self.assertEqual(rs._validate_step_verdict(_PASS_VERDICT), [])

    def test_valid_observational_fail(self):
        verdict = {
            "step_n": 3,
            "verdict": "fail",
            "checks": [
                {
                    "name": "skill_order_adherence",
                    "status": "fail",
                    "evidence": "owner runbook read happened after write",
                }
            ],
            "observed_breach": "The worker edited before owner-doctrine evidence was loaded.",
            "evidence_pointers": ["steps/3/try-1/stream.log"],
            "contract_clauses_implicated": ["owner SKILL.md: read doctrine before edit"],
            "summary": "The attempt failed doctrine order.",
            "abstain_reason": None,
        }
        self.assertEqual(rs._validate_step_verdict(verdict), [])

    def test_stale_resume_hint_is_rejected(self):
        verdict = dict(_PASS_VERDICT)
        verdict["resume_hint"] = {"headline": "old", "required_fixes": [], "do_not_redo": []}
        errors = rs._validate_step_verdict(verdict)
        self.assertTrue(any("resume_hint is no longer accepted" in e for e in errors))

    def test_stale_route_to_step_is_rejected(self):
        verdict = dict(_PASS_VERDICT)
        verdict["route_to_step_n"] = 1
        errors = rs._validate_step_verdict(verdict)
        self.assertTrue(any("route_to_step_n is no longer accepted" in e for e in errors))

    def test_fail_requires_observation_evidence_and_clause(self):
        verdict = {
            "step_n": 2,
            "verdict": "fail",
            "checks": [],
            "observed_breach": "",
            "evidence_pointers": [],
            "contract_clauses_implicated": [],
            "summary": "Failed.",
            "abstain_reason": None,
        }
        errors = rs._validate_step_verdict(verdict)
        self.assertIn("observed_breach must be null or a non-empty string", errors)
        self.assertIn("observed_breach must be a non-empty string on fail", errors)
        self.assertIn("evidence_pointers must be non-empty on fail", errors)
        self.assertIn("contract_clauses_implicated must be non-empty on fail", errors)


class CodexSchemaNormalization(unittest.TestCase):
    def test_optional_schema_fields_become_required_nullable(self):
        schema = {
            "type": "object",
            "required": ["step_n", "verdict", "checks", "summary"],
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {"type": "array", "items": {"type": "object", "properties": {}}},
                "observed_breach": {"type": "string"},
                "evidence_pointers": {"type": "array", "items": {"type": "string"}},
                "contract_clauses_implicated": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"},
                "abstain_reason": {"type": "string"},
            },
        }
        normalized = rs._codex_strict_schema(schema)
        self.assertEqual(set(normalized["required"]), set(normalized["properties"]))
        self.assertEqual(
            normalized["properties"]["observed_breach"]["type"],
            ["string", "null"],
        )
        self.assertEqual(
            normalized["properties"]["abstain_reason"]["type"],
            ["string", "null"],
        )

    def test_critic_spawn_uses_observational_schema(self):
        old_run_subprocess = rs._run_subprocess
        captured = {}

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            schema_path = Path(argv[argv.index("--output-schema") + 1])
            final_path = Path(argv[argv.index("-o") + 1])
            final_path.write_text(json.dumps(_PASS_VERDICT), encoding="utf-8")
            captured["schema_path"] = schema_path
            return 0, ""

        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": list(_PASS_VERDICT.keys()),
            "properties": {
                "step_n": {"type": "integer"},
                "verdict": {"enum": ["pass", "fail", "abstain"]},
                "checks": {"type": "array", "items": {"type": "object", "properties": {}}},
                "observed_breach": {"type": ["string", "null"]},
                "evidence_pointers": {"type": "array", "items": {"type": "string"}},
                "contract_clauses_implicated": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"},
                "abstain_reason": {"type": ["string", "null"]},
            },
        }

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "prompt.md"
            prompt.write_text("judge step\n", encoding="utf-8")
            schema_file = Path(td) / "schema.json"
            schema_file.write_text(json.dumps(schema), encoding="utf-8")

            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "critic-spawn",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "gpt-5.4",
                    "--effort",
                    "high",
                    "--schema-file",
                    str(schema_file),
                    "--runtime",
                    "codex",
                    "--step-n",
                    "1",
                    "--try-k",
                    "1",
                ]
            )

            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            normalized = json.loads(captured["schema_path"].read_text(encoding="utf-8"))

        self.assertEqual(set(normalized["required"]), set(normalized["properties"]))
        self.assertNotIn("resume_hint", normalized["properties"])


class InitRunAndPromptArtifacts(unittest.TestCase):
    def test_init_run_narrows_gitignore_and_stores_diagnostic_cap(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "orchestrator"
            target = Path(td) / "target"
            root.mkdir()
            target.mkdir()
            (root / ".gitignore").write_text(".arch_skill/\n", encoding="utf-8")
            raw = Path(td) / "raw.txt"
            raw.write_text("run process\n", encoding="utf-8")
            execution = {
                "schema_version": 2,
                "execution_defaults": {
                    "step": {
                        "runtime": "codex",
                        "model": "gpt-5.4",
                        "effort": "high",
                        "source": "user",
                    },
                    "critic": {
                        "runtime": "codex",
                        "model": "gpt-5.4-mini",
                        "effort": "high",
                        "source": "user",
                    },
                },
                "execution_preferences": [],
            }
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "init-run",
                    "--orchestrator-root",
                    str(root),
                    "--target-repo",
                    str(target),
                    "--raw-instructions-file",
                    str(raw),
                    "--profile",
                    "balanced",
                    "--stop-discipline",
                    "halt_and_ask",
                    "--per-step-retry-cap",
                    "5",
                    "--execution-json",
                    json.dumps(execution),
                ]
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(args.func(args), 0)
            [run_dir] = list((root / ".arch_skill" / "stepwise" / "runs").iterdir())
            state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
            gitignore = (root / ".gitignore").read_text(encoding="utf-8")

        self.assertEqual(state["diagnostic_turn_cap"], 10)
        self.assertIn(".arch_skill/stepwise/runs/", gitignore)
        self.assertNotIn(".arch_skill/\n", gitignore)

    def test_step_spawn_saves_prompt(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            payload = dict(_RESULT_EVENT)
            stdout = json.dumps(payload)
            stdout_stream_path.write_text(stdout, encoding="utf-8")
            return 0, stdout

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            prompt = Path(td) / "prompt.md"
            prompt.write_text("do the step\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-spawn",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "haiku",
                    "--effort",
                    "low",
                    "--runtime",
                    "claude",
                    "--step-n",
                    "1",
                    "--try-k",
                    "1",
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            self.assertEqual(
                (run_dir / "steps" / "1" / "try-1" / "prompt.md").read_text(encoding="utf-8"),
                "do the step\n",
            )


class DiagnosticCommand(unittest.TestCase):
    def test_step_diagnose_writes_diagnostic_turn_without_new_try(self):
        old_run_subprocess = rs._run_subprocess

        def fake_run(argv, stdout_stream_path, out_dir, cwd=None, stamp_prefix=None):
            final_path = Path(argv[argv.index("-o") + 1])
            final_path.write_text("I understand the issue.\n", encoding="utf-8")
            stdout_stream_path.write_text(
                '{"type":"thread.started","thread_id":"thread-1"}\n',
                encoding="utf-8",
            )
            return 0, '{"type":"thread.started","thread_id":"thread-1"}\n'

        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run"
            target = Path(td) / "target"
            run_dir.mkdir()
            target.mkdir()
            (run_dir / "state.json").write_text("{}\n", encoding="utf-8")
            (run_dir / "steps" / "6" / "try-1").mkdir(parents=True)
            prompt = Path(td) / "diag.md"
            prompt.write_text("Diagnostic conversation only.\n", encoding="utf-8")
            parser = rs._build_parser()
            args = parser.parse_args(
                [
                    "step-diagnose",
                    "--run-dir",
                    str(run_dir),
                    "--target-repo",
                    str(target),
                    "--prompt-file",
                    str(prompt),
                    "--model",
                    "gpt-5.4",
                    "--effort",
                    "high",
                    "--session-id",
                    "thread-1",
                    "--runtime",
                    "codex",
                    "--step-n",
                    "6",
                    "--try-k",
                    "1",
                    "--round-k",
                    "2",
                    "--with-step-m",
                    "4",
                ]
            )
            try:
                rs._run_subprocess = fake_run
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(args.func(args), 0)
            finally:
                rs._run_subprocess = old_run_subprocess

            diag = run_dir / "steps" / "6" / "try-1" / "diagnostic"
            self.assertTrue((diag / "turn-2.with-step-4.prompt.md").is_file())
            self.assertTrue((diag / "turn-2.with-step-4.response.md").is_file())
            self.assertFalse((run_dir / "steps" / "6" / "try-2").exists())


class SourceTagChecker(unittest.TestCase):
    def test_numbered_repair_steps_require_source_tags(self):
        with tempfile.TemporaryDirectory() as td:
            good = Path(td) / "good.md"
            bad = Path(td) / "bad.md"
            good.write_text("1. Do thing. [source: manifest]\n", encoding="utf-8")
            bad.write_text("1. Do thing.\n", encoding="utf-8")
            self.assertEqual(cst.check_file(good), [])
            self.assertEqual(len(cst.check_file(bad)), 1)


class LearningLedger(unittest.TestCase):
    def _entry(self) -> dict:
        return {
            "schema_version": 1,
            "source": {
                "run_id": "run-1",
                "step_n": 6,
                "try_k": 1,
                "diagnostic_path": "steps/6/try-1/diagnostic/",
            },
            "scope": {
                "owner_skill": "$lesson-copy-discipline",
                "failure_class": "copy-gate",
                "surface": "copy",
                "support_skills": [],
            },
            "observation": "Worker treated placeholder cleanup as non-copy.",
            "underlying_principle": "Learner-visible placeholder cleanup is copy work.",
            "applicability_test": "Apply when a worker inserts learner-visible copy.",
            "contraindications": "Do not apply to non-visible metadata cleanup.",
            "process_change_suggestion": "Ask the worker whether it made a copy exception.",
            "promotion_target": "skills/stepwise/references/examples.md",
        }

    def test_append_is_idempotent_and_transition_updates_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")

            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out1:
                self.assertEqual(append_args.func(append_args), 0)
            first_id = out1.getvalue().strip()
            with contextlib.redirect_stdout(io.StringIO()) as out2:
                self.assertEqual(append_args.func(append_args), 0)
            self.assertEqual(out2.getvalue().strip(), first_id)

            accept_args = parser.parse_args(["--root", str(root), "accept", first_id])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(accept_args.func(accept_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[first_id]["status"], "accepted")

    def test_sync_from_md_accepts_known_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "learnings"
            entry_file = Path(td) / "entry.json"
            entry_file.write_text(json.dumps(self._entry()), encoding="utf-8")
            parser = sl._build_parser()
            append_args = parser.parse_args(
                ["--root", str(root), "append", "--entry-file", str(entry_file)]
            )
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(append_args.func(append_args), 0)
            learning_id = out.getvalue().strip()
            (root / "accepted.md").write_text(f"# Accepted\n\n## {learning_id}\n", encoding="utf-8")

            sync_args = parser.parse_args(["--root", str(root), "sync-from-md"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(sync_args.func(sync_args), 0)

            events = sl._current_by_id(sl._events(root))
            self.assertEqual(events[learning_id]["status"], "accepted")


if __name__ == "__main__":
    unittest.main()
