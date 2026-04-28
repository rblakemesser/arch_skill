# Git Safety

This skill changes Git history. Treat safety as part of the work, not as a
cleanup step after the messages are written.

## Allowed rewrite

The default rewrite is message-only for the current branch's linear commit span
from its nearest parent branch:

- same number of commits
- same commit order
- same tree snapshot for every logical step
- same final branch tree
- same author name, author email, and author date
- new commit messages

The helper recreates commits with `git commit-tree`, then moves the branch with
`git update-ref`. It does not run interactive rebase and does not push.

## Parent and base selection

- By default, infer the nearest parent branch by scanning local and remote
  branch refs, excluding the current branch, same-name remote-tracking refs,
  backup refs, and `*/HEAD` refs.
- Choose the parent whose fork point leaves the shortest `base..HEAD` range.
  Ties prefer `origin/main`, `main`, `origin/master`, `master`, `origin/trunk`,
  `trunk`, `origin/develop`, `develop`, then lexical order.
- Use `git merge-base --fork-point <parent> HEAD` when available. Fall back to
  `git merge-base <parent> HEAD`.
- Use `--parent <ref>` when the user names the parent branch.
- Use `--base <ref>` only when the user wants an exact boundary override.
- The resolved base must be an ancestor of `HEAD`.
- `--base` and `--parent` are mutually exclusive.

The current branch's own remote-tracking refs, such as
`origin/<current-branch>`, are allowed to contain target commits. That is the
normal case for a feature branch that has been pushed already.

## Blocked states

Stop instead of rewriting when:

- the worktree or index is dirty
- the current branch is detached
- the branch is protected or shared, such as `main`, `master`, `trunk`,
  `develop`, `release/*`, or `hotfix/*`, unless the user explicitly approved
  that exact branch risk
- the branch-span range is empty
- the current branch's own remote-tracking ref is ahead of local `HEAD`
- any commit in the target range is reachable from an unrelated remote ref
- the target range contains a merge commit
- any replacement message file is missing or empty
- the helper cannot create a backup branch
- the final tree after rewrite differs from the old head tree

Untracked files count as dirty. This keeps the user's uncommitted work out of a
history rewrite.

## Script contract

Inspect mode:

```bash
python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py inspect --repo . [--parent <ref> | --base <ref>]
```

Apply mode:

```bash
python3 skills/commit-history-authoring/scripts/rewrite_commit_messages.py apply --repo . --messages-dir <dir> [--parent <ref> | --base <ref>]
```

Replacement message files must be named with the full old commit SHA:

```text
<messages-dir>/<old-sha>.msg
```

The script exits nonzero and prints one clear error on unsafe state. On success,
inspect prints JSON with the range mode, inferred or explicit parent, base,
allowed current-branch remote refs, commit list, and message-file pattern. Apply
prints JSON with the same range fields plus backup branch, old head, new head,
per-commit mapping, tree-equivalence result, and recovery command.

## Recovery

Every apply creates a local backup branch before moving the current branch:

```text
backup/commit-history-authoring/<branch-safe>-<timestamp>
```

To recover:

```bash
git reset --hard <backup-ref>
```

Do not run that recovery command automatically unless the user explicitly asks
for rollback. It is destructive to the rewritten branch state.
