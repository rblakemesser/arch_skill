#!/usr/bin/env python3
"""Remove or verify absence of the old arch_skill Claude Stop hook."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path


HOOK_SCRIPT_NAME = "arch_controller_stop_hook.py"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--remove", action="store_true")
    action.add_argument("--verify-absent", action="store_true")
    parser.add_argument("--settings-file", required=True)
    parser.add_argument("--skills-dir")
    return parser.parse_args()


def command_mentions_repo_runner(command: str) -> bool:
    return any(part.endswith(HOOK_SCRIPT_NAME) for part in command.split())


def load_settings_file(settings_file: Path) -> dict:
    if not settings_file.exists():
        return {"hooks": {}}
    raw_text = settings_file.read_text(encoding="utf-8")
    if not raw_text.strip():
        return {"hooks": {}}
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse {settings_file}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{settings_file} must contain a top-level JSON object")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"{settings_file} must contain an object at hooks")
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
        if hook.get("type") != "command":
            continue
        command = str(hook.get("command", ""))
        if command_mentions_repo_runner(command):
            return True
    return False


def repo_managed_groups(stop_groups: list[object]) -> list[object]:
    return [group for group in stop_groups if is_repo_managed_group(group)]


def _open_for_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return open(path, "a+", encoding="utf-8")


def remove_hook(settings_file: Path) -> None:
    if not settings_file.exists():
        return
    with _open_for_lock(settings_file) as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        data = load_settings_file(settings_file)
        stop_groups = data["hooks"].get("Stop", [])
        if stop_groups is None:
            stop_groups = []
        if not isinstance(stop_groups, list):
            raise SystemExit(f"{settings_file} must contain a list at hooks.Stop")

        remaining_groups = [group for group in stop_groups if not is_repo_managed_group(group)]
        if remaining_groups == stop_groups:
            return
        if remaining_groups:
            data["hooks"]["Stop"] = remaining_groups
        else:
            data["hooks"].pop("Stop", None)

        write_json_file(settings_file, data)


def verify_absent(settings_file: Path) -> None:
    if not settings_file.exists():
        return
    data = load_settings_file(settings_file)
    stop_groups = data["hooks"].get("Stop", [])
    if not isinstance(stop_groups, list):
        raise SystemExit(f"{settings_file} must contain a list at hooks.Stop")

    managed_groups = repo_managed_groups(stop_groups)
    if managed_groups:
        raise SystemExit(
            "arch_skill Claude Stop hook entries are still present in "
            f"{settings_file}. Run `make install` to remove them."
        )


def main() -> int:
    args = parse_args()
    settings_file = Path(args.settings_file).expanduser()
    if args.verify_absent:
        verify_absent(settings_file)
    else:
        remove_hook(settings_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
