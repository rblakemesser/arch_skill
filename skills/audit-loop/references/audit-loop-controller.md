# audit-loop Auto Status

## Verdict Source

`audit-loop auto` reads the `Controller verdict` block in `_audit_ledger.md`
after each fresh `review` pass.

- `CONTINUE` means mapping work or real unresolved risk remains.
- `CLEAN` means no credible audit work remains; delete `_audit_ledger.md` and remove the `.gitignore` entry before finishing.
- `BLOCKED` means the next pass would be speculative, contract-changing, or materially unchanged.

## Continuation Rule

Native goal mode supplies the repeated turns. Run `run`, then `review`, then
continue only while the review verdict is `CONTINUE`. The first turns may be
mapping-only; that is correct behavior, not a failure to make progress.

Outside goal mode, complete one `run` plus `review` cycle and print the next
exact command.
