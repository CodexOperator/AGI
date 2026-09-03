---
id: task:t-079
mint_id: 8c083a1b8c1e4995b480c4244b6107e1
type: task
parents:
  - hyp:autoresearch-tree-skill-r4
acceptance_criteria:
  - R4.1 (briefing names current chains with length/depth/recency/mvp_count)
  - R4.2 (briefing names each candidate chain's attractiveness score from chain-engine)
blocked_by:
  - task:t-049
  - task:t-051
  - task:t-052
  - task:t-056
cavekit_req: autoresearch-tree-skill/R4
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-079: Per-agent briefing — chain stats"
---
**Description:** Implement `build_briefing(graph, candidate_chains)` that calls chain-engine queries and assembles per-chain stats: length, depth, recency, mvp_count, attractiveness. Output is a structured JSON-serializable dict.

**Files:** `agi-tree/src/skill/briefing.py`, `agi-tree/tests/skill/test_briefing_stats.py`

**Test Strategy:** Fixture with three chains; assert briefing contains all five stat fields per chain.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R4` under `hyp:autoresearch-tree-skill-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r4-by-citation` citing `build:src-chain-engine-query-api`, `build:bin-dispatch`: `chain_engine/query_api.py` (`task_attractiveness`, `chain_gaps`, `next_best_hypothesis`, `coverage_report`) is the briefing data and `dispatch.py` assembles the kid brief.
<!-- THOUGHT:END -->
