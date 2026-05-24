# Arbiter And Review

`plan-swarm` uses review to hold quality without serializing all implementation
work.

## Arbiter

The arbiter is a delegated observation-only worker. It compares the phase
contract, execution ledger, current diff, worker logs, and proof evidence.

Ask it:

- Was the phase implemented exactly as specified?
- Did the work stop at the requested boundary?
- Is the implementation architecturally clean?
- Are owner boundaries, persistence, QA, and cleanup obligations covered?
- Which findings are in-scope blockers versus unrelated old debt?

The arbiter does not edit files.

## Thermonuclear Gate

Run `thermo-nuclear-code-quality-review` before phase closure unless the user
explicitly disables it. Treat findings as input, not automatic scope expansion.

## Triage

Each finding becomes:

- `accepted`: in-scope and must be repaired.
- `rejected`: incorrect or contradicted by evidence.
- `deferred`: real but outside the requested phase.

Accepted findings route back to implementation workers, usually by resuming the
related healthy session. Record the rationale for rejected or deferred findings.
