# Figma MCP Agent Gotchas

Use this reference when an agent is inspecting, creating, repairing, exporting,
or uploading Figma artifacts through MCP, plugin API scripts, or another
tool-mediated Figma runtime.

This file does not replace `figma-file-craft.md`. It covers the operational
failure modes that make otherwise sound Figma file-craft work appear complete
when the file is actually broken, blank, overlapped, unbound, or unusable by
Dev Mode and model consumers.

## Ground Truth

Successful tool output is not the same as successful Figma state. Treat every
write, upload, import, and export as provisional until the target artifact is
read back and visually checked.

Strong proof usually combines:

- returned node IDs for created or changed objects
- structure reads from the actual target page or node
- variable, style, component, property, fill, and bounds reads where relevant
- screenshots of the real frame, component set, or documentation board
- source-of-truth checks against code, tokens, assets, or a product decision

If a parity task depends on exact Figma values, cite the frame or node IDs and
measure them. If MCP quota or file access prevents measurement, stop the exact
parity claim instead of inventing values.

## Runtime And Script Limits

Different MCP, plugin, and wrapper runtimes expose different subsets of the
Figma API. Treat the observed runtime as the contract for the current task.
When an API is unsupported, narrow the script and use another supported proof
path instead of guessing that the write partially worked.

Read-only scripts can fail atomically too. A typo in a returned object or an
unguarded property read can abort the entire inventory and return no partial
truth. If a broad read fails, reduce the query to one page, section, component
family, or known node ID and rerun from the intended page.

Some runtimes reject large JavaScript payloads before they run. For large
library builds or parity audits, split work into section-level calls, repeat
small helper functions in each call as needed, and do a separate readback pass
across the returned node IDs.

For broad inventories, start small:

- page names and IDs
- target page top-level sections
- component sets with property definitions
- standalone components
- variables and styles
- evidence screenshot frames or source-map notes

Do not rely on runtime-returned file identity when the user supplied an
explicit Figma URL or file key. Some headless or plugin contexts return
placeholder file keys. Keep the user-provided file identity in the audit or
handoff record.

## Before Writing

Inspect before changing the file:

- pages and top-level page bounds
- the `Index` page, if present; treat it as the file-native organization
  contract and check whether it is stale before editing
- existing page backgrounds, top-level section fills, and annotation text
  styles, so new work follows one file-wide canvas chrome standard
- the target node type; Figma URLs can point at a page, frame, component, or
  ordinary layer
- the file's organizational model: page role, section role, frame/category
  role, component naming pattern, description/link usage, and evidence/docs
  split
- existing local components, component sets, variables, styles, sections, and
  published library references
- nearby top-level section bounds so new work does not overlap existing work
- the production source of truth when the Figma artifact maps to shipped code

Search the design system surface available to the runtime before creating
components, variables, or styles. If the runtime cannot search published
libraries directly, inspect local imports, existing instances, component
descriptions, variables, styles, and Dev Mode or Code Connect context where
available.

Re-read the target page immediately before a repair. Earlier inventories can
go stale inside the same session when imports, captures, or another agent add
loose frames or sections.

Screenshots and exported Figma code are evidence, not automatically the source
of truth for reusable system artifacts. Use code, tokens, and app-owned assets
for exact implementation values when the task is building a durable library or
handoff surface.

Long reports, duplicate indexes, audit notes, source maps, and acceptance
matrices belong in repo docs. Do not create Figma pages whose main content is a
wall of text just to prove the run happened.

The one allowed text-heavy Figma page is `Index`. It may list pages,
conventions, ownership, chrome rules, and links to repo docs. It must not
contain the full audit, duplicate index, acceptance matrix, or worklog.

For source context, prefer this order:

1. component or style descriptions for short searchable usage notes
2. Dev Resources for code, Storybook, tickets, and external documentation
3. Dev Mode annotations for callouts tied to a specific design object
4. repo docs for long reports, source maps, audits, and acceptance matrices

Do not replace those channels with oversized text layers on the canvas.

After writes, update `Index` when any page is added, removed, renamed, reordered,
or repurposed, or when file-wide naming, chrome, or documentation rules change.
If the tool run is read-only or lacks edit permission, include the required
Index update in the handoff.

When a file has both generated local components and imported or published
library components, label the generated work as evidence or repair work unless
inspection proves it is the canonical source.

## Audit Write Boundary

Audits are read-heavy by default. Do not mutate Figma while auditing unless the
user asked for authoring or repair.

If the user asked only for an audit:

- inspect pages, nodes, images, variables, components, screenshots, and source
  links
- return findings, ledgers, source maps, and repair plans outside Figma
- do not create report pages, duplicate indexes, acceptance matrices, or
  explanatory boards in the file

If the user asked for repair:

- inspect the target immediately before writing
- keep changes scoped to the named file, page, section, component, or node
- write source anchors into component descriptions, Dev Resources, or compact
  Dev Mode annotations rather than large canvas text
- verify changed node IDs, parentage, fills, bounds, component properties,
  screenshots, and source links before claiming success

## Readback And Bounds

After any major write, verify the created or changed target through multiple
proof paths:

- returned node IDs still exist and have the expected parent
- structural metadata names the intended page, section, frame, or component set
- fills, variables, styles, and component properties read back where relevant
- bounds show no top-level overlap, component-set clipping, or card collision
- screenshots of the actual target artifact are nonblank and readable

Do not treat a screenshot of a parent Section as proof that separately
appended frames live inside that section. Capture the component set, frame, or
documentation board that must be readable.

Large-section child lists returned by a script can be stale or partial in some
runtimes. For final structural proof, cross-check known node IDs, metadata,
and parent references before deleting or rebuilding around an apparent
child-count mismatch.

Nodes parented inside a Section may report coordinates relative to that
section. Do not compare local section coordinates directly against page-level
section bounds. Compute absolute bounds only when a true page-level collision
check needs them.

## Script Runtime Rules

Prefer small scripts that inspect, create, or repair one coherent artifact and
return structured data. Return created node IDs, mutated node IDs, counts,
artifact names, and verification facts. Do not rely on console logs.

Start each script by finding and loading the intended page:

```js
const page = figma.root.children.find((node) => node.name === "Components");
await figma.setCurrentPageAsync(page);
```

Page context can reset between calls. Do not assume the currently visible page
is still the page your next script will mutate.

Use top-level `await` and `return` when the runtime supports it. Avoid wrapping
the whole script in an async IIFE unless the tool explicitly requires that
shape.

Failed plugin scripts are often atomic in MCP runtimes. If a script errors,
read the error, repair the cause, and retry from the intended start state
rather than assuming a partial canvas mutation landed.

Unsupported API calls should be treated as runtime facts, not mysteries to
work around blindly. Common examples in restricted MCP runtimes include
notification APIs, private plugin data APIs, and text inspection APIs that are
available in some contexts but not others. Use returned node IDs, shared plugin
data where supported, explicit page traversal, and concrete font reads instead.

Write idempotent helpers for section and component creation. Even if the
current runtime usually rolls back failed writes, future or adjacent runtimes
may leave partial named sections that the next attempt should find and repair
instead of duplicating.

## Node API Traps

Not every property exists on every node type. Page nodes do not behave like
frames, and variant children do not expose the same APIs as standalone
components or component sets. Guard optional reads by property existence or
node type.

Guard broad inventories and cleanups for node-specific fields, including
`description`, `strokes`, `layoutMode`, layout sizing fields, geometry fields,
`variantProperties`, variable publishing fields, and component property
definitions. Page and Section nodes in particular often lack fields that
frames, components, or rectangles expose.

Set parent-dependent properties only after the node is inside the right parent:

- Append text into the component before assigning component property
  references.
- Append children to an Auto Layout parent before setting absolute positioning
  that depends on that parent.
- Set fill or sizing values after the node is in the structure when the runtime
  rejects unattached edits.

Rectangles cannot contain children. If a placeholder or visual surface needs a
label, helper note, or nested evidence, create a frame with fills and strokes
instead of trying to append children to a rectangle.

Use component property definitions from a component set or non-variant
component. Do not read them from variant children as if they were standalone
component definitions.

Add component properties on the component root, not a nested frame inside the
component. Assign `componentPropertyReferences` only after the target child is
appended into the component.

Auto Layout property values are Figma API values, not CSS values. For example,
do not assume a CSS-like `STRETCH` value exists for counter-axis alignment; set
valid alignment values on the parent and fill behavior on appended children.

Name-based audits can lie because instances can share component names. Filter
by both name and node type, and prefer stable parent context when layer names
can repeat.

Figma color channels are `0..1` floats, not `0..255` integers. Fills and
strokes are effectively replace-by-value in many plugin operations, so clone
and reassign arrays instead of mutating them in place.

Resetting instance overrides can leave stale frame metadata such as radius,
fills, or strokes. Verify both the rendered screenshot and the underlying
paint, stroke, and radius values after override cleanup.

Do not assume page deletion, all-page loading, UI message bridges, network
fetching, base64 helpers, or URL image creation are available in the plugin
runtime. Prefer known node IDs, explicit page traversal, and runtime-provided
upload or asset helpers when they exist.

## Fonts And Text

Load fonts before creating or changing text, text styles, text wrapping,
characters, or auto-resize settings. Treat layout edits on text as font-touching
operations.

Load the font currently on an existing text node before changing its
characters, even when the next step will assign a different target font. Some
runtimes validate the old font during the edit.

Font family and style names are runtime-specific:

- Flutter or CSS names may not exist in Figma.
- Figma style names can differ by family, such as spaced `Semi Bold` versus
  unspaced `SemiBold`.
- A product font declared in app assets may still be unavailable in the Figma
  file.

When a font is unavailable, document the substitute in the Figma artifact and
avoid making that substitute look like production truth.

Use the text auto-resize property supported by the current runtime; similarly
named fields may not exist. Some plugin contexts expose `textAutoResize` rather
than a generic `autoResize` field. For notes and documentation frames, make
text fill the available width and verify height after write. A structurally
rich board can still be useless if evidence notes render as clipped one-line
text or read back as near-zero height.

## Components And Variants

After creating a component set or calling `combineAsVariants`, inspect and lay
out the variant children. Variants can overlap even when the component set was
created successfully.

Resize component sets from actual child bounds. Wide sets, imported examples,
and generated documentation cards can overflow or overlap the section even when
each child component looks correct in isolation.

Set the returned component set's name, position, description, child layout,
size, and clipping deliberately after combining variants. `combineAsVariants`
can reparent supplied components and leave children stacked at the origin.

When variant children have different intrinsic sizes, lay out the matrix from
the maximum child width and height, not the current child's own dimensions.
Verify component-set bounds after adding variants by clone, because a set can
keep its old width, height, or clipping while new children sit outside it.

Keep variant property keys consistent across every child in a component set.
Mixed property keys can render visually while making component property reads
or downstream mapping fail.

Broad scans that read variant properties or component property definitions can
throw when a component set has internal errors. For cleanup work, match exact
names, descriptions, or text first, then inspect suspect sets by ID.

After cloning or adding variants, read back the clone parent and component-set
child count. A cloned child can remain as a loose page component unless it is
explicitly appended back into the intended set.

When wrapper component variants contain nested exact instances, clear
unintended default wrapper fills or strokes after combining if those paints
visually alter the nested source-backed asset.

Keep icons as standalone components, not icon variants. When SVG imports create
wrapper frames, flatten finalized wrappers where appropriate, clear fills on
non-vector containers, and bind color only to vector-like nodes. A root fill on
an icon instance can render as a square even when vector children are correct.

For instance-swap repairs, do not rely only on a slot layer name. After a swap,
the layer may display the swapped component name. Find the slot by parent
structure, position, or the swapped main component.

Use screenshots as part of component verification. Metadata can look green
while the rendered component shows square icons, clipped labels, blank fills,
or stacked variants.

## Images, Uploads, And Screenshots

Treat asset upload as a transport step. An upload can return HTTP success and
an image hash while the target rectangle still has its old fill or a solid
placeholder. Read the target node's `fills` after upload.

Create a real target rectangle first when the exact asset aspect ratio matters.
Use the target node ID in the runtime's upload helper, then verify the target
fill after upload. If the shell command uploads to a signed URL, quote URLs
that include query strings.

When readback does not show the intended image fill, bind the returned hash
explicitly:

```js
const image = figma.createImage(imageHash);
slot.fills = [{ type: "IMAGE", scaleMode: "FIT", imageHash: image.hash }];
```

Use `scaleMode: "FIT"` for visual reference slots unless the intended crop is
part of the artifact. Verify that every expected slot has an image fill and the
expected scale mode.

For duplicate image assets, upload once and copy the verified fill or image
hash to duplicate targets. Do not redraw or re-upload the same source asset as
different art unless the product asset pipeline owns those differences.

Some plugin runtimes do not expose `fetch`, `atob`, URL image creation, UI
message bridges, or filesystem access. Use the runtime's upload helper or an
outside transport step instead of embedding asset-fetch logic that cannot run.

Large screenshot boards can exceed upload or renderer comfort even when they
are technically valid images. Batch uploads, slice large boards, or convert
risky 16-bit PNGs into 8-bit PNG32 copies when a client or MCP renderer shows
blank output.

Re-uploading the same bytes is a useful diagnostic. If Figma returns the same
image hash, the node may already point at the intended asset and the problem is
more likely render compatibility, stale client cache, or a missing explicit
fill binding.

Do not treat `get_metadata` as visual proof. It reports names, structure, and
geometry, not whether an image hash renders. Pair metadata with screenshot and
fill inspection.

A screenshot of a Section is not proof that separately appended frames live
inside that section. Capture the actual component set, frame, or documentation
board that must be readable.

## Layout And Page Organization

Create the page or wrapper frame first, then append sections and cards inside
it. New top-level nodes often begin at `(0, 0)`, so a valid component family can
still be sitting on top of another section.

For component-library pages that intentionally use top-level Sections, verify
the page has no loose frames, text, temp imports, or scratch nodes after repair.
For files with a different policy, state the policy before treating loose
top-level nodes as defects.

Audit direct child bounds after major writes:

- no top-level section overlap
- no component set overflow outside its section
- no documentation-card collision
- no horizontal row fixed-height clipping after text expands
- no blank section screenshots caused by frames living beside, not inside, the
  section

For large visual inventories, use manifest-backed contact sheets instead of
placing hundreds or thousands of individual image nodes. The manifest proves
exact paths and source files; the Figma page provides a reviewable visual
surface.

## Source Truth And Handoff

Figma exports and MCP asset URLs are reference artifacts unless explicitly
promoted into the product asset pipeline. Never put short-lived MCP asset URLs
or generated reference code into runtime code.

For source-backed parity work, also read `figma-source-backed-parity.md`.
Generated components are not canonical until they cite the source component,
token source, asset source, and verification anchor that make them reusable.

Map Figma values into app-owned tokens, generated assets, and component APIs.
When exact parity depends on an exported layer, record the Figma node, the
measured value, and the app owner path that should receive the implementation.

Visible exports beat hidden or clipped layer guesses. If a hidden text layer,
off-canvas label, or mock-only helper conflicts with the visible frame, do not
render it as product UI without an explicit product decision.

Product intent can override the current mock, but the override must be recorded
near the handoff or parity plan. Otherwise future audits will keep repairing
the implementation back to the stale mock.

## Completion Checks

Before calling MCP-mediated Figma work done, verify the relevant checks:

- The intended page or frame was inspected after the write.
- Created or changed nodes are returned and still exist.
- Component sets have expected variants and no stacked children.
- Text uses loaded fonts and does not clip.
- Variables are scoped and bound to supported fields.
- Uploaded image slots have real image fills and expected scale modes.
- Screenshots of target artifacts are nonblank and readable.
- Top-level sections and wide component sets do not overlap or overflow.
- Broad reads used guarded node-type checks and did not rely on partial
  script output after an exception.
- Source-backed components cite the source component, tokens, assets, or
  product decision that owns them.
- Component descriptions or documentation notes name the source code, token, or
  asset truth when the artifact maps to production.
- Reference exports remain out of runtime code unless they have been promoted
  through the product's normal asset pipeline.
