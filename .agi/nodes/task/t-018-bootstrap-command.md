---
acceptance_criteria:
  - R10.1 (empty dir → context skeleton with subdirs schemas/kits/storage)
  - R10.2 (running twice is no-op
  - no overwrite)
  - R10.3 (skeleton includes minimal example node and schema sufficient to load)
  - R10.4 (reports created paths in single summary)
blocked_by:
  - task:t-016
cavekit_req: graph-core/R10
effort: M
id: "task:t-018"
mint_id: 01c15ddfcf774745b8e8c493a0094042
origin: build-site
parents:
  - hyp:graph-core-r10
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-018: Bootstrap command"
type: task
---

**Description:** Implement `agi-tree bootstrap` CLI. Creates `context/{schemas,kits,nodes,plans,impl,refs,designs}` if missing. Writes a minimal `[example].md` schema and `nodes/example.md` referencing it. Idempotent: existing files are not touched. Prints a summary of created vs skipped paths.

**Files:** `agi-tree/src/graph_core/cli/bootstrap.py`, `agi-tree/src/graph_core/templates/example_schema.md`, `agi-tree/src/graph_core/templates/example_node.md`, `agi-tree/tests/graph_core/test_bootstrap.py`

**Test Strategy:** Run bootstrap on empty tempdir; assert directory tree matches expected. Run twice; assert second run reports zero changes and no file's mtime changed.
