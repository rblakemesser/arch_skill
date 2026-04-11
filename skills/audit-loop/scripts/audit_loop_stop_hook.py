#!/usr/bin/env python3
"""Codex Stop hook for the audit-loop automatic controller."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


STATE_RELATIVE_PATH = Path(".codex/audit-loop-state.json")
COMMAND_NAME = "auto"
DEFAULT_LEDGER_PATH = "_audit_ledger.md"
CONTROLLER_START = "<!-- audit_loop:block:controller:start -->"
CONTROLLER_END = "<!-- audit_loop:block:controller:end -->"
VALID_VERDICTS = {"CONTINUE", "CLEAN", "BLOCKED"}
DETAIL_LIMIT = 800


@dataclass
class FreshReviewResult:
    process: subprocess.CompletedProcess[str]
    last_message: str | None


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
            f"audit-loop {COMMAND_NAME} state was invalid JSON; the controller was disarmed. {exc}"
        )
    if not isinstance(state, dict):
        clear_state(state_path)
        block_with_message(
            f"audit-loop {COMMAND_NAME} state was not a JSON object; the controller was disarmed."
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


def block_with_json(reason: str, system_message: str | None = None) -> None:
    payload: dict[str, object] = {
        "continue": True,
        "decision": "block",
        "reason": reason.strip(),
    }
    if system_message:
        payload["systemMessage"] = system_message.strip()
    sys.stdout.write(json.dumps(payload) + "\n")
    raise SystemExit(0)


def stop_with_json(stop_reason: str, system_message: str | None = None) -> None:
    payload: dict[str, object] = {
        "continue": False,
        "stopReason": stop_reason.strip(),
    }
    if system_message:
        payload["systemMessage"] = system_message.strip()
    sys.stdout.write(json.dumps(payload) + "\n")
    raise SystemExit(0)


def resolve_path(cwd: Path, path_value: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = cwd / path
    return path.resolve()


def validate_session_id(payload: dict, state_path: Path, state: dict) -> bool:
    session_id = state.get("session_id")
    if session_id is None:
        state["session_id"] = payload.get("session_id")
        write_state(state_path, state)
        return True
    if not isinstance(session_id, str):
        clear_state(state_path)
        block_with_message(
            f"audit-loop {COMMAND_NAME} state had a non-string session_id; the controller was disarmed."
        )
    return session_id == payload.get("session_id")


def validate_state(payload: dict, state_path: Path) -> tuple[Path, str, dict] | None:
    cwd = Path(payload["cwd"]).resolve()
    state = load_state(state_path)
    if state is None:
        return None
    if state.get("command") != COMMAND_NAME:
        return None
    if not validate_session_id(payload, state_path, state):
        return None

    ledger_path_value = state.get("ledger_path", DEFAULT_LEDGER_PATH)
    if not isinstance(ledger_path_value, str) or not ledger_path_value.strip():
        clear_state(state_path)
        block_with_message(
            f"audit-loop {COMMAND_NAME} state was missing ledger_path; the controller was disarmed."
        )

    ledger_path = resolve_path(cwd, ledger_path_value)
    return ledger_path, ledger_path_value, state


def run_fresh_review(cwd: Path) -> FreshReviewResult:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("`codex` is not available on PATH for the Stop hook")

    prompt = (
        "Use $audit-loop review\n"
        "Fresh context only. Repair or update `_audit_ledger.md`, set the controller verdict truthfully, "
        "and keep the final response short."
    )

    with tempfile.TemporaryDirectory(prefix="audit-loop-review-") as temp_dir:
        last_message_path = Path(temp_dir) / "last_message.txt"
        process = subprocess.run(
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
        last_message = None
        if last_message_path.exists():
            last_message = last_message_path.read_text(encoding="utf-8").strip() or None
        return FreshReviewResult(process=process, last_message=last_message)


def summarize_child_output(
    process: subprocess.CompletedProcess[str],
    last_message: str | None,
) -> str | None:
    for detail in (
        last_message,
        process.stderr.strip(),
        process.stdout.strip(),
    ):
        if detail:
            compact = " ".join(detail.split())
            if len(compact) > DETAIL_LIMIT:
                return compact[: DETAIL_LIMIT - 3] + "..."
            return compact
    return None


def read_controller_fields(ledger_path: Path) -> dict[str, str] | None:
    if not ledger_path.exists():
        return None
    text = ledger_path.read_text(encoding="utf-8")
    start = text.find(CONTROLLER_START)
    end = text.find(CONTROLLER_END)
    if start == -1 or end == -1 or end < start:
        return None
    block = text[start + len(CONTROLLER_START) : end]
    fields: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def clean_gitignore(gitignore_path: Path, entry: str, created_by_skill: bool, entry_added: bool) -> None:
    if not entry_added or not gitignore_path.exists():
        return

    original_text = gitignore_path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    kept_lines = [line for line in lines if line.strip() != entry]
    trailing_newline = original_text.endswith("\n")

    if kept_lines:
        new_text = "\n".join(kept_lines)
        if trailing_newline or new_text:
            new_text += "\n"
        gitignore_path.write_text(new_text, encoding="utf-8")
        return

    if created_by_skill:
        gitignore_path.unlink()
    else:
        gitignore_path.write_text("", encoding="utf-8")


def cleanup_runtime_artifacts(cwd: Path, ledger_path: Path, state: dict) -> None:
    if ledger_path.exists():
        ledger_path.unlink()

    gitignore_path = cwd / ".gitignore"
    clean_gitignore(
        gitignore_path=gitignore_path,
        entry=DEFAULT_LEDGER_PATH,
        created_by_skill=bool(state.get("gitignore_created")),
        entry_added=bool(state.get("gitignore_entry_added")),
    )


def handle_auto(payload: dict) -> int:
    cwd = Path(payload["cwd"]).resolve()
    state_path = cwd / STATE_RELATIVE_PATH
    validated = validate_state(payload, state_path)
    if validated is None:
        return 0

    ledger_path, ledger_path_value, state = validated

    try:
        review = run_fresh_review(cwd)
    except RuntimeError as exc:
        clear_state(state_path)
        stop_with_json(
            f"audit-loop could not start a fresh review pass: {exc}. The controller was disarmed.",
            system_message="audit-loop fresh review could not start.",
        )

    child_summary = summarize_child_output(review.process, review.last_message)
    if review.process.returncode != 0:
        clear_state(state_path)
        reason = "audit-loop ran a fresh review pass, but that review failed."
        if child_summary:
            reason += f" Failure: {child_summary}."
        stop_with_json(
            reason + " Treat the run as blocked, keep the ledger, and stop honestly.",
            system_message="audit-loop fresh review failed.",
        )

    fields = read_controller_fields(ledger_path)
    if not fields:
        clear_state(state_path)
        reason = (
            f"audit-loop fresh review finished, but {ledger_path_value} does not contain a usable controller block. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review left no usable controller block.")

    verdict = fields.get("Verdict", "").strip().upper()
    if verdict not in VALID_VERDICTS:
        clear_state(state_path)
        reason = (
            f"audit-loop fresh review finished, but {ledger_path_value} has an invalid verdict. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review left an invalid verdict.")

    if verdict == "CLEAN":
        clear_state(state_path)
        cleanup_runtime_artifacts(cwd, ledger_path, state)
        stop_reason = "audit-loop fresh review finished clean. The audit ledger was removed."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop completed clean.")

    if verdict == "BLOCKED":
        clear_state(state_path)
        stop_reason = fields.get("Stop Reason") or "audit-loop review marked the loop blocked."
        if child_summary:
            stop_reason += f" Review summary: {child_summary}"
        stop_with_json(stop_reason, system_message="audit-loop stopped blocked.")

    next_area = fields.get("Next Area", "").strip()
    if not next_area:
        clear_state(state_path)
        reason = (
            f"audit-loop review returned CONTINUE without Next Area in {ledger_path_value}. "
            "The controller was disarmed."
        )
        if child_summary:
            reason += f" Review summary: {child_summary}"
        stop_with_json(reason, system_message="audit-loop review omitted Next Area.")

    reason = (
        f"audit-loop fresh review found more worthwhile work. Continue now with `Use $audit-loop`. "
        f"Next area: {next_area}. Keep .codex/audit-loop-state.json armed and stop naturally when this pass finishes."
    )
    if child_summary:
        reason += f" Review summary: {child_summary}"
    block_with_json(reason, system_message="audit-loop review found more work.")


def main() -> int:
    payload = load_stop_payload()
    handle_auto(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
