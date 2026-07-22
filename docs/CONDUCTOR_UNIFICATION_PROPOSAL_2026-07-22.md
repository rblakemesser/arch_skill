# Proposal: One `conductor` Skill — Plans Or Outcomes In, Verified Code Out

Date: 2026-07-22
Status: IMPLEMENTED 2026-07-22 — `plan-conductor` renamed to `conductor`
with the shaping stage and fleet default; `skills/_shared/aim-rotation.md`
extracted; `agent-delegate` gained usage-limit continuity.

## The pattern being encoded

Amir's recurring hand-typed invocation:

> Claude Fable is the expensive executive. It preserves its own context,
> thinks at the highest level, decomposes the problem, and guards scope.
> GPT-5.6 Sol at ultra is the fast, cheap, very smart worker fleet — but it
> over-scopes and iterates pedantically, so Fable owns judgment. Dispatch
> workers in parallel where possible. If a worker hits a usage limit, rotate
> accounts with `aim codex use` and keep going. Sometimes swap the fleet to
> Kimi or another provider. Input ranges from a full plan to a partial plan
> to just a described outcome.

## Recommendation in one paragraph

Evolve `plan-conductor` into a single skill named **`conductor`** that
accepts the full intake spectrum — described outcome, partial plan, or
finished plan — and retire the `plan-conductor` name. The readiness gate that
makes delegated execution safe does not require a skill boundary; it becomes
an internal stage gate: workers are never dispatched until an artifact with
observable done-ness and a frozen scope boundary exists, and when the input
doesn't already satisfy that, an executive shaping stage produces it first.
Separately (unchanged from v1): move the `aim` rotation facts into
`skills/_shared/` and teach `agent-delegate` the usage-limit-rotate-resume
runbook, because rate-limit continuity is transport mechanics, not conductor
doctrine.

## Why unify instead of wrap (correcting v1)

The v1 proposal kept `plan-conductor` intact and added an `outcome-conductor`
wrapper whose full-plan path was "hand off to plan-conductor unchanged." That
made the wrapper a strict superset of the wrapped skill — exactly the invalid
split ownership and routing sprawl this repo's own architecture doctrine
hunts. The specific v1 arguments, re-examined:

- **"The readiness gate is the safety property; don't loosen it."** True, but
  the gate is a precondition on *dispatch*, not a reason for two skills. A
  unified skill enforces it identically: no worker launches until done-ness
  and frozen scope exist on disk. Shaping runs before the gate, never around
  it.
- **"Wrappers are house style (arch-epic wraps arch-step)."** arch-step
  itself is the stronger precedent: one skill, many modes, one artifact.
  A conductor with an intake ladder is one skill with stages, not a new
  topology.
- **Migration cost is bounded.** Live surfaces referencing `plan-conductor`:
  `AGENTS.md`, `README.md`, `Makefile`, `docs/arch_skill_usage_guide.md`, and
  three files under `skills/plan-implement/`. The other hits are dated
  historical analysis docs that stay untouched. One rename plus five surface
  updates.

The one real cost of unification: the skill's description/trigger surface
gets wider, and description text is how routing happens. Mitigation: the
intake ladder is a single dimension — "what already exists on disk" — not a
family of modes, and the description can say exactly that in one clause.

## The unified `conductor` design

Everything below plan-conductor already does is retained verbatim: role
economy, conductor log, chunking, parallelism doctrine, watchdog heartbeats,
inverted-burden audits, send-back caps, scope triage, checkpoint commits,
final gate, cold verifier, and the `terra` delivery preset. What changes is
the front of the skill and the default execution policy.

### 1) Intake ladder (new front stage)

Resolve once at invocation, by inspecting what the user provided:

- **Finished plan with observable done-ness** → existing intake and readiness
  gate, unchanged. Straight to execution.
- **Partial plan** → parent reads what exists, names the gaps (requirements
  without done-ness, missing non-goals, unordered work), and fills only the
  gaps into the outcome map. Existing plan text stays authoritative; the map
  anchors into it rather than rewriting it.
- **Outcome only** → full executive shaping stage.

### 2) Executive shaping stage (new)

The "work with the fleet to define the solution" step:

- The parent may dispatch parallel cheap workers to *research and propose* —
  read code, scope options, draft slice proposals — returning compact
  summaries. Worker output is evidence, not decisions. This keeps the
  executive's context unpolluted by file-level detail, which is half the
  point of the pattern.
- The parent — explicitly the scope judge, because the fast fleet over-scopes
  — trims to the smallest sufficient solution and writes a lightweight
  **outcome map** beside the work: North Star, non-goals / do-not-build
  boundary, ordered slices each with observable done-ness and verification,
  dependency notes. Deliberately lighter than an arch-mini-plan; its job is
  to satisfy the readiness gate and `scope-and-convergence` provenance and
  make the run resumable.
- **One approval pause**: the user approves the scope boundary (mirrors
  arch-epic's decomposition approval). After approval the boundary is frozen;
  worker and reviewer discoveries cannot silently expand it — the same
  freeze discipline the execution stages already enforce. An explicit
  `full-auto` phrase may skip the pause for low-stakes runs.
- The readiness gate then runs against the outcome map exactly as it runs
  against a finished plan today. Shaping output that still lacks done-ness
  fails the gate and stops the run — the gate is never waived.

### 3) Fleet execution policy (new default)

- Default fleet: parallel external Codex workers, `gpt-5.6-sol`, effort
  `ultra`, dispatched through `$agent-delegate` (fresh-resumable, receipts,
  exact-session resume for send-backs). These values are already the
  repo-wide omitted-value defaults; the change is that conduction defaults to
  the external cheap-fleet lane instead of native-first.
- This is a deliberate standing policy choice under
  `_shared/agent-orchestration-policy.md`, stated once in the skill: the
  entire premise of conduction is parent-context preservation plus cheap fast
  worker cycles, so the exact cheaper/faster external model *is* the concrete
  benefit the policy asks for. Native children remain available when the user
  asks or when a slice genuinely fits one better (tiny read-only checks,
  same-host verification).
- One-word fleet swap via `agent-delegate`'s existing resolution table:
  "use kimi" → `kimi-code/k3` at `max`; "use grok" → `grok-4.5`;
  "use cursor" → `composer-2.5-fast`; "use claude" → supported Claude models.
  Mixed fleets per-slice when the user says so. Resolution stays in
  `agent-delegate`; `conductor` points at it and never duplicates the table.
- The `terra` preset carries over unchanged as the locked
  worktree/xhigh/three-review/PR delivery path.

### 4) Boundaries after unification

- `bugs-flow` — single bug investigation and fix.
- `goal-loop` — goal clear, path unknown, bet-per-iteration learning. The
  conductor requires a definable done-state; goal-loop does not.
- `arch-epic` — multiple full arch plans with per-sub-plan ceremony.
- `arch-step` / `arch-mini-plan` / `lilarch` — when the *plan artifact
  itself* is the deliverable or the work needs full architecture ceremony
  before any execution. The conductor's outcome map is an execution artifact,
  not an architecture plan; users who want real architectural grounding still
  plan first and hand the finished plan to `conductor`.
- `plan-implement` — the parent implements the plan itself.
- `agent-delegate` — one delegated task, no orchestration.
- `plan-audit`, `fresh-consult` — audit and read-only opinions.

## Usage-limit continuity (unchanged from v1)

- Extract the "aim rotation facts" from
  `skills/codex-babysit/references/signals-and-runbook.md` into
  `skills/_shared/aim-rotation.md`: `aim status --accounts`, pick a `ready`
  account low on both 5h and weekly, `aim codex use <label>` rewrites
  `~/.codex/auth.json`, and a process restart is required because codex reads
  auth at startup. `codex-babysit` keeps its tmux pane signals and points at
  the shared file.
- Add a "usage-limit continuity" section to
  `skills/agent-delegate/references/model-and-invocation.md`: when a Codex
  worker's `stderr.log`/`events.jsonl` shows a hard usage-limit failure (not
  a transient reconnect), rotate per the shared reference, then continue the
  **exact same session** via the existing `resume` mode with the captured
  `session_id.txt` — new process on the new account, same conversation. This
  makes "rotate and keep going" automatic anywhere `agent-delegate` is the
  transport, including under `conductor`.

## Migration plan (retiring the `plan-conductor` name)

1. `git mv skills/plan-conductor skills/conductor`; update `name:` and the
   description for the intake spectrum; add the shaping-stage and outcome-map
   references; keep all existing references intact.
2. Update the five live surfaces: `AGENTS.md` routing entry, `README.md`
   inventory, `Makefile` install list, `docs/arch_skill_usage_guide.md`
   section, and the three `skills/plan-implement/` mentions
   (`$plan-conductor` → `$conductor`).
3. Retire cleanly per house red lines: no stub skill, no alias package, no
   runtime dependency on the old path. Historical dated docs keep the old
   name as history and are not edited.
4. Existing in-flight conductor logs (`*_CONDUCTOR_LOG.md`) remain valid —
   the log contract does not change.

## Open decisions (need Amir)

1. **Name.** `conductor` (recommended — short, plain, the pattern's family
   name). Alternative: `outcome-conductor` if collision with the English word
   in prose feels too fuzzy for routing.
2. **Fleet-by-default vs. preset keyword.** Recommended: cheap external
   fleet is the conductor's default execution policy (stated once as a
   standing policy choice). Alternative: keep native-first and require a one
   word `fleet` preset, like `terra`. Default-on matches how Amir actually
   uses the pattern.
3. **Approval pause.** Recommended: mandatory one-time scope approval for
   shaped/partial intake, with an explicit `full-auto` opt-out. Finished
   plans keep today's no-pause behavior.
4. **Outcome map format.** Recommended: minimal purpose-built format (North
   Star, non-goals, slices, done-ness) as a `conductor` reference, not a
   forced arch-mini-plan shape.

## Build order

1. `skills/_shared/aim-rotation.md` + `codex-babysit` pointer + the
   `agent-delegate` rotation/resume runbook (small, independently useful
   regardless of the rename).
2. The `conductor` rename and front-stage additions via `$skill-authoring`
   (intake ladder, shaping stage, outcome-map contract, fleet policy).
3. The five live-surface reference updates.
4. `npx skills check` + `make verify_install` (install surface changes with
   the rename).
