#!/usr/bin/env python3
"""Codex Stop hook for arch-step implement-loop."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


STATE_RELATIVE_PATH = Path(".codex/implement-loop-state.json")
EXPECTED_COMMAND = "implement-loop"
VERDICT_PATTERN = re.compile(r"^Verdict \(code\): (COMPLETE|NOT COMPLETE)\s*$", re.MULTILINE)


def load_stop_payload() -> dict:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid stop-hook input JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("invalid stop-hook input: expected a JSON object")
    return payload


def load_state(state_path: Path) -> dict | None:
    if not state_path.exists():
        return None
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        clear_state(state_path)
        block_with_message(
            "arch-step implement-loop state was invalid JSON; the loop was disarmed. "
            "Fix the state contract, update the plan and worklog truthfully, and stop."
        )
    if not isinstance(state, dict):
        clear_state(state_path)
        block_with_message(
            "arch-step implement-loop state was not a JSON object; the loop was disarmed. "
            "Fix the state contract, update the plan and worklog truthfully, and stop."
        )
    return state


def clear_state(state_path: Path) -> None:
    if state_path.exists():
        state_path.unlink()


def write_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def block_with_message(message: str) -> None:
    sys.stderr.write(message.strip() + "\n")
    raise SystemExit(2)


def resolve_doc_path(cwd: Path, doc_path_value: str) -> Path:
    doc_path = Path(doc_path_value)
    if not doc_path.is_absolute():
        doc_path = cwd / doc_path
    return doc_path.resolve()


def derive_worklog_path(doc_path: Path) -> Path:
    return doc_path.with_name(f"{doc_path.stem}_WORKLOG.md")


def run_fresh_audit(cwd: Path, doc_path_value: str) -> subprocess.CompletedProcess[str]:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        f"Use $arch-step audit-implementation {doc_path_value}\n"
        "Fresh context only. Update the authoritative implementation audit block and any reopened "
        "phase statuses in DOC_PATH. Keep the final response short."
    )

    with tempfile.TemporaryDirectory(prefix="arch-step-implement-loop-") as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        return subprocess.run(
            [
                codex,
                "exec",
                "--ephemeral",
                "--disable",
                "codex_hooks",
                "--cd",
                str(cwd),
                "--full-auto",
                "-o",
                str(last_message_path),
                prompt,
            ],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )


def read_verdict(doc_path: Path) -> str | None:
    if not doc_path.exists():
        return None
    matches = VERDICT_PATTERN.findall(doc_path.read_text(encoding="utf-8"))
    if not matches:
        return None
    return matches[-1]


def validate_state(payload: dict, state_path: Path) -> tuple[Path, str] | None:
    cwd = Path(payload["cwd"]).resolve()
    state = load_state(state_path)
    if state is None:
        return None
    if state.get("command") != EXPECTED_COMMAND:
        return None
    session_id = state.get("session_id")
    if session_id is None:
        state["session_id"] = payload.get("session_id")
        write_state(state_path, state)
    elif not isinstance(session_id, str):
        clear_state(state_path)
        block_with_message(
            "arch-step implement-loop state had a non-string session_id; the loop was disarmed. "
            "Update the plan and worklog truthfully, then stop."
        )
    elif session_id != payload.get("session_id"):
        return None
    doc_path_value = state.get("doc_path")
    if not isinstance(doc_path_value, str) or not doc_path_value.strip():
        clear_state(state_path)
        block_with_message(
            "arch-step implement-loop state was missing doc_path; the loop was disarmed. "
            "Update the plan and worklog truthfully, then stop."
        )
    doc_path = resolve_doc_path(cwd, doc_path_value)
    return doc_path, doc_path_value


def main() -> int:
    payload = load_stop_payload()
    cwd = Path(payload["cwd"]).resolve()
    state_path = cwd / STATE_RELATIVE_PATH
    validated = validate_state(payload, state_path)
    if validated is None:
        return 0

    doc_path, doc_path_value = validated
    if not doc_path.exists():
        clear_state(state_path)
        block_with_message(
            f"arch-step implement-loop doc path does not exist: {doc_path_value}. "
            "The loop was disarmed. Update the plan and worklog truthfully, then stop."
        )

    try:
        result = run_fresh_audit(cwd, doc_path_value)
    except RuntimeError as exc:
        clear_state(state_path)
        block_with_message(
            f"fresh implement-loop audit could not start: {exc}. "
            "The loop was disarmed. Explain the blocker and stop."
        )

    if result.returncode != 0:
        clear_state(state_path)
        details = result.stderr.strip() or result.stdout.strip() or "unknown child-audit failure"
        block_with_message(
            "fresh implement-loop audit failed and the loop was disarmed.\n"
            f"Failure: {details}\n"
            "Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop."
        )

    verdict = read_verdict(doc_path)
    if verdict == "COMPLETE":
        clear_state(state_path)
        return 0

    if verdict == "NOT COMPLETE":
        worklog_path = derive_worklog_path(doc_path)
        block_with_message(
            "Fresh implement-loop audit returned Verdict (code): NOT COMPLETE.\n"
            f"Read the authoritative Implementation Audit block and reopened phases in {doc_path_value}, "
            f"implement the missing code work, update {worklog_path.relative_to(cwd)} if it exists, "
            "keep the loop armed, and stop again for another fresh audit."
        )

    clear_state(state_path)
    block_with_message(
        f"fresh implement-loop audit did not leave a usable verdict in {doc_path_value}. "
        "The loop was disarmed. Treat the run as blocked, update the plan and worklog truthfully, explain the blocker, and stop."
    )


if __name__ == "__main__":
    raise SystemExit(main())
