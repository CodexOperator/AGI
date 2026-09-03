---
id: task:t-066
mint_id: a3be09e096fa47f6ad13654a35f0d31a
type: task
parents:
  - hyp:renderers-r6
acceptance_criteria:
  - R6.1 (subgraph-flagged node rendered with visible nested view in renderers that support nesting)
  - R6.2 (ASCII renderer renders nested subgraphs to max depth of two levels)
  - R6.3 (renderers that do not support nesting render single placeholder line per nested subgraph)
  - R6.4 (nesting depth configurable
  - respects documented maximum)
blocked_by:
  - task:t-061
  - task:t-063
  - task:t-064
  - task:t-065
  - task:t-009
cavekit_req: renderers/R6
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-066: Recursive rendering with depth bound"
---
**Description:** Add `render_subgraph(node, depth)` recursion to ASCII renderer with default `max_depth=2` and configurable. Other renderers default to a `[subgraph: <id>]` placeholder line.

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/src/renderers/mermaid.py`, `agi-tree/src/renderers/git_tree.py`, `agi-tree/src/renderers/git_diff.py`, `agi-tree/tests/renderers/test_recursive_rendering.py`

**Test Strategy:** Three-level subgraph fixture: ASCII shows two levels then a marker; others show placeholder.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R6` under `hyp:renderers-r6`, whose disposition is disposition GENUINELY-OPEN, not run: no nested-subgraph rendering with a depth bound in `ascii.py` or elsewhere; no existing goal obviously covers it, so this THOUGHT is the record.
<!-- THOUGHT:END -->
