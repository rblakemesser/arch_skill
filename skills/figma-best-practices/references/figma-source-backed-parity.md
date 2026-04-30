# Figma Source-Backed Parity

Use this reference when a Figma component, library page, handoff board, or audit
claims to represent production UI from source code, tokens, shipped assets,
screenshots, or runtime behavior.

This is source-truth discipline, not a tool-operation guide and not a visual
diff method. Use `figma-audit-toolkit.md` for target/candidate matching and
report contracts. Use `figma-visual-fidelity.md` for source-pair manifests,
screenshots, captures, and visual comparison boundaries.

## Source Truth

Name the source before judging exactness. Depending on the task, source truth
may be:

- production component code and layout contracts
- app-owned tokens, theme files, variable modes, or asset manifests
- shipped bitmap, vector, icon, and illustration assets
- screenshots or renders from an actual runtime state
- product decisions recorded in handoff notes, descriptions, or Dev Resources
- existing published library components, variables, styles, and component
  properties

Figma exports, generated local components, MCP asset URLs, screenshot boards,
and name similarity are evidence unless the task explicitly promotes them into
the system. Do not treat a plausible component name, successful write, imported
frame, or tool metadata result as canonical.

## Source-Of-Truth Hierarchy

When evidence conflicts, prefer the highest source that actually owns the
runtime behavior:

1. production source code on the active render path
2. source token/theme/asset manifests used by that render path
3. runtime state proof: route, props, fixture, screenshot, snapshot, or golden
4. published Figma library components with matching source links
5. component descriptions, Dev Resources, Code Connect, or handoff notes that
   name source ownership
6. screenshot/reference boards
7. generated local Figma objects, labels, or visual similarity

Use lower tiers for discovery and triage. Do not let lower tiers override a
clear higher-tier source.

## Claim Semantics

Every source-backed claim should say:

- Figma target: file, page, node, component, or frame
- artifact role: canonical, evidence, approximate, stale, blocked, not
  inspected, or out of scope
- source target: component, route, token, asset, runtime state, or product
  decision
- exact surfaces: what is source-backed and verified
- approximate surfaces: what is sampled, proxy-only, or outside Figma's model
- evidence: source path, node ID, screenshot, runtime state, measurement,
  description, Dev Resource, Code Connect map, or handoff note
- blocked evidence: what prevents a stronger verdict

If a claim cannot name its source target and evidence, it is not source-backed.
Use `Evidence only`, `Blocked`, or a narrower verdict.

## Canonical Status

Classify every relevant Figma artifact before reusing it:

- `Canonical`: source-backed, named, verified, and safe for Assets/search.
- `Evidence`: useful screenshot, import, or documentation surface that should
  guide work but not be instanced as a system component.
- `Approximate`: intentionally partial or visual-only; label it and keep it out
  of reusable component paths.
- `Stale`: contradicted by current source or product intent; replace, archive,
  or delete it.
- `Blocked`: potentially relevant but unverified because required source,
  runtime, or Figma evidence is unavailable.

A generated component becomes canonical only when the artifact or nearby
documentation names the source widget or code component, token source, asset
source, and verification anchor. The verification anchor may be a node ID,
screenshot, runtime state, source file, measured layout contract, component
description, Dev Resource, or Code Connect mapping.

## Component Repair

Repair toward the source-owned concept, not toward the old audit name. If the
source-backed replacement exists, rename the component to the production concept
and remove misleading generated names.

Delete stale reusable components and variants instead of preserving them as
deprecated options when they do not represent runtime behavior. Warning labels
inside Assets/search still leave the wrong building blocks available to future
designers and agents.

Use additive deprecation only for legitimate published system migrations where
downstream consumers need time to move. Do not keep non-runtime variants,
partial shells, placeholder states, or old asset wrappers as if they were
intentional API.

When replacing generated work:

- preserve exact child instances that are still source-backed
- delete or rebuild children that only look plausible
- update names, descriptions, Dev Resources, and notes so they no longer
  contradict the repair
- verify removal from component search or registry surfaces, not only by looking
  up one deleted ID

## Text, Props, And Variants

Keep Figma property modeling aligned with source semantics:

- variants for real source enumerations
- booleans for source booleans or visibility flags
- instance swaps for guarded component or icon replacement
- slots for freeform children
- text properties for source-owned copy that should be edited safely

Expose text as component properties when designers need realistic mocks, but do
not share one text property across variants if variant-specific copy is part of
the runtime contract. Verify each variant's rendered text after resetting or
removing overrides.

Do not infer a reusable Figma component from a runtime kind name, enum value, or
screenshot label alone. Trace the actual render path before creating a
component family.

## Assets And Images

When the product uses shipped bitmap or vector assets, use those assets. Do not
redraw exact asset-backed UI as schematic Figma shapes unless the task is
explicitly exploratory.

For duplicate assets, reuse the same fill or image hash after one verified
upload rather than re-uploading or redrawing variants. For exact asset
components, keep target rectangles at the source aspect ratio and verify the
rendered fill, not just the upload response.

Visible exports beat hidden, clipped, or off-canvas layer guesses. If hidden
helper text or a mock-only layer conflicts with the visible runtime frame,
record the product decision before turning it into Figma truth.

## Layout And Runtime Behavior

Prefer executable layout contracts, source constants that are actually used by
the render path, and measured runtime screenshots over eyeballed screenshot
heights. A token or constant that exists in code is not automatically the owner
of the current layout.

Check source-framework semantics before translating values into Figma. Common
traps include opacity units, alpha composition, line-height units, font style
names, layout scaling, and transforms that Figma cannot represent directly.

When Figma cannot model a runtime behavior exactly, document the boundary near
the component. Good boundary notes say what is exact, what is sampled, what is
proxy-only, and where the source behavior lives.

## Alpha And Paint Binding

Be careful binding variables to paints that need semantic alpha. Some
operations reset paint opacity while binding color variables, turning subtle
overlays into fully opaque fills.

Until the system has a real alpha-bearing token or supported variable binding,
preserve raw paint opacity and document the source color, token, and alpha in
the component description or handoff note.

## Cleanup Scans

Search for bad generated artifacts with terms tied to actual cleanup risk, such
as `approx`, `deprecated`, `legacy`, `stale`, `repair candidate`, `do not use`,
and `not exact`. Avoid broad terms that catch legitimate words.

After cleanup, verify:

- stale components and variants are gone from component search surfaces
- descriptions no longer claim unsupported parity
- screenshots of replacement components are readable
- source-backed components cite the source code, tokens, assets, or product
  decision that owns them
- evidence boards remain evidence instead of becoming reusable components

## Acceptance Check

Before calling source-backed Figma work done, the artifact should answer these
questions without hidden context:

- What production source owns this component or frame?
- Which tokens, assets, layout rules, and runtime states are exact?
- Which behavior is approximate, sampled, proxy-only, or outside Figma's model?
- Which generated, duplicate, or stale artifacts were removed or relabeled?
- What screenshot, node ID, source path, description, Dev Resource, Code Connect
  map, or handoff note proves the claim?
- Which evidence is blocked or not inspected?
