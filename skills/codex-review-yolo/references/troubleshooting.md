# Troubleshooting codex -p yolo

Common failure modes when invoking codex exec for review, and what to do.

## `codex: command not found`

- Verify install: `which codex`. If missing, this skill does not apply — tell the user codex isn't installed and stop.
- On macOS the install is typically `/opt/homebrew/bin/codex`.

## Profile `yolo` not found

- `grep -A2 '^\[profiles.yolo\]' ~/.codex/config.toml` must return the profile block.
- If missing, the user needs to configure it before this skill is usable. Do not invent a substitute profile — the model (gpt-5.4) and reasoning effort (xhigh) are the point of this skill.

## `-o /tmp/codex_audit.txt` file never appears

- Most common cause: codex errored before producing a final message. Read the stream log at `/tmp/codex_audit_stream.log` — the error is usually near the end.
- Second cause: codex still running. At xhigh with a realistic prompt, audits take 2–10 minutes. Use `TaskOutput` with `block: false` to check status without waiting.
- Third cause: you used `--ephemeral` and expected the file anyway — `-o` still writes, but the session isn't saved. That's fine.

## Codex output is short / evasive

- Prompt too thin. Re-draft with: explicit commit SHAs, claimed changes, numbered list of what to check, tooling hints. See `prompt-template.md`.
- If codex says "I cannot verify without more context", provide that context explicitly in the prompt — don't expect it to ask for it.

## Codex reads stale files

- Codex at xhigh does read the current filesystem state, but if there's been a `git commit --amend` or reset between invocations, be explicit in the prompt: "the current HEAD is <sha>, committed just now; read it, not the branch history from earlier today."

## Rate limits / fast-tier saturation

- Fast tier may return a transient error or slow to baseline. The stream log will contain the error. Usually re-invoking in 30–60 seconds clears it.
- Don't switch profiles to work around rate limits — downgrading off `yolo` changes the reasoning depth and defeats the review value.

## Codex missed the verdict block

- See `verdict-contract.md` §"When codex doesn't produce the block". Don't hand-write the verdict.

## Codex made up a file path that doesn't exist

- Classic hallucination. Spot-check every cited path with `ls` before acting on the finding.
- If the hallucinated path is used to justify a blocking finding, the finding is likely wrong — discount that line of the verdict and report that to the user.

## Audit takes way too long (>15 min)

- Prompt is probably too wide. Codex is trying to audit more than one pass can cover.
- Kill the run, split the prompt into two narrower audits, run them in parallel. Parallel invocations of `codex exec` are fine — they don't share session state.

## Stream log grows huge / fills disk

- It shouldn't — the stream is event JSONL, a few MB at most for a normal audit. If it's multi-GB, codex is probably in a tool-calling loop; kill it and tighten the prompt.

## The figma MCP token or other env var isn't visible to codex

- Codex exec inherits the shell's environment, but background shells started via the Bash tool may not have run `source .env`. Always use:

  ```bash
  set -a; source /path/to/.env; set +a
  codex exec -p yolo ...
  ```

  on the same line (or in the same shell invocation). Don't source in one Bash call and invoke codex in a separate Bash call — they are separate shells.
