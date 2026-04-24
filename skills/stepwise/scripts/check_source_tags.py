#!/usr/bin/env python3
"""Validate Stepwise repair prompts for source-tagged operational steps."""

from __future__ import annotations

import re
import sys
from pathlib import Path


STEP_RE = re.compile(r"^\s*\d+\.\s+")
BULLET_RE = re.compile(r"^\s*-\s+")
HEADING_RE = re.compile(r"^\s*##\s+(.+?)\s*$")
SOURCE_RE = re.compile(
    r"\[source:\s*(user|manifest|owner runbook|critic evidence|confirmed diagnosis)\]",
    re.IGNORECASE,
)


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        return [f"{path}: cannot read: {e}"]

    current_section: str | None = None
    for lineno, line in enumerate(lines, start=1):
        heading = HEADING_RE.match(line)
        if heading:
            current_section = heading.group(1).strip().lower()
            continue
        if STEP_RE.match(line) and not SOURCE_RE.search(line):
            errors.append(f"{path}:{lineno}: numbered repair step lacks source tag")
        if (
            current_section == "hard boundaries"
            and BULLET_RE.match(line)
            and not SOURCE_RE.search(line)
        ):
            errors.append(f"{path}:{lineno}: hard boundary lacks source tag")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: check_source_tags.py <prompt.md> [...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for arg in args:
        errors.extend(check_file(Path(arg)))

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
