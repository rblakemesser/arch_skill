#!/usr/bin/env python3
"""Deterministic ledger operations for Stepwise learnings."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUSES = {"candidate", "accepted", "rejected", "superseded", "promoted"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _die(msg: str, code: int = 2) -> None:
    print(f"stepwise_learnings: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _die(f"file missing: {path}")
    except json.JSONDecodeError as e:
        _die(f"invalid JSON in {path}: {e}")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _ledger_root(args: argparse.Namespace) -> Path:
    return Path(args.root).resolve()


def _index_path(root: Path) -> Path:
    return root / "index.jsonl"


def _normalize_scope(scope: Any) -> str:
    return json.dumps(scope, sort_keys=True, separators=(",", ":"))


def compute_fingerprint(scope: Any, principle: str) -> str:
    payload = _normalize_scope(scope) + "\n" + principle.strip()
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _learning_id(fingerprint: str, now: str) -> str:
    day = now[:10].replace("-", "")
    return f"LRN-{day}-{fingerprint[:10]}"


def _locked_index(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    path = _index_path(root)
    f = path.open("a+", encoding="utf-8")
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    f.seek(0)
    return f


def _events(root: Path) -> list[dict[str, Any]]:
    path = _index_path(root)
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as e:
            _die(f"invalid JSONL at {path}:{lineno}: {e}")
        if isinstance(event, dict):
            events.append(event)
    return events


def _current_by_id(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    current: dict[str, dict[str, Any]] = {}
    for event in events:
        learning_id = event.get("id")
        if isinstance(learning_id, str):
            current[learning_id] = event
    return current


def _validate_entry(entry: dict[str, Any]) -> None:
    required = [
        "schema_version",
        "source",
        "scope",
        "observation",
        "underlying_principle",
        "applicability_test",
        "contraindications",
        "process_change_suggestion",
        "promotion_target",
    ]
    for key in required:
        if key not in entry:
            _die(f"entry missing required field: {key}")
    if entry["schema_version"] != 1:
        _die("schema_version must be 1")
    for key in [
        "observation",
        "underlying_principle",
        "applicability_test",
        "contraindications",
        "process_change_suggestion",
        "promotion_target",
    ]:
        value = entry.get(key)
        if not isinstance(value, str) or not value.strip():
            _die(f"{key} must be a non-empty string")
    source = entry.get("source")
    if not isinstance(source, dict):
        _die("source must be an object")
    for key in ["run_id", "diagnostic_path"]:
        value = source.get(key)
        if not isinstance(value, str) or not value.strip():
            _die(f"source.{key} must be a non-empty string")
    for key in ["step_n", "try_k"]:
        if not isinstance(source.get(key), int):
            _die(f"source.{key} must be an integer")

    scope = entry.get("scope")
    if not isinstance(scope, dict):
        _die("scope must be an object")
    for key in ["owner_skill", "failure_class", "surface"]:
        value = scope.get(key)
        if not isinstance(value, str) or not value.strip():
            _die(f"scope.{key} must be a non-empty string")
    support_skills = scope.get("support_skills")
    if not isinstance(support_skills, list):
        _die("scope.support_skills must be an array")
    for i, item in enumerate(support_skills):
        if not isinstance(item, str) or not item.strip():
            _die(f"scope.support_skills[{i}] must be a non-empty string")


def _write_learning_md(root: Path, event: dict[str, Any]) -> None:
    status = event.get("status", "candidate")
    learning_id = event["id"]
    folder = {
        "candidate": "candidates",
        "accepted": "accepted",
        "rejected": "rejected",
        "superseded": "rejected",
        "promoted": "accepted",
    }.get(status, "candidates")
    body = f"""# {learning_id}

Status: {status}

Applied success count: {event.get("applied_success_count", 0)}

Applied null count: {event.get("applied_null_count", 0)}

## Observation

{event.get("observation", "")}

## Underlying Principle

{event.get("underlying_principle", "")}

## Applicability Test

{event.get("applicability_test", "")}

## Contraindications

{event.get("contraindications", "")}

## Process Change Suggestion

{event.get("process_change_suggestion", "")}

## Promotion Target

{event.get("promotion_target", "")}
"""
    promotion = event.get("promotion")
    if isinstance(promotion, dict):
        body += f"""
## Promotion Record

Target path: {promotion.get("target_path", "")}

Summary: {promotion.get("summary", "")}
"""
    _write_text(root / folder / f"{learning_id}.md", body)


def cmd_append(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    entry = _read_json(Path(args.entry_file))
    if not isinstance(entry, dict):
        _die("entry file must contain a JSON object")
    _validate_entry(entry)

    now = _utc_now_iso()
    fingerprint = compute_fingerprint(entry["scope"], entry["underlying_principle"])

    with _locked_index(root) as f:
        existing_events = []
        for line in f.read().splitlines():
            if line.strip():
                existing_events.append(json.loads(line))
        for event in existing_events:
            if event.get("fingerprint") == fingerprint:
                print(event["id"])
                return 0

        event = dict(entry)
        event["id"] = entry.get("id") or _learning_id(fingerprint, now)
        event["created_at"] = entry.get("created_at") or now
        event["updated_at"] = now
        event["status"] = entry.get("status") or "candidate"
        event["applied_success_count"] = int(entry.get("applied_success_count", 0))
        event["applied_null_count"] = int(entry.get("applied_null_count", 0))
        event["fingerprint"] = fingerprint
        if event["status"] not in STATUSES:
            _die(f"invalid status: {event['status']}")
        f.seek(0, os.SEEK_END)
        f.write(json.dumps(event, sort_keys=True) + "\n")

    _write_learning_md(root, event)
    print(event["id"])
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    scope = _read_json(Path(args.scope_json))
    if not isinstance(scope, dict):
        _die("scope JSON must be an object")
    events = _current_by_id(_events(root))
    matches: list[dict[str, Any]] = []
    for event in events.values():
        event_scope = event.get("scope")
        if not isinstance(event_scope, dict):
            continue
        if all(event_scope.get(k) == v for k, v in scope.items()):
            matches.append(event)
    print(json.dumps(matches, indent=2, sort_keys=True))
    return 0


def _transition(args: argparse.Namespace, status: str) -> int:
    root = _ledger_root(args)
    events = _events(root)
    current = _current_by_id(events)
    if args.id not in current:
        _die(f"unknown learning id: {args.id}")
    event = dict(current[args.id])
    event["status"] = status
    event["updated_at"] = _utc_now_iso()
    with _locked_index(root) as f:
        f.seek(0, os.SEEK_END)
        f.write(json.dumps(event, sort_keys=True) + "\n")
    _write_learning_md(root, event)
    print(args.id)
    return 0


def cmd_accept(args: argparse.Namespace) -> int:
    return _transition(args, "accepted")


def cmd_reject(args: argparse.Namespace) -> int:
    return _transition(args, "rejected")


def cmd_promote(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    events = _events(root)
    current = _current_by_id(events)
    if args.id not in current:
        _die(f"unknown learning id: {args.id}")
    now = _utc_now_iso()
    event = dict(current[args.id])
    event["status"] = "promoted"
    event["updated_at"] = now
    if args.target_path or args.summary:
        if not args.target_path or not args.summary:
            _die("--target-path and --summary must be provided together")
        event["promotion"] = {
            "promoted_at": now,
            "target_path": args.target_path,
            "summary": args.summary,
        }
    with _locked_index(root) as f:
        f.seek(0, os.SEEK_END)
        f.write(json.dumps(event, sort_keys=True) + "\n")
    _write_learning_md(root, event)
    print(args.id)
    return 0


def cmd_record_application(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    events = _events(root)
    current = _current_by_id(events)
    if args.id not in current:
        _die(f"unknown learning id: {args.id}")
    event = dict(current[args.id])
    success_count = int(event.get("applied_success_count", 0))
    null_count = int(event.get("applied_null_count", 0))
    if args.outcome == "success":
        success_count += 1
    elif args.outcome == "null":
        null_count += 1
    else:
        _die(f"invalid outcome: {args.outcome}")

    event["applied_success_count"] = success_count
    event["applied_null_count"] = null_count
    if event.get("status") == "candidate" and success_count >= 2:
        event["status"] = "accepted"

    applications = event.get("applications")
    if not isinstance(applications, list):
        applications = []
    applications.append(
        {
            "recorded_at": _utc_now_iso(),
            "outcome": args.outcome,
            "run_id": args.run_id,
            "diagnostic_path": args.diagnostic_path,
            "note": args.note or "",
        }
    )
    event["applications"] = applications
    event["updated_at"] = _utc_now_iso()

    with _locked_index(root) as f:
        f.seek(0, os.SEEK_END)
        f.write(json.dumps(event, sort_keys=True) + "\n")
    _write_learning_md(root, event)
    print(args.id)
    return 0


def cmd_export_md(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    current = _current_by_id(_events(root))
    accepted = [
        event for event in current.values()
        if event.get("status") in {"accepted", "promoted"}
    ]
    accepted.sort(key=lambda e: e.get("id", ""))
    parts = ["# Accepted Stepwise Learnings", ""]
    for event in accepted:
        parts.extend(
            [
                f"## {event['id']}",
                "",
                f"Status: {event.get('status')}",
                "",
                f"Principle: {event.get('underlying_principle')}",
                "",
                f"Applies when: {event.get('applicability_test')}",
                "",
                f"Do not apply when: {event.get('contraindications')}",
                "",
            ]
        )
    _write_text(root / "accepted.md", "\n".join(parts).rstrip() + "\n")
    print(str(root / "accepted.md"))
    return 0


def cmd_sync_from_md(args: argparse.Namespace) -> int:
    root = _ledger_root(args)
    path = root / "accepted.md"
    if not path.exists():
        _die(f"accepted.md missing: {path}")
    ids = re.findall(r"^##\s+(LRN-\d{8}-[0-9a-fA-F]+)\s*$", path.read_text(encoding="utf-8"), re.M)
    events = _events(root)
    current = _current_by_id(events)
    changed: list[str] = []
    with _locked_index(root) as f:
        f.seek(0, os.SEEK_END)
        for learning_id in ids:
            event = current.get(learning_id)
            if event is None:
                continue
            if event.get("status") in {"accepted", "promoted"}:
                continue
            accepted = dict(event)
            accepted["status"] = "accepted"
            accepted["updated_at"] = _utc_now_iso()
            f.write(json.dumps(accepted, sort_keys=True) + "\n")
            _write_learning_md(root, accepted)
            changed.append(learning_id)
    print(json.dumps({"accepted": changed}, indent=2, sort_keys=True))
    return 0


def cmd_fingerprint(args: argparse.Namespace) -> int:
    scope = _read_json(Path(args.scope_json))
    if not isinstance(scope, dict):
        _die("scope JSON must be an object")
    print(compute_fingerprint(scope, args.principle))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="stepwise_learnings")
    p.add_argument(
        "--root",
        default=".arch_skill/stepwise/learnings",
        help="ledger root directory",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    ap = sub.add_parser("append")
    ap.add_argument("--entry-file", required=True)
    ap.set_defaults(func=cmd_append)

    q = sub.add_parser("query")
    q.add_argument("--scope-json", required=True)
    q.set_defaults(func=cmd_query)

    for name, func in [("accept", cmd_accept), ("reject", cmd_reject)]:
        sp = sub.add_parser(name)
        sp.add_argument("id")
        sp.set_defaults(func=func)

    promote = sub.add_parser("promote")
    promote.add_argument("id")
    promote.add_argument("--target-path", default=None)
    promote.add_argument("--summary", default=None)
    promote.set_defaults(func=cmd_promote)

    record = sub.add_parser("record-application")
    record.add_argument("id")
    record.add_argument("--outcome", required=True, choices=["success", "null"])
    record.add_argument("--run-id", required=True)
    record.add_argument("--diagnostic-path", required=True)
    record.add_argument("--note", default=None)
    record.set_defaults(func=cmd_record_application)

    sub.add_parser("export-md").set_defaults(func=cmd_export_md)
    sub.add_parser("sync-from-md").set_defaults(func=cmd_sync_from_md)

    fp = sub.add_parser("fingerprint")
    fp.add_argument("--scope-json", required=True)
    fp.add_argument("--principle", required=True)
    fp.set_defaults(func=cmd_fingerprint)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
