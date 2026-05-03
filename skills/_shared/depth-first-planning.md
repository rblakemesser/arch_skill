# Depth-First Planning Doctrine

Use this reference when an arch-series skill writes, repairs, implements, or
audits phased plans. The purpose is to protect the full destination while
proving the architecture early, not to make the plan smaller or looser.

## The mental model

Depth-first planning has five planning objects:

- `Destination map`: the full known final scope. It is preserved across TL;DR,
  Section 0, target architecture, call-site audit, approved decisions, and the
  phase plan. It is not the Phase 1 checklist.
- `First working slice`: the narrowest real end-to-end path that proves the
  canonical owner path, hardest risk-bearing seam, compatibility or migration
  posture, and verification shape on real inputs. It is not a stub, fake demo,
  unused foundation layer, or special-case path.
- `Expansion map`: the ordered widening after the first slice works. It names
  later axes such as more callers, data states, surfaces, formats, migrations,
  user flows, compatibility cases, or rollout coverage.
- `Proof gate`: the evidence that a phase or sub-plan is safe to build on. It
  answers what later work can now rely on.
- `Scope cut`: a removal, downgrade, or optionalizing of destination-map scope.
  It requires explicit user approval and a `Scope cut (user-approved)` Decision
  Log entry.

The WHY: breadth-first plans feel complete because many final surfaces appear
early, but they defer the highest-risk learning until the blast radius is large.
Depth-first plans keep final scope visible while forcing one real path to work
before expanding breadth.

## Phase and sub-plan count

Count is an outcome, not a target. Do not start with three, five, seven, or
`3-7` and squeeze the work to fit.

Create a phase or sub-plan boundary when there is a real dependency edge, proof
gate, reversibility boundary, migration boundary, or user-review boundary. Split
when one unit blends separately provable work. Merge when a unit only moves
files, creates unused scaffolding, or proves nothing later work can rely on.

The useful version of phase splitting is only this: split blended work at the
proof gate. The useful version of an epic count range is only this: a long list
is a cognitive-load smell, not a target range.

## Audit states

Apply these states when implementing, auditing, or reviewing epic scope:

- Missing approved current scope: fail. The work was due in the current
  approved frontier and is not done.
- Scheduled later expansion: pass for now when the destination-map obligation
  remains visible and is assigned to a named later phase or sub-plan whose proof
  gate is not yet due.
- Silent scope reduction: fail unless the user explicitly approved the cut. A
  vague "later", "defer", "out of scope", "MVP", or dropped obligation is not
  scheduled expansion.

## Failure modes

Use these as recognition tests, not keyword rules:

- Final-form Phase 1: the first phase builds the production version of one
  whole surface or layer, then later phases repeat that shape elsewhere.
- Fake foundations: the plan builds abstractions, schemas, helpers, prompts, or
  harnesses that no real path exercises.
- Layer cake planning: phases are split as data, service, UI, polish, or
  similar layers, and no phase produces a working vertical until the end.
- Preset phase count: the plan chooses a count before mapping proof gates.
- Everything-everywhere checklist: the destination map is copied into Phase 1.
- Expansion treated as cut: a later destination item is failed even though it is
  visibly carried by a named later phase or sub-plan.
- Cut hidden as expansion: approved destination scope disappears under vague
  "later" language without a named owner and proof gate.
- Toy MVP: the first slice is narrow but not real enough for later phases to
  build on.

## Section 7 guidance

Keep the existing Section 7 shape. Do not introduce mandatory `Destination
Map`, `First Working Slice`, or `Expansion Map` headings. Instead, make the
phase `Goal`, `Work`, `Checklist`, `Verification`, and `Exit criteria` show:

- which destination-map obligation this phase protects
- which real slice or expansion axis this phase owns
- which proof gate says the next phase can rely on it
- which later named phase owns any scheduled breadth not due now

The phase plan remains the single execution checklist. The destination map is
not a competing checklist, and the expansion map is not a junk drawer.
