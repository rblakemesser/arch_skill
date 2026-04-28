#!/usr/bin/env python3
"""Safely rewrite branch-span commit messages on the current branch."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


PROTECTED_BRANCHES = ("main", "master", "trunk", "develop")
PROTECTED_PREFIXES = ("release/", "hotfix/")
PREFERRED_PARENT_REFS = (
    "origin/main",
    "main",
    "origin/master",
    "master",
    "origin/trunk",
    "trunk",
    "origin/develop",
    "develop",
)


class SafetyError(RuntimeError):
    """Raised when the requested rewrite is not safe to apply."""


def run_git(
    repo: Path,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if check and process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise SafetyError(f"git {' '.join(args)} failed: {detail}")
    return process


def git_stdout(repo: Path, args: list[str], *, check: bool = True) -> str:
    return run_git(repo, args, check=check).stdout.strip()


def repo_root(repo: Path) -> Path:
    root = git_stdout(repo, ["rev-parse", "--show-toplevel"])
    return Path(root).resolve()


def current_branch(repo: Path) -> str:
    branch = git_stdout(repo, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)
    if not branch:
        raise SafetyError("current HEAD is detached; refusing to rewrite history")
    return branch


def is_protected_branch(branch: str) -> bool:
    return branch in PROTECTED_BRANCHES or branch.startswith(PROTECTED_PREFIXES)


def ensure_clean(repo: Path) -> None:
    status = git_stdout(repo, ["status", "--porcelain=v1"])
    if status:
        raise SafetyError("worktree or index is dirty; commit, stash, or remove changes before rewriting")


def resolve_upstream(repo: Path) -> str | None:
    process = run_git(
        repo,
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        check=False,
    )
    if process.returncode != 0:
        return None
    upstream = process.stdout.strip()
    return upstream or None


def remote_branch_name(full_ref: str) -> str | None:
    prefix = "refs/remotes/"
    if not full_ref.startswith(prefix):
        return None
    remainder = full_ref[len(prefix):]
    parts = remainder.split("/", 1)
    if len(parts) != 2:
        return None
    if parts[1] == "HEAD":
        return None
    return parts[1]


def is_current_branch_remote(full_ref: str, branch: str) -> bool:
    return remote_branch_name(full_ref) == branch


def list_refs(repo: Path, prefixes: list[str]) -> list[tuple[str, str]]:
    raw = git_stdout(
        repo,
        ["for-each-ref", "--format=%(refname)%00%(refname:short)", *prefixes],
    )
    refs: list[tuple[str, str]] = []
    for line in raw.splitlines():
        if not line:
            continue
        full, short = line.split("\x00", 1)
        refs.append((full, short))
    return refs


def current_branch_remote_refs(repo: Path, branch: str) -> list[tuple[str, str]]:
    return [
        (full, short)
        for full, short in list_refs(repo, ["refs/remotes"])
        if is_current_branch_remote(full, branch)
    ]


def ensure_current_branch_remotes_not_ahead(
    repo: Path,
    current_remote_refs: list[tuple[str, str]],
) -> None:
    for _full, short in current_remote_refs:
        process = run_git(repo, ["rev-list", "--left-right", "--count", f"HEAD...{short}"], check=False)
        if process.returncode != 0:
            continue
        parts = process.stdout.strip().split()
        if len(parts) == 2 and int(parts[1]) > 0:
            raise SafetyError(
                f"current branch remote {short} is ahead of HEAD; "
                "pull or reconcile before rewriting"
            )


def fork_point_or_merge_base(repo: Path, parent_ref: str) -> tuple[str, str]:
    fork_point = run_git(repo, ["merge-base", "--fork-point", parent_ref, "HEAD"], check=False)
    if fork_point.returncode == 0 and fork_point.stdout.strip():
        return fork_point.stdout.strip(), "fork-point"
    merge_base = run_git(repo, ["merge-base", parent_ref, "HEAD"], check=False)
    if merge_base.returncode != 0 or not merge_base.stdout.strip():
        raise SafetyError(f"could not find merge-base between {parent_ref} and HEAD")
    return merge_base.stdout.strip(), "merge-base"


def candidate_parent_refs(repo: Path, branch: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for full, short in list_refs(repo, ["refs/heads", "refs/remotes"]):
        if full == f"refs/heads/{branch}":
            continue
        if full.startswith("refs/heads/backup/") or full.startswith("refs/remotes/backup/"):
            continue
        if full.startswith("refs/remotes/") and full.endswith("/HEAD"):
            continue
        if is_current_branch_remote(full, branch):
            continue
        candidates.append((full, short))
    return candidates


def preferred_parent_rank(short: str) -> tuple[int, str]:
    try:
        return PREFERRED_PARENT_REFS.index(short), short
    except ValueError:
        return len(PREFERRED_PARENT_REFS), short


def rev_list_count(repo: Path, rev_range: str) -> int:
    raw = git_stdout(repo, ["rev-list", "--count", rev_range])
    return int(raw)


def resolve_parent_base(repo: Path, branch: str, parent_ref: str) -> dict[str, Any]:
    git_stdout(repo, ["rev-parse", "--verify", f"{parent_ref}^{{commit}}"])
    base_sha, base_resolution = fork_point_or_merge_base(repo, parent_ref)
    ensure_base_ancestor(repo, base_sha)
    commit_count = rev_list_count(repo, f"{base_sha}..HEAD")
    if commit_count == 0:
        raise SafetyError(f"parent {parent_ref} does not leave any branch commits to rewrite")
    return {
        "range_mode": "explicit_parent",
        "parent_ref": parent_ref,
        "base_ref": parent_ref,
        "base": base_sha,
        "base_resolution": base_resolution,
        "candidate_commit_count": commit_count,
    }


def auto_parent_base(repo: Path, branch: str) -> dict[str, Any]:
    scored: list[tuple[int, tuple[int, str], str, str, str]] = []
    for _full, short in candidate_parent_refs(repo, branch):
        process = run_git(repo, ["rev-parse", "--verify", f"{short}^{{commit}}"], check=False)
        if process.returncode != 0:
            continue
        try:
            base_sha, base_resolution = fork_point_or_merge_base(repo, short)
        except SafetyError:
            continue
        if base_sha == git_stdout(repo, ["rev-parse", "HEAD"]):
            continue
        process = run_git(repo, ["merge-base", "--is-ancestor", base_sha, "HEAD"], check=False)
        if process.returncode != 0:
            continue
        commit_count = rev_list_count(repo, f"{base_sha}..HEAD")
        if commit_count == 0:
            continue
        scored.append((commit_count, preferred_parent_rank(short), short, base_sha, base_resolution))

    if not scored:
        raise SafetyError(
            "could not infer a parent branch; provide --parent <ref> or --base <ref>"
        )
    commit_count, _rank, parent_ref, base_sha, base_resolution = sorted(scored)[0]
    return {
        "range_mode": "auto_parent",
        "parent_ref": parent_ref,
        "base_ref": parent_ref,
        "base": base_sha,
        "base_resolution": base_resolution,
        "candidate_commit_count": commit_count,
    }


def resolve_base(
    repo: Path,
    branch: str,
    explicit_base: str | None,
    explicit_parent: str | None,
) -> dict[str, Any]:
    if explicit_base and explicit_parent:
        raise SafetyError("provide either --base or --parent, not both")
    if explicit_base:
        base_sha = git_stdout(repo, ["rev-parse", "--verify", f"{explicit_base}^{{commit}}"])
        return {
            "range_mode": "explicit_base",
            "parent_ref": None,
            "base_ref": explicit_base,
            "base": base_sha,
            "base_resolution": "explicit-base",
            "candidate_commit_count": None,
        }
    if explicit_parent:
        return resolve_parent_base(repo, branch, explicit_parent)
    return auto_parent_base(repo, branch)


def ensure_base_ancestor(repo: Path, base_sha: str) -> None:
    process = run_git(repo, ["merge-base", "--is-ancestor", base_sha, "HEAD"], check=False)
    if process.returncode != 0:
        raise SafetyError("base is not an ancestor of HEAD; refusing ambiguous rewrite range")


def branch_commits(repo: Path, base_sha: str) -> list[str]:
    raw = git_stdout(repo, ["rev-list", "--reverse", f"{base_sha}..HEAD"])
    commits = [line for line in raw.splitlines() if line]
    if not commits:
        raise SafetyError("no branch commits found in base..HEAD")
    return commits


def ensure_linear(repo: Path, base_sha: str) -> None:
    merges = git_stdout(repo, ["rev-list", "--merges", f"{base_sha}..HEAD"])
    if merges:
        first = merges.splitlines()[0]
        raise SafetyError(f"target range contains merge commit {first}; message-only linear rewrite required")


def remote_refs_containing(repo: Path, commit: str) -> list[tuple[str, str]]:
    raw = git_stdout(
        repo,
        ["for-each-ref", "--contains", commit, "--format=%(refname)%00%(refname:short)", "refs/remotes"],
    )
    refs: list[tuple[str, str]] = []
    for line in raw.splitlines():
        if not line:
            continue
        full, short = line.split("\x00", 1)
        refs.append((full, short))
    return refs


def ensure_not_shared_remote_reachable(
    repo: Path,
    commits: list[str],
    allowed_current_remote_refs: list[tuple[str, str]],
) -> list[str]:
    allowed_full_refs = {full for full, _short in allowed_current_remote_refs}
    for commit in commits:
        blocked = [
            short
            for full, short in remote_refs_containing(repo, commit)
            if full not in allowed_full_refs
        ]
        if blocked:
            raise SafetyError(
                f"commit {commit} is reachable from shared remote ref {blocked[0]}; "
                "refusing shared history rewrite"
            )
    return []


def commit_info(repo: Path, commit: str) -> dict[str, str]:
    metadata = git_stdout(repo, ["show", "-s", "--format=%an%x00%ae%x00%aI%x00%T%x00%s", commit])
    parts = metadata.split("\x00", 4)
    if len(parts) != 5:
        raise SafetyError(f"could not parse metadata for commit {commit}")
    author_name, author_email, author_date, tree, subject = parts
    return {
        "sha": commit,
        "short": commit[:12],
        "author_name": author_name,
        "author_email": author_email,
        "author_date": author_date,
        "tree": tree,
        "subject": subject,
    }


def inspect_state(
    repo_arg: str,
    base_arg: str | None,
    parent_arg: str | None,
    allow_protected: bool,
) -> dict[str, Any]:
    root = repo_root(Path(repo_arg))
    branch = current_branch(root)
    if is_protected_branch(branch) and not allow_protected:
        raise SafetyError(f"current branch {branch!r} is protected; explicit approval is required")
    ensure_clean(root)
    upstream = resolve_upstream(root)
    current_remote_refs = current_branch_remote_refs(root, branch)
    ensure_current_branch_remotes_not_ahead(root, current_remote_refs)
    base_state = resolve_base(root, branch, base_arg, parent_arg)
    base_sha = base_state["base"]
    ensure_base_ancestor(root, base_sha)
    commits = branch_commits(root, base_sha)
    ensure_linear(root, base_sha)
    blocked_shared_refs = ensure_not_shared_remote_reachable(root, commits, current_remote_refs)
    head = git_stdout(root, ["rev-parse", "HEAD"])
    return {
        "status": "ok",
        "repo": str(root),
        "branch": branch,
        "range_mode": base_state["range_mode"],
        "parent_ref": base_state["parent_ref"],
        "base_ref": base_state["base_ref"],
        "base": base_sha,
        "base_resolution": base_state["base_resolution"],
        "upstream": upstream,
        "head": head,
        "commit_count": len(commits),
        "allowed_current_branch_remote_refs": [short for _full, short in current_remote_refs],
        "blocked_shared_refs": blocked_shared_refs,
        "commits": [commit_info(root, commit) for commit in commits],
        "message_file_pattern": "<messages-dir>/<full-old-sha>.msg",
    }


def read_message(messages_dir: Path, commit: str) -> str:
    path = messages_dir / f"{commit}.msg"
    if not path.is_file():
        raise SafetyError(f"missing replacement message file: {path}")
    message = path.read_text(encoding="utf-8")
    if "\x00" in message:
        raise SafetyError(f"replacement message contains NUL byte: {path}")
    if not message.strip():
        raise SafetyError(f"replacement message is empty: {path}")
    return message


def safe_branch_component(branch: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    return safe or "branch"


def create_backup_ref(repo: Path, branch: str, old_head: str) -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    prefix = f"refs/heads/backup/commit-history-authoring/{safe_branch_component(branch)}-{timestamp}"
    ref = prefix
    suffix = 1
    while run_git(repo, ["show-ref", "--verify", "--quiet", ref], check=False).returncode == 0:
        suffix += 1
        ref = f"{prefix}-{suffix}"
    run_git(repo, ["update-ref", ref, old_head])
    return ref.removeprefix("refs/heads/")


def commit_tree(repo: Path, tree: str, parent: str, message_path: Path, info: dict[str, str]) -> str:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": info["author_name"],
            "GIT_AUTHOR_EMAIL": info["author_email"],
            "GIT_AUTHOR_DATE": info["author_date"],
        }
    )
    process = run_git(
        repo,
        ["commit-tree", tree, "-p", parent, "-F", str(message_path)],
        env=env,
    )
    return process.stdout.strip()


def apply_rewrite(
    repo_arg: str,
    base_arg: str | None,
    parent_arg: str | None,
    messages_dir_arg: str,
    allow_protected: bool,
) -> dict[str, Any]:
    state = inspect_state(repo_arg, base_arg, parent_arg, allow_protected)
    root = Path(state["repo"])
    messages_dir = Path(messages_dir_arg).resolve()
    if not messages_dir.is_dir():
        raise SafetyError(f"messages directory does not exist: {messages_dir}")

    branch = state["branch"]
    old_head = state["head"]
    messages = {
        info["sha"]: read_message(messages_dir, info["sha"])
        for info in state["commits"]
    }
    old_head_tree = git_stdout(root, ["rev-parse", f"{old_head}^{{tree}}"])
    backup_ref = create_backup_ref(root, branch, old_head)

    parent = state["base"]
    mapping: list[dict[str, str]] = []
    for info in state["commits"]:
        old_sha = info["sha"]
        message = messages[old_sha]
        message_path = messages_dir / f"{old_sha}.msg"
        new_sha = commit_tree(root, info["tree"], parent, message_path, info)
        new_subject = message.strip().splitlines()[0]
        mapping.append(
            {
                "old": old_sha,
                "new": new_sha,
                "old_short": old_sha[:12],
                "new_short": new_sha[:12],
                "old_subject": info["subject"],
                "new_subject": new_subject,
            }
        )
        parent = new_sha

    new_head = parent
    new_head_tree = git_stdout(root, ["rev-parse", f"{new_head}^{{tree}}"])
    tree_equivalent = old_head_tree == new_head_tree
    if not tree_equivalent:
        raise SafetyError("rewritten head tree differs from old head tree; branch was not moved")

    run_git(
        root,
        [
            "update-ref",
            "-m",
            "commit-history-authoring: rewrite commit messages",
            f"refs/heads/{branch}",
            new_head,
            old_head,
        ],
    )

    return {
        "status": "ok",
        "mode": "apply",
        "repo": str(root),
        "branch": branch,
        "range_mode": state["range_mode"],
        "parent_ref": state["parent_ref"],
        "base_ref": state["base_ref"],
        "base": state["base"],
        "base_resolution": state["base_resolution"],
        "allowed_current_branch_remote_refs": state["allowed_current_branch_remote_refs"],
        "backup_ref": backup_ref,
        "old_head": old_head,
        "new_head": new_head,
        "commit_count": len(mapping),
        "tree_equivalent": tree_equivalent,
        "mapping": mapping,
        "recovery_command": f"git reset --hard {backup_ref}",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="inspect rewrite safety")
    inspect_parser.add_argument("--repo", default=".", help="repository path")
    inspect_parser.add_argument("--base", help="exact base ref; overrides parent-branch inference")
    inspect_parser.add_argument("--parent", help="parent branch ref; defaults to nearest inferred parent")
    inspect_parser.add_argument(
        "--allow-protected",
        action="store_true",
        help="allow protected branch names after explicit user approval",
    )

    apply_parser = subparsers.add_parser("apply", help="apply message-only rewrite")
    apply_parser.add_argument("--repo", default=".", help="repository path")
    apply_parser.add_argument("--base", help="exact base ref; overrides parent-branch inference")
    apply_parser.add_argument("--parent", help="parent branch ref; defaults to nearest inferred parent")
    apply_parser.add_argument("--messages-dir", required=True, help="directory of <old-sha>.msg files")
    apply_parser.add_argument(
        "--allow-protected",
        action="store_true",
        help="allow protected branch names after explicit user approval",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_state(args.repo, args.base, args.parent, args.allow_protected)
        elif args.command == "apply":
            result = apply_rewrite(args.repo, args.base, args.parent, args.messages_dir, args.allow_protected)
        else:
            parser.error("unknown command")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except SafetyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
