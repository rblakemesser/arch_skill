# Verdict Contract

Codex output is long prose by default. The verdict block at the end of the audit prompt exists so the final decision is findable and consistent. Always require exactly this shape.

## Required footer

```
VERDICT: ship | ship-with-notes | do-not-ship
BLOCKING: <bullets or "none">
NON-BLOCKING: <bullets or "none">
ACCURACY OF EXECUTING AGENT'S CLAIMS: <one paragraph>
```

## Field semantics

- **VERDICT** — one of three literal strings.
  - `ship` — no notes, no asterisks, push it.
  - `ship-with-notes` — safe to push, but the notes in `NON-BLOCKING` should be triaged.
  - `do-not-ship` — there is at least one blocking issue in `BLOCKING`.
- **BLOCKING** — issues that must be resolved before push/merge. Each bullet names the file + line + the specific fix.
- **NON-BLOCKING** — observations that can wait (e.g., "Phase B will re-touch this file, defer the rename"). Still report them so they're captured.
- **ACCURACY OF EXECUTING AGENT'S CLAIMS** — codex's direct assessment of whether the claim list you provided matches the diff. Catches the "I said I did X but actually did Y" failure mode.

## Parsing

Don't write a formal parser. Read the file, find the `VERDICT:` line, skim the three sections underneath. That's all. The footer is for human (or LLM-acting-as-human) consumption, not a machine interface.

## Relaying to the user

When reporting back:

1. Lead with the VERDICT, verbatim.
2. Quote the BLOCKING bullets — do not paraphrase. Paraphrasing loses nuance.
3. Summarize NON-BLOCKING if there are many; list verbatim if there are few.
4. Always include the ACCURACY line, especially if codex flagged a claim–diff mismatch.
5. Note the full audit file path (`/tmp/codex_audit.txt`) so the user can read the long-form reasoning.

## When codex doesn't produce the block

If the verdict block is missing or malformed:

- **First try:** re-invoke with a prompt that calls out the failure — "Your last response did not include the required VERDICT footer. Produce ONLY the verdict block for the work described in <path to prior prompt>."
- **Don't** hand-write a verdict on codex's behalf. Report to the user that codex didn't follow the contract and ask whether to re-run.

## Overriding codex

Codex is a second opinion, not the final word. If its blocking finding is wrong (you read the file and codex is mistaken), say so explicitly: "codex flagged X as blocking, but the file actually does Y — codex was wrong here." Don't silently ignore it. Transparency about disagreement is the whole point of getting a second opinion.
