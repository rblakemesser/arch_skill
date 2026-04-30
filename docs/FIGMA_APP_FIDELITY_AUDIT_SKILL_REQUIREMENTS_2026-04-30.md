# Figma App Fidelity Audit Skill Requirements

Date: 2026-04-30

Implementation status: durable guidance from this requirements catalog was
folded into the existing `figma-best-practices` skill instead of shipping as a
new `figma-app-fidelity-audit` skill. Treat this document as planning source
material, not runtime skill doctrine.

Proposed skill name: `figma-app-fidelity-audit`

Status: research and requirements catalog folded into the existing
`figma-best-practices` skill. This document does not ship runtime doctrine.

## Goal

Build a reusable audit skill that deeply audits a supplied Figma item against
the real application and, when provided, screenshot/reference Figma nodes. The
skill should return a grounded checklist of compliant and non-compliant aspects
covering pixel fidelity, component/source parity, Figma file craft, design
system health, duplicate/stale artifacts, metadata, handoff readiness, and
coverage gaps.

The skill is an audit-focused complement to `$figma-best-practices`. That skill
owns general Figma file-craft doctrine. This proposed skill owns source-backed
fidelity: "does this Figma item accurately represent the app, and is it
structured so designers, developers, Dev Mode, Code Connect, MCP agents, and
future audits can trust it?"

Canonical user asks:

- "Audit this Figma node against the current app and tell me every fidelity gap."
- "Audit this component/page/screen using these Figma screenshot nodes as
  visual reference."
- "Run this exhaustively over every current app surface so we have a complete
  Figma-vs-app gap ledger."

Strong anti-case:

- "Implement this Figma design in code." That belongs to a Figma implementation
  workflow, not this audit skill. This skill can name code-side fixes, but its
  output is an audit, checklist, and repair plan unless the user separately
  asks to implement.

## Source Research

This requirement catalog was built from:

- Existing `$figma-best-practices`, especially `figma-file-craft.md` and
  `figma-mcp-agent-gotchas.md`.
- Poker Skill parity reports under
  `/Users/aelaguiz/workspace/psmobile/docs/AGENT/`, especially:
  - `FIGMA_CURRENT_UX_PARITY_AUDIT_2026-04-29.md`
  - `FIGMA_CURRENT_UX_PARITY_PHASE0_TRACKER_2026-04-29.md`
  - `FIGMA_COMPONENT_SYSTEM_PARITY_AUDIT_2026-04-29.md`
  - `FIGMA_GLOBAL_COMPONENT_PARITY_AUDIT_2026-04-29.md`
  - `FIGMA_LESSONS_COMPONENTS_SCREENS_AUDIT_2026-04-30.md`
- Figma official documentation and best-practice materials:
  - Figma MCP server overview and tools:
    `https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server`
    and
    `https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/`
  - Figma REST file/image endpoints:
    `https://developers.figma.com/docs/rest-api/file-endpoints/`
  - Figma REST file property types and component metadata:
    `https://developers.figma.com/docs/rest-api/file-property-types/`
  - Figma REST node global properties:
    `https://developers.figma.com/docs/rest-api/files/`
  - Auto Layout:
    `https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout`
  - Variables, collections, modes, scopes, and Dev Mode variables:
    `https://help.figma.com/hc/en-us/articles/14506821864087-Overview-of-variables-collections-and-modes`,
    `https://help.figma.com/hc/en-us/articles/15145852043927-Create-and-manage-variables-and-collections`,
    and
    `https://help.figma.com/hc/en-us/articles/27882809912471-Variables-in-Dev-Mode`
  - Component properties, variants, slots, and component management:
    `https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties`,
    `https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants`,
    `https://help.figma.com/hc/en-us/articles/38231200344599-Use-slots-to-build-flexible-components-in-Figma`,
    `https://help.figma.com/hc/en-us/articles/360038663994-Name-and-organize-components`,
    `https://help.figma.com/hc/en-us/articles/7938814091287-Add-descriptions-to-styles-components-and-variables`,
    `https://help.figma.com/hc/en-us/articles/39747637290263-Components-collection-Tips-for-component-management`,
    and
    `https://www.figma.com/best-practices/creating-and-organizing-variants/`
  - Sections and Dev Mode:
    `https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections`,
    `https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode`,
    `https://help.figma.com/hc/en-us/articles/23918228264855-Dev-Mode-ready-for-dev-view`,
    and
    `https://help.figma.com/hc/en-us/articles/15023193382935-Compare-changes-in-Dev-Mode`
  - Code Connect:
    `https://developers.figma.com/docs/code-connect/react/` and
    `https://developers.figma.com/docs/figma-mcp-server/skill-figma-code-connect/`
  - Code/export/AI-agent readiness:
    `https://developers.figma.com/docs/figma-mcp-server/structure-figma-file/`,
    `https://help.figma.com/hc/en-us/articles/22012921621015-Guide-to-inspecting`,
    `https://developers.figma.com/docs/figma-mcp-server/skill-figma-create-design-system-rules/`,
    and
    `https://developers.figma.com/docs/code/write-design-system-guidelines/`
  - Shared library best practices:
    `https://www.figma.com/best-practices/components-styles-and-shared-libraries/`
  - Developer handoff and design-system adoption:
    `https://www.figma.com/best-practices/how-figma-uses-dev-mode/`,
    `https://www.figma.com/best-practices/tips-on-developer-handoff/`,
    `https://www.figma.com/best-practices/guide-to-developer-handoff/`,
    and
    `https://www.figma.com/blog/the-designers-handbook-for-developer-handoff/`
  - Schema 2025 design-system changes:
    `https://help.figma.com/hc/en-us/articles/35794667554839-What-s-new-from-Schema-2025`
- Visual and app-rendering verification sources:
  - Playwright visual comparison documentation:
    `https://playwright.dev/docs/test-snapshots`
  - Chromatic Storybook visual testing workflow:
    `https://www.chromatic.com/docs/storybook`
  - Flutter adaptive/responsive design:
    `https://docs.flutter.dev/ui/adaptive-responsive`
  - Flutter golden-file matcher and font caveats:
    `https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html`
  - Flutter custom design-system theme extensions:
    `https://api.flutter.dev/flutter/material/ThemeExtension-class.html`
- Standards sources:
  - W3C Design Tokens Format Module 2025.10:
    `https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/`
  - WCAG 2.2:
    `https://www.w3.org/TR/WCAG22/`

Research notes that affect the future skill:

- Figma MCP exposes `get_design_context`, `get_variable_defs`,
  `get_code_connect_map`, `get_screenshot`, `get_metadata`,
  `search_design_system`, and write-capable `use_figma` tooling. An audit skill
  should prefer read tools and use write tools only if the user asks for repair.
- Figma REST `GET file`, `GET file nodes`, `GET image`, and `GET image fills`
  give enough structure to perform node mapping, rendered-reference capture,
  component/source discovery, image-fill verification, and diffable screenshots.
  Image export URLs are temporary and image rendering can return null per node,
  so successful API calls are not proof of visual truth.
- Figma stores component and component-set descriptions, documentation links,
  remote/local status, property definitions, bound variables, component
  property references, and explicit variable modes in API-readable structures.
  These are core audit fields.
- Figma officially recommends Auto Layout for dynamic/responsive UI, with
  `Hug contents`, `Fill container`, `Fixed`, min/max dimensions, and
  `Ignore auto layout` serving different layout intents.
- Figma component properties cover booleans, instance swaps, text properties,
  nested instance exposure, variants, and now slots. Slots are in beta but are
  official and relevant for cards, modals, repeating regions, flexible layout
  containers, and code-like composition.
- Figma recommends clear, code-aligned names, slash-separated hierarchy,
  semantic layer names, component descriptions, accessibility documentation,
  testing library changes before publishing, graceful deprecation, and use of
  analytics where available.
- Figma descriptions are not decorative. Figma uses component descriptions in
  component search, shows them in the Assets panel, exposes component/style
  descriptions in Dev Mode, and allows descriptions and documentation links on
  components, component sets, and variants. Descriptions are therefore part of
  the audit surface for searchability, reuse, and handoff.
- Figma's own "better code" guidance for MCP/AI output emphasizes components,
  Code Connect, variables, semantic names, Auto Layout, annotations, and dev
  resources. The skill should audit these as code-output prerequisites, not as
  optional cleanup.
- Figma's handoff guidance repeatedly points to names, styles, variables,
  descriptions, documentation links, source-code links, Storybook/dev-resource
  links, annotations, and explicit deviation notes as the difference between a
  usable design and a static picture. The audit should treat missing source
  links, missing style names, and unexplained detached/deviated components as
  implementation-fidelity defects.
- Dev Mode inspection exposes layout, color, typography, text strings,
  component properties, styles, variables, documentation links, dev resources,
  export settings, asset export choices, and autogenerated code snippets. The
  skill should treat bad authorship as a code-export defect because these
  surfaces are what developers and agents actually consume.
- Figma Make guidelines favor small, specific guideline files over huge
  catch-all documents. For code generation readiness, the audit should check
  whether component and token guidance is granular, findable, and routable
  rather than buried in one broad note.
- Figma's design-system-rules workflow for MCP explicitly analyzes codebase
  component organization, styling approach, token locations, naming, props,
  architecture, asset handling, accessibility, testing, and performance. A
  Figma item is not fully code-export-ready if it cannot support that mapping.
- Dev Mode prioritizes sectioned Ready-for-dev content, tracks changed status,
  supports compare-changes, shows layer properties and variables, and can expose
  Code Connect mappings. Unsectioned or poorly named work is harder to audit
  and hand off.
- W3C DTCG 2025.10 makes `$value`, `$type`, `$description`, aliases, and typed
  tokens stable enough to treat token structure as a real interoperability
  check, while remembering Figma variables are not a complete DTCG token file.
- WCAG 2.2 adds audit obligations for contrast, non-text contrast, target size,
  focus visibility, motion/animation considerations, orientation, labels, and
  robust state coverage. The skill should not pretend Figma proves runtime
  accessibility, but it should flag design-level accessibility omissions.
- Visual regression tooling is useful but environmental. Playwright documents
  that browser rendering can vary by OS, browser, settings, hardware, power
  state, headless mode, fonts, and similar factors; Flutter golden tests also
  document that custom fonts and Flutter versions can change pixels. The audit
  must capture the comparison environment and avoid pretending a diff is pure
  product drift when the renderer changed.
- Component-level visual baselines are often more stable and useful than only
  full-screen baselines. The skill should prefer a hierarchy of evidence:
  design-system component golden, route-state screenshot, full flow screenshot,
  then app-store/marketing screenshots only as weak supporting evidence.
- Flutter supports custom `ThemeExtension` values, and the Poker Skill app
  already exposes app-specific design-system surfaces such as `AppColors`,
  `AppTypography`, `AppSpacing`, `AppRadii`, `AppShadows`, `AppMotion`, `Ps*`
  primitives, and debug design-system gallery screens. For this app, "matches
  the app" means matching those runtime sources and their current rendered
  behavior, not only matching a visual memory of the app.
- Sampled Figma target
  `https://www.figma.com/design/SymgmezTdwwtIdpWyZMRQB/Poker-Skill--AE---CURRENT-?node-id=1992-404`
  resolved through MCP metadata as an `Account Components` canvas containing
  numbered Phase 9 sections, source-map/acceptance-note frames, and many
  route/state symbol instances named `State=...`. The screenshot shows dense
  state boards rather than a single app screen. The audit skill must therefore
  classify state-board, evidence-board, component-library, source-map,
  screenshot-reference, and canonical-component surfaces differently.
- The same Figma sample exposed practical audit blockers and gotchas:
  `get_design_context` and `get_variable_defs` were selection-limited in the
  current session, `get_code_connect_map` required a Developer seat in an
  Organization/Enterprise plan, and a broad design-system search did not return
  variable/style matches. These must become explicit `Blocked` or
  `Insufficient evidence` statuses, not silent failures or invented verdicts.

## Core Principles

1. Source-backed truth beats visual resemblance.
   A Figma item is trustworthy only when it maps to actual app source, tokens,
   assets, and states. Screenshot similarity alone is evidence, not canonical
   truth.

2. Pixel fidelity requires rendered evidence.
   Exactness claims need at least one visual capture of the Figma node and one
   visual capture of the corresponding app state or supplied screenshot
   reference. Metadata-only inspection cannot prove pixel match.

3. Figma structure is part of fidelity.
   A static lookalike can pass a casual screenshot review and still fail
   implementation fidelity because it uses detached layers, wrong props, raw
   values, unsearchable names, or duplicate component families.

4. Authorship is product metadata, not housekeeping.
   Names, descriptions, documentation links, section roles, variant/property
   labels, annotations, dev resources, and source notes are how downstream
   humans and agents discover intent. Missing or misleading authorship is a
   fidelity defect because it causes wrong reuse and wrong implementation even
   when the pixels look close.

5. Screenshots are optional inputs, not optional evidence.
   If screenshots are provided, use them. If they are not, the skill should try
   to capture or locate current app screenshots. If that is impossible, it
   should mark the visual exactness portion as unverified instead of inventing
   a pass.

6. The skill should find the right comparison target.
   The user should be able to provide one Figma URL and expect the agent to
   search intelligently through Figma metadata, app routes, component names,
   source paths, Code Connect maps, existing screenshot packs, and visual
   reference pages.

7. Exhaustive means coverage plus exceptions.
   Every route/component/state can be `Pass`, `Fail`, `Partial`,
   `Evidence only`, `Out of scope`, `Blocked`, or `Not inspected`, but it cannot
   disappear. Out-of-scope and evidence-only are explicit statuses with reasons.

## App Fidelity Match Surface

This section is the exhaustive answer to "what must actually match the app?"
The future skill should use it as the base inventory for every single-item
audit and every app-wide sweep. It is deliberately broader than pixel diffing:
Figma must match the current app's runtime look, source structure, style-guide
contract, component model, and authored project organization.

### 1. Comparison Identity And Runtime Environment

Before judging any pixel or component, the audit must establish the exact app
and Figma identities being compared.

Required matches or explicit blockers:

- App build identity:
  - repository path
  - git branch/commit if available
  - app flavor/environment
  - app version/build number if visible or relevant
  - feature flags
  - remote config
  - experiment/A-B assignment
  - seeded/mock/live data mode
  - auth/account state
  - subscription/entitlement state
  - network/offline state when relevant
- Platform identity:
  - iOS, Android, web, desktop, or simulator/emulator
  - OS version
  - device model or viewport
  - device pixel ratio
  - orientation
  - safe-area insets
  - status bar/navigation bar inclusion
  - keyboard/input accessory visibility
  - text scale/dynamic type
  - high-contrast/reduced-motion settings
  - light/dark/theme mode
  - locale, language, timezone, currency, and number/date formatting
- Figma identity:
  - file key
  - page/canvas
  - section
  - frame/component/component-set/node ID
  - artifact role
  - published/local/remote status
  - Ready-for-dev status if applicable
  - branch/version/date if available
  - supplied reference nodes or screenshots

Failure patterns:

- Comparing an app screenshot from one build to a Figma board from another
  phase with no version note.
- Comparing different account states or entitlement states.
- Cropping out status bars/safe areas on one side but not the other.
- Treating a screenshot board as current truth without checking the app build
  and route source.

### 2. Screen, Route, And Flow Coverage

The Figma item must represent the same user-visible app surface, not just a
nearby concept.

Required matches:

- Route path, route name, tab, modal, sheet, overlay, or embedded component.
- Navigation entry point:
  - bottom tab
  - stack route
  - deeplink
  - modal trigger
  - paywall/gate trigger
  - post-action transition
  - notification/deeplink recovery
- Flow position:
  - first-load state
  - returning-user state
  - mid-flow state
  - completion state
  - recovery/error state
  - dismissed/confirmed state
- Route chrome:
  - app shell
  - stable header
  - bottom tabs
  - top bars
  - nav affordances
  - close/back/share buttons
  - status/system chrome handling
- Scroll position and scroll ownership:
  - screen scroll
  - nested list
  - horizontal carousel
  - sheet body
  - sticky header/footer
  - fixed CTA

Failure patterns:

- Figma shows a component body but omits the real app chrome without labeling
  it as a component-only view.
- A route-state board exists, but the actual route source has additional
  states or overlays absent from Figma.
- The audit cannot tell whether a Figma state is a route, modal, component, or
  screenshot reference.

### 3. Spatial Geometry And Pixel Metrics

Geometry is the first strict visual layer. The audit should measure before it
editorializes.

Required matches:

- Outer frame size and aspect ratio.
- App content bounds and safe-area-adjusted content region.
- X/Y position of major regions.
- Width/height of components and repeated items.
- Padding, margin, and inset values.
- Gaps between siblings.
- Alignment:
  - left/right/center alignment
  - top/middle/bottom alignment
  - baseline alignment
  - optical alignment for icons/cards/badges
- Responsive sizing behavior:
  - fixed
  - fills available space
  - hugs content
  - min/max constraints
  - wraps
  - scrolls
  - clips intentionally
- Grid and list geometry:
  - column count
  - row height
  - card aspect ratio
  - list item height
  - separator thickness and inset
  - section spacing
- Layering geometry:
  - z-order
  - overlays
  - badges
  - shadows/halos
  - clipped children
  - hit-area overlays

Poker Skill app-specific examples to trace:

- `AppSpacing.tokens` values such as `xs=4`, `sm=8`, `md=12`, `lg=16`,
  `xl=20`, `xxl=24`, `xxxl=32`, and text spacing values.
- Feature UI specs such as `learn_ui_spec.dart`, `signed_out_ui_spec.dart`,
  `puzzles_ui_spec.dart`, `post_puzzle_sheet_ui_spec.dart`, and
  `modal_chrome_ui_spec.dart`.
- Runtime component padding inside primitives such as `PsButton`, `PsCard`,
  `PsListRow`, `PsChip`, `PsTextField`, and `PsScaffold`.

Failure patterns:

- Figma values are "close" but not on the app spacing scale.
- Figma uses arbitrary coordinates for repeated rows/cards that should be an
  Auto Layout gap or app token.
- Screenshots have the right overall impression, but repeated item height or
  content insets drift by several pixels.
- Figma frames are fixed when app widgets respond to text scale or viewport.

### 4. Color, Fill, Stroke, Gradient, And Opacity

Color fidelity means exact source-backed colors and semantic intent, not
eyedropped approximation.

Required matches:

- Background fills:
  - screen
  - section
  - card
  - row
  - badge/chip
  - modal/sheet
  - overlay/scrim
- Text colors for every hierarchy and state.
- Icon/vector colors.
- Border/stroke colors, widths, alignments, and opacity.
- Disabled, pressed, selected, active, error, success, warning, premium,
  paywalled, loading, and skeleton colors.
- Gradients:
  - stops
  - stop positions
  - angle/direction
  - opacity
  - blend mode
- Transparency and overlays:
  - alpha values
  - scrim behavior
  - disabled opacity
  - glass/blur/backdrop if present
- Semantic token mapping:
  - Figma variable/style name
  - app token name
  - raw value
  - usage role
  - exception reason if raw

Poker Skill app-specific examples to trace:

- `AppColorTokens` and `AppColors` values such as `cobalt900`, `cobalt800`,
  `cobalt700`, `cobalt500`, `cobalt200`, `offWhite`, `cyan300`, `cyan700`,
  `green300`, `yellow500`, `red300`, `pink300`, `purple300`, `orange300`,
  `tan300`, and feature-specific highlight tokens.
- Third-party brand color exceptions such as Google, Discord, Instagram, and X
  colors, which should be marked as intentional brand exceptions rather than
  palette drift.
- Poker/gameplay-specific colors such as seat strokes, card backgrounds,
  selected states, and table tile colors.

Failure patterns:

- Eyedropped hex values in Figma instead of app-token variables.
- Figma names colors by appearance (`Dark Blue 2`) instead of app role.
- Similar dark surfaces use multiple untracked values across screens.
- Status colors are reused incorrectly because the style guide lacks semantic
  status variables.
- Alpha differences are missed because only solid hex values were compared.

### 5. Typography And Text Rendering

Typography must match the app's rendered text, token source, and platform
fallback behavior.

Required matches:

- Font family and fallback chain.
- Font asset availability in Figma and the app.
- Font size.
- Font weight.
- Line height.
- Letter spacing.
- Text case and transform.
- Alignment.
- Baseline position.
- Paragraph spacing.
- Text width and wrapping.
- Truncation and ellipsis.
- Max lines.
- Text scale behavior.
- Locale and dynamic-content expansion.
- Numeric rendering:
  - tabular vs proportional if applicable
  - currency
  - percentages
  - dates/times
  - countdowns/timers
- Platform-specific text behavior:
  - iOS system text exceptions
  - Android font fallback
  - Flutter golden-test font loading caveats

Poker Skill app-specific examples to trace:

- `AppFontFamilies.blinker`, `AppFontFamilies.blinkerOutline`,
  `AppFontFamilies.mono`, and `AppFontFamilies.fallback`.
- `AppFontSizes.tokens` values: `xxs=10`, `xs=12`, `sm=14`, `md=16`,
  `mlg=18`, `lg=20`, `xl=24`, `xxl=28`, `xxxl=32`, `cardTitle=20`,
  and `tile=14`.
- `AppTypography.tokens.textTheme` roles such as `displayLarge`,
  `headlineLarge`, `headlineMedium`, `titleLarge`, `titleMedium`,
  `titleSmall`, `bodyLarge`, `bodyMedium`, `bodySmall`, `labelLarge`,
  `labelMedium`, and `labelSmall`.
- Explicit runtime exceptions such as tab-bar label parity using
  `CupertinoSystemText` at 10/w500 on iOS.

Failure patterns:

- Figma uses Inter or another default because the app font is not installed.
- Figma font size matches but line height or weight does not.
- Text fits the Figma sample string but clips real app copy.
- Labels differ by punctuation, capitalization, pluralization, or numeric
  formatting.
- Pixel diffs are blamed on design drift when the test renderer did not load
  the app font.

### 6. Style Guide And Token-System Adherence

The Figma style guide is part of the audit target. If the style guide is
incomplete, stale, or too weak to express the app cleanly, that is a finding.

Required matches:

- The target uses the canonical Figma variables/styles for:
  - colors
  - typography
  - spacing
  - radii
  - shadows
  - motion durations/easing
  - opacity
  - stroke widths
  - icon sizes
  - breakpoints/viewports where the file supports them
- Figma variables map to app design-system sources, not just raw values.
- Token names and hierarchy make the same distinctions as the app:
  - primitive
  - semantic
  - component-specific
  - feature-specific
  - third-party exception
- Missing style-guide coverage is reported when a screen needs a token or
  component that does not yet exist.
- New tokens/components are proposed only when reuse or clarity justifies them.
- Deprecated app tokens and deprecated Figma styles are not used in new
  canonical work.
- Tokens can be inspected in Dev Mode and, where useful, expose code syntax.

Style-guide completion checks:

- Every app design-system primitive has a Figma equivalent or explicit
  exception.
- Every Figma foundation variable has an app source or "Figma-only" reason.
- Every product-critical semantic color appears in the style guide.
- Every typography role appears in the style guide with app source values.
- Every major spacing/radius/shadow/motion value is represented.
- Style guide examples show real app states, not generic sample boxes only.
- The guide includes usage guidance: when to use, when not to use, accessibility
  constraints, and platform exceptions.

Failure patterns:

- A screen is pixel-correct but built from raw local values because the style
  guide lacks the right component/token.
- A new one-off style appears in a screen but never graduates into the guide.
- Figma has a style guide page, but production app components use a different
  token vocabulary.
- The style guide is visually attractive but not searchable, not source-mapped,
  or not usable for implementation.

### 7. Component Identity, Reuse, And Elegant Component Creation

Fidelity includes the question: is the app represented through the right Figma
components, or did someone draw the current pixels in the quickest possible
place?

Required matches:

- Production app components map to Figma components or component sets:
  - global primitive
  - feature primitive
  - route shell
  - row/card/list item
  - modal/sheet
  - control
  - icon
  - badge/chip
  - game/playable primitive
- Figma instances use the canonical component rather than detached copies.
- Component properties map to app props, enum values, booleans, slots, text
  properties, and instance swaps.
- Component boundaries match app boundaries closely enough for implementation.
- New component creation is required when:
  - the same visual/function pattern appears repeatedly
  - an app primitive exists with no Figma equivalent
  - a Figma board duplicates a pattern because no component exposes the needed
    state
  - a style-guide gap causes repeated raw values
  - a route-state board is effectively defining reusable UI
- New component creation is not required when:
  - the design is exploratory and labeled as such
  - the item is screenshot evidence only
  - the pattern appears once and is unlikely to recur
  - the app source owns a one-off custom-rendered scene

Elegant component criteria:

- Fewest components that honestly encode reuse.
- No mega-component that hides unrelated products behind variant axes.
- No tiny component explosion that makes composition slower than drawing.
- Clear prop model with app-aligned names.
- Slots for flexible composition instead of duplicating whole cards/modals.
- Variants only for real mutually exclusive states or sizes.
- Booleans only for real independent show/hide or on/off switches.
- Text properties for labels that designers should edit without detaching.
- Instance swaps for icon/avatar/media slots with preferred values.
- Descriptions and examples that explain use and misuse.
- Component lives on the right canonical page before broad reuse.

Poker Skill app-specific examples to trace:

- Global design-system primitives in `apps/flutter/lib/design_system/components`
  such as `PsButton`, `PsCard`, `PsChip`, `PsListRow`, `PsSectionHeader`,
  `PsTextField`, `PsToggleSwitch`, `PsBadge`, `PsIconButton`, and
  `PsProgressBar`.
- Feature-specific widgets under `features/*/presentation/widgets` and
  `features/*/presentation/screens`.
- Debug gallery surfaces such as `DesignSystemGalleryScreen` and
  `DesignSystemTokensScreen`, which can help identify expected component states
  and text-scale behavior.

Failure patterns:

- Figma has many route-state symbols, but no canonical component set for the
  row/card/control they repeat.
- A component exists but cannot express the app state without detaching.
- New component proposals duplicate existing app primitives.
- Convenience boards become de facto source of truth without promotion into
  the style guide.

### 8. Figma Project Placement And Lifecycle Organization

The audit must judge whether an item is in the right place in the Figma project
or randomly stuck somewhere convenient.

Required matches:

- Page role is explicit:
  - canonical design system
  - product component library
  - route-state coverage
  - screenshot/reference evidence
  - source map
  - audit tracker
  - exploration/sandbox
  - archive/deprecated
  - research/competitor/reference
  - handoff/ready for dev
- Section role is explicit and scoped:
  - product area
  - phase
  - route family
  - component family
  - state family
  - reference board
  - acceptance notes
- Canonical reusable components live on component/library pages, not only in
  route-state boards.
- Route-state boards live near source-map/evidence notes and link to canonical
  components.
- Screenshot boards are separated from editable component truth.
- Archives/deprecated work are visibly separated and labeled with replacement.
- Random convenience placement is flagged when it blocks discovery, reuse, or
  audit automation.
- Page and section names support repeatable sweeps and tracker generation.

Specific placement questions:

- If this is a component, why is it not on the canonical component page?
- If this is a route state, where is the app route/source map?
- If this is screenshot evidence, where is the capture date/build/platform?
- If this is a repair board, where is the canonical promoted result?
- If this is a one-off local component, is it intentionally local?
- If this is out of scope, why is it in an active handoff section?

Failure patterns:

- Production-looking components live only in a phase board.
- Source-map notes are separated from the states they document.
- Screenshot references sit on component pages with no evidence label.
- Designers cannot find a component through page hierarchy or Assets search.
- The project contains multiple active locations for the same product surface.

### 9. Visual Rendering Details Beyond Simple Pixels

The audit must check details that often create "it feels off" fidelity gaps.

Required matches:

- Shadows:
  - offset
  - blur
  - spread
  - color
  - opacity
  - elevation layer
  - app/platform rendering limitations
- Radii:
  - individual corners
  - card/control/sheet consistency
  - clipping behavior
- Borders/strokes:
  - inside/center/outside alignment
  - stroke width
  - dashes
  - separators and dividers
- Effects:
  - blur
  - background blur
  - blend mode
  - glow/halo
  - image filters
  - custom painter effects
- Icons:
  - visual bounds vs frame bounds
  - optical centering
  - size
  - stroke weight
  - filled/outline variant
  - cap/join style
- Images:
  - crop
  - focal point
  - scale
  - mask
  - loading placeholder
  - error placeholder
  - remote/local ownership
- Composited surfaces:
  - modal scrims
  - sheets
  - toasts/snackbars
  - popovers/tooltips
  - overlays
  - translucent/disabled content behind overlays

Failure patterns:

- Color and size match, but shadow depth or separator opacity is wrong.
- Icon frame is correct but the vector is visually off-center.
- Figma effect is impossible or expensive in the app and lacks an app-owned
  implementation note.
- Modal/sheet background state is omitted.

### 10. Copy, Data, And Content Fidelity

The audit must compare what users actually read, not only the layout boxes.

Required matches:

- Exact visible copy:
  - words
  - punctuation
  - capitalization
  - line breaks if intentional
  - button labels
  - error messages
  - empty-state copy
  - helper text
  - legal text
- Dynamic data:
  - names/usernames
  - XP/energy/gems/streaks
  - lesson/puzzle titles
  - achievement names
  - dates/times
  - leaderboard ranks
  - friend/request counts
  - subscription/price labels
  - entitlement states
- Content source:
  - hard-coded app string
  - localization file
  - remote config
  - API response
  - CMS/catalog/manifest
  - generated content
- Data range stress:
  - zero
  - one
  - many
  - long text
  - missing image
  - missing optional field
  - max count
  - extreme score/time/rank

Failure patterns:

- Figma uses aspirational marketing copy instead of app strings.
- Numeric examples are plausible but not representative of runtime formatting.
- Empty/error/loading text differs subtly from production.
- A Figma frame passes visually only because sample data is short.

### 11. State, Variant, And Edge-Case Completeness

The audit must compare the full state space, not just the selected screenshot.

Required matches:

- Every app state visible to users has one of:
  - Figma component variant
  - route-state frame
  - screenshot evidence
  - explicit out-of-scope reason
  - explicit missing finding
- State source is mapped:
  - enum
  - sealed class
  - boolean field
  - provider/view-model state
  - route param
  - feature flag
  - remote config
  - entitlement
  - permission state
- Common state families:
  - loading
  - skeleton/loading shimmer
  - empty
  - error
  - retry
  - offline/degraded
  - disabled
  - busy/submitting
  - success
  - selected/unselected
  - pressed
  - focused
  - locked/unlocked
  - claimed/unclaimed
  - signed-out/signed-in
  - gated/ungated
  - paywalled/subscribed
  - permission allowed/denied/not-determined
  - no relationship/pending/accepted/blocked for social surfaces
  - route-specific edge cases

Failure patterns:

- State names exist in Figma but do not map to app state names.
- Route-state boards show many states, but key source states are still absent.
- Edge states are screenshots only, while reusable component states are missing.
- Figma treats one "error" as complete when app has multiple recoveries.

### 12. Interaction, Gesture, Motion, And Feedback

Static visual fidelity is incomplete if the app behavior is part of the user
experience.

Required matches:

- Interaction state:
  - default
  - hover where relevant
  - pressed
  - focused
  - disabled
  - selected
  - loading
  - dragged/swiped
  - expanded/collapsed
- Gesture model:
  - tap
  - long press
  - swipe
  - drag
  - scroll
  - pinch/zoom if relevant
  - keyboard action
  - hardware back/escape
- Motion:
  - duration
  - delay
  - easing/curve
  - spring parameters if represented
  - entrance/exit direction
  - stagger order
  - progress/keyframes
  - looping/pulsing
  - reduced-motion alternative
- Feedback:
  - ripple/press effect
  - haptic if app-owned
  - sound if app-owned
  - snackbar/toast
  - inline validation
  - modal confirmation

Poker Skill app-specific examples to trace:

- `AppMotion`, `motion.dart`, and feature motion token files.
- `PsPressable`, button loading/disabled handling, and feature-specific
  animation policies.
- Playables and puzzle surfaces where Figma may need screenshots/key states
  rather than full motion ownership.

Failure patterns:

- Figma only captures final resting state for an animated transition.
- Pressed/disabled/loading variants are absent for controls used in production.
- Runtime motion tokens drift from Figma annotation values.
- Figma prototype transitions are decorative and do not match app behavior.

### 13. Accessibility, Semantics, And Usability Fidelity

The Figma artifact should carry enough accessibility intent to verify the app
or identify missing design-system states.

Required matches:

- Contrast for text and non-text UI.
- Target size and spacing.
- Focus and keyboard traversal where relevant.
- Screen-reader label intent for icon-only or ambiguous controls.
- Semantic grouping and reading order.
- Error/help text association with inputs.
- Modal/sheet focus trapping and dismissal affordances.
- Color is not the only meaning carrier.
- Text scale behavior.
- Reduced motion.
- VoiceOver/TalkBack hints for custom gameplay or card/table surfaces where
  app code implements semantics.

Failure patterns:

- App has semantics but Figma gives no label/source note, so future repair can
  easily regress accessibility.
- Figma shows color-only status badges.
- Touch targets look good visually but are smaller than app/platform policy.
- Text-scale stress breaks the Figma layout or is untested.

### 14. Platform And Native-System Fidelity

Some surfaces are owned by the platform or rendered differently by runtime.
The audit should separate app-owned fidelity from platform-owned fidelity.

Required matches:

- Safe area and system gesture zones.
- Status bar style and contrast.
- Navigation bar/home indicator treatment.
- Keyboard overlays, input accessory, and focus shift.
- Native permission sheets:
  - push notifications
  - ATT
  - photo/media
  - contacts
  - share sheet
- Native share/purchase/auth sheets.
- iOS vs Android typography and control differences.
- Flutter renderer differences across OS/engine versions.
- App-owned pre-prompts versus native dialogs.

Failure patterns:

- Figma draws a native OS sheet as if the app owns exact pixels.
- App-owned pre-prompt is missing because the native sheet screenshot exists.
- Platform differences are treated as defects instead of scoped variants.
- Android behavior is assumed from iOS Figma only.

### 15. App Source, Token Source, And Runtime Component Use

The skill must audit the app side as aggressively as Figma. Figma can be
correct while the app is wrong, and the app can be correct while Figma is
stale.

Required matches:

- Source file for the route/screen/widget.
- Source file for the app component primitive.
- Source file for style spec or feature UI spec.
- Source file for token/foundation values.
- Source file for assets and generated registries.
- Source file for motion, animation, or custom paint.
- App code uses the intended design-system primitive.
- App code avoids hard-coded one-off values where a token exists.
- App code does not duplicate an existing component under a feature directory
  without reason.
- Tests/goldens/screenshots exist where the repo has a precedent.

Poker Skill app-specific source anchors:

- `apps/flutter/lib/design_system/app_colors.dart`
- `apps/flutter/lib/design_system/app_typography.dart`
- `apps/flutter/lib/design_system/app_spacing.dart`
- `apps/flutter/lib/design_system/app_radii.dart`
- `apps/flutter/lib/design_system/app_shadows.dart`
- `apps/flutter/lib/design_system/app_motion.dart`
- `apps/flutter/lib/design_system/app_theme.dart`
- `apps/flutter/lib/design_system/components/*.dart`
- `apps/flutter/lib/features/*/presentation/style/*.dart`
- `apps/flutter/lib/features/*/presentation/widgets/*.dart`
- `apps/flutter/lib/features/*/presentation/screens/*.dart`
- `apps/flutter/lib/features/debug/presentation/screens/design_system_*`

Failure patterns:

- App source hard-codes a color that exists in `AppColors`.
- Figma uses a token correctly but the app bypasses the matching `Ps*`
  primitive.
- A feature creates a local row/card/button with near-identical styling to a
  global primitive.
- The app has a design-system gallery state that Figma does not cover.

### 16. Screenshot, Golden, And Visual-Baseline Evidence

Screenshots are evidence, not the whole truth. The audit must record how much
confidence each visual source provides.

Required matches:

- Figma render captured from the exact node.
- App screenshot captured from the exact route/component/state.
- Screenshot metadata:
  - platform
  - device/viewport
  - pixel ratio
  - OS/browser/Flutter engine where relevant
  - app build/commit when available
  - capture date
  - account/fixture
  - theme/text scale/locale
  - crop bounds
- Baseline hierarchy:
  - component golden or Storybook/component-state baseline
  - route/screen screenshot
  - flow screenshot
  - screenshot board/contact sheet
  - app-store/marketing screenshot as low-confidence evidence
- Diff metadata:
  - threshold
  - ignored/masked dynamic regions
  - residual pixel count/percent if available
  - known renderer/font variance
  - manual visual notes

Failure patterns:

- Screenshots lack dates/builds and become stale silently.
- Pixel diffs compare different font/rendering environments.
- A screenshot board is current-looking but not tied to app source.
- Dynamic content is not masked or normalized, making diff results noisy.

### 17. Mess And Drift Detection

The skill should actively look for messy parts because those are usually where
Figma-app drift hides.

Mess signals to detect:

- Generic layer names:
  - `Frame 123`
  - `Rectangle 47`
  - `Group`
  - `Vector`
  - `Image`
  - `Text`
- Detached components.
- Hidden or off-canvas canonical-looking work.
- Overlapping sections.
- Direct children outside their intended section.
- Multiple active pages for the same product area.
- Multiple component sets with the same noun.
- Similar components differing only by tiny raw-value changes.
- Raw hexes, raw font sizes, raw shadows, and arbitrary spacing values.
- Screenshot-cropped assets used as reusable component internals.
- Components in route-state boards that are not promoted to library pages.
- Component pages that contain screenshots/evidence without labels.
- Missing descriptions on canonical items.
- Missing source paths or broken docs/dev-resource links.
- Empty or failed design-system search results for known app component names.
- Stale Ready-for-dev status or unresolved Changed status.
- Duplicate variants that visually overlap.
- Broken variant combinations or missing property defaults.
- Deprecated items in active sections.
- Long historical process notes in runtime component descriptions instead of
  concise source/use guidance.
- Style-guide examples that do not use the variables/components they teach.

Required output:

- Classify each mess signal as:
  - fidelity risk
  - authorship/search risk
  - code-export risk
  - duplicate/reuse risk
  - style-guide gap
  - archive/lifecycle cleanup
  - harmless local artifact
- Provide the smallest repair path:
  - rename
  - move
  - describe
  - source-map
  - convert to component
  - bind token
  - promote to style guide
  - deprecate
  - archive
  - delete only when explicitly authorized

### 18. Style-Guide Gap And Component-Creation Recommendations

The audit should not only say "this frame is wrong." It should say when the
system is missing the elegant primitive that would make the frame naturally
right.

Required recommendations:

- Identify reusable patterns hiding inside screens:
  - repeated card
  - repeated row
  - repeated stat block
  - repeated CTA
  - repeated modal/sheet
  - repeated loading/error/empty state
  - repeated badge/status chip
  - repeated achievement/reward/progress primitive
- Identify the best canonical destination:
  - global design system
  - product component library
  - feature component page
  - route-state evidence board only
  - source map only
- Propose new component only with:
  - name
  - source app component/path
  - variants/props/slots
  - tokens used
  - states to include
  - page/section destination
  - examples needed
  - docs/description text
  - migration plan for existing duplicates
- Propose new token/style only with:
  - semantic name
  - app source or required app follow-up
  - raw value
  - usage role
  - mode/platform behavior
  - replacement for current raw values

Failure patterns:

- The audit suggests visual tweaks screen by screen when a missing component is
  the real cause.
- A one-off Figma component is created without placing it in the style guide or
  explaining why it remains local.
- New tokens are proposed from a single screenshot without checking app source
  and existing variable/style vocabulary.

### 19. Verdict Rules For App Fidelity

The audit should make precise verdicts rather than broad "looks good" claims.

Allowed verdicts:

- `Pass`: source mapping, visual evidence, app style-guide adherence,
  component reuse, placement, and relevant states are verified.
- `Pass with notes`: fidelity passes, but there are low-risk documentation or
  follow-up improvements.
- `Partial`: some fidelity dimensions pass, but meaningful gaps remain.
- `Fail - Figma stale`: app is current, Figma no longer matches.
- `Fail - App drift`: Figma/style guide are canonical, app implementation
  diverged.
- `Fail - both drift`: app and Figma disagree with the canonical style guide or
  source map.
- `Fail - system gap`: the missing style-guide component/token causes repeated
  drift.
- `Evidence only`: the artifact is useful reference but not canonical.
- `Blocked`: required evidence/tooling/access is unavailable.
- `Not inspected`: explicitly listed in exhaustive sweeps when not yet covered.

Minimum evidence for `Pass`:

- Exact Figma target identified.
- Exact app/source target identified.
- Artifact role identified.
- At least one current visual reference or documented reason visual exactness
  is out of scope.
- Token/style/component/source mapping checked.
- Placement and lifecycle role checked.
- Duplicate/lookalike search performed.
- States either covered or explicitly excepted.
- Blockers and uncertainty documented.

## Inputs The Skill Must Accept

Required:

- One Figma target in normal language, usually a URL with file key and optional
  node ID. It may point to a component, component set, frame, section, page, or
  ordinary layer.

Optional:

- One or more Figma reference URLs, including screenshot pages or screenshot
  nodes.
- Local screenshot paths, screenshot directories, contact sheets, or previous
  screenshot inventories.
- App route names, component names, user flow names, source paths, or product
  area hints.
- A requested strictness level, such as quick, normal, exhaustive, pixel-only,
  structure-only, or full app sweep.
- A platform/viewport scope, such as iOS small phone, Android large phone,
  tablet, landscape, or all currently supported app targets.
- A state scope, such as default, loading, error, disabled, selected, paywalled,
  expanded, or all production states.
- An instruction to produce only an audit, or to also create tracker rows,
  suggested fixes, or future repair prompts.

The skill must not require the user to know whether the target is a Figma page,
component, component set, frame, section, or screenshot board. It should inspect
and classify the artifact.

## Outputs The Skill Must Produce

Minimum output for one target:

- Target summary:
  - Figma file key, page, node ID, node type, node name, and URL.
  - App comparison target: route, component, file path, screenshot reference, or
    the search result explaining why no target was found.
  - Strictness used and evidence availability.
- Verdict:
  - `Pass`, `Fail`, `Partial`, `Blocked`, `Evidence only`, or `Out of scope`.
  - One plain-English reason.
- Findings:
  - Findings first, ordered by severity.
  - Each finding has severity, category, evidence, expected behavior, actual
    behavior, affected Figma node(s), affected app source or screenshot(s), and
    the smallest recommended fix.
- Compliance checklist:
  - A checklist with pass/fail/partial/not-applicable statuses for every
    applicable category below.
- Coverage ledger:
  - States, viewports, platforms, app sources, Figma nodes, screenshots, and
    known exceptions covered or missed.
- App-fidelity match ledger:
  - Runtime environment, route/flow identity, geometry, colors, typography,
    style-guide adherence, component identity, project placement, visual
    rendering details, copy/data, states, interaction/motion, accessibility,
    platform-native behavior, app source usage, screenshot/golden evidence, and
    messy drift signals.
- Authorship ledger:
  - Naming health, description completeness, search aliases, documentation
    links, Dev Mode/code-export readiness, Ready-for-dev status, and
    canonical-owner clarity.
- Style-guide gap ledger:
  - Missing or stale Figma variables/styles/components, missing app-to-Figma
    mappings, one-off values that should be promoted, and recommended new
    components/tokens with source paths and canonical destinations.
- Duplicate/stale artifact ledger:
  - Canonical owner, duplicate candidates, stale screenshot-only copies,
    lookalikes, wrapper/fork rationale, and delete/rename/relabel guidance.
- Verification receipts:
  - Commands/tool calls used, file paths read, Figma readbacks, screenshots
    captured, visual diffs generated, and blockers.
- Repair plan:
  - Ordered fixes split into Figma repair, app repair, source-map repair,
    screenshot/evidence repair, and follow-up audit.

Output for exhaustive multi-surface audit:

- A tracker-ready table with one row per route/component/state/asset token.
- A summary count by status, phase, owner, product area, severity, and blocker.
- A page/component matrix like the Poker Skill tracker: source row, Figma link,
  app source, status, priority, owner, phase, evidence link, and notes.
- A style-guide completion matrix: app primitive/token/component, Figma
  equivalent, coverage status, missing states, duplicate candidates, and
  promotion/deprecation action.
- A short "next audit slice" recommendation based on highest-risk gaps.

## Severity Model

- `P0`: Cannot be treated as a reference. It will cause wrong implementation,
  wrong design review, or incorrect parity claims.
- `P1`: High-confidence app drift, broken source mapping, or missing critical
  state/viewport coverage.
- `P2`: Important durability, componentization, naming, token, accessibility,
  or handoff gap.
- `P3`: Cleanup, documentation, metadata, or low-risk organization issue.
- `Info`: Correctly explicit exception, platform-owned behavior, or useful
  future improvement that is not a current fidelity defect.

## Audit Workflow Requirements

### 1. Resolve And Classify The Figma Target

Specific checks:

- Parse Figma file key and node ID from URLs.
- Convert URL node IDs from `2085-836` style to API/MCP `2085:836` style when
  needed.
- Identify whether the target is a page, section, frame, component set,
  component, instance, group, vector, text, image, screenshot board, or ordinary
  layer.
- Record the page name, parent section, immediate parent chain, bounds, layout
  mode, size, component identity, variant properties, and visible/hidden status.
- Capture a Figma screenshot of the exact target when possible.
- If the URL points to a page or section, enumerate direct children and classify
  which are canonical components, screenshots, evidence, source maps, research,
  drafts, or ambiguous.
- If MCP/API access fails, mark inspection `Blocked` with the exact missing
  permission/tool/source.

Pass conditions:

- The target node is identified unambiguously.
- The audit states what kind of artifact it is and what kind of proof is
  possible for that artifact.
- The skill does not compare a page-level screenshot to a single app component
  without saying so.

Failure patterns:

- Treating a screenshot board as component truth.
- Treating a component set container screenshot as proof that all variants are
  valid.
- Auditing the wrong page because current Figma page context changed.
- Failing to capture or read back the exact selected node.

### 2. Build The Candidate App Match Set

Specific checks:

- Search Figma component descriptions, documentation links, text notes, shared
  plugin data where accessible, Code Connect maps, node names, section names,
  and nearby source-map cards for app source paths or code identifiers.
- Search app code for matching component/class/widget names, route names,
  asset keys, enum/state names, visible text, screenshot filenames, test IDs,
  semantics labels, and design-token names.
- Search existing app screenshot directories, contact sheets, and screenshot
  inventories for matching route/surface names or OCR-visible text.
- Use screenshot-reference Figma nodes, if supplied, as visual candidates but
  distinguish screenshot-derived truth from code/source truth.
- Prefer canonical app route/component ownership over visually similar
  wrappers.
- If several candidate app targets exist, return the top candidates with
  evidence and pick the best one only when evidence is strong.

Pass conditions:

- The chosen app target has a source path, route path, component name,
  screenshot, or explicit reason it is evidence-only/out-of-scope.
- Ambiguous matches are named and resolved, not hidden.

Failure patterns:

- Matching only by a superficial name such as `Button`.
- Ignoring a source path already present in a Figma description.
- Treating feature-specific wrappers and global primitives as duplicates when
  the app intentionally composes them.

### 3. Establish The Source Of Truth

Specific checks:

- Identify the app source owner:
  - route file
  - screen/widget/component file
  - design token file
  - typography source
  - asset registry or generated asset key
  - animation/motion source
  - content/remote/dynamic source
- Identify the Figma source owner:
  - page
  - section
  - component set
  - component
  - screenshot/reference board
  - source-map/evidence card
- Determine whether the target is intended to be:
  - canonical component truth
  - route-state truth
  - screenshot evidence
  - asset reference
  - source map
  - competitor/research reference
  - draft/exploration
  - deprecated/superseded
  - out of scope
- Require explicit labeling for evidence-only or out-of-scope artifacts.
- Confirm descriptions/source notes name actual app files where component truth
  is claimed.

Pass conditions:

- Canonical components name their app source.
- Evidence artifacts cannot be mistaken for canonical components.
- The audit can say who owns fixing each side.

Failure patterns:

- No app source path on a canonical-looking component.
- Screenshot evidence placed on component-library pages with no label.
- Figma contains multiple "canonical" versions of the same product component.

### 4. Pixel And Visual Fidelity

This category should be strict only when rendered references are available.

Specific checks:

- Capture/render the exact Figma target at a known scale.
- Capture or locate the matching app screenshot at the same platform, viewport,
  state, theme, and content where possible.
- Normalize only what is explicitly safe:
  - device chrome excluded or included consistently
  - safe-area handling consistent
  - same pixel ratio or documented scale transform
  - same font rendering platform when comparing exact pixels
  - same crop target and bounds
- Compare:
  - absolute dimensions and aspect ratio
  - bounding boxes
  - alignment and offsets
  - padding/insets
  - gap/spacing
  - radii
  - fills/strokes
  - shadow/effect geometry
  - typography size, weight, line height, letter spacing, text case
  - image asset content and crop/scale mode
  - icon dimensions/viewBox/visual bounds
  - z-order/layering
  - opacity/blend modes
  - scroll position
  - overflow/clipping
  - content labels and values
- Produce a visual-diff note when possible:
  - match threshold used
  - ignored regions
  - dynamic regions
  - residual diff count/percentage if tooling supports it
- For custom paint, canvas, parallax, animation, or platform-rendered effects,
  separate what Figma can represent natively from what requires screenshot or
  source-note proof.

Pass conditions:

- Pixel-match claims cite both a Figma render and an app/reference render.
- Dynamic or platform-owned regions are excluded explicitly, not silently.
- Differences are measured when possible, not described vaguely.

Failure patterns:

- Calling visual parity from metadata alone.
- Comparing iOS Figma to Android app screenshots without declaring platform
  differences.
- Treating Figma-restored text/image render failures as design defects without
  checking renderer limitations.

### 5. Layout Structure

Specific checks:

- UI containers use Auto Layout when layout is content-driven.
- `Hug`, `Fill`, and `Fixed` match actual behavior:
  - Hug for content-sized parents.
  - Fill for children that absorb available space.
  - Fixed for invariant icons, avatars, cards, slots, and control anchors.
- Min/max width/height exist where text, localizations, or responsive containers
  need guardrails.
- Auto Layout wrap is used for wrapping chips/grids where applicable.
- `Ignore auto layout` is used only for overlays, badges, sticky/floating
  pieces, tooltips, custom z-order, or similar anchored exceptions.
- Constraints are correct for non-Auto-Layout children and ignored children.
- Groups are absent from reusable UI except narrow vector-art cases.
- No fixed-size text boxes clip realistic content.
- No direct section child overflows its section.
- No top-level sections overlap.
- Custom-painted table/canvas/game scenes explicitly justify free-form layout.

Pass conditions:

- The Figma item can survive content changes that the app supports.
- Layout intent maps to the app layout mechanism, even when the app is Flutter
  rather than CSS.

Failure patterns:

- Manual eyeballed gaps.
- Spacer frame clutter where gap/padding variables should exist.
- Fixed widths where app uses flexible layout.
- Text collisions in long-copy or text-scale stress.

### 6. Componentization And Reuse

Specific checks:

- Reusable UI is represented as a component, component set, or instance.
- Feature screens compose global primitives where the app does.
- Feature-specific wrappers are documented as wrappers/forks with a reason.
- Detached lookalike frames are not counted as component coverage.
- Main components/component sets live on the correct library/product page.
- Variant axes map to real app enum/state/prop/view-model fields.
- Boolean properties map to real booleans and use positive names.
- Instance swap properties are used for guarded single replacements such as
  icons and avatars, with preferred values.
- Text properties expose labels/titles/amounts where app content changes.
- Nested instance properties expose meaningful child controls without exploding
  parent variants.
- Slots are used for flexible composition where the app has container/content
  structure, such as cards, modals, layout shells, repeated rows, or page
  regions.
- Slots have descriptions and preferred instances where ambiguity would cause
  drift.
- Variant combinations are unique and readable through Figma API/MCP.
- Component sets have no read errors, stacked variants, hidden broken variants,
  or overlapping children.
- Every component and component set has a short description when it is
  canonical.
- Icons are separate searchable components unless a specific local reason
  justifies variants.

Pass conditions:

- The component model mirrors production concepts closely enough that a
  developer or AI agent can map it to code without guessing.

Failure patterns:

- Mega-components with variant explosion.
- Icon libraries built as one giant icon variant dropdown.
- Boolean-as-variant or variant-as-boolean confusion.
- Detached instances used because the component does not expose the needed
  controls.
- Slot-less cards/modals/page shells duplicated for each content arrangement.

### 7. Token, Variable, Style, And Source Syntax Parity

Specific checks:

- Colors, spacing, radii, opacity, stroke, typography numbers, and shadow
  parts come from variables/styles where Figma supports them.
- Raw values are sampled and matched against expected token values.
- Variables use semantic names rather than color-bound or page-specific names.
- The token stack is tiered:
  - primitive/raw values
  - semantic intent values
  - component-specific values
- Component tokens alias semantic tokens rather than primitives unless there is
  a documented exception.
- Variables have useful descriptions when published or source-critical.
- Variables have scopes that reduce misuse.
- Variables include platform code syntax where useful.
- Variable modes represent real product context:
  - light/dark
  - density
  - brand
  - locale/string
  - breakpoint/device
  - high contrast
  - reduced motion
  - subscription/validation/product states where appropriate
- Styles remain only where they own bundled decisions:
  - text styles
  - effect styles
  - gradient styles
  - image fill styles
  - grid styles
- Dev Mode variable details or code syntax are sufficient for developers to map
  values back to the app.
- DTCG alignment is checked for token export/import plans:
  - `$value`
  - `$type`
  - `$description`
  - alias/reference shape
  - stable token naming
  - no illegal alias-breaking names in exchange formats

Pass conditions:

- Design values can be traced from Figma to app token source and back.
- Hard-coded values are either absent or explicitly justified.

Failure patterns:

- Raw copied hexes in canonical components.
- Component-specific tokens pointing directly at raw primitives.
- Variables scoped to everything.
- Missing app token source path or code syntax on source-critical variables.

### 8. Typography And Text Rendering

Specific checks:

- Font family, size, weight, line height, letter spacing, case, alignment, and
  text style match app source.
- Figma fonts are actually available; substitutions are documented.
- Text boxes use auto height/wrapping behavior compatible with content changes.
- Text styles map to app typography tokens.
- String variables/text properties are used when text drives multiple nodes or
  repeated labels.
- Long-copy, localization, and text-scale stress are checked for product-critical
  screens.
- Platform font differences are declared when comparing iOS/Android/Web/Flutter
  renders.

Pass conditions:

- Text visually matches the app and structurally survives realistic content.

Failure patterns:

- Inter placeholders where the app uses Blinker or app-specific typography.
- Fixed 1px or clipped text boxes from generation/import.
- Case and letter spacing mismatches hidden by similar visual size.

### 9. Asset And Icon Parity

Specific checks:

- Every image-backed Figma primitive maps to a runtime asset path, generated
  asset key, package path, URL policy, or manifest/source map.
- Image fills are read back; upload/hash success is not enough.
- Figma image scale mode/crop matches app rendering.
- Asset dimensions and pixel density match app use.
- Icons map to app vector/image sources and exact intended draw size, visual
  slot size, and hit target size.
- Decorative assets, dynamic remote assets, generated native assets, audio,
  JSON content, and runtime-only manifests are marked evidence-only or
  out-of-scope when not visual UI truth.
- Asset reference boards are labeled as reference/source maps unless actual
  components instance the assets.
- No short-lived MCP/API asset URLs are treated as runtime source.

Pass conditions:

- A future implementer can find the real asset and know whether Figma owns a
  component, a reference, or only evidence.

Failure patterns:

- Screenshot-cropped images used as canonical component assets.
- Icons with wrong viewBox/draw size but similar appearance.
- Runtime asset registry ignored in favor of visual memory.

### 10. State Coverage

Specific checks:

- Product-critical states are represented or explicitly excepted:
  - loading
  - empty
  - error
  - fatal error
  - retry
  - config missing
  - auth recovery
  - signed out
  - signed in but onboarding incomplete
  - permission pre-prompt
  - push notification permission
  - ATT pre-prompt
  - offline-adjacent recovery
  - sync/hydration waiting
  - locked
  - paywalled
  - no energy
  - purchase issue
  - restore purchase
  - disabled
  - pressed
  - loading button
  - selected
  - incorrect
  - correct
  - partial progress
  - perfect completion
  - friend request pending
  - invite accepted/invalid
  - share preview
  - quit confirmation
  - snackbar
  - busy modal
  - route-backed bottom sheet
  - full-height modal
- State names in Figma variants map to app enums, booleans, view models, or
  route states.
- Screenshot-only states are not counted as reusable component coverage unless
  that is intentionally the scope.
- Unrepresented states are marked missing with app source evidence.

Pass conditions:

- Figma covers the states users can actually see, not only the happy path.

Failure patterns:

- Missing loading/error/paywall/disabled states.
- Figma states invented from design intuition but absent from the app.
- App states hidden behind feature flags not represented or documented.

### 11. Platform, Viewport, Safe Area, And Responsiveness

Specific checks:

- Platform differences are covered when app code differs:
  - iOS
  - Android
  - web, if relevant
  - platform-owned system UI
  - native permission sheets
  - safe area/system gesture handling
  - touch feedback/shadow differences
- Viewport coverage is explicit:
  - small phone
  - large phone
  - tablet
  - landscape
  - foldable/wide if product-supported
- Responsive behavior is represented through Auto Layout/min/max/wrap, multiple
  variants, source notes, or screenshot evidence.
- Scroll behavior and sticky/fixed elements are documented.
- Fixed-format exceptions, such as card sprites or game tables, are documented.

Pass conditions:

- The audit can say which viewport/platform the Figma item represents and what
  remains unverified.

Failure patterns:

- Single iPhone-sized frame claimed as complete app coverage.
- Tablet/landscape absent with no out-of-scope note.
- Safe-area differences hidden in screenshot crop.

### 12. Interaction, Prototype, Motion, And Timing

Specific checks:

- Interactive states have variants or prototype states where meaningful.
- Prototype variables/conditionals are used when they represent real state
  transitions and reduce duplicate frames.
- Motion-heavy components have:
  - static key states
  - source timing/easing notes
  - code owner path
  - reduced-motion/accessibility note where applicable
- Runtime-only animations remain code-owned but have visual/evidence coverage.
- Smart Animate layers have stable matching names, hierarchy, and layer type if
  Smart Animate is used.
- Gestures and pointer interactions are documented when not visible in static
  designs.

Pass conditions:

- Developers know the app behavior beyond static appearance.

Failure patterns:

- Animation screenshots treated as complete motion spec.
- Missing reduced-motion or pause/disable notes for non-essential motion.
- Smart Animate broken by renamed or auto-generated layers.

### 13. Accessibility And Inclusive Design

Specific checks:

- Text contrast and meaningful non-text contrast are checked against WCAG 2.2
  where colors are known.
- Interactive target size and spacing are checked against platform/app policy
  and WCAG target-size expectations where applicable.
- Focus-visible or focus-equivalent states exist for keyboard/web surfaces and
  are documented where relevant.
- Accessibility labels, roles, reading order, focus order, and semantic hints
  are annotated or source-mapped for non-obvious controls.
- Do not rely on color alone for status where the app requires non-color cues.
- Motion triggered by interaction has a reduced/disabled path when non-essential
  and relevant.
- Modal/sheet semantics, route-backed overlays, and blocked-background behavior
  are noted.
- Text scaling and long-copy resilience are checked for critical content.

Pass conditions:

- The Figma item carries enough accessibility intent that the app can implement
  or verify it without guessing.

Failure patterns:

- Icon-only actions with no accessible name/source note.
- Disabled/focus/error states absent.
- Low-contrast component states reused throughout a system.

### 14. Metadata, Naming, Searchability, And Organization

This is the main authorship-quality section. It answers whether the Figma item
can be safely found, understood, reused, exported, mapped to code, maintained,
and audited later. Treat this as product-critical metadata, not cosmetic
cleanup.

Specific checks:

Naming architecture:

- Component names are stable, semantic, and code-aligned.
- Names describe product role, not current paint, temporary layout, screenshot
  origin, or implementation history. `Paygate/Core Paywall State` is useful;
  `Blue Big Paywall Copy 2` is not.
- The file uses one preferred term for each concept. If the app calls it a
  paywall, do not mix `Paywall`, `Paygate`, `Upgrade`, and `Subscribe Modal`
  without explicit wrapper/fork reasons.
- Slash-separated hierarchy groups related components in the Assets panel and
  Instance menu without burying the useful noun too deep.
- Page names and section names communicate role and ownership: component
  library, route states, screenshot evidence, asset reference, research,
  source map, sandbox, archive, or handoff.
- Component set names represent the family; variants represent states or
  dimensions. Do not encode all variant axes into the component-set name.
- Variant property names are descriptive and stable, not generic `Variant`,
  `Property 2`, or `Type 3`.
- Variant values are unique, meaningful, and code-mappable. They should match
  app enum values, prop values, or state names where practical.
- Component property names are consistent across the library. Do not mix
  `Show Icon`, `Has icon`, `Icon Visible`, and `With Icon` unless the
  difference is intentional and documented.
- Boolean properties use positive phrasing so `true` means present, visible, or
  enabled.
- Names avoid author initials, dates, personal shorthand, historical repair
  labels, and process residue on canonical surfaces.
- Internal-only atomic helpers use a documented prefix such as `_` or `.` and
  are hidden from publishing where appropriate.
- Deprecated or superseded names include a replacement target in the
  description and are absent from canonical working sections unless the section
  is explicitly an archive/deprecation area.

Layer naming:

- Layers with structural meaning are named semantically:
  - `Card Container`
  - `Product Image`
  - `CTA Button`
  - `Avatar Slot`
  - `Error Message`
  - `Focus Ring`
  - `Scrim`
  - `Safe Area Spacer`
- Auto-generated names such as `Frame 123`, `Rectangle 47`, `Group 12`,
  `Vector 8`, and `Image 5` are absent from canonical components unless the
  node is decorative vector internals with no handoff meaning.
- Text layers that map to code props are named for their content role, not their
  current words: `Title`, `Subtitle`, `Amount`, `CTA Label`, `Error Text`.
- Slot layers are named by region and expected content, such as
  `Header Slot`, `Media Slot`, `Action Row Slot`, or `Body Content Slot`.
- Layers used by Smart Animate retain stable names, type, and hierarchy across
  states.
- Exportable layers use names that would make sense as exported filenames if
  they leave Figma.

Descriptions and documentation links:

- Main components, component sets, important variants, styles, and variables
  have descriptions when they are canonical, published, source-critical, or
  likely to be reused.
- Descriptions are short but complete enough to be useful in Figma search, the
  Assets panel, the right sidebar, Dev Mode, MCP context, and future audits.
- Component descriptions include:
  - what the component is
  - when to use it
  - when not to use it if misuse is likely
  - app source path or code component
  - source route/screen owner when route-state truth is claimed
  - variant/property mapping to app props, enums, booleans, view models, or
    state names
  - token/source references for important colors, type, spacing, radii, motion,
    and assets
  - accessibility obligations such as label, role, focus order, reading order,
    target size, or semantic hint
  - platform/viewport scope if the component is not universal
  - exactness status: exact, source-shaped, screenshot-derived, evidence-only,
    partial, or intentionally approximate
  - replacement target if deprecated
- Descriptions include search aliases deliberately. For example, a canonical
  `Paywall` component may include `paygate`, `subscription`, and `upgrade` as
  aliases if those are real team search terms.
- Descriptions do not become long process diaries. Put long rationale,
  screenshots, source-map tables, or phased repair history in nearby docs or
  source-map frames.
- Documentation links point to durable destinations:
  - app source path or repository URL
  - design-system docs
  - Storybook/equivalent component docs
  - token documentation
  - source-map/audit doc
  - product spec or ticket when relevant
- Broken, private-without-access, or stale documentation links are audit
  findings.
- Library publish descriptions summarize meaningful changes. Auto-generated
  diffs are not enough for release history.

Searchability:

- The item can be found by:
  - product term
  - code component name
  - route/screen name
  - common team alias
  - state name
  - asset name
  - token name
  - domain noun
- Component descriptions are used as search metadata, not just human prose.
- Synonyms live in descriptions, not as duplicate component names.
- Components are organized so Assets panel browsing works even without exact
  search terms.
- Related components share predictable hierarchy and terminology, so an auditor
  can find siblings by changing one path segment.
- Evidence and research frames are searchable as evidence, not as reusable
  components.
- The audit tests searchability by querying at least the obvious code noun,
  product noun, and user-provided term when tool access allows it.

Code-export and AI-agent readability:

- The Figma item follows the structure Figma recommends for better code:
  components, Code Connect where available, variables for tokens, clear
  semantic names, Auto Layout, annotations for non-visual behavior, and dev
  resources.
- A developer inspecting the item in Dev Mode can see useful layer names,
  component identity, component properties, variables/styles, documentation
  links, and relevant dev resources.
- `get_design_context` or equivalent structured context would expose design
  intent rather than a pile of anonymous absolute-positioned layers.
- Code snippets or generated context should point toward existing app
  components through Code Connect, source notes, or design-system rules instead
  of encouraging generated duplicate code.
- Figma-generated React/Tailwind or HTML/CSS output is treated as a design
  representation, not production code style. The audit checks whether the
  Figma structure is good enough to translate into the app's actual framework
  and conventions.
- Make/MCP readiness requires that source components, variables, styles, and
  component guidance are granular and routable. A single giant guideline note
  on a page is weaker than component- and token-specific guidance.
- Exportable assets have intentional export settings or clear source-image
  policy. Dev Mode should not auto-detect the wrong layer as the asset.
- If file permissions disable Dev Mode code or asset copying, the audit records
  that as a handoff blocker or account-policy constraint.

Authorship workflow hygiene:

- A canonical component should pass this sequence before being treated as
  reusable:
  - search existing components and libraries first
  - identify the app source owner
  - choose the canonical name and hierarchy
  - build from real components/instances where possible
  - bind variables/styles/tokens
  - expose properties/variants/slots that match app state
  - name structural layers
  - write component, set, variant, style, and variable descriptions where
    applicable
  - add documentation links/dev resources
  - annotate non-visual requirements
  - check duplicate/lookalike candidates
  - read back component properties, variables, descriptions, and bounds
  - capture a screenshot of the final target
  - update the tracker/source map
- Ready-for-dev status is not valid until source mapping, state coverage,
  authorship metadata, and duplicate disposition are complete.
- Changed ready-for-dev items require a reason or re-audit note so developers
  know what changed.
- Authorship is maintained across edits. A repair that fixes pixels but strips
  descriptions, property names, variable bindings, or documentation links is a
  regression.

Page and section organization:

- Component-library pages contain canonical components, component sets,
  component docs, and compact source notes.
- Screenshot pages contain screenshot/reference/evidence boards and are labeled
  as such.
- Asset reference pages contain asset inventories/source maps and are not
  counted as component coverage unless components instance the assets.
- Research/competitor pages are marked research-only.
- Sandbox/exploration pages are separated from published or canonical pages.
- Archive/deprecation pages are explicit and do not leak deprecated components
  into canonical search paths without replacement notes.
- Top-level sections define reviewable scope and Ready-for-dev units.
- Sections have no loose siblings that should be inside them, no overlap, and
  no direct child overflow unless documented.
- Cover/release-note pages exist when auditing a library intended for broad
  reuse.

Pass conditions:

- A designer can find the right thing and use it without asking what it is.
- A developer can inspect it and map it to app code without guessing.
- An MCP or AI coding agent can read the structure and generate code that uses
  the existing system instead of rebuilding lookalikes.
- A future auditor can tell whether the item is canonical, evidence-only,
  deprecated, partial, or out of scope.

Failure patterns:

- Search fails because names describe visual styling instead of product role.
- Missing descriptions on source-critical components.
- Duplicate canonical names across pages.
- Descriptions contain no app source, no aliases, no usage rule, and no
  exactness status.
- Variant property names remain generic after combining variants.
- Ready-for-dev sections contain unlabeled screenshot references or draft
  frames.
- Code export sees anonymous frames and raw values rather than components,
  variables, semantic layers, and annotations.
- A repair pass preserves visual appearance but destroys searchability,
  documentation links, or source mapping.

### 15. Duplicate, Stale, And Lookalike Detection

Specific checks:

- Identify the canonical owner before judging duplicates. The owner can be a
  global primitive, feature wrapper, route-state component, screenshot evidence
  board, asset reference, or source-map row.
- Search same file and relevant library pages for same/similar:
  - component names
  - component set names
  - source paths
  - visible text
  - dimensions
  - asset hashes
  - screenshot crops
  - variant axes
  - rendered appearance
- Search by aliases from descriptions, not only exact component names.
- Compare both structure and use. Two components that look similar may be valid
  if one is a global primitive and one is a feature-owned wrapper; two
  components that look different may still be duplicates if they claim the same
  app source and state.
- Classify candidates:
  - canonical owner
  - feature wrapper
  - legitimate fork
  - evidence-only screenshot
  - research reference
  - stale/deprecated/superseded
  - broken/generated/approximation
  - delete candidate
- Check whether duplicates have explicit wrapper/fork reasons.
- Check for forbidden/stale labels in canonical pages:
  - `approx`
  - `fake`
  - `stale`
  - `legacy`
  - `temporary`
  - `repair candidate`
  - `needs audit`
  - `do not use`
  - `deprecated` without replacement
- Check if Figma duplicates disagree with app composition.
- Check whether duplicate candidates have different token bindings, typography,
  asset sources, dimensions, or state coverage. Visual similarity is not enough
  to prove parity.
- Check whether duplicate candidates are still published or available in the
  Assets panel. A stale component hidden on an archive page is lower risk than
  a stale published component with the same search terms as the canonical
  family.
- Check whether descriptions or source-map notes point duplicate users toward
  the correct replacement.
- Check whether component analytics, where available, suggest that a
  deprecated/stale component still has active usage before recommending removal.
- Require a migration/deprecation plan for published duplicates:
  - mark deprecated in name and description
  - name the replacement
  - preserve or migrate instances where practical
  - publish with a clear description
  - remove only after usage is understood
- For unshipped generated/draft duplicates, prefer deletion or relabeling as
  evidence/research over preserving confusing "old" copies on live pages.

Pass conditions:

- There is one canonical owner per product component or a clear wrapper/fork
  story.
- Search results and Assets panel browsing make the canonical choice obvious.
- Deprecated or duplicate artifacts cannot be mistaken for current app truth.

Failure patterns:

- Multiple button/card/table/nav systems with no source disposition.
- Stale screenshot frames sitting beside canonical components.
- Old generated components preserved for history on live pages.
- Duplicate components share one app source path but disagree on props, tokens,
  or dimensions.
- A deprecated component has no replacement or remains published/searchable as
  if current.
- Aliases are implemented as separate components instead of description/search
  metadata.

### 16. Dev Mode, Ready For Dev, Code Connect, And Handoff

Specific checks:

- Shippable units live in sections/frames/components that can be marked Ready
  for dev.
- Ready-for-dev/Completed/Changed status is recorded when accessible.
- Changed status is treated as handoff risk.
- Dev Mode compare-changes is used or recommended when a ready item changed
  since last app implementation.
- Annotations are reserved for non-visual requirements:
  - accessibility labels
  - focus order
  - keyboard shortcuts
  - interaction behavior
  - debounce/polling
  - analytics
  - API field mapping
  - i18n
- Code Connect mapping exists where available, or the blocker is explicit.
- Figma properties map to code props:
  - strings to labels/titles/placeholders
  - booleans to app booleans
  - variants to enums/states
  - instance swaps to icons/avatars
  - slots to child/content regions
  - nested properties to child controls
- Component-level MCP/custom instructions are checked where the org uses them.
- Dev resources/documentation links point to durable sources.
- Dev Mode inspect shows the right unit of meaning. If selecting the top layer
  exposes only a generic frame instead of a component, instance, or named
  screen state, the handoff is weak even if the frame renders correctly.
- Dev Mode list/code properties show variables/styles where the system expects
  tokens, not raw values.
- Dev Mode component preview, main-component link, documentation links, and
  component playground are useful for instances.
- The item has no unresolved `Changed` ready-for-dev state without a reason and
  re-audit path.
- Autogenerated code snippets are checked for warning signs:
  - anonymous wrapper layers
  - excessive absolute positioning
  - raw hexes and pixel constants where tokens exist
  - generic div/view names caused by bad layer names
  - duplicate component code where Code Connect or source notes should have
    pointed to an existing primitive
  - missing text/boolean/variant/slot props
- Design-system rules or project guidance can map the Figma item to:
  - component directory
  - token source
  - styling approach
  - import/export pattern
  - asset directory
  - accessibility/testing requirements
  - app-specific composition rules
- If Code Connect is unavailable, the Figma side still carries enough source
  metadata for a future Code Connect mapping:
  - component URL/node ID
  - main component or component set
  - code component path
  - prop/property map
  - variants and restrictions
  - slot/children model
  - framework/platform label
- Figma Make readiness is checked when relevant:
  - components and variables are available through the Make kit/design package
  - guidelines are granular enough for components/tokens/composition
  - top-level guidelines route to specific component/token files
  - guidance says what to use, not just what to avoid
  - generated output would use system components rather than raw HTML or
    one-off styles
- Export readiness is checked when relevant:
  - exportable icons/images are selected at the right layer
  - export settings, file formats, and scale are intentional
  - source image vs layer export is understood for image assets
  - SVG/text-outline choices are explicit where text/vector fidelity matters
  - exports are reference artifacts unless promoted through the app's asset
    pipeline

Pass conditions:

- Dev Mode and Code Connect would lead a developer or agent to the same app
  component and props that the audit selected.
- Code export or MCP design context would preserve intent, reuse, tokens, and
  layout behavior closely enough to be useful.
- Any account, seat, permission, framework, or product limitation is explicit
  rather than misreported as a design failure.

Failure patterns:

- Figma property names differ from code props for no reason.
- No Code Connect map and no documented access blocker.
- Visual annotations repeat obvious padding/color while missing behavior.
- Dev Mode code output is structurally anonymous because the file is a painting.
- Make guidelines or agent rules are too generic to prevent hardcoded duplicate
  components.
- Export layers produce the wrong image, wrong crop, wrong scale, or temporary
  MCP URL dependency.

### 17. Screenshot Reference Handling

Specific checks:

- Supplied screenshot Figma nodes are classified as reference, evidence, or
  source boards.
- Local screenshot paths are checked for date, platform, viewport, app build,
  route/state, and crop.
- Contact sheets are split or referenced to individual frames when possible.
- Screenshots are matched to app state and Figma node by:
  - visible text/OCR
  - dimensions
  - route labels
  - screenshot inventory metadata
  - visual similarity
  - page/source-map notes
- Screenshot evidence is not counted as component coverage unless the target
  item is intentionally screenshot evidence.
- Stale screenshots are flagged when app source or newer captures disagree.

Pass conditions:

- Screenshots increase confidence without replacing source-backed ownership.

Failure patterns:

- A screenshot board is mistaken for a reusable Figma component.
- Old app captures drive repairs against obsolete UI.
- Screenshot crop hides platform/safe-area differences.

### 18. App-Side Implementation Fidelity

This skill audits both sides. If Figma is correct and the app is wrong, the
finding should say that.

Specific checks:

- App code uses the intended component family, not a hand-coded duplicate.
- App implementation uses app tokens/assets, not hard-coded lookalikes.
- App route displays the state/content represented in Figma.
- App spacing/type/radii/shadows match the canonical token/component.
- App composes global primitives where the design system expects it.
- App has tests/screenshot captures for critical visual states where the repo
  already supports them.
- App implementation has platform/viewport behavior that matches the Figma
  intent or documents why it diverges.

Pass conditions:

- The audit can distinguish "Figma is stale" from "app implementation drifted."

Failure patterns:

- Blaming Figma for drift when the app bypassed a design-system primitive.
- Blaming app code when Figma is an approximation built from screenshots.

### 19. Exhaustive App Sweep Mode

When the user asks to run this over every app part, the skill must create a
matrix rather than a narrative-only report.

Specific checks:

- Enumerate app routes from route registries.
- Enumerate reusable components from design-system directories and feature UI
  directories.
- Enumerate token sources, typography, assets, animation/motion sources, and
  screenshot inventories.
- Enumerate current Figma pages, sections, component sets, standalone
  components, screenshot boards, and evidence/reference pages.
- Build route-to-Figma and component-to-Figma matrices.
- Assign one status per row:
  - `Complete`
  - `Complete - Evidence only`
  - `Complete - Out of scope`
  - `Partial`
  - `Missing`
  - `Blocked`
  - `Not inspected`
- Assign owner/product area/priority/phase/source-line/figma-link/app-source
  fields.
- Keep explicit exceptions:
  - redirects
  - QA/dev/internal routes
  - generated native assets
  - audio
  - JSON/content registries
  - remote/dynamic content
  - platform-owned system UI
  - runtime-only animations
  - account-access blockers
- Produce counts by status, phase, owner, product area, and severity.

Pass conditions:

- Every current app route/component/token/asset family is represented by a row
  or explicit exception.

Failure patterns:

- Auditing only what already exists in Figma.
- Marking broad areas complete without row-level source evidence.

## Recommended Starting Methodology For Fidelity Audits

This is not the only possible system. It is a good starting point if someone is
trying to confirm visual parity/fidelity because it is fast, evidence-ranked,
and worked against the Poker Skill Figma file plus the existing `../psmobile`
artifact structure. The skill should present it as a repeatable baseline, not
as the only valid way to audit.

The core method is:

1. Classify the Figma target.
2. Build a ranked set of app and screenshot candidates.
3. Establish what each artifact can prove.
4. Compare structure and source before expensive pixels.
5. Run exact visual comparison only against matched, normalized renders.
6. Report every finding with evidence strength, not just prose confidence.

### Method Spike Findings From Poker Skill

Observed Figma behavior:

- Node `16:2` is a page named `Screenshots 4/29`. Sparse metadata inspection
  quickly showed that it is a screenshot/evidence board rather than a component
  page.
- A guarded Plugin API sampler found `288` total nodes on `16:2`, including
  `40` frames, `159` text nodes, and `88` rectangles.
- The same sampler found `87` image-filled nodes and `36` screenshot/contact
  sheet label texts on `16:2`.
- Those screenshot labels are contact-sheet indexes such as
  `screenshots/contact-sheets/playables/single_select_with_board.png`, not
  necessarily the underlying individual app screenshot filenames.
- The Figma page contains no generic layer names in the sampled tree, which is
  a good authorship signal for screenshot evidence.
- The image-filled rectangles expose image hashes through the Plugin API. Those
  hashes are useful for duplicate detection and freshness checks inside Figma,
  but they do not by themselves identify the local app screenshot source.
- Node `1992:404` is a page named `Account Components`, not a single screen. It
  contains `1560` sampled nodes, `14` component sets, and `102` component
  variants. It is a component/state coverage board, not screenshot truth.
- The `Account Components` page has strong source-map descriptions on component
  sets, including Flutter file paths, tracker rows, variant state semantics,
  and referenced global primitives. That is strong app-source evidence even
  without screenshot evidence.
- `get_metadata` can summarize page contents before the Plugin API page is
  loaded. For Plugin API reads of a page node, the sampler must call
  `await figma.setCurrentPageAsync(page)` before traversing children.
- Plugin API property reads must be type-guarded. Page nodes do not have frame
  geometry properties, and variant component children can throw on
  `componentPropertyDefinitions`; the audit sampler must catch property-level
  read errors and report them instead of failing the whole audit.
- Code Connect lookup was blocked by plan/seat constraints during the spike.
  The skill must treat Code Connect as high-value when available, but fall back
  to component descriptions, tracker rows, local source search, and screenshot
  metadata when it is unavailable.

Observed app/artifact behavior in `../psmobile`:

- `../psmobile` already has a rich visual evidence system under
  `docs/artifacts/rn_flutter_parity_screenshots`, including latest parity
  grids, Flutter assets, RN baselines, locator packs, screenshots, JSON
  snapshots, and ASCII wireframes.
- The latest free locator packs contain per-surface manifests such as
  `docs/artifacts/rn_flutter_parity_screenshots/grids/latest_free/locator_packs/playable_kind__single_select_with_board__sample_1/manifest.json`.
- That manifest maps a content locator to a screenshot, snapshot, and wireframe:
  `screenshots/step.png`, `snapshots/step.json`, and
  `wireframes_ascii/step.txt`.
- The matching snapshot is not just visual evidence. It includes
  `lessons.v2.snapshot`, route/runtime IDs, playable kind, layout rectangles,
  model text, button state, header state, semantics nodes, and exact element
  bounds. This is a much better bridge between pixels and code than a screenshot
  alone.
- The matching ASCII wireframe is a fast readable digest of the same surface,
  including header, title, coach text, card labels, answer labels, CTA state,
  and home indicator.
- The sample locator screenshot had pixel dimensions `1179 x 2556`; a latest
  grid Flutter asset for the same playable family had dimensions `1170 x 2532`;
  the frozen RN baseline tile had dimensions `828 x 1792`. Dimensions differ
  across artifact families, so the skill must classify artifact source and
  viewport before comparing pixels.
- ImageMagick is available locally (`magick` and `compare`). Comparing a file to
  itself with `magick compare -metric AE ... null:` returned `0 (0)`, which is a
  good smoke check for deterministic diff tooling. Comparing RN and Flutter
  tiles produced nonzero residuals and should be treated as cross-platform or
  cross-device parity evidence, not a direct Figma pixel-perfect verdict.
- Exact screenshot names visible in Figma are not always exact local paths. For
  example, Figma contact-sheet labels use names like
  `screenshots/contact-sheets/playables/single_select_with_board.png`, while
  local latest grid assets use names like
  `assets/flutter/playable_single_select_with_board.png`, and locator packs use
  `playable_kind__single_select_with_board__sample_N/screenshots/step.png`.
  The audit therefore needs ranked matching, not exact filename matching only.

### Evidence Ranking

The skill should never jump straight from a Figma URL to one screenshot and call
that the match. It should build candidates and rank them.

Evidence tiers, strongest first:

- `Tier 0 - explicit bidirectional link`: Code Connect map, shared plugin data,
  component description, or tracker row naming both the Figma node and app
  source path.
- `Tier 1 - app source map`: Figma component/set description names actual route,
  widget, provider, token, tracker row, or state enum used by the app.
- `Tier 2 - screenshot manifest`: local app manifest names route/state/content,
  screenshot path, snapshot path, platform, entitlement context, capture mode,
  and generated time.
- `Tier 3 - semantic snapshot`: app QA snapshot provides route/runtime ID,
  surface kind, layout rects, model values, stable IDs, semantics labels, and
  control state.
- `Tier 4 - screenshot label`: Figma text or local path label points to a
  screenshot/contact sheet or route family.
- `Tier 5 - visual similarity`: screenshot or Figma render looks similar after
  dimensions/crop/platform are reconciled.
- `Tier 6 - name-only guess`: node names, page names, or broad labels match but
  no source, screenshot, or semantic proof exists.

Verdict rules:

- `Tier 0` or `Tier 1` can establish source ownership.
- `Tier 2` and `Tier 3` can establish the exact runtime state for app-side
  comparison.
- `Tier 4` can identify likely candidates but should not be treated as a
  pixel-perfect match.
- `Tier 5` can support a finding, but visual similarity must not override
  contradictory source evidence.
- `Tier 6` is enough to create an investigation row, not enough to pass.

### Target Classification Algorithm

For every Figma URL:

1. Parse file key and node ID.
2. Fetch sparse metadata for node type, page name, parent chain, bounds, direct
   children, and child counts.
3. If the node is a page, section, or large frame, classify its children before
   auditing it as a screen.
4. Run a guarded Figma sampler for:
   - node counts by type
   - direct child list
   - image fills and image hashes
   - text labels containing source paths, screenshot paths, tracker IDs, route
     names, component names, or state names
   - component sets, components, variants, and exposed properties
   - component descriptions
   - layout modes, constraints, fills, strokes, effects, typography, and raw
     values when the node type supports them
   - duplicate names and generic names
   - property read errors
5. Classify the target as one of:
   - canonical component
   - component set
   - route-state board
   - screenshot/contact-sheet board
   - single app screenshot reference
   - style-guide/token artifact
   - asset reference
   - source-map/evidence note
   - draft/exploration
   - deprecated/superseded artifact
6. Assign an audit mode:
   - `metadata-only` for evidence boards or broad pages
   - `source-parity` for source-mapped components/state boards
   - `component-craft` for canonical components and component sets
   - `visual-parity` for single screens or exact screenshot references
   - `sweep-row` for broad app inventory entries

This prevents a broad page like `Account Components` from being judged as a
single app screen and prevents a screenshot contact sheet like `Screenshots
4/29` from being mistaken for reusable component truth.

### Candidate App Matching Algorithm

Build a candidate set from independent signals:

- Figma component/set descriptions.
- Figma page, section, frame, and component names.
- Figma visible text notes, especially source paths and screenshot labels.
- Figma Code Connect maps if available.
- Figma image fill hashes and duplicate image-fill groups.
- Existing tracker rows and parity audit documents.
- App route files and route registries.
- App design-system components.
- Feature `presentation/screens` and `presentation/widgets` directories.
- View-model/provider/state enum names.
- QA command names such as `lessons.v2.snapshot`, `puzzles.v2.snapshot`, or
  route-specific snapshot commands.
- Local screenshot manifests, latest grid assets, locator packs, snapshots, and
  wireframes.
- Visible copy and stable IDs from app snapshots.
- Asset filenames and generated asset keys.

Candidate scoring should prefer independent corroboration. A strong match is:

- same route/component/state in Figma source note
- same app file exists locally
- same state appears in code or snapshot
- same screenshot family exists locally
- same copy/stable IDs appear in semantic snapshot
- same visual structure appears in screenshot or wireframe

Ambiguous candidates should remain visible in the report. The skill should say
why it selected the top candidate and what evidence would be needed to promote
an ambiguous candidate to a confirmed match.

### Duplicate Detection Methodology

Duplicate detection should be multi-pass. No single duplicate signal is enough
because real design systems intentionally repeat state variants, instances,
icons, and screenshot references.

Figma exact-identity checks:

- Same node name under the same parent.
- Same component set name on the same page or library.
- Same component name outside a component set.
- Same screenshot label or source path repeated in multiple canonical-looking
  locations.
- Same image hash used by multiple image slots.
- Same component description source path used by multiple unrelated component
  sets.
- Same tracker row claimed by multiple unrelated nodes.
- Same Code Connect source map claimed by multiple unrelated nodes.

Figma normalized-name checks:

- Normalize case, spaces, punctuation, slashes, underscores, suffix numbers,
  and copy markers.
- Compare `Profile/Home Route State`, `Profile Home`, `profile_home`, and
  `profile-home` as likely related names.
- Treat `Component 1`, `Frame 12`, `Rectangle 8`, `Copy of`, and `Untitled` as
  authorship defects, not useful component names.
- Separate legitimate state variants such as `State=Loading` from duplicate
  canonical components.

Figma structure-signature checks:

- Same width/height/aspect ratio.
- Same layout mode, padding, gap, and child count.
- Same text-node sequence after normalizing values.
- Same fill/stroke/effect/radius signature.
- Same typography signature.
- Same variant property definitions and option sets.
- Same child component instance set.
- Same image-fill scale mode and image hash.

App duplicate checks:

- Multiple app widgets/classes produce the same visual primitive while bypassing
  an existing design-system component.
- Feature directories contain local copies of global primitives such as buttons,
  chips, cards, rows, toggles, headers, paywall cards, or profile sections.
- Multiple widgets hard-code the same color, radius, spacing, shadow, or text
  style values instead of using app tokens.
- Multiple routes maintain their own versions of shared empty/loading/error
  states.
- Multiple screenshot artifacts represent the same route/state without clear
  platform, date, entitlement, or capture-mode labels.
- Multiple Figma components map to the same app class without a documented
  wrapper/fork reason.

Classification of possible duplicates:

- `Bad duplicate`: two canonical-looking items claim the same role and neither
  explains why.
- `Legitimate variant`: repeated structure is part of one component set or state
  axis.
- `Legitimate wrapper`: a feature-specific composition wraps a global primitive
  and documents the reason.
- `Screenshot evidence duplicate`: the same image appears on a reference board
  and should be labeled evidence-only.
- `Stale duplicate`: an older component or screenshot has been superseded but
  remains findable.
- `Unknown duplicate`: visual/source similarity is strong, but ownership cannot
  be established.

Duplicate findings should include:

- primary node/path
- suspected duplicate node/path
- duplicate signal type
- evidence strength
- recommended consolidation owner
- whether the duplicate is Figma-side, app-side, screenshot-side, or mixed

### Screenshot And Pixel-Fidelity Methodology

The fastest faithful path is to treat screenshot boards as indexes and treat
individual renders as comparison targets.

Do:

- Use Figma screenshot/contact-sheet boards to discover available route and
  surface families.
- Extract screenshot label text, image slot names, image hashes, and parent
  section names from Figma.
- Locate the corresponding local app screenshot family through exact names,
  normalized names, manifest paths, route names, visible copy, and semantic
  snapshots.
- Prefer local per-surface screenshot files over contact sheets for pixel
  comparison.
- Prefer screenshots with manifest metadata over loose PNGs.
- Prefer screenshots that also have JSON snapshots and wireframes.
- Render the exact Figma node when a Figma-designed screen/component is the
  target.
- Compare the exact app screenshot for the same platform, viewport, theme,
  entitlement, locale, content state, scroll position, and dynamic state.
- Compare dimensions before pixels.
- Normalize crop only when the crop operation is explicit and reversible.
- Record device chrome, safe area, pixel ratio, scale, and viewport.
- Mask or ignore dynamic regions only when named explicitly.
- Produce both numerical diff and human-readable finding.

Do not:

- Pixel-diff an entire screenshot board against an app screen.
- Pixel-diff a downscaled contact sheet slot and call it pixel-perfect.
- Resize mismatched screenshots and treat the resulting diff as exact parity.
- Compare iOS and Android renders without declaring platform differences.
- Compare RN baseline screenshots to Flutter screenshots as Figma parity unless
  the audit target is specifically legacy-to-current app parity.
- Treat a screenshot imported into Figma as proof that a Figma component is
  componentized or implementation-ready.

Recommended comparison ladder:

- `Level 0 - inventory`: Figma node, app source, screenshot candidates, and
  evidence strength are identified. No visual parity claim.
- `Level 1 - source/state parity`: Figma source notes and app source/snapshot
  agree on route, state, content, and component ownership.
- `Level 2 - screenshot availability`: matching app screenshot and/or Figma
  screenshot reference exists with platform/viewport/date metadata.
- `Level 3 - structural parity`: semantic snapshot layout rects, wireframe,
  and Figma layout measurements agree on major regions and control states.
- `Level 4 - measured visual parity`: exact Figma render and exact app render
  are compared with declared dimensions, masks, and diff metrics.
- `Level 5 - reproducible parity`: the app screenshot can be recaptured from a
  deterministic harness, and the audit records the command, locator, state, and
  artifact paths.

Pixel-diff measurements to capture when possible:

- source image paths or node IDs
- dimensions
- pixel ratio
- absolute-error pixel count
- normalized error percentage
- RMSE or perceptual metric if available
- bounding boxes for largest visible differences
- ignored masks/regions
- crop rectangle
- platform and device
- app build/environment
- Figma render scale

For `../psmobile`, the current practical starting point is:

- Use `docs/artifacts/rn_flutter_parity_screenshots/grids/latest_free` for
  checked-in latest locator-pack evidence.
- Use `docs/artifacts/rn_flutter_parity_screenshots/grids/latest/assets/flutter`
  for broad current Flutter grid screenshots.
- Use `docs/artifacts/rn_flutter_parity_screenshots/rn_baseline` only when the
  audit explicitly needs RN-to-Flutter legacy parity context.
- Use locator-pack `manifest.json` files as the best app-screenshot index.
- Use locator-pack `snapshots/*.json` files as the best source of layout,
  semantics, route, state, and stable-ID evidence.
- Use locator-pack `wireframes_ascii/*.txt` files as a fast human-readable
  preview before opening pixels.
- Use ImageMagick as a local diff smoke tool when exact image pairs are already
  known.

### App Component To Figma Component Methodology

The audit should build two directional maps:

- `Figma -> app`: each Figma target maps to app source, route/state, screenshot
  evidence, and design-system primitives.
- `App -> Figma`: each app route/component/token maps to a canonical Figma
  component, route-state board, screenshot evidence, or explicit gap.

For each app component or route:

1. Locate the owning source file.
2. Locate token usage, child primitives, assets, motion, and state model.
3. Locate test IDs, stable IDs, snapshot commands, or visual contract tests.
4. Search Figma for matching component names, descriptions, source paths,
   tracker rows, visible copy, and screenshot labels.
5. Confirm whether the Figma target is canonical component truth, route-state
   truth, or screenshot evidence.
6. Compare props/states in code to Figma variant axes and component properties.
7. Compare design-token usage in code to Figma variables/styles/raw values.
8. Compare visual states against available screenshots/snapshots.
9. Mark missing Figma components as gaps even if screenshot evidence exists.
10. Mark app implementation drift when the app bypasses the intended primitive
    or token.

For Flutter specifically, the audit should look for:

- `design_system` primitives and token files.
- `presentation/screens` route owners.
- `presentation/widgets` feature components.
- provider/view-model files that define loading, ready, empty, error, and
  entitlement states.
- `integration_test` flows and harnesses that can capture or snapshot state.
- QA command surfaces that expose structured state.
- generated asset references and actual asset file paths.
- custom painters/canvases/table scenes that cannot be represented faithfully
  as ordinary Figma Auto Layout.

### Fast Path Versus Deep Path

The skill should default to the fast path, then escalate only when evidence is
missing or the user asks for exhaustive proof.

Fast path:

- Parse the Figma URL.
- Fetch sparse Figma metadata.
- Run a bounded guarded Figma sampler.
- Extract source paths, screenshot labels, component descriptions, image hashes,
  variant axes, and generic/duplicate names.
- Search local app source and artifacts by normalized candidate terms.
- Read the top matching manifest/snapshot/wireframe files.
- Produce a checklist with evidence tiers and likely gaps.

Deep path:

- Render the exact Figma node.
- Locate or recapture the exact app screenshot.
- Normalize crop/platform/state.
- Run numerical image comparison.
- Measure geometry, typography, color, spacing, and asset differences.
- Build a matrix row for every route/component/state/token.
- Add regression recommendations for missing visual contracts or golden
  coverage.

Escalation triggers:

- No source path on a canonical-looking component.
- Multiple Figma nodes claim the same app source.
- Screenshot labels exist but no local manifest/snapshot can be found.
- Local screenshot dimensions or platform do not match the claimed Figma target.
- Figma and app use different token values.
- Component properties do not cover app states.
- The node is a critical user-facing route, paywall, gameplay surface, auth
  surface, or design-system primitive.
- The user explicitly asks for pixel-perfect proof.

### Practical Tooling Shape

The first shipped version can be mostly prompt-driven, but it should be designed
around small deterministic helpers once repeated audits prove which outputs are
stable.

Useful helpers:

- `figma-url-parse`: return file key, node ID, normalized node ID, and URL.
- `figma-node-sample`: bounded read-only sampler for node counts, image fills,
  text labels, descriptions, variants, layout, raw styles, duplicate names, and
  property read errors.
- `figma-screenshot-index`: extract screenshot/contact-sheet labels, image slot
  names, image hashes, and parent sections.
- `app-artifact-index`: index screenshot manifests, image files, snapshots,
  wireframes, generated times, platforms, entitlements, and route/state labels.
- `app-source-index`: index routes, components, design-system tokens, feature
  widgets, assets, and QA snapshot commands.
- `candidate-ranker`: score Figma/app/screenshot candidates by evidence tier.
- `dupe-scanner`: group likely duplicates by exact identity, normalized names,
  source paths, image hashes, structure signatures, and app component usage.
- `image-diff`: compare two exact images and return dimensions, AE, RMSE,
  normalized error, masks, and crop metadata.
- `audit-matrix-writer`: emit Markdown and TSV rows for exhaustive sweeps.

The helpers should keep output bounded and should write reports only when the
user asked for a document or exhaustive sweep. They should not mutate Figma or
app files during an audit.

### Minimum Report Fields For This Method

Every finding produced by this methodology should include:

- Figma file key and node ID.
- Figma page/section/path.
- Figma artifact classification.
- App candidate path/component/route.
- Screenshot candidate paths, if any.
- Evidence tier.
- Evidence summary.
- Compliance status.
- Fidelity status.
- Duplicate/staleness status.
- Exact checks passed.
- Exact checks failed.
- Blockers and missing permissions.
- Recommended next proof step.
- Recommended repair owner.

For visual findings, also include:

- Figma render source.
- App render source.
- platform/device/viewport.
- dimensions.
- scale/crop/mask.
- numerical diff if available.
- human-readable visible differences.

For duplicate findings, also include:

- duplicate signal.
- primary artifact.
- duplicate artifact.
- whether it is bad, legitimate variant, legitimate wrapper, evidence duplicate,
  stale duplicate, or unknown.

## Required Tooling Behavior

The future skill should remain prompt-first unless deterministic tooling is
proved necessary. If scripts are added later, they must have bounded output and
clear reasons.

Required tool behavior for audits:

- Prefer read-only Figma inspection by default.
- Use Figma MCP when available:
  - `get_metadata` for sparse tree/bounds/name/type inspection.
  - `get_design_context` for style/layout/component context.
  - `get_variable_defs` for variables/styles used by the target.
  - `get_screenshot` for visual receipts.
  - `get_code_connect_map` for source mappings.
  - `search_design_system` for duplicate/canonical discovery.
- Use Figma REST when MCP is unavailable or when bulk data is needed:
  - file JSON
  - node JSON
  - rendered images
  - image fills
  - component/style metadata
- Use app-local commands to inspect source and capture app state:
  - source search
  - route/component inventory
  - screenshot directories/contact sheets
  - simulator/browser capture only when the target app workflow supports it
- Never claim a write/repair happened unless the file was read back after the
  write and visually checked.

Potential deterministic scripts, if later justified:

- Figma URL parser and node ID normalizer.
- Figma REST/MCP JSON summarizer for bounded node/component/token reports.
- Screenshot crop/diff helper with explicit thresholds.
- Tracker row generator from a route/component matrix.
- Duplicate candidate detector based on names, source paths, dimensions,
  asset hashes, and component descriptions.
- Authorship-health sampler for names, descriptions, documentation links,
  aliases, generic layer names, property names, ready status, and code-export
  prerequisites.
- Raw-value/token-binding sampler.
- Section overlap/direct-child overflow checker.

Reasons not to add scripts initially:

- Much of this work requires judgment: source ownership, wrapper/fork intent,
  screenshot relevance, and exact exception handling.
- Existing `$figma-best-practices` is prompt-only.
- Figma MCP/REST tooling already provides structured access when available.

## Acceptance Checklist For A Single-Item Audit

- [ ] The Figma target node is identified by file key, page, node ID, type, and
  name.
- [ ] The target artifact is classified: component truth, route-state truth,
  screenshot evidence, reference, source map, draft, deprecated, or out of
  scope.
- [ ] The best app comparison target is identified, with source path, route,
  screenshot, Code Connect map, or explicit blocker.
- [ ] All ambiguous candidate matches are listed if they could affect the
  verdict.
- [ ] The exact Figma target has a current screenshot or a blocker explaining
  why not.
- [ ] The app/reference target has a current screenshot/reference or a blocker
  explaining why not.
- [ ] Pixel-fidelity claims cite visual evidence, not metadata only.
- [ ] The `App Fidelity Match Surface` is applied for the target scope:
  runtime identity, route/flow identity, geometry, colors, typography,
  style-guide adherence, components, placement, rendering details, copy/data,
  states, interactions, accessibility, native/platform behavior, app source,
  screenshots/goldens, and mess/drift signals.
- [ ] Figma structure is checked against `$figma-best-practices`.
- [ ] App/source parity is checked against actual code, not memory.
- [ ] Token, typography, asset, and motion sources are traced where applicable.
- [ ] Style-guide completeness is checked: missing variables, styles,
  components, states, docs, and token/component promotion needs are listed.
- [ ] Product states are covered or explicitly missing/out-of-scope.
- [ ] Platform and viewport scope is explicit.
- [ ] Accessibility annotations/states/contrast/target-size concerns are
  checked where applicable.
- [ ] Authorship health is checked: names, descriptions, aliases,
  documentation links, source notes, variant/property labels, section role, and
  searchability.
- [ ] Code-export readiness is checked: components, Code Connect or source map,
  variables, Auto Layout, semantic layers, annotations, dev resources, and
  export settings where applicable.
- [ ] Duplicate, stale, and lookalike candidates are searched.
- [ ] Canonical owner and fix owner are named.
- [ ] Findings are severity-ordered with expected vs actual evidence.
- [ ] The output includes a repair plan and verification receipts.

## Acceptance Checklist For Exhaustive App Sweep

- [ ] Every app route has a tracker row or explicit exception.
- [ ] Every reusable app UI component family has a tracker row or explicit
  exception.
- [ ] Every design token/foundation family has a tracker row or explicit
  exception.
- [ ] Every app design-system primitive has a canonical Figma equivalent,
  explicit local-only reason, or missing-component finding.
- [ ] Every user-visible asset family has a tracker row or explicit exception.
- [ ] Every product-critical state family has component or evidence coverage.
- [ ] Every Figma page has a declared role.
- [ ] Every active Figma page and section is classified as canonical library,
  product component library, route-state coverage, screenshot/reference
  evidence, source map, audit tracker, exploration, archive, research, or
  handoff.
- [ ] Every canonical Figma component set reads cleanly.
- [ ] Every canonical component has an app source path or source-map note.
- [ ] Every repeated screen-level pattern has either an existing canonical
  component, a documented wrapper/fork reason, or a recommended component
  creation/promote-to-style-guide action.
- [ ] Every canonical component, component set, important variant, source
  variable, and source style has a useful name and description where Figma
  supports it.
- [ ] Search aliases are in descriptions, not duplicate component names.
- [ ] Every screenshot/reference page is labeled as evidence or research.
- [ ] Every duplicate component family has a canonical owner or fork/wrapper
  reason.
- [ ] Every deprecated or superseded artifact has a replacement or is separated
  from canonical pages.
- [ ] Every Ready-for-dev section has complete authorship metadata and no
  unresolved Changed status.
- [ ] Every raw-value/token-binding exception is known.
- [ ] Every platform/viewport exception is known.
- [ ] Every screenshot/golden/reference artifact has build/platform/capture
  metadata or is marked low-confidence/stale.
- [ ] The tracker has status, owner, product area, priority, source, Figma link,
  and blocker fields.
- [ ] Status counts reconcile to row counts.

## Report Template

Recommended shape:

```markdown
# Figma App Fidelity Audit - <Target Name>

Date:
Target Figma URL:
Reference URL(s):
App source target:
Strictness:

## Verdict

<Pass/Fail/Partial/Blocked> - <one reason>

## Findings

| Sev | Category | Finding | Evidence | Expected | Actual | Fix |
| --- | --- | --- | --- | --- | --- | --- |

## Compliance Checklist

| Check | Status | Evidence | Notes |
| --- | --- | --- | --- |

## Visual Fidelity

- Figma render:
- App/reference render:
- Diff/measurement:
- Dynamic/ignored regions:

## App Fidelity Match Surface

- Runtime/app build:
- Route/flow/screen identity:
- Geometry/layout:
- Color/fill/stroke/opacity:
- Typography/text rendering:
- Style-guide adherence:
- Component identity/reuse:
- Project placement/lifecycle:
- Rendering details:
- Copy/data/content:
- State/edge-case coverage:
- Interaction/motion/feedback:
- Accessibility/semantics:
- Platform/native-system behavior:
- App source/runtime primitive use:
- Screenshot/golden evidence:
- Mess/drift signals:

## Source Mapping

- Figma canonical owner:
- App canonical owner:
- Tokens:
- Assets:
- Motion:
- Code Connect/MCP:

## Authorship Quality

- Naming:
- Descriptions:
- Search aliases:
- Documentation links:
- Section/page role:
- Dev Mode/code export:
- Ready-for-dev status:
- Authorship defects:

## Style Guide And Component Gaps

- Missing variables/styles:
- Missing component families:
- Repeated one-off patterns:
- New component recommendations:
- New token/style recommendations:
- Promotion/deprecation actions:

## Coverage

- States:
- Platforms:
- Viewports:
- Accessibility:
- Screenshots:
- Exceptions:

## Duplicate And Stale Artifacts

| Candidate | Type | Evidence | Disposition |
| --- | --- | --- | --- |

## Repair Plan

1. ...

## Verification Receipts

- ...
```

## Future Skill Package Shape

Likely package:

- `skills/figma-app-fidelity-audit/SKILL.md`
  - Lean runtime contract, triggers, workflow, outputs, and boundary with
    `$figma-best-practices`.
- `skills/figma-app-fidelity-audit/references/check-catalog.md`
  - The detailed checklist distilled from this document.
- `skills/figma-app-fidelity-audit/references/matching-and-evidence.md`
  - How to find the right app/Figma/screenshot comparison target.
- `skills/figma-app-fidelity-audit/references/report-contract.md`
  - Single-item and exhaustive-sweep output templates.
- Optional scripts only after prompt-only use shows repeated deterministic
  failures.

Trigger description target:

> Deeply audit a supplied Figma node/page/component/screen against a real app
> implementation and optional screenshot references for pixel fidelity,
> source-backed component parity, Figma file-craft quality, metadata,
> duplicate/stale artifacts, state/viewport coverage, and handoff readiness.
> Use for Figma-vs-app gap reports and exhaustive parity matrices; do not use
> to implement code from a design or for generic visual taste critique.

Nearest lookalike:

- `$figma-best-practices`: audits Figma file craft generally. This new skill
  should load it or its doctrine, then add app-source and visual-fidelity audit
  obligations.

Runtime stance:

- Prompt-first, audit-only by default.
- Read-heavy.
- No repair writes unless the user asks for repair.
- No pixel-perfect pass without visual receipts.
- No source parity pass without app source or explicit screenshot-only scope.

## Open Decisions Before Creating The Skill

- Exact name: `figma-app-fidelity-audit`, `figma-parity-audit`, or
  `figma-source-parity-audit`.
- Whether to support non-app artifacts, such as websites, design-system-only
  libraries, or Figma Make prototypes, in the first version.
- Whether the exhaustive mode should ship a deterministic tracker generator or
  remain prompt-authored initially.
- Which visual diff tool is the repo-standard default for Flutter/mobile app
  screenshots.
- Whether the skill should have a psmobile-specific reference pack later, or
  stay fully reusable and rely on repo-local AGENTS/docs for app commands.
- How to handle Code Connect gaps for Flutter, since official Code Connect docs
  are strongest for React/React Native and Figma account access can block live
  mapping.

## Bottom Line

The future skill should make "Figma looks close" an unacceptable stopping
point. A passing audit means the Figma item is visually faithful to the live app
or supplied reference, structurally honest as a Figma artifact, mapped to real
app source/tokens/assets/states, findable by humans and agents, and explicit
about every exception that prevents full parity.
