# Resource Leases

Verification resources are shared. The parent agent coordinates them instead of
letting every worker run expensive checks.

## Lease Examples

- full test suite
- simulator or emulator
- browser automation
- mobile device
- database migration
- code generation
- build cache-heavy compile

## Rules

- A slice that needs a scarce resource names it in the swarm ledger.
- The parent assigns at most one active worker to a scarce resource at a time.
- Workers without a lease may run cheap slice-local checks.
- A designated verification worker may hold the expensive test lease after
  implementation slices finish.
- Release leases when a worker completes, fails, or is explicitly abandoned.
