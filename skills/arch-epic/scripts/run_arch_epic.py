#!/usr/bin/env python3
"""arch-epic orchestration plumbing.

This script is deterministic infrastructure for the arch-epic skill.
It does NOT make judgments about decomposition, scope changes,
verdicts, or routing. Those decisions live in the orchestrator's
prose reasoning.

Subcommands:

  critic-spawn   Spawn a fresh ephemeral critic sub-session (claude
                 or codex), capture the EpicVerdict JSON, and write
                 run-directory artifacts.
  resolve-execution
                 Resolve automatic-mode role execution policy.
  auto-init      Create an automatic-mode run directory and state.json.
  worker-spawn   Spawn a resumable automatic-mode worker sub-session.
  worker-resume  Resume an automatic-mode worker sub-session.
  auto-critic-spawn
                 Spawn a structured critic inside an automatic-mode run.
  auto-status    Print compact automatic-mode state.
  report-scaffold
                 Write or print a deterministic automatic-mode report.

The script exits non-zero with a plain-English message whenever its
expected output shape does not appear. It never swallows errors.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SHARED_DIR = Path(__file__).resolve().parents[2] / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))

from model_resolution import (  # noqa: E402
    ModelResolutionError,
    resolve_role_execution_policy,
)


AUTO_ROLE_GROUPS = [
    "epic_planner",
    "implementation_worker",
    "repair_worker",
    "critic",
]
DEFAULT_AUTO_POLL_SECONDS = 60


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _die(msg: str, code: int = 2) -> None:
    print(f"run_arch_epic: {msg}", file=sys.stderr)
    sys.exit(code)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _die(f"JSON file not found: {path}")
    except json.JSONDecodeError as e:
        _die(f"JSON file is not valid JSON: {path}: {e}")


def _write_invocation_sh(path: Path, argv: list[str], cwd: str | None) -> None:
    def quote(s: str) -> str:
        return "'" + s.replace("'", "'\\''") + "'"

    line = " ".join(quote(a) for a in argv)
    prefix = f"cd {quote(cwd)} && " if cwd else ""
    _write_text(
        path, "#!/bin/sh\n" + prefix + "exec " + line + " < /dev/null\n"
    )
    path.chmod(0o755)


def _ensure_arch_epic_gitignore_marker(orch_root: Path) -> None:
    """Ignore arch-epic run logs without hiding other .arch_skill content."""

    gi = orch_root / ".gitignore"
    marker = ".arch_skill/arch-epic/"
    old_marker = ".arch_skill/"
    if not gi.exists():
        gi.write_text(f"{marker}\n", encoding="utf-8")
        return

    lines = gi.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    changed = False
    for line in lines:
        if line == old_marker:
            if marker not in new_lines:
                new_lines.append(marker)
            changed = True
        else:
            new_lines.append(line)

    if marker not in new_lines:
        new_lines.append(marker)
        changed = True

    if changed:
        gi.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def _run_subprocess(
    argv: list[str],
    stdout_stream_path: Path,
    out_dir: Path,
    cwd: str | None = None,
) -> tuple[int, str]:
    """Run a subprocess with stdin closed. Combined stdout+stderr
    is captured both to memory and to `stdout_stream_path`.
    """
    _write_text(out_dir / "start_ts", _utc_now_iso())
    with open(os.devnull, "rb") as devnull, open(stdout_stream_path, "wb") as out:
        proc = subprocess.run(
            argv,
            stdin=devnull,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            check=False,
        )
        out.write(proc.stdout)
    _write_text(out_dir / "end_ts", _utc_now_iso())
    _write_text(out_dir / "exit_code", str(proc.returncode) + "\n")
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def _extract_claude_result_event(payload: Any) -> dict | None:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        for ev in reversed(payload):
            if isinstance(ev, dict) and ev.get("type") == "result":
                return ev
    return None


def _parse_claude_result_event(stdout_text: str) -> dict | None:
    try:
        payload = json.loads(stdout_text.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None
    return _extract_claude_result_event(payload)


def _parse_claude_session_id(stdout_text: str) -> str | None:
    event = _parse_claude_result_event(stdout_text)
    if event is None:
        return None
    sid = event.get("session_id")
    return sid if isinstance(sid, str) and sid else None


def _parse_codex_thread_id(stdout_text: str) -> str | None:
    for line in stdout_text.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "thread.started" and isinstance(
            ev.get("thread_id"), str
        ):
            return ev["thread_id"]
    return None


def _parse_claude_final_json(stdout_text: str) -> dict | None:
    """Claude -p --output-format json prints a single JSON object
    at the end of stdout.
    """
    return _parse_claude_result_event(stdout_text)


def _extract_claude_structured_verdict(final: dict) -> dict | None:
    """Return the critic's structured verdict from a Claude `-p --output-format
    json --json-schema ...` response.

    Claude populates `structured_output` reliably when the model answers
    in one shot. When the critic uses tools (reading files) before
    answering, Claude sometimes returns the conforming JSON as text in
    `result` (often wrapped in ```json fences). Accept either path.
    """
    so = final.get("structured_output")
    if isinstance(so, dict):
        return so
    result = final.get("result")
    if not isinstance(result, str):
        return None
    text = result.strip()
    if text.startswith("```"):
        # strip opening fence (with optional language tag) and closing fence
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        obj = json.loads(text.strip())
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _slugify(name: str) -> str:
    out = []
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in ("_", "-", " "):
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "sub-plan"


def _policy_from_file(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    if not isinstance(payload, dict):
        _die("execution policy input must be a JSON object")
    roles = payload.get("roles")
    if not isinstance(roles, dict):
        _die("execution policy input must contain object field: roles")
    missing = [role for role in AUTO_ROLE_GROUPS if role not in roles]
    if missing:
        _die("execution policy missing required role(s): " + ", ".join(missing))
    role_sources: dict[str, str] = {}
    for role in AUTO_ROLE_GROUPS:
        value = roles.get(role)
        if not isinstance(value, str) or not value.strip():
            _die(f"execution policy role {role!r} must be a non-empty string")
        role_sources[role] = value
    poll_seconds = payload.get("poll_seconds", DEFAULT_AUTO_POLL_SECONDS)
    if not isinstance(poll_seconds, int):
        _die("execution policy poll_seconds must be an integer")
    codex_models = payload.get("codex_models")
    if codex_models is not None:
        if not isinstance(codex_models, list) or not all(
            isinstance(item, str) for item in codex_models
        ):
            _die("execution policy codex_models must be an array of strings")
    try:
        return resolve_role_execution_policy(
            role_sources,
            codex_models=codex_models,
            poll_seconds=poll_seconds,
        )
    except ModelResolutionError as e:
        _die(str(e))


def _auto_run_root(orchestrator_root: Path, epic_doc: Path) -> Path:
    slug = _slugify(epic_doc.stem.removeprefix("EPIC_"))
    return orchestrator_root / ".arch_skill" / "arch-epic" / "auto" / slug


def _read_state(run_dir: Path) -> dict[str, Any]:
    state = _load_json(run_dir / "state.json")
    if not isinstance(state, dict):
        _die(f"state.json must contain a JSON object: {run_dir / 'state.json'}")
    return state


def _state_role_execution(state: dict[str, Any], role: str) -> dict[str, str]:
    policy = state.get("auto_execution")
    if not isinstance(policy, dict):
        _die("auto state is missing auto_execution object")
    roles = policy.get("roles")
    if not isinstance(roles, dict):
        _die("auto_execution is missing roles object")
    block = roles.get(role)
    if not isinstance(block, dict):
        _die(f"auto_execution has no role policy for {role!r}")
    out: dict[str, str] = {}
    for key in ["runtime", "model", "effort"]:
        value = block.get(key)
        if not isinstance(value, str) or not value:
            _die(f"role {role!r} policy missing {key}")
        out[key] = value
    return out


def _codex_worker_argv(
    target_repo: Path,
    model: str,
    effort: str,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "--cd",
        str(target_repo),
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _claude_worker_argv(
    model: str,
    effort: str,
    prompt: str,
    *,
    session_id: str | None = None,
) -> list[str]:
    argv = [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        "--settings",
        '{"disableAllHooks":true}',
        "--model",
        model,
        "--effort",
        effort,
    ]
    if session_id:
        argv.extend(["-r", session_id])
    argv.append(prompt)
    return argv


def _codex_worker_resume_argv(
    session_id: str,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "resume",
        session_id,
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _codex_critic_argv(
    target_repo: Path,
    model: str,
    effort: str,
    schema_path: Path,
    final_path: Path,
    prompt: str,
) -> list[str]:
    return [
        "codex",
        "exec",
        "--cd",
        str(target_repo),
        "--ephemeral",
        "--disable",
        "codex_hooks",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--output-schema",
        str(schema_path),
        "--json",
        "-o",
        str(final_path),
        prompt,
    ]


def _claude_critic_argv(
    model: str,
    effort: str,
    schema_inline: str,
    prompt: str,
) -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        "--settings",
        '{"disableAllHooks":true}',
        "--model",
        model,
        "--effort",
        effort,
        "--json-schema",
        schema_inline,
        prompt,
    ]


def cmd_resolve_execution(args: argparse.Namespace) -> int:
    policy = _policy_from_file(Path(args.policy_file).resolve())
    if args.output:
        _write_json(Path(args.output).resolve(), policy)
        print(str(Path(args.output).resolve()))
    else:
        print(json.dumps(policy, indent=2, sort_keys=True))
    return 0


def cmd_auto_init(args: argparse.Namespace) -> int:
    epic_doc = Path(args.epic_doc).resolve()
    if not epic_doc.is_file():
        _die(f"epic doc not found: {epic_doc}")
    orchestrator_root = (
        Path(args.orchestrator_root).resolve() if args.orchestrator_root else Path.cwd()
    )
    if not orchestrator_root.is_dir():
        _die(f"orchestrator root is not a directory: {orchestrator_root}")
    _ensure_arch_epic_gitignore_marker(orchestrator_root)
    policy = _policy_from_file(Path(args.policy_file).resolve())
    run_id = _utc_now_stamp()
    run_dir = _auto_run_root(orchestrator_root, epic_doc) / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)
    policy_with_run_dir = dict(policy)
    policy_with_run_dir["auto_run_dir"] = str(run_dir)
    state = {
        "schema_version": 1,
        "run_id": run_id,
        "started_at": _utc_now_iso(),
        "epic_doc": str(epic_doc),
        "orchestrator_root": str(orchestrator_root),
        "status": "active",
        "current_sub_plan": None,
        "auto_execution": policy_with_run_dir,
        "events": [],
    }
    _write_json(run_dir / "state.json", state)
    _write_json(run_dir / "execution_policy.json", policy_with_run_dir)
    print(str(run_dir))
    return 0


def _worker_try_dir(run_dir: Path, role: str, sub_plan_name: str, try_k: int) -> Path:
    return (
        run_dir
        / "workers"
        / role
        / _slugify(sub_plan_name)
        / f"try-{try_k}"
    )


def _critic_run_dir(run_dir: Path, gate: str, sub_plan_name: str) -> Path:
    return (
        run_dir
        / "critics"
        / _slugify(gate)
        / _slugify(sub_plan_name)
        / f"run-{_utc_now_stamp()}"
    )


def _run_worker(
    *,
    run_dir: Path,
    target_repo: Path,
    role: str,
    sub_plan_name: str,
    prompt_file: Path,
    try_k: int,
    session_id: str | None = None,
) -> int:
    state = _read_state(run_dir)
    execution = _state_role_execution(state, role)
    prompt = prompt_file.read_text(encoding="utf-8")
    try_dir = _worker_try_dir(run_dir, role, sub_plan_name, try_k)
    try_dir.mkdir(parents=True, exist_ok=False)
    _write_text(try_dir / "prompt.md", prompt)
    _write_json(try_dir / "execution.json", execution)
    final_path = try_dir / "stdout.final.json"
    stream_path = try_dir / "stream.log"

    runtime = execution["runtime"]
    if runtime == "claude":
        argv = _claude_worker_argv(
            execution["model"],
            execution["effort"],
            prompt,
            session_id=session_id,
        )
        cwd = str(target_repo)
    elif runtime == "codex":
        if session_id:
            argv = _codex_worker_resume_argv(session_id, final_path, prompt)
        else:
            argv = _codex_worker_argv(
                target_repo,
                execution["model"],
                execution["effort"],
                final_path,
                prompt,
            )
        cwd = None
    else:
        _die(f"unknown worker runtime: {runtime}")

    _write_invocation_sh(try_dir / "invocation.sh", argv, cwd)
    code, stdout_text = _run_subprocess(argv, stream_path, try_dir, cwd=cwd)

    out_sid: str | None
    if runtime == "claude":
        final = _parse_claude_result_event(stdout_text)
        if final is None:
            _write_text(try_dir / "session_id.txt", "UNRECOVERABLE\n")
            _die("claude worker stdout did not parse as JSON; see stream.log", code=3)
        _write_json(final_path, final)
        out_sid = _parse_claude_session_id(stdout_text) or session_id
    else:
        out_sid = _parse_codex_thread_id(stdout_text) or session_id

    if not out_sid:
        _write_text(try_dir / "session_id.txt", "UNRECOVERABLE\n")
        _die(f"worker session id not captured (runtime={runtime}, exit={code})", code=4)
    _write_text(try_dir / "session_id.txt", out_sid + "\n")
    _write_json(
        try_dir / "metadata.json",
        {
            "role": role,
            "sub_plan_name": sub_plan_name,
            "try_k": try_k,
            "runtime": runtime,
            "model": execution["model"],
            "effort": execution["effort"],
            "session_id": out_sid,
            "resumed": session_id is not None,
        },
    )
    print(out_sid)
    return 0 if code == 0 else code


def cmd_worker_spawn(args: argparse.Namespace) -> int:
    return _run_worker(
        run_dir=Path(args.run_dir).resolve(),
        target_repo=Path(args.target_repo).resolve(),
        role=args.role,
        sub_plan_name=args.sub_plan_name,
        prompt_file=Path(args.prompt_file).resolve(),
        try_k=args.try_k,
    )


def cmd_worker_resume(args: argparse.Namespace) -> int:
    return _run_worker(
        run_dir=Path(args.run_dir).resolve(),
        target_repo=Path(args.target_repo).resolve(),
        role=args.role,
        sub_plan_name=args.sub_plan_name,
        prompt_file=Path(args.prompt_file).resolve(),
        try_k=args.try_k,
        session_id=args.session_id,
    )


def cmd_auto_critic_spawn(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    target_repo = Path(args.target_repo).resolve()
    state = _read_state(run_dir)
    execution = _state_role_execution(state, args.role)
    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file not found: {schema_path}")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    crit_dir = _critic_run_dir(run_dir, args.gate, args.sub_plan_name)
    crit_dir.mkdir(parents=True, exist_ok=False)
    _write_text(crit_dir / "prompt.md", prompt)
    _write_json(crit_dir / "execution.json", execution)
    final_path = crit_dir / "stdout.final.json"
    stream_path = crit_dir / "stream.log"
    verdict_path = crit_dir / "verdict.json"

    runtime = execution["runtime"]
    if runtime == "claude":
        schema_inline = json.dumps(
            json.loads(schema_path.read_text(encoding="utf-8")),
            separators=(",", ":"),
        )
        argv = _claude_critic_argv(
            execution["model"],
            execution["effort"],
            schema_inline,
            prompt,
        )
        cwd = str(target_repo)
    elif runtime == "codex":
        argv = _codex_critic_argv(
            target_repo,
            execution["model"],
            execution["effort"],
            schema_path,
            final_path,
            prompt,
        )
        cwd = None
    else:
        _die(f"unknown critic runtime: {runtime}")

    _write_invocation_sh(crit_dir / "invocation.sh", argv, cwd)
    code, stdout_text = _run_subprocess(argv, stream_path, crit_dir, cwd=cwd)

    if runtime == "claude":
        final = _parse_claude_result_event(stdout_text)
        if final is None:
            _die("claude critic stdout did not parse as JSON; see stream.log", code=3)
        _write_json(final_path, final)
        verdict = _extract_claude_structured_verdict(final)
        if verdict is None:
            _die("claude critic produced no schema-conforming JSON", code=5)
        _write_json(verdict_path, verdict)
    else:
        if not final_path.is_file():
            _die(f"codex critic did not write -o file: {final_path}", code=5)
        verdict = _load_json(final_path)
        _write_json(verdict_path, verdict)

    _write_json(
        crit_dir / "metadata.json",
        {
            "gate": args.gate,
            "role": args.role,
            "sub_plan_name": args.sub_plan_name,
            "runtime": runtime,
            "model": execution["model"],
            "effort": execution["effort"],
        },
    )
    print(str(verdict_path))
    return 0 if code == 0 else code


def cmd_auto_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = _read_state(run_dir)
    policy = state.get("auto_execution", {})
    roles = policy.get("roles", {}) if isinstance(policy, dict) else {}
    print(f"Run: {run_dir}")
    print(f"Status: {state.get('status', 'unknown')}")
    print(f"Epic doc: {state.get('epic_doc', '')}")
    print(f"Poll seconds: {policy.get('poll_seconds', '') if isinstance(policy, dict) else ''}")
    print("Roles:")
    if isinstance(roles, dict):
        for role in AUTO_ROLE_GROUPS:
            block = roles.get(role, {})
            if isinstance(block, dict):
                print(
                    f"- {role}: {block.get('runtime', '?')} "
                    f"{block.get('model', '?')} {block.get('effort', '?')}"
                )
    return 0


def _render_report(state: dict[str, Any]) -> str:
    policy = state.get("auto_execution", {})
    roles = policy.get("roles", {}) if isinstance(policy, dict) else {}
    lines = [
        "# Arch-Epic Automatic Run Report",
        "",
        f"Run id: {state.get('run_id', '')}",
        f"Status: {state.get('status', '')}",
        f"Epic doc: {state.get('epic_doc', '')}",
        f"Poll seconds: {policy.get('poll_seconds', '') if isinstance(policy, dict) else ''}",
        "",
        "## Role Execution",
        "",
        "| Role | Runtime | Model | Effort | Source |",
        "|---|---|---|---|---|",
    ]
    if isinstance(roles, dict):
        for role in AUTO_ROLE_GROUPS:
            block = roles.get(role, {})
            if isinstance(block, dict):
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            role,
                            str(block.get("runtime", "")),
                            str(block.get("model", "")),
                            str(block.get("effort", "")),
                            str(block.get("source", "")),
                        ]
                    )
                    + " |"
                )
    lines.extend(
        [
            "",
            "## Sub-Plan Status",
            "",
            "- Fill from the epic Decomposition and critic verdict artifacts.",
            "",
            "## Blocking Findings",
            "",
            "- none recorded in this scaffold",
            "",
            "## Artifact Roots",
            "",
            "- workers/: worker prompts, transcripts, and session ids",
            "- critics/: gate verdicts and structured outputs",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cmd_report_scaffold(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = _read_state(run_dir)
    report = _render_report(state)
    if args.write:
        path = run_dir / "report.md"
        _write_text(path, report)
        print(str(path))
    else:
        print(report, end="")
    return 0


def cmd_critic_spawn(args: argparse.Namespace) -> int:
    epic_doc = Path(args.epic_doc).resolve()
    if not epic_doc.is_file():
        _die(f"epic doc not found: {epic_doc}")

    sub_plan_doc_path = Path(args.sub_plan_doc_path).resolve()
    if not sub_plan_doc_path.is_file():
        _die(f"sub-plan doc not found: {sub_plan_doc_path}")

    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file not found: {schema_path}")

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    orch_root = Path(args.orchestrator_root).resolve() if args.orchestrator_root else Path.cwd()
    if not orch_root.is_dir():
        _die(f"orchestrator root is not a directory: {orch_root}")

    slug = _slugify(args.sub_plan_name)
    run_id = _utc_now_stamp()
    run_dir = orch_root / ".arch_skill" / "arch-epic" / "critics" / slug / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)

    _ensure_arch_epic_gitignore_marker(orch_root)

    _write_text(run_dir / "prompt.md", prompt)

    final_path = run_dir / "stdout.final.json"
    stream_path = run_dir / "stream.log"
    verdict_path = run_dir / "verdict.json"

    if args.runtime == "claude":
        # Claude's --json-schema is flaky on multi-line pretty-printed
        # JSON (model may emit prose-wrapped JSON in `result` instead of
        # populating `structured_output`). Minify the schema.
        schema_inline = json.dumps(
            json.loads(schema_path.read_text(encoding="utf-8")),
            separators=(",", ":"),
        )
        argv = _claude_critic_argv(args.model, args.effort, schema_inline, prompt)
        subprocess_cwd = str(orch_root)
    elif args.runtime == "codex":
        argv = _codex_critic_argv(
            orch_root,
            args.model,
            args.effort,
            schema_path,
            final_path,
            prompt,
        )
        subprocess_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(run_dir / "invocation.sh", argv, subprocess_cwd)
    code, stdout_text = _run_subprocess(
        argv, stream_path, run_dir, cwd=subprocess_cwd
    )

    if args.runtime == "claude":
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see stream.log",
                code=3,
            )
        _write_json(final_path, final)
        verdict = _extract_claude_structured_verdict(final)
        if verdict is None:
            _die(
                "claude critic produced no schema-conforming JSON in structured_output or result; see stdout.final.json",
                code=5,
            )
        _write_json(verdict_path, verdict)
    else:
        if not final_path.is_file():
            _die(
                f"codex critic did not write -o file: {final_path}",
                code=5,
            )
        try:
            verdict = json.loads(final_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            _die(f"codex critic output is not valid JSON: {e}", code=5)
        _write_json(verdict_path, verdict)

    print(str(verdict_path))
    return 0 if code == 0 else code


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_arch_epic")
    sub = p.add_subparsers(dest="cmd", required=True)

    resolve = sub.add_parser(
        "resolve-execution",
        help="Resolve automatic-mode role execution policy",
    )
    resolve.add_argument("--policy-file", required=True)
    resolve.add_argument("--output", default=None)
    resolve.set_defaults(func=cmd_resolve_execution)

    auto_init = sub.add_parser(
        "auto-init",
        help="Create an arch-epic automatic-mode run directory",
    )
    auto_init.add_argument("--epic-doc", required=True)
    auto_init.add_argument("--policy-file", required=True)
    auto_init.add_argument("--orchestrator-root", default=None)
    auto_init.set_defaults(func=cmd_auto_init)

    worker_spawn = sub.add_parser(
        "worker-spawn",
        help="Spawn a resumable automatic-mode worker",
    )
    for a in ["--run-dir", "--target-repo", "--role", "--sub-plan-name", "--prompt-file"]:
        worker_spawn.add_argument(a, required=True)
    worker_spawn.add_argument("--try-k", type=int, default=1)
    worker_spawn.set_defaults(func=cmd_worker_spawn)

    worker_resume = sub.add_parser(
        "worker-resume",
        help="Resume an automatic-mode worker",
    )
    for a in [
        "--run-dir",
        "--target-repo",
        "--role",
        "--sub-plan-name",
        "--prompt-file",
        "--session-id",
    ]:
        worker_resume.add_argument(a, required=True)
    worker_resume.add_argument("--try-k", type=int, required=True)
    worker_resume.set_defaults(func=cmd_worker_resume)

    auto_critic = sub.add_parser(
        "auto-critic-spawn",
        help="Spawn an automatic-mode structured critic",
    )
    for a in [
        "--run-dir",
        "--target-repo",
        "--gate",
        "--sub-plan-name",
        "--prompt-file",
        "--schema-file",
    ]:
        auto_critic.add_argument(a, required=True)
    auto_critic.add_argument("--role", default="critic")
    auto_critic.set_defaults(func=cmd_auto_critic_spawn)

    auto_status = sub.add_parser(
        "auto-status",
        help="Print compact automatic-mode run status",
    )
    auto_status.add_argument("--run-dir", required=True)
    auto_status.set_defaults(func=cmd_auto_status)

    report = sub.add_parser(
        "report-scaffold",
        help="Print or write an automatic-mode report scaffold",
    )
    report.add_argument("--run-dir", required=True)
    report.add_argument("--write", action="store_true")
    report.set_defaults(func=cmd_report_scaffold)

    critic = sub.add_parser(
        "critic-spawn",
        help="Spawn a fresh ephemeral critic sub-session",
    )
    for a in [
        "--epic-doc",
        "--sub-plan-name",
        "--sub-plan-doc-path",
        "--prompt-file",
        "--schema-file",
        "--model",
        "--effort",
    ]:
        critic.add_argument(a, required=True)
    critic.add_argument(
        "--runtime", required=True, choices=["claude", "codex"]
    )
    critic.add_argument(
        "--orchestrator-root",
        required=False,
        default=None,
        help="Root where .arch_skill/arch-epic/critics/<slug>/run-<ts>/ lives. Defaults to cwd.",
    )
    critic.set_defaults(func=cmd_critic_spawn)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
