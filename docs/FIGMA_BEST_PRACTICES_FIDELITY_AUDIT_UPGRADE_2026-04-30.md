---
title: "Figma Best Practices - Fidelity Audit Upgrade - Architecture Plan"
date: 2026-04-30
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: []
doc_type: phased_refactor
worklog: docs/FIGMA_BEST_PRACTICES_FIDELITY_AUDIT_UPGRADE_2026-04-30_WORKLOG.md
related:
  - skills/figma-best-practices/SKILL.md
  - skills/figma-best-practices/references/figma-file-craft.md
  - skills/figma-best-practices/references/figma-mcp-agent-gotchas.md
  - skills/figma-best-practices/references/figma-source-backed-parity.md
  - skills/figma-best-practices/agents/openai.yaml
  - docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md
  - /Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md
---

# TL;DR

**Outcome:** Upgrade the existing `$figma-best-practices` skill so it can guide
actual Figma file-craft audits and source-backed app fidelity audits end to end,
including duplicate/mess detection, screenshot/reference handling, app/source
matching, visual parity methodology, metadata/handoff readiness, and repair
planning, without creating a new skill or adding deterministic harnesses.

**Problem:** The current skill now has useful file-craft doctrine and a small
source-backed parity reference, but the full fidelity audit requirements and the
portable method proven by the local case-study material are still outside the
shipped runtime surface. That lets agents stop at generic Figma best practices
or screenshot resemblance instead of producing grounded, exhaustive,
Figma-clean audit work.

**Approach:** Keep `figma-best-practices` prompt-only and upgrade it as an
adaptive evidence toolkit, not a rigid prompt runner. `SKILL.md` owns the
mission, boundaries, reference-selection rails, and output expectations;
reference docs own file craft, MCP gotchas, source-backed parity,
app-fidelity audit categories, evidence ranking, report contracts,
duplicate/stale handling, and Figma output hygiene. Use `$skill-authoring` to
keep the package self-contained and correctly scoped, and `$prompt-authoring`
to keep the runtime prose mission-level, anti-heuristic, and useful across
unpredicted Figma tasks rather than locked to a brittle checklist.

**Plan:** Planning is complete through research grounding, deep-dive, and
phase planning. Implement Section 7 Phases 1-7 in order: lock the runtime
shape, add the audit toolkit reference, add the visual fidelity reference,
reconcile existing references, refactor the entrypoint and metadata, sync the
planning-source requirements doc, and verify with `npx skills check` plus
readback and whitespace checks.

**Non-negotiables:**

- Do not create `figma-app-fidelity-audit` or any other new skill.
- Keep the existing skill prompt-only. No new runners, controllers, OCR stacks,
  fuzzy matchers, or visual-diff scripts unless a later user-approved plan
  explicitly changes that.
- Preserve the skill's broad Figma file-craft lane while making app/source
  fidelity auditing a first-class mode inside the same package.
- Do not dump the full case-study methodology or giant requirement catalog into
  `SKILL.md`; keep `SKILL.md` lean and move detailed reusable doctrine into
  owned skill references.
- Do not make the shipped skill depend on, point to, or name local source docs
  as runtime reading. The final package must be fully self-contained under
  `skills/figma-best-practices/**`.
- Do not bake project-specific names, paths, commands, screenshots, or artifact
  layouts into the reusable skill. Local source material is for distillation,
  not identity.
- Do not put authoring notes, rationale about this upgrade, discussion history,
  case-study provenance, implementation commentary, or "why this was added"
  exposition into the shipped skill. Runtime doctrine must read as timeless
  operating guidance.
- Do not create an "acceptable input" gate. The skill must accept whatever
  Figma-related target, artifact, note, screenshot, source hint, or vague
  request the user provides, then classify what is knowable and ask only when
  missing information blocks the requested level of confidence.
- Do not prescribe one fixed workflow. The upgraded skill should expose tools,
  lenses, evidence levels, and common rails that smart agents can compose for
  the task at hand.
- Do not make Figma itself the report surface. The upgraded skill must continue
  to route audit reports, source maps, duplicate indexes, and acceptance
  matrices to repo docs, with Figma reserved for visual references, components,
  compact labels, component descriptions, Dev Resources, and `Index`.
- A "pass" claim must require explicit evidence: source-pair identity, Figma
  node, app/source target, artifact role, visual proof or declared visual
  blocker, and duplicate/stale disposition.

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: 2026-04-30
Verdict (code): COMPLETE
Manual QA: n/a (non-blocking)

## Code blockers (why code is not done)

- None.

## Reopened phases (false-complete fixes)

- None.

## Missing items (code gaps; evidence-anchored; no tables)

- None. The full approved Section 7 frontier is code-complete against current
  repo evidence:
  - `skills/figma-best-practices/references/figma-audit-toolkit.md` now owns
    all required audit output contracts: findings, compliance checklist,
    coverage ledger, app-fidelity match ledger, authorship ledger,
    handoff-readiness ledger, style-guide gap ledger, duplicate/stale ledger,
    verification receipts, and repair plan.
  - `skills/figma-best-practices/SKILL.md` stays lean and points to the owned
    references for app/source fidelity, audit outputs, duplicate/stale review,
    visual parity, and repair planning.
  - `skills/figma-best-practices/agents/openai.yaml` represents the expanded
    fidelity/audit lane without creating a new skill, runner, or deterministic
    audit product.
  - `skills/figma-best-practices/references/figma-file-craft.md`,
    `figma-mcp-agent-gotchas.md`, `figma-source-backed-parity.md`,
    `figma-audit-toolkit.md`, and `figma-visual-fidelity.md` have coherent
    ownership boundaries and no runtime dependency on the planning docs or
    local source packs.
  - `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` has the
    required planning-source status note; README and install behavior remain
    unchanged as planned.
  - Verification rerun during this audit: `rtk proxy npx skills check`,
    `rtk git diff --check`, trailing-whitespace `rtk rg`, local-identity leak
    review under `skills/figma-best-practices`, output-contract `rtk rg`, and
    SKILL description length check.

## Non-blocking follow-ups (manual QA / screenshots / human verification)

- None. This is a prompt-first skill package audit; no app/device or Figma UI
  manual QA is required by the plan.
<!-- arch_skill:block:implementation_audit:end -->

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-30
external_research_grounding: done 2026-04-30
deep_dive_pass_2: done 2026-04-30
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

If this upgrade is done correctly, then an agent using the existing
`$figma-best-practices` skill can take any Figma-related starting point the
user provides, including a URL, page, node, component, screenshot, source hint,
local artifact, vague complaint, or desired repair, and produce grounded
guidance or an audit that:

- classifies the Figma artifact role before judging it;
- maps claimed app fidelity to real source, tokens, assets, screenshots, and
  runtime state when available;
- distinguishes canonical components from evidence boards, screenshots,
  approximations, stale work, drafts, and research references;
- checks duplicate, stale, lookalike, overlap, long-text, page-chrome,
  source-map, metadata, and handoff-readiness risks;
- uses the distilled visual fidelity method as a good starting point for
  parity work, not as the only possible system;
- adapts the depth and order of investigation to the task, available evidence,
  risk, and user ask instead of following a prescribed sequence;
- returns findings, ledgers, and repair plans in repo docs or chat instead of
  dumping audit text into Figma; and
- still behaves like one coherent prompt-only Figma best-practices skill rather
  than a new workflow family or deterministic audit product.

The claim is false if the edited skill still lets a reasonable agent call
metadata-only inspection "pixel parity," treat screenshot boards as component
truth, skip source matching for app fidelity, hide blocked evidence, create huge
in-Figma report pages, or require a separate skill to perform app-fidelity audit
work.

## 0.2 In scope

Requested behavior scope:

- Upgrade only the existing `skills/figma-best-practices` package.
- Fold in all relevant durable doctrine from these planning-only source
  materials:
  - `/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md`
  - `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md`
- Distill those source materials into self-contained skill references. The
  shipped skill must not require, cite, or route agents to those source docs at
  runtime.
- Strip planning provenance while distilling. The skill should not mention this
  plan, this discussion, the source documents, the case-study project, or the
  fact that the doctrine was ported from anywhere.
- Make "actual auditing" explicit, not just abstract best-practice advice.
- Cover single-target audits, broad app/file sweeps, cleanup passes,
  source-backed parity checks, Figma authoring advice, and underspecified
  user asks at the prompt contract level.
- Replace rigid "workflow" framing with an adaptive set of composable tools:
  target classification, evidence ranking, source mapping, duplicate/mess
  analysis, visual-fidelity methods, report contracts, and repair planning.
- Require evidence-ranked verdicts such as `Pass`, `Partial`, `Fail`,
  `Evidence only`, `Blocked`, and `Not inspected` where the task is an audit.
- Include app/source fidelity dimensions:
  - comparison identity and environment
  - route/component/state matching
  - geometry, colors, typography, layout, tokens, assets, copy/data, states,
    interaction/motion, accessibility, platform differences, screenshot
    evidence, and app-side implementation fidelity
  - style-guide gaps and elegant component/token recommendations
  - metadata, naming, descriptions, searchability, Dev Mode, Code Connect,
    Make/MCP readiness, and handoff surfaces
  - duplicate, stale, lookalike, evidence-only, and lifecycle cleanup handling
- Preserve existing file-craft doctrine for Auto Layout, variables, components,
  pages, sections, `Index`, canvas chrome, and Figma output hygiene.

Allowed architectural convergence scope:

- Add one or more focused reference files under
  `skills/figma-best-practices/references/` when that keeps `SKILL.md` lean and
  makes the runtime package self-contained.
- Update `agents/openai.yaml` so the default prompt matches the expanded
  audit/fidelity lane.
- Leave `README.md` unchanged because the skill inventory, install behavior,
  and public skill routing remain the same.
- Add a status note to
  `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` only as a
  source/requirements doc; it must not become a runtime dependency.

Adjacent surfaces included now:

- `skills/figma-best-practices/SKILL.md`
- `skills/figma-best-practices/references/figma-file-craft.md`
- `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md`
- `skills/figma-best-practices/references/figma-source-backed-parity.md`
- any new focused reference needed for app-fidelity audit doctrine
- `skills/figma-best-practices/agents/openai.yaml`

Compatibility posture:

- Preserve the existing skill name, install surface, prompt-only stance, and
  broad trigger lane.
- Cleanly expand behavior inside the existing package. No bridge, alias skill,
  split skill, or parallel runtime skill is allowed.

## 0.3 Out of scope

- Creating `skills/figma-app-fidelity-audit/` or any other new skill.
- Adding deterministic scripts, MCP wrappers, screenshot diff runners, visual
  comparison harnesses, OCR systems, fuzzy matchers, or controllers to the
  shipped skill.
- Changing install behavior, Makefile behavior, or runtime skill discovery
  unless later evidence proves the existing package shape cannot support the
  request.
- Performing a new audit of the case-study Figma file as part of this plan
  creation. The local method doc and requirement catalog are planning inputs;
  this plan is for upgrading a reusable generic skill.
- Editing the actual Figma file.
- Implementing app code fixes or Figma repairs discovered by future audits.
- Treating local project names, paths, commands, artifact layouts, or screenshot
  examples as runtime doctrine. The reusable skill must stand without that repo.

## 0.4 Definition of done (acceptance evidence)

The upgrade is done when:

- `SKILL.md` still validates as a lean prompt-only entrypoint with a description
  under the runtime cap and clear `author`, `review`, and `repair` behavior.
- The skill's reference-selection rails make it obvious when to load file
  craft, MCP/tool-mediated work, source-backed parity, and app-fidelity audit
  references without forcing a universal sequence.
- Detailed audit categories from the requirements catalog are available in
  references without bloating `SKILL.md`.
- The case-study visual fidelity method is represented as a reusable generic
  methodology: source-pair manifest, fast structural scans, exact asset/source
  checks, deterministic app screenshot capture, normalized visual diff, and
  source/component audit.
- The upgraded skill teaches actual audit outputs: findings, compliance
  checklist, coverage ledger, app-fidelity match ledger, authorship ledger,
  style-guide gap ledger, duplicate/stale artifact ledger, verification
  receipts, and repair plan.
- The skill preserves Figma cleanliness rules: no huge audit/report/source-map
  text blobs in Figma, with `Index` as the only permitted text-heavy file-native
  organization page.
- The package is self-contained: it does not need the source method doc,
  requirements catalog, this plan, or any local repo doc at runtime.
- The runtime prose has no authoring notes, change rationale, planning
  backstory, case-study provenance, or conversation-specific language. It reads
  as enduring Figma guidance that simply exists.
- Verification has run:
  - `npx skills check`
  - readback of edited skill files
  - `rg` verification for referenced files, names, and key routing terms
  - `git diff --check` or equivalent whitespace check for edited tracked files

Behavior-preservation evidence:

- Existing file-craft use cases remain valid: a user asking for Figma
  organization, variables, components, Dev Mode readiness, Code Connect
  readiness, canvas hygiene, or MCP gotchas still gets the same or better
  guidance.
- Existing app/source parity guidance is not weakened; it is reorganized and
  expanded.
- The new audit guidance does not overtrigger for generic visual taste critique
  or implementation-from-Figma coding work.
- The new audit guidance does not undertrigger because the user supplied an
  imperfect input. It accepts messy, incomplete, informal, or indirect Figma
  requests and makes the evidence boundary explicit.

## 0.5 Key invariants (fix immediately if violated)

- One skill only: `figma-best-practices`.
- Prompt-first: no scripts or harnesses in this upgrade.
- Progressive disclosure: `SKILL.md` stays lean; references carry depth.
- Adaptive composition: the skill provides tools and rails, not a mandatory
  workflow.
- Self-contained runtime: no shipped instruction should say "go read the
  planning docs," "see the case-study pack," or rely on any local source path
  that is not part of the installed skill package.
- Timeless runtime voice: no shipped instruction should narrate authorship,
  provenance, local history, or "we added this because..." rationale.
- Source-backed truth beats visual resemblance.
- No pixel-parity claim without visual receipts or an explicit blocked status.
- No source-parity claim without app/source mapping or an explicit
  evidence-only scope.
- Figma is not the report surface; long audit artifacts belong outside Figma.
- Exactness boundaries must be explicit: canonical, evidence, approximate,
  stale, blocked, not inspected, or out of scope.
- Duplicate/lookalike findings must distinguish legitimate variants, wrappers,
  instances, aliases, and evidence boards from actual cleanup candidates.
- The skill must teach judgment and evidence ranking, not finite keyword rules
  or brittle lookup tables.
- The skill must preserve agent intelligence. It should constrain bad claims
  and messy Figma output, not reduce every task to a deterministic prompt
  script.
- `fallback_policy` remains `forbidden`; there is no approved shim or parallel
  skill path.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Self-contained runtime usefulness: the installed skill must carry enough
   doctrine to perform the audit without hidden local docs.
2. Prompt quality: the prose must teach evidence, judgment, stop rules, and
   output contracts instead of brittle heuristics or rigid task recipes.
3. Scope integrity: app-fidelity auditing becomes part of
   `figma-best-practices`, not a new skill.
4. Progressive disclosure: keep the entrypoint small enough to load routinely.
5. Real audit utility: the skill must produce grounded findings and repair
   plans, not only file-craft advice.
6. Preservation: existing Figma file-craft guidance must remain strong.

## 1.2 Constraints

- The user explicitly requested no new skill.
- The package is prompt-only today and should stay prompt-only.
- Shipped skill doctrine must be self-contained; it cannot require runtime
  access to source docs, project packs, this plan doc, hidden local context, or
  external prompt packs.
- Shipped skill doctrine must be free of authoring notes and discussion
  residue. It should present stable guidance, not the story of how the guidance
  was created.
- `npx skills check` is required after skill package edits.
- If only docs outside `skills/` change in a future pass, do not imply skill
  package verification ran.
- External Figma capabilities and docs may change; later research should verify
  current official Figma documentation before relying on unstable limits or
  feature availability.

## 1.3 Architectural principles (rules we will enforce)

- Package ownership by layer:
  - `SKILL.md`: trigger contract, boundaries, reference-selection rails, and
    output expectations.
  - `references/`: deep audit doctrine, check catalogs, evidence/report
    contracts, and examples.
  - no `scripts/`: deterministic execution is out of scope for this upgrade.
- Evidence posture:
  - classify artifact role before making strong claims;
  - map source truth before claiming source parity;
  - inspect app/source/screenshot evidence before claiming app fidelity;
  - use the cheapest reliable evidence first when the task permits it;
  - skip or reorder tools when the user's request, available evidence, or
    urgency calls for it, but name the resulting confidence boundary.
- Audit outputs must be findings-first and evidence-linked.
- Any "actual audit" mode must surface blockers explicitly rather than making
  invented passes.

## 1.4 Known tradeoffs (explicit)

- Folding the future-skill requirements into the existing skill increases
  scope, so the package must lean on references to avoid an oversized
  `SKILL.md`.
- A reusable audit catalog is necessarily long. The plan should organize it as
  a tool library, category catalog, and output contract, not as always-on
  entrypoint prose or a mandatory step list.
- Pixel-diff methodology can be described, but executable diff tooling should
  remain repo-local or user-invoked unless future repeated failures justify a
  script.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

`skills/figma-best-practices` currently owns Figma file craft, including
layout, component architecture, variables/styles, file organization, MCP
gotchas, source-backed parity, canvas hygiene, and Index-page rules.

The source materials now contain much deeper audit methodology than the
installed runtime surface:

- the local case-study visual fidelity method proves a layered evidence method
  against a real Figma file and app repo, but must be generalized before it
  reaches the shipped skill;
- the app-fidelity requirements doc enumerates the full audit surface for
  app-vs-Figma fidelity, metadata, duplicates, handoff, state coverage, and
  report shape.

## 2.2 What’s broken / missing (concrete)

- The strongest audit method and category catalog are still not fully folded
  into the installed skill.
- The current skill can still be read as mostly Figma structure/file-craft
  guidance, with source-backed parity as a smaller adjunct.
- The future-skill requirements doc still frames the behavior as a separate
  proposed skill, which conflicts with the current user decision to keep the
  capability inside `figma-best-practices`.
- The skill needs a clearer actual-audit toolkit: target classification, app
  match discovery, source truth, visual evidence, duplicate/stale detection,
  verdict rules, ledgers, and repair planning.

## 2.3 Constraints implied by the problem

- The upgrade must generalize the local case-study method without making that
  project, its paths, or its artifacts part of the runtime skill identity.
- The audit catalog must be comprehensive enough for exhaustive sweeps but
  structured so ordinary single-target audits, vague cleanup requests, and
  partial-evidence investigations can still run naturally.
- The skill must remain distinct from Figma implementation workflows and generic
  visual critique.

# 3) Research Grounding (external + internal “ground truth”)

## 3.1 External anchors (papers, systems, prior art)

Current official Figma documentation checked during planning:

- [Structure your Figma file for better code](https://developers.figma.com/docs/figma-mcp-server/structure-figma-file/):
  supports the durable file-craft lane: components, Code Connect, variables as
  tokens, semantic layer/component names, Auto Layout, and Dev Resources.
- [Guide to the Figma MCP server](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server):
  confirms that MCP can write to canvas, extract variables/components/layout
  data, reuse Code Connect context, and that skills package reusable guidance
  without adding new MCP capabilities.
- [Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect):
  confirms that Code Connect links design components to real code, can use UI
  or CLI mappings, feeds MCP context, and should be reviewed for accurate
  production representation.
- [Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout):
  supports responsive/adaptive structure through Auto Layout, wrap, gap,
  padding, resizing, min/max dimensions, grid flow, and Ignore Auto Layout.
- [Explore component properties](https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties):
  supports modeling component change surfaces through consolidated component
  properties, including visibility, instance swap, text, and variant
  properties.
- [Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables):
  supports variables as reusable values and modes as context-specific values,
  with DTCG import considerations.
- [Organize your canvas with sections](https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections)
  and [Guide to Dev Mode](https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode):
  support sections, Ready for dev, Dev Mode navigation, Dev Mode annotations,
  measurements, assets, and handoff status.

External anchors are planning/research inputs only. The shipped skill may
encode stable guidance learned from them, but it must not require runtime access
to those docs or tell agents to leave the skill package to understand the task.

## 3.2 Internal ground truth (code as spec)

Inspected anchors:

- `skills/figma-best-practices/SKILL.md`
- `skills/figma-best-practices/references/figma-file-craft.md`
- `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md`
- `skills/figma-best-practices/references/figma-source-backed-parity.md`
- `skills/figma-best-practices/agents/openai.yaml`
- `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md`
- `/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md`

The two docs are source-provenance for this plan. They are not runtime
dependencies and should not be cited from the final skill as required reading.

## 3.3 Decision gaps that must be resolved before implementation

No user decision gap is known at `new` time. The user has already resolved the
largest scope question: do not create a new skill; upgrade the existing
`figma-best-practices` skill.

Repo-evidence decisions from this pass:

- Reference split: add `figma-audit-toolkit.md` and
  `figma-visual-fidelity.md`; keep the three existing references focused on
  their current jobs.
- `agents/openai.yaml`: update so the default prompt represents the
  app/source fidelity lane after `SKILL.md` changes.
- Requirements source doc: add a docs-only status note after implementation so
  the future-skill framing does not mislead future planning.
- README: expected no change because the skill name, install surface, and
  inventory row do not change.

## 3.4 Porting inventory from source materials

This inventory is for plan traceability only. It links to the source sections
that must be distilled, but the final shipped skill must not depend on these
links. Anything carried forward must be rewritten into
`skills/figma-best-practices/SKILL.md` or
`skills/figma-best-practices/references/**` as generic, self-contained
doctrine.

Porting rules:

- Port the reusable principle, not the local project identity.
- Convert project-specific commands, paths, filenames, measurements, and
  screenshots into generic guidance or omit them.
- Convert source sections named "workflow" or "algorithm" into flexible tools,
  lenses, evidence ladders, and output contracts.
- Preserve source links in this plan only so implementation can verify coverage.
- Do not port source-provenance language, authoring commentary, planning
  rationale, or conversation-specific phrasing into the skill.

Source method pack:

- [Figma Visual Fidelity Audit Method](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#figma-visual-fidelity-audit-method): port the core warning that no single signal proves fidelity; compare source, screenshots, Figma structure, runtime renders, and human review by evidence strength.
- [What This Pass Tested](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#what-this-pass-tested): port only the lessons: screenshot boards are evidence, not canonical component truth; exact asset checks can prove imported evidence identity; duplicate-report pages in Figma are unacceptable.
- [The Audit Stack](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#the-audit-stack): port as a menu of evidence tools ordered by usual cost, not as a mandatory sequence.
- [Source-Pair Manifest](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#source-pair-manifest): port the requirement that each visual parity claim names the Figma target, runtime target, source assets, comparison mode, viewport, and ignored regions outside Figma.
- [Duplicate And Mess Checks](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#duplicate-and-mess-checks): port duplicate/mess scan categories, severity rubric, and the rule that legitimate variants/instances/repeats are review items, not automatic defects.
- [Exact Asset And Evidence Checks](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#exact-asset-and-evidence-checks): port exact evidence checks for screenshot boards, asset pages, app-owned bitmaps, icon masks, and generated images, with dimensions/byte/checksum receipts when available.
- [App Screenshot Capture](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#app-screenshot-capture): port deterministic capture requirements generically: same platform/viewport, known route/state, seeded data, hidden debug chrome, settled animation, and manifest/snapshot proof.
- [Visual Diff](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#visual-diff): port exact-byte, perceptual, and normalized pixel/patch comparison modes plus crop, scale, color-space, alpha, ignored-region, and output expectations.
- [Component-To-Figma Audit](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#component-to-figma-audit): port source/component audit causes: app render path, Figma component/frame, artifact role, tokens, assets, layout contracts, typography, and duplicate local drawings.
- [Figma Output Rule](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#figma-output-rule): port the allowed/not-allowed Figma output split, especially that full reports, duplicate indexes, raw source maps, acceptance matrices, and worklogs belong outside Figma.
- [Recommended Starting System](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#recommended-starting-system): port as a suggested baseline for visual fidelity work, explicitly non-exclusive and adjustable by task.
- [Acceptance Checks](/Users/aelaguiz/workspace/psmobile/docs/PACKS/figma_visual_fidelity_audit_method_2026-04/README.md#acceptance-checks): port completion evidence for parity claims: node/source paths, manifest rows, route/state proof, exact image receipts, diff parameters, duplicate classification, clean Figma chrome, and Index links when conventions changed.

App-fidelity requirements catalog:

- [Goal](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#goal): port the goal as part of the existing Figma skill, not a new skill.
- [Source Research](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#source-research): port stable conclusions into self-contained doctrine; do not require runtime reading of official or local docs.
- [Core Principles](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#core-principles): port principles on source-backed truth, artifact classification, evidence ranking, clean Figma output, duplicate awareness, and explicit blockers.
- [App Fidelity Match Surface](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#app-fidelity-match-surface): port the match-surface concept as a category catalog, not a mandatory checklist for every task.
- [Comparison Identity And Runtime Environment](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#1-comparison-identity-and-runtime-environment): port identity fields for app, platform, viewport, route, state, build, locale, theme, and capture context.
- [Screen, Route, And Flow Coverage](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#2-screen-route-and-flow-coverage): port route/screen/state coverage checks and explicit exception handling.
- [Spatial Geometry And Pixel Metrics](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#3-spatial-geometry-and-pixel-metrics): port geometry, size, spacing, position, crop, safe-area, and pixel-metric considerations.
- [Color, Fill, Stroke, Gradient, And Opacity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#4-color-fill-stroke-gradient-and-opacity): port color, fill, stroke, gradient, opacity, state color, and token/source comparison checks.
- [Typography And Text Rendering](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#5-typography-and-text-rendering): port font family, size, weight, line height, casing, wrapping, truncation, platform rendering, and text-style checks.
- [Style Guide And Token-System Adherence](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#6-style-guide-and-token-system-adherence): port Figma variable/style and app token parity, one-off value detection, and promotion/deprecation guidance.
- [Component Identity, Reuse, And Elegant Component Creation](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#7-component-identity-reuse-and-elegant-component-creation): port component ownership, reuse, variant/property coverage, wrappers, forks, and elegant missing-component recommendations.
- [Figma Project Placement And Lifecycle Organization](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#8-figma-project-placement-and-lifecycle-organization): port page/section placement, lifecycle states, Index ownership, archive/stale labeling, and no-report-in-Figma rules.
- [Visual Rendering Details Beyond Simple Pixels](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#9-visual-rendering-details-beyond-simple-pixels): port shadows, blur, effects, alpha, clipping, masking, border/radius, images, and rendering nuance checks.
- [Copy, Data, And Content Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#10-copy-data-and-content-fidelity): port copy, data fixture, content length, localization, dynamic value, and placeholder checks.
- [State, Variant, And Edge-Case Completeness](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#11-state-variant-and-edge-case-completeness): port state/variant coverage across loading, empty, error, disabled, selected, entitlement, edge content, and platform states.
- [Interaction, Gesture, Motion, And Feedback](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#12-interaction-gesture-motion-and-feedback): port interaction, gesture, motion timing, feedback, press/hover/focus, and prototype-vs-runtime checks.
- [Accessibility, Semantics, And Usability Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#13-accessibility-semantics-and-usability-fidelity): port contrast, hit targets, labels, focus order, semantics, usability, and accessibility exception checks.
- [Platform And Native-System Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#14-platform-and-native-system-fidelity): port native chrome, safe area, platform widgets, density, status/navigation bars, and OS-specific behavior checks.
- [App Source, Token Source, And Runtime Component Use](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#15-app-source-token-source-and-runtime-component-use): port app source ownership, token source, runtime component usage, primitive bypass detection, and source-map validation.
- [Screenshot, Golden, And Visual-Baseline Evidence](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#16-screenshot-golden-and-visual-baseline-evidence): port screenshot/golden/baseline evidence handling and limits.
- [Mess And Drift Detection](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#17-mess-and-drift-detection): port Figma/app/source drift categories and cleanup signals.
- [Style-Guide Gap And Component-Creation Recommendations](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#18-style-guide-gap-and-component-creation-recommendations): port recommendations for missing tokens/components/styles and where they should live.
- [Verdict Rules For App Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#19-verdict-rules-for-app-fidelity): port verdict vocabulary and evidence thresholds.
- [Inputs The Skill Must Accept](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#inputs-the-skill-must-accept): port as permissive intake posture, not acceptable-input gating; accept partial, vague, messy, or indirect user-provided material.
- [Outputs The Skill Must Produce](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#outputs-the-skill-must-produce): port output families as optional contracts by task depth: findings, ledgers, coverage, match surfaces, duplicate/stale records, verification receipts, and repair plans.
- [Severity Model](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#severity-model): port P0/P1/P2/P3/Info severity semantics.
- [Audit Workflow Requirements](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#audit-workflow-requirements): port the contents as an audit capability catalog, not as a prescribed workflow.
- [Resolve And Classify The Figma Target](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#1-resolve-and-classify-the-figma-target): port URL/node parsing, target type classification, artifact role, parent/page context, and broad-target handling.
- [Build The Candidate App Match Set](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#2-build-the-candidate-app-match-set): port independent candidate discovery signals and ambiguity reporting.
- [Establish The Source Of Truth](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#3-establish-the-source-of-truth): port source-of-truth hierarchy and explicit uncertainty handling.
- [Pixel And Visual Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#4-pixel-and-visual-fidelity): port visual comparison dimensions, limits, blockers, and no-false-pass rules.
- [Layout Structure](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#5-layout-structure): port layout structure, Auto Layout/source layout, constraints, spacing, and responsive behavior checks.
- [Componentization And Reuse](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#6-componentization-and-reuse): port reuse, component hierarchy, variant/property mapping, and duplicate primitive detection.
- [Token, Variable, Style, And Source Syntax Parity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#7-token-variable-style-and-source-syntax-parity): port token-variable-style-source parity checks.
- [Typography And Text Rendering](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#8-typography-and-text-rendering): port deeper typography rendering and source/text-style comparisons.
- [Asset And Icon Parity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#9-asset-and-icon-parity): port bitmap/vector/icon/source asset parity and alpha/mask handling.
- [State Coverage](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#10-state-coverage): port state and variant coverage ledgers.
- [Platform, Viewport, Safe Area, And Responsiveness](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#11-platform-viewport-safe-area-and-responsiveness): port platform/viewport/safe-area/responsiveness coverage.
- [Interaction, Prototype, Motion, And Timing](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#12-interaction-prototype-motion-and-timing): port prototype-runtime interaction and timing checks.
- [Accessibility And Inclusive Design](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#13-accessibility-and-inclusive-design): port inclusive design and accessibility audit dimensions.
- [Metadata, Naming, Searchability, And Organization](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#14-metadata-naming-searchability-and-organization): port metadata, names, aliases, descriptions, Index, searchability, page backgrounds, and organization rules.
- [Duplicate, Stale, And Lookalike Detection](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#15-duplicate-stale-and-lookalike-detection): port duplicate/stale/lookalike methodology with legitimacy classes and non-automatic-deletion posture.
- [Dev Mode, Ready For Dev, Code Connect, And Handoff](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#16-dev-mode-ready-for-dev-code-connect-and-handoff): port Dev Mode, ready-for-dev, Code Connect, source links, component descriptions, and handoff readiness.
- [Screenshot Reference Handling](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#17-screenshot-reference-handling): port screenshot boards as evidence/reference, exact source checks, and no screenshot-as-canonical-component rule.
- [App-Side Implementation Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#18-app-side-implementation-fidelity): port app-side drift checks where app code bypasses intended primitives, tokens, routes, states, or assets.
- [Exhaustive App Sweep Mode](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#19-exhaustive-app-sweep-mode): port as an available deep-audit surface, not default behavior.
- [Recommended Starting Methodology For Fidelity Audits](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#recommended-starting-methodology-for-fidelity-audits): port as a baseline method for fidelity work, explicitly not the only valid path.
- [Method Spike Findings From Poker Skill](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#method-spike-findings-from-poker-skill): port only generic lessons; omit product names, local counts, local paths, and project-specific artifacts from runtime doctrine.
- [Evidence Ranking](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#evidence-ranking): port evidence tiers and verdict implications.
- [Target Classification Algorithm](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#target-classification-algorithm): port as target-classification guidance, not a rigid algorithm.
- [Candidate App Matching Algorithm](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#candidate-app-matching-algorithm): port as candidate-discovery and evidence-corroboration guidance, not exact scoring code.
- [Duplicate Detection Methodology](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#duplicate-detection-methodology): port exact-identity, normalized-name, structure-signature, app-duplicate, classification, and finding-field guidance.
- [Screenshot And Pixel-Fidelity Methodology](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#screenshot-and-pixel-fidelity-methodology): port screenshot handling, comparison ladder, pixel-diff fields, and project-specific paths only as omitted provenance.
- [App Component To Figma Component Methodology](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#app-component-to-figma-component-methodology): port bidirectional Figma-to-app and app-to-Figma mapping, component/source/state/token comparisons, and platform-specific examples only as generic patterns.
- [Fast Path Versus Deep Path](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#fast-path-versus-deep-path): port escalation logic as adaptive depth selection, not mandatory fast/deep modes.
- [Practical Tooling Shape](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#practical-tooling-shape): port tool categories as optional future helper ideas only; do not add scripts in this upgrade.
- [Minimum Report Fields For This Method](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#minimum-report-fields-for-this-method): port report/finding fields for evidence-ranked output.
- [Required Tooling Behavior](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#required-tooling-behavior): port tool-use principles generically: readback, bounded output, blocker reporting, no blind trust, and no Figma mutation during audits unless asked.
- [Acceptance Checklist For A Single-Item Audit](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#acceptance-checklist-for-a-single-item-audit): port as completion evidence for focused audits.
- [Acceptance Checklist For Exhaustive App Sweep](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#acceptance-checklist-for-exhaustive-app-sweep): port as completion evidence for broad sweeps.
- [Report Template](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#report-template): port the report shape as an output contract outside Figma, not as in-canvas documentation.
- [Figma App Fidelity - Target Name](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#figma-app-fidelity-audit---target-name): port the title pattern generically, but do not create a separate skill identity.
- [Verdict](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#verdict): port verdict block fields.
- [Findings](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#findings): port findings-first structure.
- [Compliance Checklist](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#compliance-checklist): port applicable-category status table.
- [Visual Fidelity](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#visual-fidelity): port visual evidence summary fields.
- [App Fidelity Match Surface](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#app-fidelity-match-surface-1): port match-surface report rows.
- [Source Mapping](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#source-mapping): port source-map report fields.
- [Authorship Quality](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#authorship-quality): port naming, descriptions, searchability, and maintainability reporting.
- [Style Guide And Component Gaps](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#style-guide-and-component-gaps): port style-guide and component-gap reporting.
- [Coverage](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#coverage): port coverage matrix reporting.
- [Duplicate And Stale Artifacts](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#duplicate-and-stale-artifacts): port duplicate/stale report rows.
- [Repair Plan](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#repair-plan): port repair-plan categories.
- [Verification Receipts](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#verification-receipts): port verification receipt fields.
- [Future Skill Package Shape](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#future-skill-package-shape): do not port the new-skill package boundary; extract only reusable reference-organization ideas for the existing skill.
- [Open Decisions Before Creating The Skill](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#open-decisions-before-creating-the-skill): close or rewrite these as existing-skill implementation decisions.
- [Bottom Line](FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md#bottom-line): port the final intent only after removing new-skill framing and local-project assumptions.

<!-- arch_skill:block:research_grounding:start -->
## 3.5 Research Grounding Ledger

## External anchors (papers, systems, prior art)

- [Structure your Figma file for better code](https://developers.figma.com/docs/figma-mcp-server/structure-figma-file/)
  — adopt: components, Code Connect, variables-as-tokens, semantic names,
  Auto Layout, and Dev Resources are durable file-craft anchors for
  downstream AI/code consumers.
- [Guide to the Figma MCP server](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
  — adopt: skills package reusable guidance for MCP-backed Figma work but do
  not add MCP capabilities themselves.
- [Code Connect](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)
  — adopt: code/design mappings should represent actual production components
  and can feed MCP/Dev Mode context; availability must still be treated as
  plan/seat/tool dependent during real audits.
- [Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout)
  — adopt: Auto Layout, wrap, gap, padding, min/max dimensions, grid flow, and
  Ignore Auto Layout are core resilient-structure concepts.
- [Explore component properties](https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties)
  — adopt: component properties are the native Figma surface for communicating
  what can change in a component.
- [Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables)
  — adopt: variables and modes are the native reusable-value/context mechanism;
  DTCG import behavior matters for token parity.
- [Organize your canvas with sections](https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections)
  and [Guide to Dev Mode](https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode)
  — adopt: sections, Ready for dev, annotations, measurements, assets, and
  handoff status are real Figma/Dev Mode surfaces to account for.

External anchors are planning inputs. Runtime doctrine must be self-contained
inside `skills/figma-best-practices/**`.

## Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `skills/figma-best-practices/SKILL.md` — current prompt-only skill
    contract, trigger boundaries, non-negotiables, reference map, and output
    expectations.
  - `skills/figma-best-practices/references/figma-file-craft.md` — durable
    Figma file-craft doctrine for layout, components, variables, library
    operations, file organization, `Index`, Dev Mode, Code Connect, AI/MCP
    readiness, and anti-patterns.
  - `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md` —
    tool-mediated Figma inspection/write/readback discipline, including
    bounds, screenshots, images, source truth, and no long reports in Figma.
  - `skills/figma-best-practices/references/figma-source-backed-parity.md` —
    current source-truth and concise visual-fidelity guidance.
  - `skills/figma-best-practices/agents/openai.yaml` — current runtime
    metadata/default prompt for implicit invocation.
- Canonical path / owner to reuse:
  - `skills/figma-best-practices/` — the existing skill package owns this
    upgrade. Do not create a sibling app-fidelity skill.
- Adjacent surfaces tied to the same contract family:
  - `skills/figma-best-practices/agents/openai.yaml` — must stay aligned if
    `SKILL.md` expands the trigger/default prompt.
  - `README.md` — expected no change because skill name and install inventory
    do not change.
  - `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` —
    planning source only; add a status note after implementation so the
    future-skill framing does not remain misleading.
- Compatibility posture (separate from `fallback_policy`):
  - Preserve existing skill name, install surface, and broad Figma file-craft
    behavior. Expand the existing contract with self-contained references.
    There is no bridge, alias skill, fallback, or parallel runtime path.
- Existing patterns to reuse:
  - `SKILL.md` as lean entrypoint plus `references/**` for depth.
  - Prompt-only skill packaging with no scripts. This plan keeps scripts out
    of scope.
  - Existing file-craft `Index` and documentation placement doctrine.
- Prompt surfaces / agent contract to reuse:
  - `SKILL.md` non-negotiables and reference map.
  - `figma-file-craft.md`, `figma-mcp-agent-gotchas.md`, and
    `figma-source-backed-parity.md` as owned runtime context.
  - `agents/openai.yaml` default prompt as the implicit-invocation surface.
- Native model or agent capabilities to lean on:
  - Codex/agent reasoning over prompt references, repo files, Figma artifacts,
    screenshots, and tool outputs. The skill should constrain false claims and
    messy output, not reduce agents to brittle prompt runners.
- Existing grounding / tool / file exposure:
  - Local repo file reads and `rg` for package inspection.
  - Official Figma docs used as planning inputs only.
  - Local method and requirements docs used as planning inputs only.
- Duplicate or drifting paths relevant to this change:
  - The requirements doc still frames the capability as a future separate
    skill; implementation must fold durable doctrine into the existing skill
    and optionally mark the doc as source material.
  - `figma-source-backed-parity.md` is too compressed to own all app-fidelity,
    duplicate, verdict, report, and visual comparison doctrine alone.
  - Current `SKILL.md` `First move` and `Workflow` sections risk reading as a
    fixed sequence; implementation should reframe them as adaptive reference
    selection and working posture.
- Capability-first opportunities before new tooling:
  - Prompt/reference structure is the real lever. Add `figma-audit-toolkit.md`
    and `figma-visual-fidelity.md` before considering any deterministic
    helper.
  - Preserve native agent judgment: teach evidence levels, output contracts,
    blocked states, and Figma cleanliness rules rather than formal input gates.
- Behavior-preservation signals already available:
  - `rtk proxy npx skills check` after skill package edits.
  - Readback of every edited runtime skill file.
  - `rtk git diff --check -- <edited files>`.
  - Targeted `rg` checks for owned reference names and obvious local identity
    leaks in `skills/figma-best-practices`.

## Decision gaps that must be resolved before implementation

- None. North Star is confirmed, the canonical owner path is
  `skills/figma-best-practices/`, compatibility posture is preservation of the
  existing skill contract, and the reference split is chosen.
<!-- arch_skill:block:research_grounding:end -->

# 4) Current Architecture (as-is)

<!-- arch_skill:block:current_architecture:start -->
## 4.1 On-disk structure

Observed structure:

- `skills/figma-best-practices/SKILL.md`
- `skills/figma-best-practices/agents/openai.yaml`
- `skills/figma-best-practices/references/figma-file-craft.md`
- `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md`
- `skills/figma-best-practices/references/figma-source-backed-parity.md`

Observed sizes:

- `SKILL.md`: 155 lines.
- `figma-file-craft.md`: 1061 lines.
- `figma-mcp-agent-gotchas.md`: 427 lines.
- `figma-source-backed-parity.md`: 188 lines.
- `agents/openai.yaml`: 7 lines.

Current package shape is already prompt-only and reference-backed. The new
audit surface is too broad to put into `SKILL.md`, and too broad to fold
entirely into the current 188-line parity reference without making it a mixed
source-truth, visual-diff, duplicate, report-contract, and app-fidelity catalog.

## 4.2 Control paths (runtime)

Observed runtime posture:

- The skill trigger loads `SKILL.md`.
- The agent selects file-craft, MCP gotcha, or source-backed parity guidance
  based on the user's actual request and the evidence available; this is
  reference selection inside one skill, not a formal workflow engine.
- Output expectations distinguish `author`, `review`, and `repair` work without
  making those labels a rigid interface.
- There is no separate control path for exhaustive app/source fidelity audits,
  duplicate/stale review, visual evidence grading, or clean report placement;
  agents must infer those from compressed parity guidance and general file-craft
  rules today.

## 4.3 Object model + key abstractions

Current abstractions:

- Figma artifact types: file, page, section, frame, component set, component,
  instance, evidence board, screenshot board, asset reference, source map,
  sandbox, archive.
- Skill modes: `author`, `review`, `repair`; this plan will add explicit audit
  capabilities inside `review` without adding a runtime mode selector.
- File-craft habits: variables, Auto Layout, components, sections, semantic
  names, code-aligned component properties.
- Runtime proof channels: node IDs, structure reads, fill reads, bounds checks,
  screenshots, code/tokens/assets/product-decision anchors.
- Existing parity concepts: source truth, visual fidelity audits,
  source-pair manifest, canonical/evidence/approximate/stale status, component
  repair, text/props/variants, assets/images, runtime behavior, alpha binding,
  cleanup scans, and acceptance questions.

## 4.4 Observability + failure behavior today

Observed failure behavior:

- The skill already tells agents not to trust tool success without readback.
- The skill needs stronger blocked/insufficient-evidence behavior for app
  fidelity claims.
- The current `First move` and `Workflow` headings are useful, but the upgrade
  should rename or reframe them so agents do not treat the skill as a fixed
  prompt runner.
- The current default prompt and description understate actual app/source
  fidelity auditing compared with the requested upgraded lane.

## 4.5 UI surfaces (ASCII mockups, if UI work)

Not applicable. This is a prompt-first skill package upgrade, not product UI.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture (to-be)

<!-- arch_skill:block:target_architecture:start -->
## 5.1 On-disk structure (future)

Expected shape:

- Keep `skills/figma-best-practices/SKILL.md` as the lean entrypoint.
- Keep `figma-file-craft.md` as the durable file-craft reference.
- Keep `figma-mcp-agent-gotchas.md` as the tool-mediated Figma work reference.
- Keep `figma-source-backed-parity.md` as the source-truth discipline reference;
  expand it only where source ownership and canonical status belong.
- Add `references/figma-audit-toolkit.md` for artifact-role classification,
  permissive intake, evidence tiers, verdicts, severity, app-fidelity match
  surfaces, duplicate/stale/mess analysis, output contracts, and report
  placement.
- Add `references/figma-visual-fidelity.md` for source-pair manifests,
  screenshot/reference handling, exact asset/evidence checks, deterministic
  app capture requirements, visual comparison ladders, normalized diff
  expectations, and component-to-source comparison guidance.
- Do not add `scripts/`, `assets/`, runner files, or a new skill package.
- Do not make any runtime reference point back to the plan, requirement doc,
  local method pack, local project paths, or source-research docs.

## 5.2 Control paths (future)

Expected runtime posture:

- The agent starts from whatever the user supplied and classifies what kind of
  Figma help is being requested without rejecting partial, vague, or mixed
  inputs up front.
- The agent loads the smallest useful owned reference set for that request;
  this remains adaptive reference selection, not a prescribed sequence.
- File-craft guidance, MCP gotchas, source-backed parity, app-fidelity audit
  categories, duplicate/mess checks, and repair planning are composable tools.
- Any claim involving app code, tokens, assets, screenshots, runtime state, or
  visual fidelity must use source-backed/app-fidelity evidence guidance.
- The agent reports evidence-ranked findings, blockers, or repair guidance in
  the shape the task actually calls for.

Reference ownership by file:

| File | Owns |
|---|---|
| `SKILL.md` | Mission, boundaries, invocation posture, reference selection, and output expectations. |
| `figma-file-craft.md` | Figma cleanliness, page organization, components, variables/tokens, Dev Mode readiness, Code Connect readiness, and Figma-native documentation placement. |
| `figma-mcp-agent-gotchas.md` | Tool-mediated inspection, write, screenshot, image, readback, and blocked-state discipline. |
| `figma-source-backed-parity.md` | Source-truth discipline, canonical status, and source-backed pass/fail semantics. |
| `figma-audit-toolkit.md` | Artifact-role classification, evidence levels, duplicate/stale/mess review, report contracts, severity/verdict vocabulary, and Figma-clean audit behavior. |
| `figma-visual-fidelity.md` | Source-pair manifests, screenshot/runtime capture expectations, normalized comparison ladders, and component-to-app visual parity guidance. |

## 5.3 Object model + abstractions (future)

Expected abstractions:

- Artifact role classification: canonical, evidence, approximate, stale,
  draft, research, out of scope, blocked, not inspected.
- Evidence hierarchy: source truth, Figma structure, app source, exact
  asset/source checks, deterministic runtime screenshots, normalized visual
  diffs, human review.
- Output ledgers: findings, compliance checklist, coverage ledger,
  app-fidelity match ledger, authorship ledger, style-guide gap ledger,
  duplicate/stale ledger, verification receipts, repair plan.

## 5.4 Invariants and boundaries

- No new skill.
- No runtime script dependency.
- No dependency on the local case-study project, paths, commands, or artifacts.
- No runtime dependency on this plan, source docs, official docs, or external
  prompt packs.
- Every durable runtime rule required by the upgraded skill lives in
  `skills/figma-best-practices/SKILL.md` or an owned file under
  `skills/figma-best-practices/references/**`.
- No authoring notes, planning rationale, source provenance, or discussion
  residue in `SKILL.md` or references.
- No generic "looks close" pass.
- No Figma audit-report dumping.
- No source truth without source evidence.
- No pixel parity without rendered evidence or a blocked status.

## 5.5 UI surfaces (ASCII mockups, if UI work)

Not applicable.
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site Audit (exhaustive change inventory)

<!-- arch_skill:block:call_site_audit:start -->
## 6.1 Change map (table)

Change inventory:

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
|---|---|---|---|---|---|---|---|
| Skill entrypoint | `skills/figma-best-practices/SKILL.md` | Description, non-negotiables, first move, adaptive rails, outputs, reference map | General file-craft skill with source-backed parity reference | Reframe as adaptive Figma file-craft and source-backed fidelity toolkit; remove fixed workflow feel; keep prompt-only and timeless | User wants broad Figma usefulness, actual auditing, no brittle heuristics, no new skill | Same skill name; expanded reference-selection contract | `npx skills check`, readback |
| File craft reference | `skills/figma-best-practices/references/figma-file-craft.md` | File organization, components, variables, handoff | Strong file-craft doctrine, including Index/page chrome/no report pages | Add only needed cross-links or small clarifications for audit toolkit, visual evidence, and self-contained report placement | Avoid duplicate doctrine while preserving file-craft center | Same reference, stronger links to audit/fidelity surfaces | Readback |
| MCP gotchas | `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md` | Tool-mediated Figma work | Strong operational gotchas | Align language with adaptive audit tools, blocked evidence, screenshot/evidence handling, and no report dumping | Actual audits are often tool-mediated | Same reference, no new APIs | Readback |
| Source parity reference | `skills/figma-best-practices/references/figma-source-backed-parity.md` | Entire reference | Carries source truth plus concise visual-fidelity guidance | Keep as source-truth and canonical-status discipline; point to focused audit/visual references instead of absorbing everything | Prevent one reference from becoming a giant mixed catalog | Same reference, narrower clearer role | Readback |
| Audit toolkit reference | `skills/figma-best-practices/references/figma-audit-toolkit.md` | New reference | Missing | Add self-contained audit toolkit: permissive intake, artifact roles, evidence tiers, verdict/severity, match surfaces, duplicate/stale/mess, output contracts, Figma-clean reporting | Carries the exhaustive app/file audit catalog without bloating `SKILL.md` | New prompt reference, no runtime dependency outside package | `npx skills check`, readback |
| Visual fidelity reference | `skills/figma-best-practices/references/figma-visual-fidelity.md` | New reference | Missing | Add self-contained visual/source evidence method: source-pair manifests, screenshot/reference handling, exact evidence checks, deterministic capture requirements, visual comparison ladder, component-source mapping | Carries parity methodology as a generic starting point | New prompt reference, no scripts | `npx skills check`, readback |
| Agent metadata | `skills/figma-best-practices/agents/openai.yaml` | `default_prompt`, short description | File-craft wording | Mention source-backed fidelity/audit lane concisely and trigger-safely | Metadata currently underrepresents expanded behavior | Same skill metadata | `npx skills check` |
| Runtime self-containment | `skills/figma-best-practices/**` | All edited skill prose | Existing package is self-contained, but new doctrine is still in planning/source docs | Port durable rules into owned skill files and avoid runtime links to source docs, local paths, official docs, or this plan | Skill must install and operate without external planning context | Owned references only | Readback and manual local-identity leak review |
| Requirements source doc | `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` | Future-skill framing | Describes proposed new skill | Mark as planning source folded into existing skill after implementation | Avoid stale planning truth | Docs-only note | Readback |

## 6.2 Migration notes

- Canonical owner path: `skills/figma-best-practices`.
- Shared runtime path: the existing prompt-only skill package and owned
  `references/**` files. No new command, mode, runner, or parallel skill path.
- Deprecated APIs: none.
- Compatibility posture: preserve existing skill name, invocation, install
  surface, and broad file-craft trigger lane; expand the contract with
  additional self-contained references.
- Delete list: none known. Do not add any shim, alias skill, or generated
  helper that would later require deletion.
- Adjacent surfaces: `README.md` remains unchanged because this is an existing
  skill upgrade with no install or inventory change. `agents/openai.yaml` must
  be updated because it is the implicit invocation surface. The requirements
  source doc receives a docs-only status note after implementation.
- Capability-replacing harnesses to delete or justify: none present; adding one
  is out of scope unless the plan is reopened and user-approved.
- Live docs/comments/instructions to update or delete:
  - `SKILL.md` runtime wording must be rewritten to adaptive reference
    selection and timeless voice.
  - Existing references receive concise cross-links where ownership boundaries
    require them, but no authoring notes or planning provenance.
  - The requirements source doc is not runtime truth and must not be referenced
    by the shipped skill.
- Behavior preservation signals for refactors:
  - `rtk proxy npx skills check`
  - readback of edited runtime files
  - frontmatter description length check
  - `rtk git diff --check -- <edited files>`
  - representative manual readback that file-craft, MCP, source-backed parity,
    and app-fidelity audit tasks each choose an owned reference without a fixed
    workflow.

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope |
|---|---|---|---|---|
| Skill package | `skills/figma-best-practices/SKILL.md` | Lean mission plus adaptive reference selection | Prevents `SKILL.md` from becoming a giant checklist or rigid runner | include |
| File craft reference | `skills/figma-best-practices/references/figma-file-craft.md` | Figma cleanliness, `Index`, page chrome, documentation placement ladder | Keeps new audit doctrine aligned with existing file organization truth | include |
| MCP gotchas reference | `skills/figma-best-practices/references/figma-mcp-agent-gotchas.md` | Readback, bounded evidence, no in-Figma report blobs | Prevents tool-mediated audits from claiming success on metadata or making canvas messes | include |
| Source parity reference | `skills/figma-best-practices/references/figma-source-backed-parity.md` | Source-truth discipline and canonical status | Prevents visual-fidelity expansion from weakening source-backed truth | include |
| New audit reference | `skills/figma-best-practices/references/figma-audit-toolkit.md` | Audit tools, evidence tiers, verdicts, duplicate/stale/report contracts | Gives exhaustive audit doctrine one owned runtime home | include |
| New visual reference | `skills/figma-best-practices/references/figma-visual-fidelity.md` | Source-pair manifests and visual comparison boundaries | Separates visual method from broad audit and source-truth doctrine | include |
| Agent metadata | `skills/figma-best-practices/agents/openai.yaml` | Concise expanded default prompt | Prevents implicit invocation undertriggering for source-backed audit tasks | include |
| Install inventory | `README.md` | Existing skill inventory remains valid | Skill name/install surface does not change | exclude |
| Planning source doc | `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` | Status note only | Prevents future planning from reviving a separate skill while keeping runtime self-contained | Phase 6 |
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

For this prompt-only skill package, the canonical boundary for new
patterns/gotchas is the owned runtime skill/reference prose, not app code
comments.

## Phase 1 - Lock The Runtime Shape

Status: COMPLETE.

Completed work:

- Confirmed the implementation remains one prompt-only package under
  `skills/figma-best-practices`.
- Kept README and install behavior out of scope.
- Used this plan, requirements, local method material, and official Figma docs
  only as planning inputs; runtime doctrine stays inside the skill package.

Goal:

- Establish the package boundary and adjacent-surface decisions before any
  runtime prose is written.

Work: finalize the package architecture before writing runtime prose. This
phase prevents the implementation from becoming a new skill, a project-specific
case-study skill, or a script-backed audit product.

Checklist (must all be done):

- Preserve one package: `skills/figma-best-practices`.
- Preserve prompt-only packaging: no `scripts/`, harnesses, runners, OCR,
  visual-diff implementation, MCP wrapper, launcher, or controller.
- Lock the owned runtime file set:
  - `SKILL.md`
  - `agents/openai.yaml`
  - `references/figma-file-craft.md`
  - `references/figma-mcp-agent-gotchas.md`
  - `references/figma-source-backed-parity.md`
  - `references/figma-audit-toolkit.md`
  - `references/figma-visual-fidelity.md`
- Treat this plan, the requirements doc, the local method pack, and official
  Figma docs as source inputs only; runtime guidance must be fully contained in
  the skill package.
- Keep README out of the edit set because the skill name, install target, and
  inventory surface do not change.
- Reserve the requirements-doc status note for Phase 6 after the runtime skill
  package is updated.

Verification (required proof):

- Read back Section 5 and Section 6 before editing runtime files.
- Confirm the implementation scope is still only `skills/figma-best-practices`
  plus the one planning-source note in Phase 6.

Docs/comments:

- No live documentation changes in this phase. This phase records the intended
  runtime boundary only.

Exit criteria (all required):

- The implementation target is one existing skill, not a new sibling skill.
- The runtime file set is explicit and matches Section 6.
- No phase below depends on external docs, local project paths, or hidden
  context at runtime.
- README is explicitly out of scope for this implementation plan.

Rollback:

- Revert only Phase 1 runtime-boundary edits if implementation later proves
  the chosen owner path cannot carry the work; then repair the plan instead of
  adding a sibling skill or helper script.

## Phase 2 - Add The Self-Contained Audit Toolkit Reference

Status: COMPLETE.

Completed work:

- Added `references/figma-audit-toolkit.md` as the owned runtime home for
  permissive intake, artifact roles, evidence tiers, verdicts, severity,
  target/app matching, duplicate/stale review, clean Figma reporting, audit
  write boundaries, and output contracts.
- Kept the reference generic, self-contained, and adaptive rather than a fixed
  audit sequence.
- Added the missing output-contract shapes for compliance checklist, authorship
  ledger, handoff-readiness ledger, and style-guide gap ledger.

Repaired (code):

- `references/figma-audit-toolkit.md` now defines findings, compliance
  checklist, coverage ledger, app-fidelity match ledger, authorship ledger,
  handoff-readiness ledger, style-guide gap ledger, duplicate/stale ledger,
  verification receipts, and repair plan.

Goal:

- Give broad Figma audit behavior one owned runtime home without bloating
  `SKILL.md` or prescribing a fixed audit sequence.

Work: create `references/figma-audit-toolkit.md` as the durable home for
actual audit behavior that is not specifically visual-diff mechanics. This
reference gives agents a broad set of audit tools without turning the skill
entrypoint into a giant checklist.

Checklist (must all be done):

- Write the reference in timeless runtime voice: no authoring notes, plan
  rationale, case-study provenance, local project names, local paths, or
  "ported from" language.
- Start with permissive intake: accept whatever Figma-related artifact or
  complaint the user supplies; classify what is knowable; ask only when missing
  information blocks the requested confidence level.
- Define target resolution and app/source matching guidance:
  URL and node parsing, page/parent context, broad-target handling, candidate
  app/source match-set construction, ambiguity reporting, source-of-truth
  hierarchy, and explicit uncertainty handling.
- Assign target and candidate matching to `figma-audit-toolkit.md`; assign
  source-truth hierarchy and claim semantics to
  `figma-source-backed-parity.md`, with cross-links reconciled in Phase 4.
- Define artifact-role classifications:
  - canonical
  - evidence
  - approximate
  - stale
  - draft/exploration
  - research/reference
  - out of scope
  - blocked
  - not inspected
- Define evidence tiers generically:
  - explicit bidirectional source/design link
  - component or source map
  - screenshot or capture manifest
  - semantic/runtime snapshot
  - screenshot label or visible source hint
  - visual similarity
  - name-only guess
- Define verdicts and when they are allowed:
  - `Pass`
  - `Partial`
  - `Fail`
  - `Evidence only`
  - `Blocked`
  - `Not inspected`
  - `Out of scope`
- Define severity:
  - `P0`: cannot be used as a reference or causes false implementation/parity
    claims.
  - `P1`: high-confidence app/Figma/source drift or missing critical coverage.
  - `P2`: important durability, componentization, naming, token,
    accessibility, or handoff issue.
  - `P3`: cleanup, metadata, organization, or low-risk maintainability issue.
  - `Info`: correct explicit exception or useful future improvement.
- Port the app-fidelity match surface as a category catalog, not a mandatory
  checklist:
  comparison identity, route/flow coverage, geometry, color, typography,
  tokens, component identity, file placement, visual rendering details,
  copy/data, state coverage, interaction/motion, accessibility, platform/native
  behavior, app source usage, screenshot evidence, mess/drift, style-guide
  gaps, metadata, naming, descriptions, searchability, Dev Mode, Ready for Dev,
  Code Connect, Make/MCP readiness, source links, component descriptions,
  handoff readiness, and verdict rules.
- Port duplicate/stale/lookalike methodology:
  exact identity, normalized names, structure signatures, app-side duplication,
  screenshot evidence duplication, stale artifacts, legitimate variants,
  legitimate wrappers, and unknown duplicates.
- Port Figma cleanliness rules:
  audit reports, duplicate indexes, source maps, acceptance matrices, and
  worklogs stay outside Figma; `Index` is the only text-heavy file-native page.
- Port the audit write-boundary: audits are read-heavy and no-mutation by
  default; Figma writes or repairs happen only when the user asks for authoring
  or repair work, and require readback plus visual verification.
- Port output contracts as optional task-depth shapes:
  findings, compliance checklist, coverage ledger, app-fidelity match ledger,
  authorship ledger, handoff-readiness ledger, style-guide gap ledger,
  duplicate/stale ledger, verification receipts, and repair plan.

Verification (required proof):

- Re-read `references/figma-audit-toolkit.md` after writing it.
- Confirm the file can support single-item review, broad cleanup review, and
  exhaustive audit work without requiring a predetermined step order.

Docs/comments:

- This phase creates one runtime reference. No repo docs outside the skill
  package are updated in this phase.

Exit criteria (all required):

- A reader can perform a single-item audit, broad cleanup pass, or exhaustive
  sweep from this reference without leaving the skill package.
- The reference is a tool catalog and output contract, not a fixed workflow.
- The reference contains no local project identity or source-provenance
  exposition.
- The reference makes Figma-clean reporting explicit: long reports outside
  Figma, compact native labels/descriptions inside Figma, and `Index` as the
  only text-heavy native page.
- The reference covers target resolution, candidate app/source matching,
  ambiguity reporting, source-truth handoff, metadata/handoff readiness, and
  the no-mutation audit write-boundary.

Rollback:

- Remove the new reference and its entrypoint references if it cannot remain
  self-contained; do not leave a broken runtime link.

## Phase 3 - Add The Self-Contained Visual Fidelity Reference

Status: COMPLETE.

Completed work:

- Added `references/figma-visual-fidelity.md` as the owned runtime home for
  source-pair manifests, screenshot/contact-sheet handling, fast structural
  scans, exact asset checks, deterministic capture expectations, comparison
  modes, normalization, pixel-parity boundaries, and completion evidence.
- Described the method as a starting system for fidelity work, not the only
  valid path.

Goal:

- Give screenshot, source-pair, and visual-parity methodology one owned
  runtime home while keeping it generic and capability-first.

Work: create `references/figma-visual-fidelity.md` as the durable home for
visual parity and screenshot/source-evidence methods.

Checklist (must all be done):

- Write the reference in timeless runtime voice with no source-doc or
  case-study provenance.
- Define the source-pair manifest as a repo-doc or artifact shape, never an
  in-Figma report. Include generic fields for:
  - Figma file/page/node/role
  - runtime route/component/state
  - app screenshot or render path
  - source code, token, and asset anchors
  - platform, viewport, device, theme, locale, and state
  - comparison mode
  - ignored regions and dynamic content
- Define screenshot/contact-sheet boards as evidence indexes unless explicitly
  promoted by source-backed proof.
- Define fast structural scans as cheap evidence: Figma tree, layer, bounds,
  style, component, and source-map scans; what they can prove; and where they
  stop short of visual parity or source parity.
- Define exact asset/evidence checks:
  dimensions, byte length, checksum or content hash when available, Figma image
  fill identity, local/source image identity, and the limited claim each check
  can prove.
- Define deterministic capture requirements generically:
  same platform and viewport, known route/state, seeded data, hidden debug
  chrome, settled animation, stable auth/entitlement, raw screenshot, and
  route/state proof.
- Define visual comparison modes:
  exact bytes, perceptual duplicate/similarity, structural comparison,
  normalized pixel/patch diff, and human review of failures.
- Define normalization requirements:
  crop, scale, color space, bit depth, alpha, safe areas, system chrome,
  dynamic regions, masks, ignored regions, platform differences, and viewport.
- Define pixel-parity claim boundaries:
  no pixel-perfect claim without explicit pair, render proof, dimensions,
  normalization, ignored regions, and blocker disclosure.
- Define component-to-Figma comparison:
  Figma-to-app and app-to-Figma maps, component/source path, tokens, assets,
  typography, layout contracts, states, and duplicate local drawings.
- Define completion evidence:
  node/source paths, manifest rows, route/state proof, exact evidence receipts,
  diff parameters, duplicate classification, clean Figma chrome, and `Index`
  link when file conventions changed.

Verification (required proof):

- Re-read `references/figma-visual-fidelity.md` after writing it.
- Confirm the method distinguishes screenshot resemblance, source-backed
  fidelity, rendered evidence, blocked evidence, and pixel-perfect claims.

Docs/comments:

- This phase creates one runtime reference. No repo docs outside the skill
  package are updated in this phase.

Exit criteria (all required):

- A reader can evaluate visual fidelity without pretending screenshots alone
  prove everything.
- The method is described as a good starting point that adapts by task, not the
  only way.
- No executable helper or local-project command is required by the shipped
  skill.
- Pixel-perfect claims require explicit pair identity, render proof,
  dimensions, normalization, ignored regions, and blocker disclosure.
- Fast structural scans are present as a low-cost evidence layer with clear
  limits.

Rollback:

- Remove the new reference and any links to it if it cannot stay prompt-only
  and generic; do not replace it with a visual-diff runner in this plan.

## Phase 4 - Reconcile Existing References

Status: COMPLETE.

Completed work:

- Rewrote `references/figma-source-backed-parity.md` around source-truth
  hierarchy, claim semantics, canonical status, source-backed repair, props,
  variants, assets, runtime boundaries, alpha/paint binding, cleanup scans, and
  acceptance checks.
- Updated `figma-file-craft.md` and `figma-mcp-agent-gotchas.md` with concise
  cross-links and audit/write-boundary alignment while preserving their
  existing file-craft and tool-mediated-work jobs.

Goal:

- Keep the five references coherent by assigning each reference one clear job
  and preserving existing file-craft behavior.

Work: update existing references so the new guidance has one coherent home and
does not duplicate or contradict existing file-craft doctrine.

Checklist (must all be done):

- Update `figma-source-backed-parity.md` so it owns source-truth discipline,
  canonical status, source-backed repair, source-owned props/variants, assets,
  runtime behavior boundaries, source-truth hierarchy, explicit uncertainty
  handling, alpha/paint binding, cleanup scans, and acceptance questions.
- Cross-link `figma-audit-toolkit.md` target/candidate matching guidance to
  `figma-source-backed-parity.md` source-truth and claim-semantics guidance.
- Move or summarize detailed visual-audit mechanics out of
  `figma-source-backed-parity.md` into `figma-visual-fidelity.md`.
- Add concise cross-references from `figma-source-backed-parity.md` to
  `figma-audit-toolkit.md` and `figma-visual-fidelity.md`.
- Update `figma-file-craft.md` only where needed to preserve the broader file
  craft lane: one file-wide canvas chrome standard, `Index` as native map,
  documentation placement ladder, page/section/frame separation, Dev Mode,
  Ready for Dev, Code Connect, Make/MCP readiness, source links, component
  descriptions, handoff readiness, and long audit artifacts outside Figma.
- Update `figma-mcp-agent-gotchas.md` only where needed to align tool-mediated
  work with the audit toolkit: readback, target classification, blocked
  evidence, screenshot/asset handling, bounds/overlap checks, audit
  no-mutation-by-default behavior, write/repair readback, and no giant
  in-Figma reports.
- Avoid copying the same long checklist into multiple references. Prefer one
  canonical home and short links from adjacent references.

Verification (required proof):

- Re-read every edited existing reference.
- Confirm `figma-source-backed-parity.md` remains the source-truth discipline
  reference, `figma-file-craft.md` remains the file-craft reference, and
  `figma-mcp-agent-gotchas.md` remains the tool-mediated work reference.

Docs/comments:

- Live runtime reference prose is updated here. Repo docs outside the skill
  package are not updated in this phase.

Exit criteria (all required):

- Each reference has a clear job.
- Existing file-craft, MCP, and source-backed parity behavior remains at least
  as strong as before.
- No runtime reference contains authoring notes, local project identity, or
  source-doc dependency.
- Cross-references point only to owned files inside
  `skills/figma-best-practices/references/**`.
- Dev Mode, Ready for Dev, Code Connect, Make/MCP readiness, source links,
  component descriptions, handoff readiness, source-truth hierarchy, and audit
  write-boundaries remain covered in the owned references.

Rollback:

- Revert only the conflicting reference edits and restore the previous
  reference boundaries before retrying; do not leave duplicated or
  contradictory doctrine in multiple references.

## Phase 5 - Refactor The Skill Entrypoint And Metadata

Status: COMPLETE.

Completed work:

- Refactored `SKILL.md` into a lean prompt contract covering mission, use
  cases, non-use boundaries, non-negotiables, adaptive reference selection,
  working posture, output expectations, and the expanded reference map.
- Updated `agents/openai.yaml` so implicit invocation and the default prompt
  cover the expanded source-backed fidelity and audit lane without presenting
  it as a separate skill or deterministic runner.

Goal:

- Make the installed skill route agents into the expanded references while
  staying lean, adaptive, timeless, and generic.

Work: update `SKILL.md` and `agents/openai.yaml` so the installed skill routes
agents into the new references without becoming rigid, verbose, or
case-study-specific.

Checklist (must all be done):

- Update the frontmatter description so it includes source-backed app/Figma
  fidelity and audit readiness while staying under the runtime cap and avoiding
  marketing copy.
- Preserve clear non-use boundaries:
  - not generic visual taste critique
  - not implementing frontend code from Figma
  - not operating the Figma UI/tool itself
  - not a deterministic audit runner
- Preserve the existing `author`, `review`, and `repair` behavior surfaces;
  app/source fidelity audits live inside `review`, not as a new mode selector.
- Replace fixed-sequence entrypoint language with adaptive reference-selection
  guidance.
- Keep `SKILL.md` lean:
  mission, use cases, non-negotiables, reference selection, working posture,
  output expectations, reference map.
- Add non-negotiables for:
  - permissive intake
  - no fixed workflow
  - no report dumping into Figma
  - source-backed claims requiring source evidence
  - pixel-parity claims requiring explicit visual evidence or blocked status
  - audits are read-heavy by default, with Figma writes only when the user asks
    for authoring or repair and with readback plus visual verification
  - self-contained runtime doctrine
  - timeless runtime voice
- Update the reference map to include `figma-audit-toolkit.md` and
  `figma-visual-fidelity.md`.
- Update `agents/openai.yaml` so the default prompt represents the expanded
  source-backed fidelity/audit lane without turning the skill into a separate
  audit product.

Verification (required proof):

- Re-read `SKILL.md` and `agents/openai.yaml`.
- Confirm the entrypoint points to owned references by need and does not
  require one fixed workflow, one input shape, or external source docs.

Docs/comments:

- Runtime metadata changes are made in `agents/openai.yaml`. No install docs
  are updated because the skill name and install surface stay unchanged.

Exit criteria (all required):

- `SKILL.md` is still a reusable prompt contract, not a report, checklist dump,
  plan summary, or authorship memo.
- The skill can handle messy user-provided Figma requests without an input
  gate.
- The entrypoint clearly tells agents which owned reference to load by need,
  while preserving agent judgment.
- The skill description/default prompt now covers app/source fidelity audits
  without claiming to operate Figma or run deterministic visual tooling.
- Existing `author`, `review`, and `repair` surfaces remain clear, and audit
  capability is represented inside `review`.

Rollback:

- Revert entrypoint and metadata edits together if either becomes inconsistent
  with the owned reference map; do not leave metadata pointing at missing
  references.

## Phase 6 - Sync Planning Docs Only Where Truthfully Needed

Status: COMPLETE.

Completed work:

- Added a docs-only status note to
  `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` stating that
  durable guidance was folded into the existing `figma-best-practices` skill.
- Left README unchanged because the skill name, install target, and inventory
  surface did not change.

Goal:

- Prevent non-runtime docs from contradicting the installed skill after the
  runtime package is upgraded.

Work: update the one non-runtime source doc that would otherwise keep pointing
future work toward a separate skill.

Checklist (must all be done):

- Confirm `README.md` remains unchanged because this plan preserves the skill
  name, install target, and inventory surface.
- Add a short status note to
  `docs/FIGMA_APP_FIDELITY_AUDIT_SKILL_REQUIREMENTS_2026-04-30.md` saying the
  durable content was folded into the existing `figma-best-practices` skill
  instead of becoming a new skill.
- Keep that note clearly outside runtime and do not make the skill depend on
  the requirements doc.

Verification (required proof):

- Re-read the requirements-doc status note.
- Confirm no `README.md` edit was made.

Docs/comments:

- This phase updates the planning-source requirements doc only. It does not
  update runtime skill files.

Exit criteria (all required):

- Runtime package truth and planning docs do not contradict each other.
- No non-runtime doc is needed to use the installed skill.
- README remains untouched because the install surface did not change.

Rollback:

- Remove or revise only the requirements-doc status note if implementation
  scope changes before landing.

## Phase 7 - Verify Package Integrity And Runtime Quality

Status: COMPLETE.

Completed work:

- Ran `rtk proxy npx skills check`.
- Re-read every edited runtime skill file and reference.
- Ran whitespace/diff checks and targeted `rg` readback support for reference
  routing, verdict terms, `Index`, Dev Mode, Code Connect, and local-identity
  leak review.
- Confirmed `make verify_install` and app/device tests are out of scope because
  install behavior, app code, and external audit scripts did not change.
- Re-read `references/figma-audit-toolkit.md` and `SKILL.md` after the Phase 2
  repair; readback confirmed all required output contracts are now present and
  discoverable.

Repaired (code):

- Re-ran `rtk proxy npx skills check`, whitespace checks, tracked-file
  `git diff --check`, targeted output-contract `rg`, and local-identity leak
  review after adding the missing output-contract shapes.

Goal:

- Prove the edited skill package is valid, self-contained, and aligned with
  the plan before reporting completion.

Work: verify the skill package as a shipped artifact, not just as edited text.

Checklist (must all be done):

- Run `rtk proxy npx skills check` after skill package edits.
- Re-read every edited `SKILL.md`, `agents/openai.yaml`, and reference file.
- Confirm readback quality:
  - generic Figma skill, not local-project-specific
  - self-contained
  - timeless runtime voice
  - prompt-only
  - adaptive, not a fixed workflow
  - no authoring notes
  - no giant checklist in `SKILL.md`
  - no runtime instruction to read this plan, local packs, source docs, or
    external docs
- Run `rtk git diff --check -- <edited files>`.
- Use `rtk rg` to locate owned reference names and source-dependency terms for
  manual readback; the review, not keyword counting, is the proof.
- Inspect `skills/figma-best-practices` for local project names or absolute
  local paths and remove any that appear in runtime prose.
- Do not run `make verify_install`; install behavior is unchanged in this plan.
- Do not run app/device tests; this plan does not change app code or external
  audit scripts.

Verification (required proof):

- `rtk proxy npx skills check`
- Readback of all edited runtime files.
- `rtk git diff --check -- <edited files>`
- Targeted `rtk rg` readback support for owned references and local-identity
  leak review.

Docs/comments:

- Final reply must name changed files, verification run, and any verification
  that could not be run. No extra runtime docs are created.

Exit criteria (all required):

- `npx skills check` passes.
- Readback confirms the runtime prose is self-contained, generic, adaptive, and
  free of discussion residue.
- Whitespace/diff checks pass.
- Final reply names changed files and states any verification that could not be
  run.
- No app/device testing is claimed because this plan does not change app code
  or external audit tooling.

Rollback:

- Fix failing skill-package checks or runtime-prose readback issues in place
  before completion; if the package cannot pass without changing scope, repair
  the plan rather than weakening the exit criteria.

<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

Avoid verification bureaucracy. This is a prompt-first skill package upgrade;
proof should show package validity, self-contained doctrine, and preserved
behavior, not enforce doc inventory by brittle gates.

## 8.1 Unit tests (contracts)

- `npx skills check`
- Read back edited `SKILL.md` and references.
- During readback, confirm runtime prose is generic, self-contained, timeless,
  and free of authoring notes, planning backstory, local project identity, and
  required external-doc references.
- Check frontmatter description length stays below runtime cap.

## 8.2 Integration checks (representative tasks)

- Use `rg` to locate key routing terms for manual readback; do not treat term
  presence as proof by itself:
  - `app fidelity`
  - `source-pair manifest`
  - `Evidence only`
  - `Blocked`
  - `duplicate`
  - `Dev Mode`
  - `Code Connect`
  - `Index`
- Manually inspect that a single-target Figma audit and an exhaustive audit
  would both have the right tools available without requiring the same ordered
  procedure.

## 8.3 E2E / device tests (realistic)

No device test is required for the skill package itself. This plan does not
change app audit scripts or app code; those changes belong to a different plan.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

This is an installed skill-package edit. After implementation, run the required
skill check and report the changed files. Do not run `make verify_install`
because install behavior is unchanged.

## 9.2 Telemetry changes

None.

## 9.3 Operational posture

After the upgrade, future agents using `$figma-best-practices` should have
these reusable capabilities available as needed:

- classify the Figma task and artifact role;
- load file-craft guidance when structure, components, variables, pages, or
  canvas hygiene are in scope;
- load MCP gotchas for tool-mediated Figma work;
- load app/source fidelity references when app/source/screenshot truth is in
  scope;
- return evidence-ranked findings, blockers, or repair plans;
- keep long reports out of Figma.

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass

- Reviewers: explorer 1, explorer 2, self-integrator
- Scope checked:
  - Frontmatter, TL;DR, North Star, scope, constraints, and decision log.
  - Research grounding, current architecture, target architecture, and
    call-site audit.
  - Section 7 phase plan against Sections 0, 3, 5, 6, 8, and 9.
  - Adjacent surfaces: `SKILL.md`, references, `agents/openai.yaml`, README,
    and the planning-source requirements doc.
  - Compatibility posture, runtime owner path, no-new-skill boundary,
    prompt-only boundary, verification burden, and rollout posture.
- Findings summary:
  - Initial cold read found stale pre-planning language in TL;DR and the
    Decision Log.
  - Initial cold read found approved audit obligations stranded in research
    inventory instead of Section 7: target/app matching, source-truth
    hierarchy, metadata/handoff readiness, fast structural scans, audit write
    boundaries, and `author`/`review`/`repair` preservation.
  - Initial cold read found Section 8 wording that could read like keyword
    presence was proof rather than readback support.
- Integrated repairs:
  - Updated TL;DR and Decision Log follow-up so planning is no longer presented
    as pending.
  - Added Phase 2 obligations for target resolution, candidate app/source
    matching, ambiguity reporting, source-truth handoff, metadata/handoff
    readiness, output ledgers, and no-mutation audit boundaries.
  - Added Phase 3 obligations for fast structural scans as cheap evidence with
    explicit limits.
  - Added Phase 4 obligations for source-truth hierarchy, cross-reference
    ownership, Dev Mode, Ready for Dev, Code Connect, Make/MCP readiness,
    source links, component descriptions, handoff readiness, and write/repair
    readback.
  - Added Phase 5 obligations preserving `author`, `review`, and `repair`
    surfaces while placing app/source fidelity audits inside `review`.
  - Clarified that prompt/reference prose is the canonical boundary for this
    prompt-only package, and that `rg` is readback support rather than a
    keyword gate.
- Remaining inconsistencies:
  - none
- Unresolved decisions:
  - none
- Unauthorized scope cuts:
  - none
- Decision-complete:
  - yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->

# 10) Decision Log (append-only)

## 2026-04-30 - Keep app-fidelity audit inside figma-best-practices

Context

The requirements catalog originally proposed a future
`figma-app-fidelity-audit` skill, but the user explicitly requested that this
capability be folded into the existing `figma-best-practices` skill instead.

Options

- Create a new audit skill.
- Fold the audit capability into `figma-best-practices`.

Decision

Fold the audit capability into `figma-best-practices`.

Consequences

- The package must stay one coherent skill with stronger references and
  reference-selection rails.
- The future-skill requirements doc becomes source material, not a runtime
  package boundary or runtime dependency.
- The implementation must preserve existing file-craft behavior while adding
  actual app-fidelity audit behavior.

Follow-ups

- Completed in this plan: North Star confirmed, research grounding completed,
  deep-dive completed, and phase plan authored for implementation.
