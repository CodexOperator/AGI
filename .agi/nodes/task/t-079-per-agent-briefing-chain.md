---
acceptance_criteria:
  - R4.1 (briefing names current chains with length/depth/recency/mvp_count)
  - R4.2 (briefing names each candidate chain's attractiveness score from chain-engine)
blocked_by:
  - task:t-049
  - task:t-051
  - task:t-052
  - task:t-056
cavekit_req: autoresearch-tree-skill/R4
effort: M
id: "task:t-079"
mint_id: 8c083a1b8c1e4995b480c4244b6107e1
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r4
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-079: Per-agent briefing — chain stats"
type: task
---

**Description:** Implement `build_briefing(graph, candidate_chains)` that calls chain-engine queries and assembles per-chain stats: length, depth, recency, mvp_count, attractiveness. Output is a structured JSON-serializable dict.

**Files:** `agi-tree/src/skill/briefing.py`, `agi-tree/tests/skill/test_briefing_stats.py`

**Test Strategy:** Fixture with three chains; assert briefing contains all five stat fields per chain.
