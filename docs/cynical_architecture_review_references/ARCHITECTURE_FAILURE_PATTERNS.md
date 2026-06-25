# Architecture Failure Patterns

Date: 2026-06-25

Parent brief:
[Cynical Architecture Review Intention](../CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)

Research base:
[Simplicity and architecture research](SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md)

Doctrine base:
[Doctrine notes](CYNICAL_ARCHITECTURE_REVIEW_DOCTRINE_NOTES.md)

## How To Use This Catalog

This catalog is for judgment, not pattern matching. The reviewer should
use these patterns to sharpen suspicion, then prove the issue from current code.

Each pattern asks:

```text
Did this architecture exist because the problem required it, or because
iteration made it happen?
```

## 1. Architecture That "Just Happened"

Signal:

- The current structure is explainable as a sequence of patches, but not as a
  clean design chosen from today's requirements.
- Every piece has a local reason, but the total system has no clear owner or
  concept model.

Why it matters:

- Local reasons accumulate into global complexity.
- Future agents will assume the structure is intentional and copy it.

Review move:

- Reconstruct the simplest architecture from user experience and constraints.
- Mark every piece that only exists because of historical iteration.

## 2. Invalid Split Ownership

Signal:

- Two modules both partially own the same domain concept, state, lifecycle,
  validation, persistence, routing, prompt behavior, or contract.
- Callers must choose between owners or know when each owner is valid.

Why it matters:

- Split ownership creates drift and makes correctness depend on developer
  memory.

Review move:

- Name the invariant.
- Name the one owner that should enforce it.
- Identify the losing owner path that should be deleted, moved, or made
  impossible.

## 3. Duplicate Truth With Different Names

Signal:

- Two fields, configs, schemas, helpers, prompts, commands, or docs express the
  same truth with different wording.
- Both are still live or can influence behavior.

Why it matters:

- The codebase now has two answers to one question.
- Tests may cover one truth while runtime follows the other.

Review move:

- Trace readers and writers.
- Collapse to one representation or one generated source.

## 4. Compatibility Shim That Became Architecture

Signal:

- A migration bridge, fallback reader, old API, alias, feature flag, adapter, or
  "temporary" path is still active after the new path exists.
- New code has started depending on the shim.

Why it matters:

- The shim becomes a second architecture and blocks convergence.

Review move:

- Ask which active consumer still requires it.
- If real, require an explicit sunset path.
- If not real, delete it or fail loudly.

## 5. Abstraction Laundering

Signal:

- A wrapper, service, manager, registry, provider, orchestrator, factory, or
  adapter gives messy logic a respectable name without reducing concept count.
- The abstraction mostly passes data through or exposes the same flags as the
  underlying implementation.

Why it matters:

- The abstraction hides confusion and makes later reviewers hesitate to remove
  it.

Review move:

- Ask what dangerous detail the abstraction hides.
- If the answer is unclear, inline, delete, or move the real logic to the
  canonical owner.

## 6. Layer Added To Avoid A Decision

Signal:

- A new layer routes between old and new paths instead of choosing one.
- The code now supports multiple modes because nobody decided which model is
  correct.

Why it matters:

- Decision avoidance becomes runtime complexity.

Review move:

- Identify the missing decision.
- Push for one canonical path, or a time-boxed migration path with a deletion
  condition.

## 7. Generic Machinery For One Concrete Case

Signal:

- The code adds plugins, registries, metadata schemas, event buses, policy
  engines, strategy maps, or model matrices for a single current variation.

Why it matters:

- Generality taxes every future maintainer before variation exists.

Review move:

- Ask what current variation requires runtime genericity.
- If none, replace with direct code or a smaller static boundary.

## 8. Feature Flag As Architecture Boundary

Signal:

- A flag changes which architecture owns the behavior, not just which user
  behavior is enabled.
- Both flag paths require separate state, validation, or downstream handling.

Why it matters:

- The repo now has two systems behind one interface.

Review move:

- Preserve experiment requirements, but ask whether the flag can select a
  behavior inside one owner instead of selecting between two owners.

## 9. State Spread

Signal:

- Several places track related state and must stay synchronized.
- A caller can observe impossible or partial combinations.

Why it matters:

- Bugs become timing, lifecycle, and forgotten-update failures.

Review move:

- Find the single state model.
- Make invalid combinations unrepresentable or fail loud at the owner.

## 10. Caller Memory Contract

Signal:

- Correct use requires callers to remember ordering, magic flags, cleanup calls,
  lifecycle transitions, matching IDs, or hidden validation rules.

Why it matters:

- The architecture leaks internal rules to every caller.

Review move:

- Move the rule into the API, type, state model, command path, or owner.
- Make wrong use hard or impossible.

## 11. Process-Step Decomposition

Signal:

- Modules mirror execution steps rather than hiding design decisions likely to
  change.
- Changing a representation requires edits across many steps.

Why it matters:

- The system can only be understood as a whole.

Review move:

- Recut ownership around volatile decisions and hidden representations.

## 12. Shallow Module Sprawl

Signal:

- Many files or classes have tiny implementations but large interfaces,
  configuration surfaces, or caller obligations.

Why it matters:

- The module boundary costs more than it hides.

Review move:

- Merge shallow modules or replace them with a deeper owner that hides more
  complexity behind a smaller interface.

## 13. Pattern Laundering

Signal:

- The code claims a pattern is acceptable because similar code exists nearby.
- The nearby pattern was never proven to be intentional or healthy.

Why it matters:

- Accidents become precedents.

Review move:

- Audit the origin and current role of the existing pattern.
- Mark it as canonical, accidental-but-contained, or wrong-road.

## 14. Over-Documented Bad Boundary

Signal:

- Docs or comments explain how not to misuse an API, but the API still permits
  misuse.

Why it matters:

- Documentation is weaker than an enforced boundary.

Review move:

- Push the rule into code shape: type, constructor, route, command, schema,
  validator, or state transition.

## 15. Test-Mocked Architecture

Signal:

- Tests prove an internal abstraction, mocked flow, or fixture contract, but do
  not prove the real runtime owner path.

Why it matters:

- The architecture can be wrong while tests are green.

Review move:

- Treat tests as claims.
- Trace runtime flow and identify whether test boundaries mirror real
  boundaries.
- Do not turn this into a coverage complaint. It matters only when the test
  surface hides or preserves the wrong architecture boundary.

## 16. Orchestrator Gravity

Signal:

- A central orchestrator keeps gaining conditional branches, sequencing rules,
  retries, special cases, and knowledge of child internals.

Why it matters:

- The orchestrator becomes the real domain model by accident.

Review move:

- Push decisions down to the owner that has the invariant.
- Keep orchestration focused on ordering, not domain meaning.

## 17. Adapter Pile

Signal:

- Several adapters translate between internal shapes that could have shared one
  contract.

Why it matters:

- Translation layers hide the fact that the model is unsettled.

Review move:

- Identify the canonical internal shape.
- Keep adapters only at true external boundaries.

## 18. Configuration As Programming Language

Signal:

- Config files, YAML, JSON, environment matrices, or prompt metadata encode
  branching logic that belongs in code or a simpler static choice.

Why it matters:

- The system gains a second programming language without tooling, types, or
  owner clarity.

Review move:

- Ask whether runtime configurability is required.
- Move logic to code or collapse to fixed explicit cases.

## 19. Generated Artifact Drift

Signal:

- Generated files, schemas, snapshots, docs, examples, or prompt surfaces can
  disagree with source code.

Why it matters:

- Reviewers and agents may follow stale generated truth.

Review move:

- Find the generator or canonical source.
- Make downstream artifacts generated from one owner or clearly non-authority.
- Do not turn this into docs cleanup. It matters only when stale artifacts
  preserve duplicate truth, old owner paths, or future-copy traps.

## 20. Architecture Theater

Signal:

- The change adds diagrams, layers, categories, modes, scorecards, policy
  language, or review artifacts without making the actual code path simpler.

Why it matters:

- It creates the feeling of control while adding concepts.

Review move:

- Demand a code-level simplification or delete the ceremony.

## 21. Experiment Requirement Overreach

Signal:

- The implementation claims A/B testing, reversibility, measurement, or staged
  rollout requires duplicated architecture.

Why it matters:

- Real experiment constraints matter, but they are often used to justify
  permanent split-brain systems.

Review move:

- Preserve the experiment, but force the split to the smallest possible level:
  data, config, or behavior selection inside one owner where possible.

## 22. User Experience Mismatch

Signal:

- The architecture is elegant for internal builders but does not map cleanly to
  the actual user job.

Why it matters:

- Architecture exists to serve behavior. Internal elegance that distorts the
  product is not simplicity.

Review move:

- Restate the user job.
- Keep the experience fixed and simplify the implementation path underneath.

## 23. Cemented First Draft

Signal:

- Initial scaffolding, exploratory files, prototype naming, or temporary
  directory layout now carries production behavior.

Why it matters:

- The codebase inherits prototype assumptions after the experiment becomes
  real.

Review move:

- Identify which first-draft pieces now need real ownership.
- Delete or rename scaffolding that would mislead future work.
