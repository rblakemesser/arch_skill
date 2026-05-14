# ELI10 Tables

Use this reference when an ELI10 answer has compact grid-shaped information.

Tables are not proof of clarity. A table helps only when the cells stay short
and the reader can scan each row without reconstructing wrapped text.

## Good Table Uses

Use native table rendering directly for compact, repeated shapes:

- option comparisons with short labels
- metric snapshots with numeric values
- before/after differences
- small status grids
- short good/bad contrasts

Good:

```markdown
| Choice | Best For | Risk |
|---|---|---|
| Table | Short comparisons | Wraps if cells get long |
| Bullets | Explanations | Less compact |
| Sections | Root causes | More vertical space |
```

Why it works:

- each cell is a label or short phrase
- each row can be read in one glance
- the table compares things instead of carrying the whole explanation

## Bad Table Uses

Bad tables usually fail because the apparent structure is visual, not mental.
The table looks organized, but the reader still has to untangle wrapped prose.

### Bad: Dense Audit Matrix

```markdown
| Area | File / Symbol | Pattern to adopt | Why | Scope |
|---|---|---|---|---|
| Shared per-kind doctrine | shared/prompts/playable_kind_selection_contract/AGENTS.prompt | One shared contract emitted into every kind skill | Prevents 32 packages from drifting on evidence posture, label-shim language, and "not good for" semantics | include |
```

Why it fails:

- too many dense columns
- long path-like cells
- long prose cells
- rationale and decision state crammed into the same row
- the user has to reconstruct the meaning from broken visual layout

Better ELI10 shape:

```text
Pattern Consolidation Sweep

✅ Include now
- Shared per-kind doctrine: emit one shared contract into every kind skill.
  Why: prevents 32 packages from drifting on evidence posture and label-shim language.

- Existing hard-kind skills: add selection-fit sections without changing proof-owner flow.
  Why: prevents duplicate selection packages from competing with proof specialists.

⚠️ Defer
- MCP playable-author contexts: read as adjacent evidence only.
  Why: useful for contradictions, but too wide for this pass.

Proof:
- Put long paths here, after the meaning.
```

### Bad: Root Cause Forced Into A Table

Bad:

```markdown
| Symptom | Cause | Fix |
|---|---|---|
| It restarted Android | Readiness check mismatch | Change check |
```

Why it fails:

- the user asked why, not for a compressed ticket
- the system belief is the important part
- the fix is unsolicited if the user only asked for explanation

Better:

```text
It did not think Android was missing. It thought its own readiness check had not passed.

🧠 Mechanism:
The simulator window can be visible before the worker sees the exact "booted and reachable" signal it waits for.

Net: the visible symptom was Android opening; the root cause was the worker's readiness check.
```

### Bad: Long Commands Or Paths In Cells

Bad:

```markdown
| Step | Command | Why |
|---|---|---|
| Verify | npx skills check | Confirms the skill package still validates |
```

Better:

Verify the skill package:

```bash
npx skills check
```

Why: confirms the changed skill surface still validates.

Use path tables only when the paths are short and the table has no prose-heavy
cells. If the path is the evidence, put it after the meaning.

## Final Check

Before using a table, ask:

- Can the reader understand each row in one glance?
- Are the cells short labels, values, or phrases?
- Is this a real comparison, not an explanation pretending to be a comparison?
- Would bullets or short sections be clearer?
- Are long strings, paths, commands, or sentences forcing the table to wrap?

Net: if the table makes the answer feel organized but harder to read, do not
use the table.
