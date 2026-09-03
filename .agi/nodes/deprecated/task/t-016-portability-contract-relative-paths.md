---
id: task:t-016
mint_id: 93615883194d4ea393a45d53e6fc3854
type: task
parents:
  - hyp:graph-core-r9
acceptance_criteria:
  - R9.1 (no node/cache/config file references absolute path outside project root)
  - R9.2 (copying context dir to fresh checkout reproduces graph)
  - R9.3 (loads with no env vars beyond optional model selector)
blocked_by:
  - task:t-014
  - task:t-015
cavekit_req: graph-core/R9
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-016: Portability contract — relative paths only"
---
**Description:** Audit every path-handling site to use `Path(project_root) / relative`. Reject configuration values containing absolute paths outside the project root. Document the optional model-selector env var as the only permitted environment dependency.

**Files:** `agi-tree/src/graph_core/paths.py`, `agi-tree/tests/graph_core/test_portability.py`

**Test Strategy:** Copy fixture context dir to `/tmp/<random>/`, load, assert node count and id list match the original site.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R9` under `hyp:graph-core-r9`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: no dedicated portability self-test exists (no `test_portability.py`); the small experiment is an absolute-path audit plus copying `.agi/` to a tempdir and reloading it through the real loader -- hours, not architecture.
<!-- THOUGHT:END -->
