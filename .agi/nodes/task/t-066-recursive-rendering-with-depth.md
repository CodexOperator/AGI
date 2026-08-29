---
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
effort: M
id: "task:t-066"
mint_id: a3be09e096fa47f6ad13654a35f0d31a
origin: build-site
parents:
  - hyp:renderers-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-066: Recursive rendering with depth bound"
type: task
---

**Description:** Add `render_subgraph(node, depth)` recursion to ASCII renderer with default `max_depth=2` and configurable. Other renderers default to a `[subgraph: <id>]` placeholder line.

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/src/renderers/mermaid.py`, `agi-tree/src/renderers/git_tree.py`, `agi-tree/src/renderers/git_diff.py`, `agi-tree/tests/renderers/test_recursive_rendering.py`

**Test Strategy:** Three-level subgraph fixture: ASCII shows two levels then a marker; others show placeholder.
