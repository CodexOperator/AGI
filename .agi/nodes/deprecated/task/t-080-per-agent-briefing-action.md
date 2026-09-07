---
id: task:t-080
mint_id: dfd4ec1b544b45548e9476b7b49fcd99
type: task
parents:
  - hyp:autoresearch-tree-skill-r4
acceptance_criteria:
  - {"R4.3 (briefing lists available actions per chain": "extend at tail"}
  - fork at named node
  - hop to mid-chain candidate
  - start fresh)
  - R4.4 (briefing generated from chain-engine queries only; does not include implementation details of engine)
blocked_by:
  - task:t-079
  - task:t-058
cavekit_req: autoresearch-tree-skill/R4
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-080: Per-agent briefing — action menu and engine purity"
---
**Description:** Extend briefing dict with an `actions: list[Action]` per chain. Each `Action` has `kind ∈ {extend, fork, hop, fresh_start}` plus the relevant `target_node`. Audit imports: only `chain_engine.queries` is permitted.

**Files:** `agi-tree/src/skill/briefing.py`, `agi-tree/tests/skill/test_briefing_actions.py`

**Test Strategy:** Fixture with branching graph; assert all four action kinds present where applicable. Static audit of imports asserts no internal chain-engine module is touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R4` under `hyp:autoresearch-tree-skill-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r4-by-citation` citing `build:src-chain-engine-query-api`, `build:bin-dispatch`: `chain_engine/query_api.py` (`task_attractiveness`, `chain_gaps`, `next_best_hypothesis`, `coverage_report`) is the briefing data and `dispatch.py` assembles the kid brief.
<!-- THOUGHT:END -->