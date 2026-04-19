# Audit Prompt Template

Use this skeleton when drafting `/tmp/codex_audit_prompt.md`. Fill every `<...>` placeholder; delete any section that genuinely doesn't apply (but default to keeping them).

## Skeleton

```markdown
You are auditing <what — one phrase, e.g. "Phase A of the Seller Portal Figma Code Connect rollout">. Another Claude agent (me) just completed the work and wants an independent review before <push | merge | ship>. Be skeptical. If the work is wrong, say so plainly.

# What to audit

Working directory: <absolute path>

## <repo or artifact heading>
- HEAD commit: <sha> ("<subject>")
- Relevant docs:
  - <path>  (one line on why it matters)
  - <path>

## <submodule / other component heading, if applicable>
- <sha> <subject>   (one line of context)
- <sha> <subject>

All commits are LOCAL ONLY — nothing has been pushed.

# Context — what was claimed

The executing agent says it:

1. <claim 1, specific, verifiable>
2. <claim 2>
3. ...

# What I want you to check

Please do ALL of the following. Read files directly from the filesystem — don't trust my claims.

1. **<concern 1>.** <what to look at, where to look>
2. **<concern 2>.** <...>
...
N. **Anything else you notice.** Unused imports, broken contract, security concerns, red flags.

# Tooling hints (if applicable)

- For Figma verification: use `https://api.figma.com/v1/files/<KEY>/nodes?ids=...` with header `X-Figma-Token: $FIGMA_ACCESS_TOKEN` (already in env).
- For CircleCI config parsing: `ruby -r yaml -e 'YAML.load_file(".circleci/config.yml")'`.
- For <other external system>: <endpoint + auth pattern>

# How to report

End with a final verdict block:

    VERDICT: ship / ship-with-notes / do-not-ship
    BLOCKING: <list blocking issues, or "none">
    NON-BLOCKING: <list notable issues that can wait>
    ACCURACY OF EXECUTING AGENT'S CLAIMS: <concise assessment>

Be direct. I want the real assessment, not reassurance.
```

## Variants

### Diff-only review

If the artifact is a single uncommitted diff rather than commits:

- Replace "HEAD commit" with "Uncommitted diff in <branch>; see `git diff HEAD`".
- In "what to check", tell codex: "Run `git diff HEAD` to see the diff".

### Plan / design doc review

If the artifact is a plan doc (not code):

- Drop the commit section entirely.
- In "What to audit", list the doc paths and the specific sections in scope.
- In "What I want you to check", focus on: logical consistency, hidden dependencies, missing preconditions, blast radius of each step, reversibility.
- Keep the verdict block — but rename `BLOCKING` → `BLOCKING BEFORE EXECUTION`.

### Cross-repo / submodule review

When both a super-repo commit and a submodule commit need to be audited together:

- In "What to audit", list both. Explicitly note which commits belong to which repo.
- Tell codex: "The submodule lives at `services/<name>`; `git -C services/<name> log` is how you read its history."

## Anti-patterns

Don't:

- Send a terse prompt like "review my work" — codex has no context and will hallucinate.
- Omit the verdict block — you'll get a narrative that's hard to act on.
- Paste the diff inline instead of pointing at commits — it inflates the prompt and codex can't cross-reference with the rest of the tree.
- List secrets inline. Point at `.env` and source it into the codex env before invocation.
- Ask codex to "also fix the issues it finds". This skill is review-only; fixing is a separate turn after you've read the verdict.

## Sizing

Keep the prompt under ~400 lines. If it's growing beyond that, you're probably trying to audit too much in one pass — split into two audits (e.g. "code correctness" and "drift-proofing strength") and run them in parallel.
