---
description: Add ASCII mockups for current + target UI states.
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
If the change touches UI/UX, add ASCII mockups for current and target states in $DOC_PATH.
Keep them contract-level, not illustrative.

OUTPUT FORMAT (insert into sections 4.5 and 5.5):
Current UI ASCII:
```ascii
<ASCII mockups for current UI states>
```

Target UI ASCII:
```ascii
<ASCII mockups for target UI states>
```
