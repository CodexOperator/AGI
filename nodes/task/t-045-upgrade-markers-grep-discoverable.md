---
acceptance_criteria:
  - R9.2 (each indexer has at least one upgrade-marker comment block naming the section eligible for replacement)
  - R9.3 (markers discoverable via single grep over indexers dir)
blocked_by:
  - task:t-044
cavekit_req: environment-indexers/R9
effort: S
id: "task:t-045"
mint_id: 6a32006efeaf4efabf3df85484120118
origin: build-site
parents:
  - hyp:environment-indexers-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-045: Upgrade markers grep-discoverable"
type: task
---

**Description:** Standardize `# UPGRADE-MARKER: <slug> — <section description>` lines. Each indexer must have at least one. The `agi-tree self-test indexer-docs` (T-046) greps for them.

**Files:** Each indexer source file

**Test Strategy:** `grep -r 'UPGRADE-MARKER:' agi-tree/src/environment_indexers/` returns >=5 hits (one per indexer).
