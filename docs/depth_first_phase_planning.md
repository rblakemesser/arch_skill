# Depth-First Phase Planning

This document explains how this repo should think about implementation order,
phase size, and phase count when writing `arch-step` plans or `arch-epic`
decompositions.

The core rule is simple: know the full destination, prove the path with the
smallest real working slice, then expand along that proven path.

Depth-first planning is not vague MVP work. It is not a permission slip to hide
scope. It is a way to protect the final scope while learning early whether the
chosen architecture actually works.

## The Mental Shift

Breadth-first planning starts with the final feature shape and tries to spread
that shape across the first phase. Phase 1 becomes a wide shell: many surfaces
are touched, many final promises are named, but the riskiest path may still be
unproven. Later phases then add more breadth, polish, migration, or cleanup on
top of a path that was never forced to work end-to-end early.

Depth-first planning starts with the same final destination, but it does not
make the first phase carry the full final breadth. It asks: what is the
narrowest real path that proves the architecture, the owner path, the contract,
the migration posture, and the proof shape? Build that. Then widen it.

The difference is not "small scope" versus "large scope." The difference is
when the plan chooses to learn. Depth-first plans learn while the blast radius
is still small.

## Five Planning Objects

Every strong phased plan should make these five objects clear. They do not need
heavy ceremony, but they must be visible enough that an implementer and auditor
can tell what is due now, what is due later, and what would be a real scope cut.

### Destination map

The destination map is the full known final scope. It names the intended final
behavior, important surfaces, owner paths, adjacent surfaces, compatibility
posture, migration or delete posture, and any user-visible obligations that must
survive the plan.

The destination map is not the Phase 1 checklist. It protects final scope from
being forgotten while leaving implementation order free to be depth-first.

### First working slice

The first working slice is the narrowest real end-to-end implementation that
proves the architecture. It should run through the canonical path on real
inputs, touch the highest-risk seam, and produce a state that later work can
trust.

The first working slice is not a stub, demo, toy path, fake fixture path, or
unexercised foundation layer. "Narrow" means narrow but real.

### Expansion map

The expansion map is the ordered widening after the first slice works. It names
the axes that will be expanded: more callers, more data states, more surfaces,
more formats, more migrations, more user flows, more compatibility cases, or
more rollout coverage.

The expansion map is not a junk drawer for "maybe later." If a destination item
is scheduled for later, the expansion map should say what later phase or proof
gate will make it due.

### Proof gate

A proof gate is the evidence that says a phase is safe to build on. It can be a
test, fixture, preview, CLI run, audit result, migration proof, manual check, or
other concrete signal. The right proof depends on the risk.

A proof gate is not a status sentence. It should answer: what can the next
phase now rely on?

### Scope cut

A scope cut removes, downgrades, or makes optional something that was part of
the approved destination map. A scope cut needs explicit user approval and must
be recorded as a scope decision.

Scheduling work for a later expansion phase is not a scope cut when the
destination map still includes it and the expansion map names how it will be
reached.

## Ordering Work From First Principles

Implementation order should come from dependency, architectural risk, and proof.
It should not come from a preset phase count or from the shape of the final
feature.

Start with dependency. If one piece cannot honestly begin until another piece
has shipped a stable output, the stable output comes first. That output must be
real enough for the dependent work to use.

Then look at architectural risk. If a seam might invalidate the rest of the
plan, exercise it early. The highest-risk seam often belongs in the first
working slice even when a cheaper seam would be faster to build.

Then widen breadth. Once the path is proven, expansion phases add more cases
along the same path. They should not create parallel owner paths or surprise
architectural seams unless the destination map and decision log are updated to
explain the discovery.

For agent-backed work, this usually means the first slice should exercise the
prompt, grounding, tool exposure, and native model capability end-to-end before
adding deterministic scaffolding. If the real risk is model behavior, prove or
repair that behavior before building a large harness around it.

## Phase Boundaries And Phase Count

Phase boundaries are proof boundaries. A phase should produce a working state
that can be inspected, tested, and safely built on.

A phase is probably too broad when failure would invalidate a lot of later work
or when several independently provable units are blended together. Split it at
the proof gates.

A phase is probably too small when it only moves files, creates unused
scaffolding, or proves nothing that later work can rely on. Merge it into the
nearest real working slice.

Phase count is a result, not a target. The plan should not start with "three
phases," "five phases," or "three to seven sub-plans" and then squeeze the work
to fit. Count emerges from real dependency edges, proof gates, reversibility
boundaries, migration boundaries, and user-review boundaries.

The useful version of "prefer more phases than fewer" is narrower: if a phase
contains multiple independently provable units, split it. Do not use phase count
as its own quality signal.

The useful version of `arch-epic`'s "3-7 sub-plans" guidance is also narrower:
it is a cognitive-load warning, not a decomposition rule. If a reader cannot
hold the whole map in their head, look for better grouping. If the real gates
produce two or nine sub-plans, do not distort the work just to satisfy a number.

## Proof Gates, Not Coverage Gates

A coverage gate asks whether every final surface exists. That can push plans
toward breadth-first work: touch everything, declare coverage, and defer the
hardest proof.

A proof gate asks whether the current path works well enough to build on. It is
stricter where it matters and lighter where breadth is not due yet.

For a first working slice, a good proof gate usually shows:

- the canonical owner path is being used
- the hardest seam works on real inputs
- the compatibility or migration posture is exercised
- the verification method can catch the failure that matters
- the next expansion axis is concrete

Audits should fail missing work in the current approved frontier. They should
also fail fake expansion maps that hide dropped destination scope. But they
should not treat a destination item as missing current work merely because it is
explicitly scheduled for a later expansion phase.

## Common Failure Modes

Final-form Phase 1: Phase 1 builds the production version of one whole surface
or layer, then later phases repeat that shape elsewhere. Tell: the first phase
has lots of final breadth but little architectural learning.

Fake foundations: Phase 1 builds abstractions, schemas, helpers, or prompts
that are not exercised by a real path. Tell: the proof gate can pass even if no
user-visible or caller-visible path works.

Layer cake planning: phases are split as "data," "service," "UI," and "polish"
even though no phase produces a working vertical. Tell: the first usable state
does not arrive until the end.

Preset phase count: the plan decides the number of phases before mapping proof
gates. Tell: phases have generic names or combine unrelated work to fit a
number.

Everything-everywhere checklist: the destination map is copied into Phase 1.
Tell: the first checklist tries to satisfy every final surface instead of
proving one path.

Expansion treated as cut: a later destination item is marked as missing scope
even though it remains visible in the expansion map. Tell: the audit ignores
the planned order.

Cut hidden as expansion: approved destination scope disappears under words like
"later," "out of scope," "simplify," or "MVP" without user approval. Tell: the
destination map no longer contains the obligation.

Toy MVP: the first slice is narrow, but not real. Tell: it uses fake data,
special paths, or shortcuts that later phases cannot safely build on.

## Implications For The Arch Skills

This document is doctrine, not an implementation plan. It should guide later
changes to the live skill surfaces without replacing those surfaces by itself.

For `arch-step`, the main adjustment is to separate final scope from first
phase scope. Section 7 should keep the destination map visible, define the first
working slice, and name the expansion map. The obligation sweep should protect
all final obligations, but it should not force all final breadth into the first
phase checklist.

`arch-step` should also clarify that "fundamental" means the risk-bearing owner
path, contract, prompt surface, migration seam, or verification shape that later
work depends on. It should not mean "build the whole foundation layer before any
real vertical works."

The "more phases than fewer" line should become a proof-boundary rule: split
work when separately provable units are blended together. Do not reward phase
count by itself.

Implementation and audit loops should continue to honor the approved frontier.
The tighter rule is that the current frontier and the expansion map must be
read together. Missing current-frontier work fails. Visible planned expansion is
not a failure just because it is not due yet. Silent removal from the
destination map is still a hard failure.

For `arch-epic`, decomposition should start with dependency, risk, and proof
gates, then count the resulting sub-plans. The `3-7` language should be treated
as a review-size smell, not a target range.

The first sub-plan should prove the epic's hardest path as early as the true
dependencies allow. If a real prerequisite must come first, that prerequisite
should still ship a usable contract or path, not just a broad platform layer.

Epic critics should distinguish three states:

- missing approved scope, which fails
- planned later expansion, which can pass if the expansion map is explicit
- silent scope reduction, which fails unless the user approved the cut

The goal is not more process. The goal is a clearer mental model: protect the
destination, prove one real path, then expand with evidence.
