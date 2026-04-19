# Review Prompt Template

Use this skeleton when drafting a namespaced prompt file such as `$PROMPT_PATH`. Fill every `<...>` placeholder; delete any section that genuinely doesn't apply (but default to keeping them).

## Skeleton

```markdown
You are performing an independent review of <what — one phrase, e.g. "Phase B completion of the Seller Portal rollout">. The requester wants a skeptical external audit before <merge | ship | execute | share | mark-complete>. Be skeptical. Read the artifacts directly. If the work is not approved, say so plainly.

# Review goal

- Requested decision: <what approval means here>
- Standard for approval: <the bar codex should apply>

# What to audit

Working directory: <absolute path>

## Primary artifacts
- <path | commit | branch | checklist | doc> — <why it matters>
- <path | commit | branch | checklist | doc> — <why it matters>

## Supporting artifacts (if applicable)
- <path | commit | branch | checklist | doc> — <why it matters>
- <path | commit | branch | checklist | doc> — <why it matters>

## Scope notes (if applicable)
- <local-only note, repo relationship, or boundary>

# Claims / expected outcomes / completion targets

## Explicit claims (if provided)

1. <claim 1, specific, verifiable>
2. <claim 2>
3. ...

## Expected outcomes or checklist items (if provided)

1. <outcome 1 or completion item>
2. <outcome 2>
3. ...

If neither subsection applies, say: "No explicit claims or checklist were provided; inspect the artifact directly."

# What I want you to check

Please do ALL of the following. Read files directly from the filesystem — don't trust the supplied claims or summaries.

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

    VERDICT: approve / approve-with-notes / not-approved
    BLOCKING: <list blocking issues, or "none">
    NON-BLOCKING: <list notable issues that can wait>
    ACCURACY OF CLAIMS / COMPLETION: <concise assessment>

Be direct. I want the real assessment, not reassurance.
```

## Example adaptations

These are examples, not a mandatory menu. Adapt the skeleton to the actual review goal.

### Example: diff-only review

If the artifact is a single uncommitted diff rather than commits:

- In "Primary artifacts", list "Uncommitted diff in <branch>; see `git diff HEAD`".
- In "what to check", tell codex: "Run `git diff HEAD` to see the diff".

### Example: implementation completion audit

If the user wants an external audit of whether a plan phase or implementation checklist was actually completed:

- In "Review goal", define the approval bar in terms of completion, not shipping.
- In "Expected outcomes or checklist items", list the phase goals or acceptance items you want audited.
- In "what to check", ask codex to compare the implemented artifacts against those outcomes and call out any claimed-but-missing work.

### Example: plan / design doc review

If the artifact is a plan doc (not code):

- In "What to audit", list the doc paths and the specific sections in scope.
- In "What I want you to check", focus on: logical consistency, hidden dependencies, missing preconditions, blast radius of each step, reversibility, and whether the plan actually earns approval for execution.
- Keep the generic verdict block unchanged.

### Example: cross-repo / submodule review

When both a super-repo commit and a submodule commit need to be audited together:

- In "What to audit", list both. Explicitly note which commits belong to which repo.
- Tell codex: "The submodule lives at `services/<name>`; `git -C services/<name> log` is how you read its history."

## Anti-patterns

Don't:

- Send a terse prompt like "review my work" — codex has no context and will hallucinate.
- Omit the verdict block — you'll get a narrative that's hard to act on.
- Treat one example above like a hardcoded prompt shape — adapt the sections to the real review objective.
- Paste the diff inline instead of pointing at commits or files — it inflates the prompt and codex can't cross-reference with the rest of the tree.
- List secrets inline. Point at `.env` and source it into the codex env before invocation.
- Ask codex to "also fix the issues it finds". This skill is review-only; fixing is a separate turn after you've read the verdict.

## Sizing

Keep the prompt under ~400 lines. If it's growing beyond that, you're probably trying to audit too much in one pass — split into two audits (e.g. "code correctness" and "drift-proofing strength") and run them in parallel.
