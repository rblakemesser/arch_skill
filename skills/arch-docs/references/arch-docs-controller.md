# arch-docs Auto Status

## Verdict Source

`arch-docs auto` uses a fresh review/evaluator pass. The review reads
`.doc-audit-ledger.md` and current code, then emits:

- `CONTINUE` when another grounded pass is credible for the resolved docs-health intent.
- `CLEAN` when the resolved stop condition is satisfied; the default pass deletes `.doc-audit-ledger.md` before the run ends.
- `BLOCKED` when the next pass would be speculative, taxonomy-imposing, disconnected from a narrowed scope, or materially unchanged.

## Continuation Rule

Native goal mode supplies the repeated turns. Run a grounded DGTFO pass, run
fresh review, then continue only while the review verdict is `CONTINUE`.

In this repo family, keep treating point-in-time docs older than 30 days as
presumptively stale until the pass records explicit code-grounded current-reader
value for each survivor. A pass that mainly refreshed metadata labels is not
progress.

Outside goal mode, complete one pass plus review and print the next exact
command.
