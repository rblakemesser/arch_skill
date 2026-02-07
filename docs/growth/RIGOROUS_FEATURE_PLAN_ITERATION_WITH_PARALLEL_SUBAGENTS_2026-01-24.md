# Rigorous Feature Plan Iteration (Ground-Truth Loop + Parallel Subagents)

**Date created:** 2026-01-24  
**Owner:** (add)  
**Scope:** This document defines a repeatable workflow for turning a feature plan into a continuously verified, ground-truth-aligned decision system using parallel specialist subagents (human or AI).

This doc exists so that **someone else can pick up the workflow** and continue iterating the plan without needing implicit context, “things Amir remembers”, or hidden assumptions.

---

## 0.0) Prompt journey (where we're headed)

This is the **5-prompt** “operating loop” we want to standardize so the process is re-runnable and parallelizable.

Key convention:
- Prompt 1 creates/updates the single canonical **feature brief doc** (using the appropriate Growth Feature Template).
- Prompts 2–5 take **no required human input**: they infer the active docs by starting from that feature brief and following its linked anchors (goals, SSOT, baselines, exports).

### Names (short, order-obvious, distinct from other prompt families)
- `gflow-1-bootstrap`
- `gflow-2-reality`
- `gflow-3-baselines`
- `gflow-4-refine`
- `gflow-5-build`

### UX overlay upgrade (what we mean by “UX focus” in this flow)
UX overlay is not just a negative review (“how this could fail”). It is a **two-sided contract**:
1) **Positive experience principles that must be true** for the plan to be good (value-prop aligned).
2) **Failure modes + guardrails** (how it could go wrong and how we detect/stop it).

We give the positive contract first billing because it defines what “good” looks like, rooted in:
- UX best practices (clarity, coherence, progress, agency, reliability), and
- our value prop / “why users are here” (trust, skill-building credibility, guided ramp).

By the end of `gflow-3-baselines`, we must have:
- A crisp **UX contract** (user promise + “how we earn credibility” + progress + escape hatches).
- A **UX scoreboard** (leading indicators of “good experience”, not only guardrails).

### Prompt 1 — Bootstrap + contract lock
- Holistic goal: take “idea + why + goals/research” and instantiate the feature brief using the existing template as the contract (scope, freshness, and success measurement intent included up front).
- Human input: optional but often helpful (idea notes, template choice, desired doc path/name).

### Prompt 2 — Journey reality map + lever ranking (with feedback overlay)
- Holistic goal: build the journey-driven reality map (sliced by versions + power-law segments + contexts), rank near-term levers for the locked goal, and cross-check with user feedback overlay.
- Human input: optional.
- Default behavior: infer the active plan/brief doc from Prompt 1 and use its linked goal/research docs as scope anchors.
- UX emphasis: produce an **Experience Principles Review** (positive “must be true” list) and then a feedback overlay risk check (themes that could veto a lever).

### Prompt 3 — Measurement + baselines pack (SSOT-first, two-way, composition-aware)
- Holistic goal: lock measurement reality and baseline truth before building: SSOT definitions, dashboards/queries, Way 1 + Way 2 baselines, and composition checks (platform, entrypoint/moment, paywall source mix, BOTH formation).
- Human input: optional.
- Default behavior: use the measurement section + linked SSOT docs from the brief/template and the most recent referenced export bundle (or the newest conventional export bundle if none is referenced).
- UX emphasis: establish a **UX scoreboard** alongside economics baselines (positive signals + guardrails), and link dashboards/queries up front.

### Prompt 4 — R&D refinement loop (parallel AI cross-validation + Amir intuition)
- Holistic goal: repeatedly refine the feature brief against the template until it is decisionable and internally consistent, with disagreements surfaced and resolved by evidence.
- Human input: optional.
- Default behavior: re-read the same feature brief + worklog and only update what new evidence forces to change.
- UX emphasis: one parallel reviewer is responsible for “positive UX principles” (not just failure-mode critique) and must tie them back to “why users are here”.

### Prompt 5 — Implementation + architecture deep dive + cross-goal multipliers
- Holistic goal: apply the same rigor to the implementation/architecture plan (code touchpoints, instrumentation, rollout/kill-switch/guardrails) and shape the feature to also produce signal/lift for adjacent goals (e.g., UA + lifecycle) without diluting the primary goal.
- Human input: optional.
- Default behavior: derive implementation detail from the refined brief and repo SSOT locations; then propose a minimal phased implementation plan.
- UX emphasis: convert the UX contract into **testable UX acceptance criteria** (progress/agency/fallbacks/credibility) and wire corresponding monitoring/stop-the-line triggers.

---

## 0.1) The holistic workflow (how Amir is actually working)

This is the high-level system we are trying to automate. It describes the end-to-end workflow from “idea” to “now code shit”, using the feature templates as the forcing function.

1) **Journey-driven analysis (reality first)**
   - Start from the actual user journey and slice it multiple ways:
     - versions/build windows
     - power-law usage segments (heavy vs mid vs light users)
     - moment/entry contexts (e.g., onboarding vs need-moment paywalls)
   - Output is not “insights”; output is a ranked list of where the journey leaks and where leverage plausibly exists.

2) **Set near-term goals + scope boundaries**
   - Define the near-term goal(s) and the explicit scope:
     - in scope
     - out of scope
   - This prevents the plan from becoming a generic “make onboarding better” exercise.

3) **Identify biggest near-term levers for the goal(s)**
   - Pick the few levers that plausibly move the goal within the timeframe.
   - Cross-validate these levers with a **user feedback overlay** so we don’t choose a lever that looks good numerically but creates a feedback cliff.

4) **Use the feature template as the contract**
   - Build/choose the right feature template such that, if it is filled out, it forces:
     - alignment to the goals + levers above
     - measurement SSOT (no drift)
     - dashboards / success measurement up front (before implementation)
   - The template is the “ledger”; we do not invent competing artifacts.

5) **Deeply iterate each R&D project against the template**
   - Repeatedly analyze the idea until it “passes muster” against the template:
     - grounded in code truth + telemetry truth + economics truth
     - cross-validated by multiple independent AIs and Amir’s own intuition
   - The goal is not to generate a prettier doc; it is to remove false assumptions and converge on a decisionable plan.

6) **Apply the same rigor to implementation + architecture**
   - After the plan is decisionable, do the same level of scrutiny on:
     - what exactly must change in code
     - what instrumentation must exist
     - what rollout/kill-switch/guardrails must exist
     - where the architecture could create drift or regressions

7) **Multiply impact across adjacent goals (the “systems move”)**
   - Ask: how can this feature also produce signal or lift for other goals?
     - Example: if optimizing onboarding completion + BOTH formation, how does it also help UA and lifecycle?
   - This is explicitly a design step, not an afterthought.

8) **Now code**
   - Only after the plan + measurement + architecture are ready do we implement.

### Reformulation (what this is, in one sentence)
We are building a system that takes: **(idea + goals + prior research)** and repeatedly forces it through the **feature template contract**, using grounded analysis (journey slices, SSOT measurement, and feedback overlay) plus parallel reviewers, until it yields a **decisionable feature brief and a safe implementation plan**.

---

## 0) What this workflow is (and isn’t)

### What it is
A feature plan treated as a **living hypothesis**, repeatedly tested against:

1. **Code truth**: what the product actually does (flows, gating, flags, surfaces).
2. **Telemetry truth**: what is actually tracked and how metrics are computed.
3. **Economics truth**: the objective function (profit, retention, payback) and its decomposition.
4. **Operational truth**: rollout safety, guardrails, reversibility, monitoring.

The plan evolves through **short investigation iterations**. Every iteration yields:
- Updated plan text (explicitly changed assumptions/claims).
- Evidence artifacts (queries, exports, screenshots, code anchors).
- A decision (proceed / modify / split / stop).

### What it is not
- Not “write a doc that sounds good”.
- Not “one analysis pass then ship”.
- Not “trust a single metric” or “trust a single narrative”.

---

## 1) Ground-truth anchors (concrete, reproducible sources)

This section is the “do not argue about reality” anchor list. If any anchor changes, update this section first.

### 1.1 Plan doc being iterated
- `docs/growth/PM_ONBOARDING_SWITCH_PUZZLES_VS_LESSONS_DEEP_DIVE_2026-01-23.md`

### 1.2 Supporting ground-truth docs in this repo (psmobile4)
These are frequently referenced when iterating onboarding/revenue plans:
- `docs/growth/PM_REALITY_MAP_BASELINES_2026-01-20.md`
- `docs/growth/PM_JOURNEY_TELEMETRY_MAPPING_2026-01-22.md`
- `docs/growth/UA_PAYBACK_METRICS_AUDIT_2026-01-23.md`
- `docs/growth/PLAN_TO_NORTH_STAR_UA_5K_D30_PAYBACK_2026-01-23.md`
- `docs/growth/ECONOMY_NEAR_TERM_OPPORTUNITIES_D30_2026-01-23.md`
- `docs/growth/BOTH_SEGMENT_DECONFUND_ONBOARDING_PUZZLE_2026-01-23.md`
- `docs/growth/ANDROID_UA_PAYBACK_DEEP_DIVE_2026-01-23.md`

### 1.3 Canonical templates (live in the `psmobile` repo)
The original “growth feature plan templates” referenced in prior sessions live here (verify you have this repo checked out):
- `/Users/aelaguiz/workspace/psmobile/docs/GROWTH_FEATURE_TEMPLATE.md`
- `/Users/aelaguiz/workspace/psmobile/docs/growth/GROWTH_FEATURE_TEMPLATE_UA_PROFIT_90D_2026-01-24.md`

If you are not in that repo, you can still use this workflow, but you should **copy the relevant sections** into the plan you’re writing or link to the canonical location.

### 1.4 Export bundle SSOT (live in the `psmobile` repo)
Prior workflows explicitly constrained analysis to a single “today’s export bundle” directory (to enforce freshness + reproducibility). Those exports live at:
- `/Users/aelaguiz/workspace/psmobile/apps/analytics/report_exports/<YYYY-MM-DD>/`

Example bundle used in prior sessions:
- `/Users/aelaguiz/workspace/psmobile/apps/analytics/report_exports/2026-01-24/`

**Rule:** Any analysis claim that changes the plan must cite exactly which export bundle(s) it used.

### 1.5 Evidence: prior Codex sessions that established this workflow
These session logs are ground truth for “what workflows we were actually using” (and what constraints were enforced).

They live in:
- `~/.codex/sessions/2026/01/23/`
- `~/.codex/sessions/2026/01/24/`

Depending on how Codex was run, you may also find related logs inside a repo-local directory:
- `<repo>/.codex/` (often includes `sessions/`, `history.jsonl`, and/or CLI logs)

Sessions directly relevant to the onboarding deep dive + rigorous workflow patterns:
- `~/.codex/sessions/2026/01/24/rollout-2026-01-24T07-49-14-019bf044-1bef-78b3-b453-0177d512ff00.jsonl` (doc extractor / orientation)
- `~/.codex/sessions/2026/01/24/rollout-2026-01-24T07-49-15-019bf044-218a-7323-a28b-1c2f57cc06b7.jsonl` (code anchor spot-check)
- `~/.codex/sessions/2026/01/23/rollout-2026-01-23T20-46-13-019bede5-1ca6-7361-b4cb-ed1945b0e60c.jsonl` (UA-profit lens applied to routing / plan claims)
- `~/.codex/sessions/2026/01/23/rollout-2026-01-23T22-44-13-019bee51-252b-7871-a85a-a6397ee58826.jsonl` (baselines replacement; “today’s exports only” discipline)
- `~/.codex/sessions/2026/01/23/rollout-2026-01-23T22-44-17-019bee51-3254-7bd3-a3b6-2630f5589217.jsonl` (feedback guardrails)
- `~/.codex/sessions/2026/01/23/rollout-2026-01-23T22-44-21-019bee51-40db-79d2-bb54-0998f386385c.jsonl` (template compliance checklist)

If you need to find other relevant sessions:
- Search by doc name: `rg -l "PM_ONBOARDING_SWITCH_PUZZLES_VS_LESSONS_DEEP_DIVE_2026-01-23" ~/.codex/sessions -S`
- Search by a distinctive phrase (“Way 1”, “Way 2”, “Payback_D30”): `rg -n "Way 1|Way 2|Payback_D30" ~/.codex/sessions/2026/01 -S | head`

### 1.6 How to read/mine Codex session logs (so this is reproducible)
Codex session files are **JSONL** (one JSON object per line). Common record shapes:
- `type: "session_meta"`: metadata like `cwd`, `model_provider`, `cli_version`.
- `type: "response_item"` with `payload.type: "message"`: user/assistant messages.
- Other `type`s may represent tool calls, progress, etc.

Practical commands (examples):

1) **Print only user/assistant text (chronological)**
```bash
jq -r '
  select(.type=="response_item" and .payload.type=="message")
  | (.payload.role + ":\n" + ((.payload.content[]? | .text? // "") | select(length>0) | .) )
' ~/.codex/sessions/2026/01/24/rollout-2026-01-24T07-49-14-019bf044-1bef-78b3-b453-0177d512ff00.jsonl
```

2) **List which repos/cwds a session was run in**
```bash
jq -r '
  select(.type=="session_meta")
  | .payload.cwd
' ~/.codex/sessions/2026/01/24/rollout-2026-01-24T07-49-14-019bf044-1bef-78b3-b453-0177d512ff00.jsonl
```

3) **Quickly find sessions that mention a file or phrase**
```bash
rg -l "ONBOARDING_FIND_YOUR_LEVEL_PLAN_2026-01-23|Way 2|export bundle" ~/.codex/sessions/2026/01 -S
```

If you want to preserve mined outputs for future humans, paste them into the plan worklog using the “Evidence log entry” schema in §5.3.

---

## 2) Non-negotiables (the rigor contract)

These are rules that keep the system from drifting into vibes.

### 2.1 Separate truths: code truth vs telemetry truth vs business truth
Treat these as distinct “layers” with explicit contracts:
- **Code truth**: the actual user journey and gating logic.
- **Telemetry truth**: what events/properties exist, how users are identified, how metrics are computed.
- **Business truth**: what we are optimizing (profit, payback, BOTH, retention, etc.).

When the plan is wrong, it’s almost always because one of these layers was assumed rather than verified.

### 2.2 Two-way verification for any “load-bearing” claim
Any claim that would change the plan must have **Way 1** and **Way 2**:
- **Way 1:** the primary method (query, export table, code path, measurement computation).
- **Way 2:** an independent cross-check (separate query, separate export, alternative computation, sanity bounds).

If Way 2 fails, the claim is **Inconclusive** (not “probably true”).

### 2.3 Confidence tags (explicit, consistent)
Use a 3-level confidence tag on claims:
- **G (Green):** verified; Way 1 + Way 2 agree; freshness is acceptable.
- **Y (Yellow):** plausible but incomplete; evidence exists but a critical check is missing.
- **R (Red):** contradicted, broken measurement, or unverified assumptions.

### 2.4 Freshness discipline
Every analysis output must state:
- Exact export bundle used (or exact data source + date range).
- Known staleness or schema caveats.

### 2.5 Adoption math is always explicit
If the mechanism changes behavior only for adopters/exposed users:

`Δ overall = adoption_rate * Δ within_adopters`

Plans routinely fail when we confuse a huge within-adopter effect with a tiny adoption rate (or vice versa).

### 2.6 Composition effects are first-class
If you change routing, entrypoints, or paywall source mix, you are often changing:
- Which users see the flow (selection)
- Which paywall is shown (source / placement)
- Which intent states are overrepresented

Always decompose: “Is this a true uplift, or did the mix shift?”

---

## 3) The generalized workflow loop (“plan as executable argument”)

Each iteration ends with a concrete plan update and evidence artifacts. If you can’t produce both, you’re still in exploration.

### Iteration inputs
- Current plan doc (the thing you will edit)
- A locked export bundle / data snapshot (or explicitly justified alternative)
- A known list of code anchors relevant to the flow

### Iteration outputs
- Updated plan doc with: changed claims, updated SSOT, and decisions.
- Evidence bundle: query links / export filenames / code references / screenshots.
- Claims ledger updates (see §5).

### The iteration steps
1. **Lock the objective function**
   - Write the objective as an equation (even if approximate).
   - Name the primary metric(s) and guardrail metric(s).
2. **Lock SSOT definitions**
   - Numerator/denominator, cohort definition, time window, and join key.
   - Revenue definition (net vs gross) and inclusion/exclusion rules.
3. **Extract hypotheses from the plan**
   - Convert prose into testable claims with predictions and disconfirmers.
4. **Run parallel specialist work (subagents)**
   - Assign roles with strict allowed inputs and required outputs.
5. **Synthesize**
   - Decide which claims become Green/Yellow/Red.
   - Update the plan (and remove/replace claims that don’t survive reality).
6. **Decide**
   - Proceed / modify / split into a smaller test / stop.

---

## 4) Parallel subagents: roles, constraints, and required outputs

Parallelization only works when subagents produce **structured artifacts** that are easy to merge into the plan.

### Universal contract for all subagents
Every subagent output must include:
1. **Question** it answered (exact).
2. **Allowed inputs** it used (exact paths, export bundle(s), code files).
3. **Method** (Way 1) and **Cross-check** (Way 2).
4. **Result** (numbers, deltas, or concrete yes/no).
5. **Confidence tag** (G/Y/R) with why.
6. **What would change the conclusion** (missing evidence / next check).

If an output is missing any of the above, treat it as incomplete.

### Role A: Doc Extractor / Claims Ledger Builder
Purpose: convert plan prose into checkable claims.

**Inputs:**
- The plan doc being iterated.

**Outputs:**
- A claims ledger table (see §5.1) containing:
  - Claim ID, hypothesis, prediction, metric, cohort, and confidence.
  - Explicit “unknowns” (assumptions).

### Role B: Code Truth Anchor
Purpose: ensure the plan describes what the product can/will actually do.

**Inputs:**
- Repo codebase and config/flag systems.

**Outputs:**
- A “code truth” map:
  - Entry points (screens/routes)
  - Gating logic / policy
  - Where the switch happens (puzzles vs lessons)
  - Any flags/config that could cause segmentation
- Explicit references to code files and symbols (not just “it seems like…”).

### Role C: Telemetry Truth / Metric SSOT
Purpose: ensure measurement is real, stable, and reproducible.

**Inputs:**
- Event/telemetry docs, event registry, analytics definitions, export schemas.

**Outputs:**
- A metric SSOT block (see §5.2):
  - Event names and required properties
  - Identity/join keys
  - Grain (per-install, per-user, per-session)
  - Known gaps and failure modes

### Role D: Baseline + Decomposition Analyst
Purpose: answer “what is true today?” and “where is the opportunity coming from?”

**Inputs:**
- Locked export bundle(s) or agreed data snapshot(s).

**Outputs:**
- Baselines for core metrics (levels, not just deltas).
- Decomposition by critical segments:
  - Platform (iOS/Android)
  - Entry point/routing source
  - Paywall source/placement
  - Intent proxy buckets (if defined)
- Explicit composition checks (share of traffic, share of revenue).

### Role E: Guardrails / Kill-Switch Designer
Purpose: make the plan safe to run.

**Inputs:**
- Mechanism details and failure modes.

**Outputs:**
- Guardrails list with:
  - Thresholds
  - Monitoring triggers (alert definitions)
  - Rollback actions
  - Halt conditions

### Role F: Experiment Designer
Purpose: make the plan testable and decision-ready.

**Inputs:**
- Hypotheses, baselines, and constraints (engineering, rollout).

**Outputs:**
- Exposure unit + randomization strategy.
- Ramp plan (0% → small % → larger %).
- Duration/MDE estimate or at least a “decision feasibility” note.

### Role G: Skeptic / Red Team
Purpose: prevent confirmation bias and catch confounders.

**Inputs:**
- Current synthesized argument (claims ledger + evidence summary).

**Outputs:**
- Top confounders and how to rule them out.
- Explicit “what would make this wrong?” list.

---

## 5) Required artifacts (copy/paste-ready blocks)

These are designed to be pasted into the plan doc or an adjacent worklog without reformatting.

### 5.1 Claims ledger (minimum viable schema)

| Claim ID | Hypothesis | Prediction (direction + rough size) | Metric (SSOT name) | Cohort / Segment | Way 1 | Way 2 | Confidence (G/Y/R) | Last updated | Notes / Unknowns |
|---|---|---|---|---|---|---|---|---|---|
| C-001 |  |  |  |  |  |  |  |  |  |

**Rules:**
- Every claim in the plan must have a Claim ID.
- If a claim is load-bearing, Way 2 is mandatory.

### 5.2 Metric SSOT block (paste into plan appendix)

**Metric name:** (e.g., `Payback_D30_net`, `BOTH_post_onboarding`, `checkout_verified_per_install`)  
**Objective role:** primary / guardrail / diagnostic  
**Definition:** numerator / denominator (in one paragraph)  
**Cohort:** (install cohort? onboarding completers? exposed users?)  
**Time window:** (D1, D30, rolling 7d, etc.)  
**Grain:** per user / per install / per exposure / per session  
**Identity/join key:** (explicit)  
**Revenue definition:** net vs gross; refunds; fees; tax  
**Data source:** export bundle path(s) + file(s) OR query name(s)  
**Known caveats:** (missingness, platform differences, event drift risks)  
**Way 1 / Way 2 checks:** (how you validate)

### 5.3 Evidence log entry (one per analysis)

**Date:** YYYY-MM-DD  
**Question:**  
**Inputs used:** (export bundle path(s), file(s), code references)  
**Way 1:**  
**Way 2:**  
**Result:**  
**Confidence:** G/Y/R  
**Impact on plan:** (what claim changed / added / removed)  
**Next:** (follow-up needed)

### 5.4 Guardrails block

**Risk:** (failure mode)  
**Metric/Signal:** (what you monitor)  
**Threshold:** (numbers)  
**Detection cadence:** (real-time / daily)  
**Action:** rollback / disable flag / halt ramp / investigate  
**Owner:** (person / rotation)

---

## 6) How to actually run this with humans + AI (or humans only)

### 6.1 The orchestration pattern
One orchestrator (human or AI) runs the loop and delegates to specialists.

**Orchestrator responsibilities:**
- Maintain the claims ledger.
- Enforce the SSOT + freshness rules.
- Reject incomplete outputs (missing Way 2, missing inputs, missing join keys).
- Update the plan doc and decision record every iteration.

**Specialist responsibilities:**
- Answer a narrowly scoped question with explicit inputs and a cross-check.
- Provide a copy/paste artifact, not narrative.

### 6.2 Input constraints to keep people honest
When delegating:
- Specify the exact export bundle directory and forbid other data sources unless explicitly approved.
- Specify which doc sections are in scope (and which are not).
- Specify required segment splits (platform, entrypoint, paywall source).

This is the main defense against accidental “analysis drift”.

---

## 7) Practical checklist (fast version)

Use this checklist at the start/end of each iteration.

### Start-of-iteration
- [ ] Objective function stated as an equation.
- [ ] Export bundle/date snapshot locked.
- [ ] Metric SSOT defined (or explicitly marked “unknown”).
- [ ] Claims ledger extracted/updated.

### End-of-iteration
- [ ] Every changed claim has Way 1 + Way 2 or is marked Inconclusive.
- [ ] Confidence tags updated for changed claims.
- [ ] Plan doc updated with decisions and evidence references.
- [ ] Guardrails/rollback plan exists for any rollout.

---

## 8) Notes on what we were specifically doing in the onboarding deep-dive workflow

This section records the “shape” of the prior workflow so it can be replicated.

### 8.1 The recurring north star framing
The plan work consistently framed a north star like:
- “manufacture more post-onboarding BOTH (after Celebrate)”

This framing matters because it forces the plan to target the revenue head (post-onboarding monetization behaviors), not just top-of-funnel vanity improvements.

### 8.2 The recurring failure mode we were guarding against
Routing changes (puzzles vs lessons) can look good while actually being:
- a composition shift in paywall sources (high-intent vs low-intent)
- a selection effect in who reaches checkout

So the workflow emphasized:
- explicit paywall source mix tracking
- segment splits
- adoption math

### 8.3 “Power-law lever” reminder (paywall source mix)
One consistent theme was that paywall sources are not equal:
- some sources are “high-intent” and disproportionately produce verified checkouts and net revenue
- moving traffic between sources can dominate the measured outcome

This is why decomposition by paywall source/placement is non-optional.

---

## 9) Change log (keep this updated)

| Date | What changed | Why / Evidence | Owner |
|---|---|---|---|
| 2026-01-24 | Created doc | Established generalized workflow + anchored sources | (add) |
