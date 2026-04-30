# Figma Visual Fidelity

Use this reference when a task asks whether Figma visually matches an app,
source component, screenshot, asset, or runtime state.

This is a starting system for visual fidelity work, not the only valid path.
Choose the cheapest evidence that can support the requested claim, and downgrade
or block the verdict when the evidence is not strong enough.

## Source-Pair Manifest

Do not compare unnamed screenshots. A visual parity claim needs an explicit
source pair. Keep the manifest in a repo doc, audit artifact, or chat output,
not as a long Figma page.

Useful fields:

- Figma file, page, node ID, node role, and artifact role
- runtime route, screen, component, story, or state
- app screenshot, rendered export, golden, or capture path
- source code, token, theme, and asset anchors
- platform, viewport, device, theme, locale, data fixture, and entitlement
- capture time or build identity when it matters
- comparison mode
- crop/scale/normalization rules
- ignored regions and dynamic content
- blocked evidence and confidence boundary

A source pair does not have to be perfect to be useful. It does have to be named
clearly enough that a reviewer can tell what was compared.

## Screenshot And Contact-Sheet Boards

Screenshot boards are evidence indexes unless source-backed proof promotes a
specific artifact into canonical component truth.

Use screenshot/contact-sheet boards for:

- visual references
- route/state coverage
- before/after comparison
- evidence that a source pair exists
- spotting duplicates, stale captures, and missing states

Do not use screenshot boards as:

- reusable component libraries
- source-of-truth token tables
- proof that local Figma components are canonical
- long audit reports

When a screenshot board is in Figma, keep labels compact and put the manifest,
acceptance matrix, and findings outside Figma.

## Fast Structural Scans

Fast structural scans are cheap evidence. They are useful before slower visual
diffs or source deep-dives.

Scan:

- Figma tree shape: pages, sections, frames, component sets, instances, and
  loose top-level nodes
- layer names, component names, variant properties, descriptions, and Dev
  Resources
- bounds, section overlap, clipping, overflow, and children outside owning
  sections
- styles, variables, fills, strokes, effects, text styles, and token bindings
- source-map notes, Code Connect hints, component descriptions, and runtime
  anchors
- repeated image fills, repeated component names, duplicate page names, and
  obvious stale/approximate labels

Fast scans can prove structure, identity hints, obvious drift, missing metadata,
and cleanup risk. They cannot prove pixel-perfect fidelity, current runtime
truth, or source-backed correctness by themselves.

## Exact Asset And Evidence Checks

When Figma is supposed to contain an uploaded screenshot, bitmap, icon, or
source asset, exact evidence can be stronger than a visual diff.

Check what is available:

- source image dimensions
- Figma fill dimensions
- byte length
- content hash or checksum
- image fill hash or asset identity
- target rectangle aspect ratio
- scale mode and crop behavior
- alpha channel or mask behavior

State the limited claim the check supports. A matching bitmap can prove that a
Figma node contains the same image evidence. It does not prove the screenshot is
current, the app is implemented correctly, or surrounding Figma components are
canonical.

## Deterministic App Capture

A runtime screenshot is useful only when the runtime state is knowable.

Capture context should name:

- platform and device class
- viewport, density, safe-area, and system chrome handling
- route, deeplink, story, component state, or screen
- theme, locale, and data fixture
- auth, entitlement, feature flags, or account state
- settled animations and hidden debug chrome
- raw screenshot path and any processed derivative
- snapshot, log, or manifest proving the state

If these cannot be controlled, use the screenshot as evidence with a boundary,
not as proof of pixel parity.

## Visual Comparison Modes

Choose the mode that matches the question:

- Exact bytes: best for uploaded evidence or source assets; too strict for most
  rendered UI.
- Perceptual duplicate/similarity: useful for triage and duplicate grouping.
- Structural comparison: compares tree, layout, names, tokens, and source links.
- Normalized pixel/patch diff: useful for explicit app/Figma pairs after crop,
  scale, color, alpha, and ignored regions are defined.
- Human review of failures: required when the diff finds meaningful change but
  source or product intent determines whether it is acceptable.

Image diff is evidence, not the whole audit. Pair it with source checks for
widgets, layout contracts, tokens, assets, typography, and component instances.

## Normalization

Before claiming a pixel or patch diff:

- crop the same region
- align scale and pixel density
- use the same color space and bit depth
- handle alpha and transparent backgrounds deliberately
- account for safe areas, status bars, navigation bars, browser chrome, and
  platform widgets
- ignore dynamic regions such as timestamps, avatars, data values, ads, or
  animation frames
- document masks, clipped regions, rounded corners, and shadows
- name viewport and platform differences

Unnormalized diffs can still be useful triage. They are not pixel-perfect proof.

## Pixel-Parity Boundaries

No pixel-perfect or visual-parity pass without:

- explicit Figma target
- explicit app/source target
- rendered evidence or screenshot evidence
- dimensions and capture context
- normalization rules
- ignored regions
- source/token/asset anchors where relevant
- duplicate/stale disposition
- blocker disclosure

If any of those are missing, use a weaker verdict such as `Partial`, `Evidence
only`, or `Blocked`.

## Component-To-App Comparison

Compare in both directions when the task asks for component fidelity.

Figma to app:

- Which production component, route, or state does this Figma artifact claim to
  represent?
- Which tokens, assets, typography, layout rules, props, variants, and states
  are source-backed?
- Is it canonical, evidence, approximate, stale, or blocked?
- Does the artifact use existing library components or local drawings?

App to Figma:

- Which Figma component, frame, or page should represent this source component?
- Are required states, variants, text behaviors, slots, assets, and responsive
  layouts modeled?
- Does Figma expose component properties that match source semantics?
- Are there duplicate local drawings or generated shells that should be moved to
  evidence/archive or deleted?

## Completion Evidence

A visual-fidelity audit or repair is not complete until the output names:

- Figma file/page/node paths
- app route/component/state paths
- source code, token, and asset anchors
- screenshot or render paths
- manifest rows or comparison identity
- exact asset receipts when available
- diff mode and normalization parameters when used
- duplicate/stale classification
- clean Figma output: no report blobs on canvas, with `Index` links when file
  conventions changed
- blocked evidence, not-inspected surfaces, and out-of-scope boundaries
