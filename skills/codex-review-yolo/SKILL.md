---
name: codex-review-yolo
description: "Invoke the local codex CLI with profile `yolo` (gpt-5.4 xhigh, fast tier) to get an independent, context-free audit of work just completed — diffs, commits, or plans — before pushing. Use when the user says \"have codex review\", \"get a second opinion from codex\", \"audit my work with codex -p yolo\", or asks for an independent/fresh-eyes review of code or a plan. Do NOT use for: asking codex to write code (this is review-only), generic LLM-as-judge evaluations where codex adds nothing, or any case where the reviewable unit is a single sentence rather than a real artifact."
metadata:
  short-description: "Request an independent review from codex -p yolo"
---

# codex-review-yolo

Use this skill when the user wants an independent code / plan / diff audit from the locally-installed `codex` CLI using profile `yolo`. The value is that codex runs as a separate agent with zero session history — it must read the artifacts itself, so its verdict is genuinely independent.

This skill is intentionally narrow. It teaches the invocation pattern, the prompt shape that makes codex actually read files, and how to consume the verdict. It does not wrap every possible codex use case.

## When to use

- User says any of: "review with codex", "audit this with codex", "get a second opinion from codex", "run codex -p yolo", "have codex audit my work".
- User has just finished non-trivial work (diff, multi-commit change, plan, design doc) and wants fresh eyes before push / merge / share.
- User wants an adversarial / skeptical review from a model that doesn't share your blind spots.

## When not to use

- The user wants codex to *write* code, not review it. This skill is review-only.
- The user wants a quick yes/no on a one-line change — the setup cost exceeds the value.
- The user has not yet produced a concrete artifact to review (diff, file, commit, plan doc). Don't spin up codex on vapor.
- `codex` is not installed on the host — `which codex` returns nothing. Stop and tell the user.

## Non-negotiables

- **Run codex with `-p yolo` explicitly.** The profile carries gpt-5.4 + xhigh reasoning + fast service tier + `danger-full-access` sandbox. Any other profile changes the contract.
- **Use `codex exec` (non-interactive), not `codex` (interactive TUI).** You are orchestrating, not babysitting a session.
- **Brief codex like a colleague who just walked in.** It has no memory of your session. Name the commit SHAs, file paths, claimed changes, and what you want checked.
- **Require a structured verdict block at the end.** Without it, codex drifts into narrative and you cannot act on the result.
- **Never pass secrets in the prompt.** If codex needs `FIGMA_ACCESS_TOKEN` or similar, source `.env` into the codex env and instruct codex to read it from the environment.
- **Run in the background for non-trivial audits.** Codex at xhigh takes minutes. Kick it off with `run_in_background: true` so you can keep working.
- **Capture output to a file.** Use `-o /tmp/codex_audit.txt` for the final message; redirect the stream log separately. The final-message file is the consumable deliverable; the stream log is diagnostic.
- **Trust but verify.** Codex can be wrong. Spot-check any blocking finding by reading the cited file before acting on it.

## First move

1. Confirm `codex` exists and the `yolo` profile is defined: `which codex && grep -A2 '^\[profiles.yolo\]' ~/.codex/config.toml`.
2. Identify the exact artifact to review: commit SHA(s), branch, files, or doc path. Write them down in the prompt.
3. If the review needs API tokens, confirm `.env` has them and plan to `set -a; source .env; set +a` before invoking.
4. Draft the prompt to `/tmp/codex_audit_prompt.md` (never inline — prompts get long and multi-line is inevitable).
5. Invoke via `codex exec -p yolo -C <repo-root> -o /tmp/codex_audit.txt < /tmp/codex_audit_prompt.md`, in background.
6. Continue other work while codex reasons; when it completes, Read `/tmp/codex_audit.txt` and relay the verdict to the user.

## Workflow

### 1. Shape the prompt

A good prompt for codex review has these sections, in this order:

1. **Role + posture.** One line. "You are auditing X. Be skeptical. If the work is wrong, say so plainly."
2. **What to audit.** Working directory, branch, commit SHAs, file paths, doc paths. Be specific — codex has no context.
3. **Context — what was claimed.** Summarize the claimed changes in the executing agent's own words, so codex can compare diff vs. claim.
4. **What to check.** Numbered list. Each item names a specific concern and where codex should look.
5. **Tooling hints.** If codex needs external APIs (e.g. Figma REST), tell it the endpoint shape and where the token lives (env var, not inline value).
6. **Verdict block requirement.** Demand a specific footer format so the result is machine-ish-readable.

See `references/prompt-template.md` for the full skeleton.

### 2. Invoke codex

Standard pattern, adjust the repo root and prompt path:

```bash
# If the audit needs API tokens, source them into the codex environment.
set -a; source /Users/aelaguiz/workspace/cjdev/.env; set +a

codex exec -p yolo \
  -C /Users/aelaguiz/workspace/cjdev \
  -o /tmp/codex_audit.txt \
  < /tmp/codex_audit_prompt.md \
  > /tmp/codex_audit_stream.log 2>&1
```

Key flags:

- `-p yolo` — the profile. Non-negotiable.
- `-C <dir>` — the working root. Use the repo root (or the submodule root if that's the reviewed unit).
- `-o <file>` — writes the final assistant message to this file. This is what you Read at the end.
- `< prompt.md` — feeds the prompt via stdin. Keeps command lines sane and lets you iterate on prompts in a file.
- `> stream.log 2>&1` — captures the full event stream. Use for diagnosis if codex errored or went sideways.

Run via the Bash tool with `run_in_background: true` for any audit you expect to take more than ~30 seconds. The final-message file is created when codex exits.

### 3. Consume the verdict

When codex finishes:

1. Read `/tmp/codex_audit.txt`.
2. Locate the `VERDICT:` / `BLOCKING:` / `NON-BLOCKING:` footer.
3. Relay findings to the user. Do not blindly trust — spot-check any blocking claim against the actual file before acting.
4. If codex found nothing actionable, say so directly. Don't manufacture issues to justify the invocation.

## Output expectations

- A short summary to the user: what codex's verdict was, what blocking issues it found (if any), and whether you agree after verification.
- The full `/tmp/codex_audit.txt` stays on disk — mention the path so the user can read the full review if they want.
- Never claim codex said something it didn't. If the output is ambiguous, say "codex was ambiguous on X" and ask the user how to proceed.

## Reference map

- `references/prompt-template.md` — full skeleton for the audit prompt, plus variants for diff review, plan review, and cross-repo review
- `references/verdict-contract.md` — the exact footer format and how to parse it
- `references/troubleshooting.md` — common failure modes (no output, rate-limit, truncation, codex can't find files)
