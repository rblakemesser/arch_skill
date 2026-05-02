#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).with_name("agent_history.py")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


class AgentHistoryScriptTests(unittest.TestCase):
    def run_tool(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def extract_run_dir(self, stdout: str) -> Path:
        match = re.search(r"run=([^\s]+)", stdout)
        self.assertIsNotNone(match, stdout)
        return Path(match.group(1))

    def make_codex_home(self, root: Path, project: Path) -> Path:
        home = root / "codex"
        home.mkdir()
        rollout = home / "sessions" / "2026" / "05" / "02" / "rollout-2026-05-02T10-00-00-codex-thread.jsonl"
        write_jsonl(
            rollout,
            [
                {
                    "timestamp": now_iso(),
                    "type": "session_meta",
                    "payload": {"id": "codex-thread", "cwd": str(project)},
                },
                {
                    "timestamp": now_iso(),
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "text", "text": "Actually use helper scripts instead."}],
                    },
                },
                {
                    "timestamp": now_iso(),
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "create_goal",
                        "arguments": "{\"objective\":\"ship agent-history\"}",
                    },
                },
            ],
        )
        write_jsonl(
            home / "history.jsonl",
            [
                {
                    "session_id": "codex-thread",
                    "ts": int(datetime.now(timezone.utc).timestamp()),
                    "text": "What prompt did I run here?",
                }
            ],
        )
        conn = sqlite3.connect(home / "state_5.sqlite")
        conn.execute(
            """
            CREATE TABLE threads (
                id TEXT,
                rollout_path TEXT,
                cwd TEXT,
                title TEXT,
                created_at_ms INTEGER,
                updated_at_ms INTEGER,
                first_user_message TEXT,
                model TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE thread_goals (
                thread_id TEXT PRIMARY KEY,
                goal_id TEXT,
                objective TEXT,
                status TEXT,
                token_budget INTEGER,
                tokens_used INTEGER,
                time_used_seconds INTEGER,
                created_at_ms INTEGER,
                updated_at_ms INTEGER
            )
            """
        )
        conn.execute(
            "INSERT INTO threads VALUES (?,?,?,?,?,?,?,?)",
            (
                "codex-thread",
                str(rollout),
                str(project),
                "Agent history work",
                now_ms(),
                now_ms(),
                "What prompt did I run here?",
                "gpt-test",
            ),
        )
        conn.execute(
            "INSERT INTO thread_goals VALUES (?,?,?,?,?,?,?,?,?)",
            (
                "codex-thread",
                "goal-1",
                "ship agent-history",
                "active",
                None,
                10,
                0,
                now_ms(),
                now_ms(),
            ),
        )
        conn.commit()
        conn.close()
        return home

    def make_claude_home(self, root: Path, project: Path) -> Path:
        home = root / "claude"
        home.mkdir()
        write_jsonl(
            home / "history.jsonl",
            [
                {
                    "display": "/arch-step status",
                    "project": str(project),
                    "sessionId": "claude-session",
                    "timestamp": now_ms(),
                },
                {
                    "display": "Find all the places I corrected the agent",
                    "project": str(project),
                    "sessionId": "claude-session",
                    "timestamp": now_ms(),
                },
            ],
        )
        project_file = home / "projects" / "-tmp-project" / "claude-session.jsonl"
        write_jsonl(
            project_file,
            [
                {
                    "type": "custom-title",
                    "customTitle": "Claude history work",
                    "sessionId": "claude-session",
                    "timestamp": now_iso(),
                },
                {
                    "type": "user",
                    "sessionId": "claude-session",
                    "cwd": str(project),
                    "timestamp": now_iso(),
                    "message": {
                        "role": "user",
                        "content": "No, that is wrong; use the bundled helper.",
                    },
                },
                {
                    "type": "queue-operation",
                    "sessionId": "claude-session",
                    "cwd": str(project),
                    "timestamp": now_iso(),
                    "operation": "enqueue",
                    "content": "/goal improve history lookup",
                },
            ],
        )
        return home

    def test_codex_prompts_and_show(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            codex_home = self.make_codex_home(root, project)
            out_root = root / "runs"
            proc = self.run_tool(
                "prompts",
                "--runtime",
                "codex",
                "--codex-home",
                str(codex_home),
                "--cwd",
                str(project),
                "--output-root",
                str(out_root),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("OK agent-history prompts", proc.stdout)
            self.assertIn("What prompt did I run here?", proc.stdout)
            run_dir = self.extract_run_dir(proc.stdout)
            self.assertTrue((run_dir / "results.jsonl").exists())

            show = self.run_tool("show", "--run", str(run_dir), "--id", "r0001")
            self.assertEqual(show.returncode, 0, show.stderr)
            self.assertIn("What prompt did I run here?", show.stdout)

    def test_codex_goals_include_state_and_tool_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            codex_home = self.make_codex_home(root, project)
            proc = self.run_tool(
                "goals",
                "--runtime",
                "codex",
                "--codex-home",
                str(codex_home),
                "--cwd",
                str(project),
                "--since",
                "today",
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("ship agent-history", proc.stdout)
            self.assertIn("create_goal", proc.stdout)

    def test_claude_commands_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            claude_home = self.make_claude_home(root, project)
            commands = self.run_tool(
                "commands",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(commands.returncode, 0, commands.stderr)
            self.assertIn("/arch-step status", commands.stdout)
            self.assertIn("/goal improve history lookup", commands.stdout)

            search = self.run_tool(
                "search",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs2"),
                "wrong",
            )
            self.assertEqual(search.returncode, 0, search.stderr)
            self.assertIn("No, that is wrong", search.stdout)

    def test_current_project_scope_filters_other_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            other = root / "other"
            project.mkdir()
            other.mkdir()
            claude_home = self.make_claude_home(root, project)
            write_jsonl(
                claude_home / "projects" / "-other" / "other-session.jsonl",
                [
                    {
                        "type": "user",
                        "sessionId": "other-session",
                        "cwd": str(other),
                        "timestamp": now_iso(),
                        "message": {"role": "user", "content": "wrong project marker"},
                    }
                ],
            )
            proc = self.run_tool(
                "search",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
                "wrong",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn("wrong project marker", proc.stdout)
            self.assertIn("No, that is wrong", proc.stdout)


if __name__ == "__main__":
    unittest.main()
