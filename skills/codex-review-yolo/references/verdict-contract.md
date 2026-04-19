# Verdict Contract

Codex output is long prose by default. The verdict block at the end of the review prompt exists so the final decision is findable and consistent. Always require exactly this shape.

## Required footer

```
VERDICT: approve | approve-with-notes | not-approved
BLOCKING: <bullets or "none">
NON-BLOCKING: <bullets or "none">
ACCURACY OF CLAIMS / COMPLETION: <one paragraph>
```

## Field semantics

- **VERDICT** — one of three literal strings.
  - `approve` — the artifact meets the requested review bar for the next step.
  - `approve-with-notes` — the artifact is good enough for the requested next step, but the notes in `NON-BLOCKING` should be triaged.
  - `not-approved` — there is at least one blocking issue in `BLOCKING`.
- **BLOCKING** — issues that prevent approval for this review objective. For file-based reviews, each bullet names the file + line + the specific fix. For plan or completion audits, each bullet names the unmet outcome, section, or acceptance item.
- **NON-BLOCKING** — observations that can wait (e.g., "Phase B will re-touch this file, defer the rename"). Still report them so they're captured.
- **ACCURACY OF CLAIMS / COMPLETION** — codex's direct assessment of whether the explicit claims, checklist items, or completion targets you provided match the artifacts. If you did not provide any explicit claims or completion targets, codex should say that plainly instead of inventing them.

## Parsing

Don't write a formal parser. Read the file, find the `VERDICT:` line, skim the three sections underneath. That's all. The footer is for human (or LLM-acting-as-human) consumption, not a machine interface.

## Relaying to the user

When reporting back:

1. Lead with the VERDICT, verbatim.
2. Quote the BLOCKING bullets — do not paraphrase. Paraphrasing loses nuance.
3. Summarize NON-BLOCKING if there are many; list verbatim if there are few.
4. Always include the ACCURACY line, especially if codex flagged a claim-to-artifact or completion-to-artifact mismatch.
5. Note the full final-output file path so the user can read the long-form reasoning.

## When codex doesn't produce the block

If the verdict block is missing or malformed:

- **First try:** re-invoke with a prompt that calls out the failure — "Your last response did not include the required VERDICT footer. Produce ONLY the verdict block for the work described in <path to prior prompt>."
- **Don't** hand-write a verdict on codex's behalf. Report to the user that codex didn't follow the contract and ask whether to re-run.

## Overriding codex

Codex is a second opinion, not the final word. If its blocking finding is wrong (you read the file and codex is mistaken), say so explicitly: "codex flagged X as blocking, but the file actually does Y — codex was wrong here." Don't silently ignore it. Transparency about disagreement is the whole point of getting a second opinion.
