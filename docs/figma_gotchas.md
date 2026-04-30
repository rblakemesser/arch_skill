# Figma MCP Gotchas

This is a field note for Figma component-library work through Codex MCP. Keep it command-first and update it when a real Figma run exposes a repeatable failure mode.

## Required Setup

- Load and follow `figma-use` before every `use_figma` call.
- Pass `skillNames: "figma-use"` on every `use_figma` call.
- Use `await figma.setCurrentPageAsync(page)`. Do not assign `figma.currentPage`.
- Before creating components, call `search_design_system` for likely existing components, variables, and styles.
- After write operations, verify with `get_metadata` and at least one `get_screenshot` for the changed section or node.
- Treat read-only `use_figma` scripts as atomic too. A small JavaScript typo in
  a returned object, such as assigning to an undefined name inside an object
  literal, fails the whole read and returns no partial result.
- `use_figma` rejects JavaScript payloads over 50,000 characters before the
  script runs. For large parity/component builds, split the work into
  section-level calls with shared helper code repeated in each call, then do a
  separate readback pass across all created nodes.

## Fonts

- Load the font currently on a text node before changing its characters. Figma can throw even if the next step changes the node to a different font.
- Load the target font before assigning `fontName`, `fontSize`, or `characters`.
- Inter styles use spaces for some weights: `Semi Bold`, `Extra Bold`.
- Blinker styles are exposed without spaces in this environment, for example `SemiBold`, `ExtraBold`.
- `Menlo Regular` was not available in the PokerSkill Figma runtime during
  the puzzle-components pass. Avoid loading Menlo for notes/code labels unless
  `figma.listAvailableFontsAsync()` confirms it first; the failed write script
  was atomic and created no nodes.

## Page Structure

- Component-library pages should use top-level `SECTION` nodes only when the file policy says so. Do not leave loose frames, text, temp imports, or scratch nodes on the page.
- Re-check top-level children immediately before a repair. A previous audit can
  be stale within the same work session if another import or capture has added
  loose frames back onto the component page.
- After a large section rewrite, `section.children` inside `use_figma` may read
  as a partial child list even while `get_metadata` and `getNodeByIdAsync`
  report the missing nodes with the correct section parent. For final audits,
  cross-check large sections with metadata or known node IDs before deleting or
  rebuilding around an apparent child-count mismatch.
- Nodes parented inside a `SECTION` report local `x`/`y` coordinates relative to
  that section. Do not compare those local coordinates directly against
  page-level section bounds, or a component can appear to sit in an older
  section. Read `node.parent` first and compute absolute bounds only when a
  true page-level collision check needs them.
- `figma.closePlugin(JSON.stringify(...))` can expose that same stale child
  list right after a section write. In the PokerSkill Phase 3 pass, the new
  section reported `children: 0` through the close-plugin readback, while
  `get_metadata` immediately showed every child correctly parented under the
  section. Treat `get_metadata` as the final structural readback for section
  contents.
- `counterAxisAlignItems` does not support a CSS-like `STRETCH` value in this
  Figma MCP runtime. Use valid Figma values such as `MIN`, `CENTER`, `MAX`, or
  `BASELINE`, then make children fill by setting child sizing such as
  `layoutSizingHorizontal = 'FILL'` after appending them to the Auto Layout
  parent.
- Keep component sets before example frames inside a section.
- Icons that are meant to be individually reusable should be standalone components, not a single icon variant set, unless the file policy explicitly wants variants.
- Use component descriptions to name the source file or contract behind the component.
- Treat Figma page backgrounds, section fills, and annotation fonts as file
  chrome, not product UI. Use one neutral page/canvas background, one
  top-level section fill pattern, and one Inter-based annotation style across
  the file unless the file policy explicitly defines a different single
  standard. Product dark mode and brand color belong inside mockup/component
  frames, not in page chrome.
- Do not create pages whose main content is audit text, duplicate indexes,
  source maps, acceptance matrices, or agent worklogs. Put that material in
  repo docs and cite Figma node IDs.
- Keep the Figma organization layers separate: pages separate work type,
  sections group canvas and handoff scope, frames create contained design
  surfaces and useful Assets-panel hierarchy, component names/descriptions
  drive search, Dev Resources link code/docs, and repo docs carry long-form
  proof.
- Durable Figma files should have a maintained `Index` page. It is the one
  allowed text-heavy page, and it should list every page, what belongs there,
  what does not, file-wide chrome/naming rules, owners/status, and links to
  repo docs. It must be updated whenever pages or conventions change. It is not
  a place for full audits, duplicate indexes, acceptance matrices, or worklogs.
- For parity/component-state phases, descriptions should say both what is
  complete and what is not. In the PokerSkill Phase 5 pass, every new component
  set description was normalized to include `Source mapped` plus the caveat
  that exact asset, motion, platform, viewport, and screenshot parity remain a
  later phase.
- Give top-level sections enough vertical gap. In the Poker Skill file, the SSOT requires at least 160px between sections.

## Components And Instances

- A main component cannot contain another main component. Use an instance inside the component, or draw local primitives.
- `figma.combineAsVariants(...)` returns a component set and reparents the supplied components. Set the returned component set name, position, and description after combining.
- If a component set is created from source-code variants, verify the child count and a representative sample of variant properties after creation.
- Keep variant property keys consistent across every child component in a
  component set. A mixed set such as `State=Ready, Balance=Sufficient` for one
  child and only `State=Empty` for another can render visually but makes
  `componentPropertyDefinitions` throw `Component set has existing errors`.
- Duplicate visual assets should share fills/image hashes when the source resolver maps them to the same asset. Do not re-upload or redraw them as different art.
- Exact image-backed primitives are not the same thing as exact runtime
  components. For PokerSkill table work, `Poker Table/Felt`,
  `Poker Table/Mobile Background`, and `Poker Table/Player Avatar` can be exact
  PNG wrappers while runtime scene components still need their own source-shaped
  systems. `Playables/Table Scene/Flat`, `Playables/Table Seat`,
  `Playables/Table Board Row`, `Playables/Table Hero Hand`, and
  `Playables/Table Speech Bubble` now exist as exact lesson-table components.
  `Playables/Parallax Table Scene` now exists as a first exact preflop-neutral
  fixture component, but it is not full parallax coverage; new tilt, board,
  player, speech, badge, and answer-state variants still need source-backed
  additions.
- When a runtime scene intentionally overflows its source panel, make the Figma
  component wrapper large enough for previews and instance bounds, then document
  the source panel rect in the description. For PokerSkill
  `Playables/Table Scene/Flat`, the source panel starts at wrapper x=20, while
  the component variant wrapper is 510x610 so table-seat, table-rim, and hero
  pocket-card overflows are not clipped in Assets previews or screenshots.
- Re-read component-set bounds after adding variants by clone. Figma may keep
  the old `COMPONENT_SET` width/height and `clipsContent=true` even when new
  variant children sit outside those bounds. In the PokerSkill table pass, the
  new `Rail Width=440` action-button variants and `Panel=557` scene variant
  existed structurally but were hidden from set screenshots until the component
  sets were explicitly resized and unclipped.
- When creating wrapper component variants with instances inside them, clear
  the wrapper `fills` and `strokes` after `combineAsVariants`. Figma can leave
  default white component fills on the variant frames, which visually changes
  source-backed assets even when the nested instances are exact.
- Do not trust freshly created auto-layout HUG widths for tiny runtime labels.
  In the PokerSkill `Playables/Table Seat` repair, chip label capsules were
  initially positioned before Figma resolved text width and rendered as tiny
  clipped marks. Set explicit source-measured widths/positions from the Flutter
  layout contract, then verify with a screenshot.
- Cloning a child component from a component set does not necessarily attach it
  to that component set. In the PokerSkill bet-stack pass, cloned `Amount=5`
  and `Amount=10` variants initially appeared as loose page components until
  explicitly appended back into `Playables/Table Bet Chip Stack`. Always read
  back the clone parent and component-set child count after adding variants.
- Use `textAutoResize`, not `autoResize`, on `TEXT` nodes in this MCP Figma
  runtime. Assigning `autoResize` threw before the parallax scene write could
  finish; the partial write had to be cleaned up and replayed.
- `RECTANGLE` nodes cannot contain children. If a generated placeholder needs a
  visible label or helper text, create a `FRAME` with fills/strokes instead of
  a rectangle, then append the text inside the frame.
- Screenshot-check generated component sets after text-heavy writes. In the
  PokerSkill Phase 4 pass, wrapped title/subtitle text rendered with stale
  fixed heights even after source strings were correct. The fix was to resize
  text nodes explicitly from estimated line count, set `textAutoResize`, and
  re-run component-set screenshots before accepting the section.
- Load fonts before changing text auto-resize or text box sizing. In the
  PokerSkill Phase 10 proof pass, changing `textAutoResize` on an existing
  `Inter Semi Bold` node threw until `figma.loadFontAsync({ family: "Inter",
  style: "Semi Bold" })` was awaited. Also read back text nodes with very small
  heights after large proof-board writes; the first Phase 10 pass structurally
  succeeded while 147 text nodes were only 1px tall.
- Broad scans that read `variantProperties` can throw when a component set has
  internal errors. For cleanup scans, prefer exact name/text/description
  matching first, then inspect suspect component sets by ID.
- Guard node-specific property reads even in read-only audits. In the
  PokerSkill Phase 4 verification pass, reading `node.layoutMode` directly on
  a `TEXT` node threw and aborted the whole read. Use checks like
  `'layoutMode' in node` before reading Auto Layout properties.

## Image Assets

- Do not approximate shipped image assets with schematic Figma shapes when the app uses PNG/WebP/JPG assets. Use exact image fills.
- `use_figma` in this environment has no global `fetch`.
- `use_figma` in this environment also has no global `atob`; do not rely on
  base64-decoding local image bytes inside plugin JavaScript.
- `figma.createImageAsync(url)` is not supported in this MCP runtime.
- `figma.ui.onmessage` and `figma.on("message", ...)` are not supported here, so a hidden UI fetch bridge is not reliable.
- `figma.createImage(...)` can create images from supported byte arrays if you already have bytes inside the plugin runtime, but the runtime does not expose filesystem APIs.
- `figma.createImage(...)` rejected lossless WebP bytes in this run with `Image type is unsupported`; prefer PNG/JPEG uploads.
- `createNodeFromSvg(...)` with an external `<image href="http://...">` did not create an image fill.
- When creating components to be combined inside a specific section, set the
  current page to the section's parent first. `combineAsVariants` fails if the
  new component nodes are on the current page but the parent section belongs to
  another page, even when you hold the section node by ID.
- Use `upload_assets` for local files:
  - Call it with `fileKey`, `nodeId`, `scaleMode`, and `count: 1`.
  - POST the local file to the returned `submitUrl`, preferably as multipart form data: `curl -sS -X POST -F "file=@path/to/asset.png;type=image/png" "$submitUrl"`.
  - For duplicate assets, upload once and copy the resulting image fill to the duplicate target node.
- `upload_assets` supports up to 5 URLs per call. Parallel URL requests and parallel `curl` submits work, but each URL is single-use and expires.
- Prepare a real target rectangle first when setting an image fill onto an existing component variant. Keep the target at the exact asset aspect ratio when the component contract depends on it, for example card backs at 60x80.

## SVG And Vector Paths

- Figma `vectorPaths` parsing can reject compact Flutter SVG path data. In this run it rejected compact command syntax and relative arc commands.
- `createNodeFromSvg(...)` can import the original SVG path string when `vectorPaths` rejects it.
- SVG imports may wrap the vector in a frame with a default fill. Clear wrapper fills and verify the inner vector fill.
- For deck-aware card suits, verify rank and suit colors from actual node fills, not only from a visual screenshot.

## Poker Skill Specific Notes

- Card face components should match `apps/flutter/lib/ui/poker_cards/poker_card_sprite.dart` and `apps/flutter/lib/ui/poker_cards/poker_card_layout_contract.dart`.
- Four-color cards use one resolved suit color for both rank text and suit glyph:
  - clubs `#1E852C`
  - diamonds `#294ACA`
  - hearts `#D33122`
  - spades `#151414`
- Two-color cards use red for hearts/diamonds and black for clubs/spades.
- Card backs should use exact 60x80 PNG fills from `apps/flutter/lib/ui/poker_cards/card_back_sku_resolver.dart` and `apps/flutter/assets/images/cards/**`.
- In the current resolver, `DEFAULT` and `CRIMSON_CLASSIC` intentionally map to the same `apps/flutter/assets/images/cards/card-back.png`.
- Table chips and seat badges should use exact PNG fills from `apps/flutter/assets/images/table/**`, not redrawn approximations.
- `apps/flutter/assets/images/table/table_2_5/table/2026-03-03_table_asset.png`
  is a 2048x2048 parallax table source asset. Runtime derives felt bounds from
  `PlayablesParallaxTable25Tuning.feltBoundsInAsset`, so do not crop or resize
  it by eye and call that a table scene.
- Figma cannot natively represent Flutter's parallax `Matrix4` perspective warp.
  For PokerSkill `Playables/Parallax Table Scene`, store exact source/rendered
  geometry, real asset/component instances, and a screenshot anchor in component
  metadata. Document any table raster proxy explicitly instead of pretending a
  flat Figma image layer is a pixel-perfect runtime projection.
- `apps/flutter/assets/images/table/table_bg.png` is a 440x767 felt background
  asset. Runtime sizing comes from `resolvePokerTableFeltSize(frameWidth)` and
  `BoxFit.fill`; a small Figma wrapper around the image is only an asset
  sample unless it also models that sizing contract.
- Table avatar samples should cite whether they are 54x54 head assets from
  `poker_table_avatar_policy.dart` or 1024x1024 parallax avatar angle assets
  from `playables_parallax_table_layers.dart`. Do not collapse those into one
  vague avatar component without source-backed `Policy`/`Angle` props.

## 2026-04-29 PokerSkill Playables Audit Notes

- Guard `componentPropertyDefinitions` reads. Calling it on a variant child can
  throw `Can only get component property definitions of a component set or
  non-variant component`, even in a read-only audit. Only read definitions from
  `COMPONENT_SET` nodes or standalone `COMPONENT` nodes whose parent is not a
  component set.
- Treat optional variable API fields as unsafe until read back in the current
  runtime. Reading `hiddenFromPublishing` on a variable collection threw
  `Node with id "VariableCollectionId:61:2" not found` in this run. For broad
  inventories, omit optional publishing fields or wrap them in a small guarded
  reader.
- Broad Figma inventories can exceed the tool response budget and get
  truncated. Start with page names and counts, then make targeted reads for
  one page, section, or component family at a time.
- `figma.fileKey` may come back as `headless` in the plugin runtime. Do not use
  that returned value as source truth; keep the explicit file key from the
  user-provided URL in the audit record.
- Read-only scripts fail atomically too. If a read script throws, assume no
  partial data is trustworthy, reduce the query, and rerun from the intended
  page.
- Page child counts can vary by loading strategy or by what the script chooses
  to summarize. For a final audit, cite page IDs, node IDs, component names,
  and the exact query scope instead of relying only on loaded child count.
- Code decision states are not automatically durable screens. In PokerSkill
  lessons, access-gate blocked/missing/taxonomy states are real source states,
  but the app logs/telemeters, shows a spinner, and redirects to Learn instead
  of rendering full blocked screens. Model them as decision/recovery states
  unless product wants the behavior changed.
- Do not assume an enum value is the live UI state owner. In PokerSkill lessons,
  `LessonRunnerPhase.running` exists, but the inspected production interaction
  path is owned by `LessonStateMachinePhase.active` plus the runtime
  controller/feedback state.
- Code-supported playable kinds are not the same as shipped standalone content.
  In PokerSkill Phase 5, several `gw_*` snapshot kinds were supported by
  Flutter source but were not found as top-level standalone catalog steps in
  this branch. Mark that as source/component coverage, not content-instance
  parity.
- Component set containers often show `layoutMode: NONE` and no direct bound
  variables even when descendants are bound and render correctly. Inspect
  descendant structure before claiming a component is un-tokenized.
- Screenshot boards are evidence, not components. In the PokerSkill file,
  playable screenshot frames were mostly `TEXT`, `TEXT`, and `RECTANGLE`
  wrappers around image slots, so they should guide component work without
  becoming reusable mock structure.
- Screenshot/reference frames with image fills can be counted as `emptyFrame`
  because the bitmap is the frame fill rather than a child node. Treat
  `emptyFrame` as "has no child layers", not as "visually blank", until image
  fills are inspected.
- Empty top-level frames with gameplay-looking names are not evidence. In the
  PokerSkill file, several `Global Components` frames had poker/chess-like
  names but zero children.
- Page shapes can change between Figma reads. In the PokerSkill audit,
  `Global Components` later loaded as three current top-level sections instead
  of the earlier broader child list. Re-read the target page before publishing
  node IDs or component names in a final audit.
- Reference pages with zero components are not necessarily broken. For
  screenshot boards, competitor boards, style guides, and asset inventories,
  record them as evidence-only unless the task is explicitly to promote an item
  into `Global Components` or `Play Components`.
- When auditing componentization, flag duplicated child layers inside compound
  components. For example, an action-button group that repeats `Button Surface`
  and `Label` layers is weaker than a group composed from child button
  instances.
- Expose sample text as component properties when designers need realistic
  mocks. Amounts, player names, stack values, pot labels, action labels, CTA
  labels, and feedback copy should not be locked inside one-off text layers.
- Use the smallest useful Figma read:
  - page inventory
  - target page top-level sections
  - component sets with property definitions
  - standalone components
  - variables/styles
  - evidence screenshot frames
  This sequencing makes failures local and keeps returned data readable.

## 2026-04-29 PokerSkill Exactness Repair Notes

- Do not turn a runtime text tag into a visual chip because the audit calls it
  an "eyebrow". In PokerSkill lessons, `NEW CONCEPT` and `PREVIOUS MISTAKE`
  are `LessonHeading` subtitle text, not a pill: no fill, no stroke, no radius,
  Blinker Bold 16/24, 0.64px letter spacing, cyan300 or purple300.
- Treat generated Figma components as non-canonical until their descriptions
  name the source widget, token file, and screenshot anchor. If the component
  proves approximate, delete or replace it; do not keep it as a reusable draft.
  A plausible component name such as `Playable/Status Eyebrow` or
  `Answer/Text Choice Tile` is not proof that the Figma node matches the app.
- Shared Figma text component properties can accidentally force every variant
  to show the same string. If variant-specific copy is part of the runtime
  contract, remove the shared text property or verify each variant text after
  resetting instance overrides.
- `removeOverrides()` can clear old instance fills/strokes, but stale metadata
  such as `cornerRadius` may remain on a component frame. Validate both the
  rendered screenshot and the underlying fills/strokes/radii after repair.
- When replacing an invalid generated component, rename the replacement to the
  code-owned concept instead of preserving a misleading audit name. For example,
  `Playable/Status Eyebrow` became `Lesson Heading/Subtitle Tag`, and
  `Playable/Prompt Header` became `Lesson/Heading`.
- For answer controls, separate non-table lesson text buttons from table action
  buttons. `_LessonActionButton` uses dark cobalt surfaces, 2px border, 44px
  min height, 8px radius, and hardSm `(0,2)` shadow; `PlayablesTableActionButton`
  uses cyan fill, `(0,4)` hard shadow, and a different selected/disabled
  palette.
- Check whether a token is actually used by the layout contract before copying
  it into Figma. In the PokerSkill CTA pass, `feedbackCtaOverlayHeight=72`
  existed, but the rendered global CTA overlay was derived through
  `resolveLessonsAnswersSectionLayout(...)`: content height is the 48px
  shadow container plus the 16px bottom gap, then the compact answers section
  adds 16px top padding and 16px bottom padding, producing a 96px overlay in
  the current contract. The Figma component had to follow the rect resolver,
  not the stale-looking standalone constant.
- When binding a text component property to a newly created text node, append
  the text node into the component/variant before assigning
  `componentPropertyReferences`. Setting the reference while the node is still
  unattached throws `Can only set component property references on symbol
  sublayer`.
- For runtime image icons, create exact-size target rectangles first, call
  `upload_assets` with the target `nodeId`, then POST the local PNG. Quote
  upload URLs that include query strings in zsh, for example
  `curl -sS -X POST -F file=@icon.png "$submitUrl"`, or `?scaleMode=FIT`
  can be treated as a glob and the upload will not run.
- After uploading image assets, read the target nodes back and require
  `fills[0].type === "IMAGE"`, the expected `imageHash`, and
  `scaleMode: "FIT"`. A successful upload response is not enough by itself.
- Coach bubbles are easy to fake incorrectly. PokerSkill's current
  `LessonCoachBubble` uses a real side arrow painter with a 10x16 arrow,
  6px protrusion, 22px top offset, a 2px cobalt500 border, radius 8, padding
  12x8, and Blinker Regular 18/22 text. Do not model it as a generic
  rounded cyan card with Inter text.
- The feedback panel uses shipped PNG icons from
  `apps/flutter/assets/images/icons/{correct,incorrect,flag}.png`. Do not
  redraw check, x, or flag icons when exact asset upload is available.
- Lesson header chrome should be modeled from the Flutter header, not old
  app-header or generated playable-header approximations. Current PokerSkill
  lesson header is 56px high, with 16px horizontal padding, a 40x40 side slot,
  16px progress-side gaps, 12px progress height, and `EnergyWidget(size: sm)`
  rendered as a 28x18 custom painter plus Blinker Bold 16 label. A pill with a
  circular energy icon is not exact.
- `LessonProgressBar` is not always one long bar. Runtime chooses Segments for
  totals <=10, Dots for totals <=24, and Bar above that; all modes are 12px
  high with a 6px segment/dot gap. If Figma only shows one fixed bar or uses a
  10px cyan fill, it is an approximation.
- Table-action buttons are not `_LessonActionButton`. The runtime table action
  button is cyan-filled, 44px high, radius 8, Blinker Bold 18/24, hard shadow
  `0 4 0` in cyan700, and pressed translate-down is 4px. Do not reuse the dark
  single-choice answer button for scripted-hand/table choices.
- Poker table chip stacks and pot badges are amount-derived runtime widgets,
  not fixed asset badges. The bet chip stack derives chip mix from thresholds
  in `poker_bet_chip_stack_contract.dart`; the current pot badge is a cobalt
  pill with text, not the old `pot.png` art.
- Be careful binding Figma variables to paints that need semantic alpha. In
  the Range7 pass, adding a color variable alias to a paint reset the paint
  opacity to `1`, which turned `8%` suited hints and `24%` selections into
  fully opaque cells. For alpha-bearing fills/strokes, use raw paint opacity
  and document the source token/color in the component description or plugin
  data until an alpha token exists.
- After `figma.combineAsVariants(...)`, immediately lay out the variant
  children and resize the component set from the child bounds. In the lesson
  choice tile pass, the API created the component sets successfully but left
  every variant stacked at `(0, 0)`, so the first screenshot rendered overlapped
  states instead of a usable variant matrix.
- The same `combineAsVariants` overlap can affect shell-scale component sets.
  In the PokerSkill shell pass, `Lesson/Playable Surface Shell` first stacked
  both 440x897 variants at `(0, 0)`; the repair set the second variant to
  `x=488`, resized the set to `928x897`, and verified the side-by-side result
  with a screenshot.
- When laying out variant children with different intrinsic sizes, compute
  columns from the maximum child width/height, not the current child's own
  dimensions. In the puzzle table pass, `Game/Seat Badge` variants overlapped
  because `x = col * (child.width + gap)` placed narrow children too close to
  wider neighbors.
- Check the source framework's alpha semantics before translating opacity into
  Figma. In Flutter 3.41, `Color.a` is already a `0..1` double; the current
  `LessonPressableTile` selected overlay computes `(overlayFill.a / 255)`, so
  an opaque token becomes roughly `0.0039` opacity in the app. Modeling it as a
  full-opacity overlay hid the hand cards in Figma and was wrong.
- Prefer executable layout contracts and tests over eyeballed screenshot
  heights for shell geometry. In the PokerSkill single-choice shell pass, the
  source-derived `answersContentHeight=120` produced `answersRect
  16,464,408,160`, `answersContentRect 16,488,408,120`, and `CTA overlay
  0,801,440,96` for the 440x897 scaffold sample; an earlier eyeballed answer
  height was wrong.
- Do not infer a reusable component from a playable kind name. Current
  PokerSkill `single_select_token*` playables map token `mode: card|rank`
  options into `PlayablesCardGridItem` values and render
  `LessonCardChoiceTile`. Delete generated Figma `Answer/Token Choice Tile`
  nodes while that source contract holds. If the source later changes, create a
  new exact component from the changed source; do not retain warning
  components.
- When the source-backed replacement exists, remove the bad generated node from
  the Figma page. Do not keep "deprecated" local components alongside the real
  component; they still show up in Assets/search and agents may accidentally
  compose with them.
- The same rule applies inside component sets. If one variant is non-runtime
  or approximate, delete that variant instead of leaving a `State=Dimmed` or
  `Deprecated` option in the set. In the PokerSkill repair pass,
  `Lesson/Coach Avatar` kept only `Character=Max, State=Default`; dimming stays
  in the parent opacity/focus source behavior.
- Apply the deletion rule to partially source-backed shells too. In the
  PokerSkill playable pass, `Lesson/Playable Surface Shell` `1253:801` was
  deleted because it composed some exact children but did not yet model the
  full scaffold, resolver placement, debug ribbon, feedback overlay, or
  per-kind slots. The replacement shell `1739:2061` was created only after the
  single-choice/global-CTA and table/immediate-submit scaffold samples were
  anchored in source geometry and exact child instances. Do not keep a partial
  shell as a reusable component just because several children inside it are
  exact.
- Delete non-runtime variants inside otherwise useful component sets. In the
  PokerSkill repair pass, `Game/Pot Badge` `Variant=LegacyAsset` `1577:5235`
  was removed and the related descriptions were cleaned because current
  `TablePotBadge` is a styled pill, not fixed `pot.png` art.
- After deleting Figma nodes, verify deletion through page/document traversal,
  not direct ID lookup alone. In this MCP runtime, `getNodeByIdAsync` can still
  return a parentless object for a just-deleted component ID, while
  `figma.root.findAllWithCriteria({ types: [...] })` correctly shows it is no
  longer in the document/component registry.
- Keep bad-artifact scans narrow. A regex for `bad` will match legitimate words
  such as `badge`, and `Placeholder` is a valid poker-card state. Use explicit
  cleanup terms such as `approx`, `deprecated`, `legacy`, `stale`,
  `repair candidate`, `do not use`, and `not exact`, then delete or reword the
  actual offenders instead of leaving warning labels on reusable pages.
- When an asset name includes `legacy`, verify that it is still runtime-owned
  before preserving it. In this run, `Asset/Puzzle/pot_legacy` had no active
  Flutter/source-backed usage and was deleted from Figma rather than kept as a
  deprecated component.
- Do not resize `Poker Card/Face` instances down to `45x60` for small45 cards.
  In this file, resizing the instance changed the outer bounds but left some
  internal card artwork constrained at the larger 60x80 scale, causing clipped
  ranks/suit glyphs. Use `instance.rescale(0.75)` for small45 Figma card
  instances so internals scale like `PokerCardSprite(width: 45, height: 60)`.
- Preserve source label token quirks instead of making labels look
  semantically tidy. `single_select_with_hand_board`,
  `single_select_with_parallax_table`, `pick_n_from_pool_with_hand_board`, and
  `pick_n_vs_reference` pass `boardLabelToken: "cards.pocket.label"` for the
  `Community Cards` board label, so the label is uppercase Blinker Bold
  10/15 in cobalt200. A pretty Blinker SemiBold 14/16 board label is only exact
  for the default `cards.community.label` path.
- A coach focus target is not a cyan filled rounded rectangle. The current
  Flutter source wraps arbitrary children with `LessonCoachFocusHighlight`,
  which draws a ring/glow outside the child bounds: outset 4, ring width 2,
  glow width 8, cyan300, animated 800ms pulse. Delete filled focus-overlay
  approximations and model static pulse samples or the real child wrapper.
- Parallax screenshot opponent identities can be runtime-session assigned. If
  the lesson source has seat ids but the retained attempt log is absent, do
  not invent canonical avatar slugs from code. Use code for deterministic
  facts such as slot order, hero seat, and angle mapping; if screenshot visual
  matching is needed for the exact image sprite, document it explicitly as a
  screenshot-derived identity match.
- Swipe-hole-card direction controls are not answer buttons. Source
  `_SwipeDirectionLabels` uses pill chips with padding 14x10, radius 999,
  cobalt900 fill, cobalt700/cyan300 border, and uppercase Blinker SemiBold 14.
  Delete rectangular button-like direction zones.
- `SwipeHoleCardsDeck` is a 160x120 base hand scaled by `cardScale`, not a
  framed card/button panel. The card pair uses 60x80 `PokerCardSprite` cards,
  x translations +/-10, rotations +/-5deg, and optional drag stamps with
  4px border, radius 8, padding 8x2, top 20, offset 40, rotation 15deg, and
  `swipe_hole_cards.stamp` Blinker ExtraBold 24 with 2px letter spacing.

## Verification Checklist

- Confirm top-level page children are only allowed node types, usually `SECTION`.
- Confirm no stale explanatory text contradicts the implementation after a repair.
- Confirm image-backed component variants have one `IMAGE` fill, the expected `scaleMode`, and the expected dimensions.
- Confirm representative screenshots are nonblank and readable.
- Re-run metadata checks after deleting temporary nodes or repairing failed partial writes.

## 2026-04-29 PokerSkill Global Components Repair Notes

- In the Figma plugin runtime, `description` is not a property on ordinary
  `FRAME` nodes. Broad inventories that read descriptions need a type guard
  such as `('description' in node)` or they can fail before returning any data.
- `description` is also not guaranteed on `SECTION` nodes. In the PokerSkill
  Phase 6 puzzle pass, a read-only inventory that assumed section descriptions
  threw before returning data. Guard every broad description read with
  `('description' in node)`, not just frame reads.
- `strokes` is not guaranteed on `SECTION` nodes. In the PokerSkill Phase 9
  account/social/settings pass, setting `section.strokes = ...` threw
  `node.strokes: no such property 'strokes' on SECTION node` after creating a
  partial section. Guard section styling fields with a helper before assigning
  them, then let the next write clean up any partial section by name.
- `addComponentProperty(...)` must be called on the component root, not on a
  nested `FRAME` inside the component. In the PokerSkill Phase 2 primitive
  build, trying to attach a text property from a nested frame threw
  `node.addComponentProperty: no such property 'addComponentProperty' on FRAME
  node`. The write was atomic and created no partial sections; the fix was to
  add component properties only from `ComponentNode` roots and leave nested
  explanatory text as ordinary text layers unless the root owns the property.
- Assign `componentPropertyReferences` only after the target child has been
  appended into the component. During the PokerSkill Phase 2 badge repair,
  setting `{ characters: key }` on a newly created `TEXT` node before
  `component.appendChild(textNode)` threw `Can only set component property
  references on symbol sublayer`. The fix was append first, then set
  `textNode.componentPropertyReferences`.
- `componentPropertyDefinitions` cannot be read from variant child components.
  Read it from the component set, or from standalone components whose parent is
  not a `COMPONENT_SET`.
- Layout fields such as `layoutMode`, `layoutSizingHorizontal`, and
  `layoutSizingVertical` are not present on every node type. Guard them with
  `('layoutMode' in node)` or equivalent checks during broad tree inventories.
- `CupertinoSystemText Medium` was not loadable in this file, but `SF Pro
  Medium` was available. Use `SF Pro Medium` as the Figma-side iOS system-font
  proxy for Flutter Cupertino tab labels, and document that choice on the
  affected component.
- Code Connect context can be unavailable for plan/account reasons. During the
  PokerSkill Phase 6 puzzle pass, a Code Connect context read failed with a
  Developer-seat requirement, so component parity had to rely on normal
  `use_figma` readbacks, component descriptions, source-map notes, metadata,
  and screenshots instead.
- Do not trust `textAutoResize = 'HEIGHT'` by itself for generated
  documentation/card text. In the PokerSkill Phase 6 puzzle pass, generated
  text nodes had the right characters but read back as 1px tall through
  metadata. The repair was to estimate line count, set `textAutoResize =
  'NONE'`, resize text nodes explicitly, then resize note frames and component
  sets before screenshot validation.
- Code Connect map access can fail before any mappings are returned if the
  Figma account lacks the required plan or seat. During the PokerSkill Phase 11
  handoff pass, `get_code_connect_map` returned that a Developer seat in an
  Organization or Enterprise plan was required. Treat that as an explicit
  access blocker, not as missing component readiness, and record the exception
  in the handoff docs.
- Page deletion can be blocked in the MCP/plugin runtime even when a page is
  empty. During the PokerSkill Phase 11 handoff pass, a `PageNode.remove()`
  attempt failed atomically with `Removing this node is not allowed`. Prefer
  explicit page labels, exclusions, or user/admin cleanup rather than assuming
  an agent can remove placeholder pages.
- Do not assume `figma.loadAllPagesAsync()` is available in the MCP plugin
  runtime. During the PokerSkill Phase 11 verification pass, it threw
  `"loadAllPagesAsync" is not a supported API`. For read-only proof, use known
  node IDs with `figma.getNodeByIdAsync(...)` and avoid broad page walking when
  a user-owned page is out of scope.
- Page nodes do not expose `x`, `y`, `width`, `height`, or
  `absoluteBoundingBox` in this MCP/plugin runtime. During the PokerSkill
  Phase 12 Paygates inventory, a broad `rect(node)` helper that read those
  fields on the page node failed before returning any data. Guard all geometry
  reads by node type or by `('field' in node)` checks.
- Failed `use_figma` writes appear atomic in this runtime: the PokerSkill
  Phase 12 Paygates sectioning attempts that threw on unsupported `SECTION`
  strokes and `FRAME` descriptions did not leave the expected section or
  description mutations behind. Still write idempotent section helpers so a
  partial section can be found by name if a future runtime does leave one.
