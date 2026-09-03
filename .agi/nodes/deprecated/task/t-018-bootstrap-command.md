---
id: task:t-018
mint_id: 01c15ddfcf774745b8e8c493a0094042
type: task
parents:
  - hyp:graph-core-r10
acceptance_criteria:
  - R10.1 (empty dir → context skeleton with subdirs schemas/kits/storage)
  - R10.2 (running twice is no-op
  - no overwrite)
  - R10.3 (skeleton includes minimal example node and schema sufficient to load)
  - R10.4 (reports created paths in single summary)
blocked_by:
  - task:t-016
cavekit_req: graph-core/R10
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-018: Bootstrap command"
---
**Description:** Implement `agi-tree bootstrap` CLI. Creates `context/{schemas,kits,nodes,plans,impl,refs,designs}` if missing. Writes a minimal `[example].md` schema and `nodes/example.md` referencing it. Idempotent: existing files are not touched. Prints a summary of created vs skipped paths.

**Files:** `agi-tree/src/graph_core/cli/bootstrap.py`, `agi-tree/src/graph_core/templates/example_schema.md`, `agi-tree/src/graph_core/templates/example_node.md`, `agi-tree/tests/graph_core/test_bootstrap.py`

**Test Strategy:** Run bootstrap on empty tempdir; assert directory tree matches expected. Run twice; assert second run reports zero changes and no file's mtime changed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R10` under `hyp:graph-core-r10`, whose disposition is disposition GENUINELY-OPEN, not run: no `bootstrap.py` or CLI subcommand exists; `agi`'s real bootstrap story is `QUICKSTART.md` plus the `init`/scaffolding half `goal:g1.5` still owes, not this generic-library command -- noted on `goal:g1.5`.
<!-- THOUGHT:END -->
