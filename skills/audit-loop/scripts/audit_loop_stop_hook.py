#!/usr/bin/env python3
"""Compatibility tombstone for stale sessions still invoking the old audit-loop Stop hook."""

from __future__ import annotations


def main() -> int:
    # New installs route all arch_skill auto controllers through the shared
    # arch-step Stop hook. Older live Codex sessions can still hold the
    # removed audit-loop hook path in memory until restart; succeed quietly so
    # those sessions stop erroring while the on-disk hooks.json now points to
    # the unified runner.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
