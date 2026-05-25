#!/usr/bin/env python3
"""Remove or verify absence of the old arch_skill Codex Stop hook."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path


STATUS_MESSAGE = (
    "arch_skill automatic controllers are running; planning continuations are quick, fresh reviews or docs evaluations can take a few minutes, and delay polls can wait much longer"
)
HOOK_SCRIPT_NAME = "arch_controller_stop_hook.py"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--remove", action="store_true")
    action.add_argument("--verify-absent", action="store_true")
    parser.add_argument("--hooks-file", required=True)
    parser.add_argument("--skills-dir")
    return parser.parse_args()


def command_mentions_repo_runner(command: str) -> bool:
    return any(part.endswith(HOOK_SCRIPT_NAME) for part in command.split())


def load_hooks_file(hooks_file: Path) -> dict:
    if not hooks_file.exists():
        return {"hooks": {}}
    raw_text = hooks_file.read_text(encoding="utf-8")
    if not raw_text.strip():
        return {"hooks": {}}
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse {hooks_file}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{hooks_file} must contain a top-level JSON object")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"{hooks_file} must contain an object at hooks")
    return data


def write_json_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def is_repo_managed_group(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    hooks = group.get("hooks")
    if not isinstance(hooks, list):
        return False
    for hook in hooks:
        if not isinstance(hook, dict):
            continue
        command = str(hook.get("command", ""))
        status_message = hook.get("statusMessage")
        if status_message == STATUS_MESSAGE or command_mentions_repo_runner(command):
            return True
    return False


def repo_managed_groups(stop_groups: list[object]) -> list[object]:
    return [group for group in stop_groups if is_repo_managed_group(group)]


def _open_for_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return open(path, "a+", encoding="utf-8")


def remove_hook(hooks_file: Path) -> None:
    if not hooks_file.exists():
        return
    with _open_for_lock(hooks_file) as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        data = load_hooks_file(hooks_file)
        stop_groups = data["hooks"].get("Stop", [])
        if stop_groups is None:
            stop_groups = []
        if not isinstance(stop_groups, list):
            raise SystemExit(f"{hooks_file} must contain a list at hooks.Stop")

        remaining_groups = [group for group in stop_groups if not is_repo_managed_group(group)]
        if remaining_groups == stop_groups:
            return
        if remaining_groups:
            data["hooks"]["Stop"] = remaining_groups
        else:
            data["hooks"].pop("Stop", None)

        write_json_file(hooks_file, data)


def verify_absent(hooks_file: Path) -> None:
    if not hooks_file.exists():
        return
    data = load_hooks_file(hooks_file)
    stop_groups = data["hooks"].get("Stop", [])
    if not isinstance(stop_groups, list):
        raise SystemExit(f"{hooks_file} must contain a list at hooks.Stop")

    managed_groups = repo_managed_groups(stop_groups)
    if managed_groups:
        raise SystemExit(
            "arch_skill Codex Stop hook entries are still present in "
            f"{hooks_file}. Run `make install` to remove them."
        )


def main() -> int:
    args = parse_args()
    hooks_file = Path(args.hooks_file).expanduser()
    if args.verify_absent:
        verify_absent(hooks_file)
    else:
        remove_hook(hooks_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
