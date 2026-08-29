---
acceptance_criteria:
  - R4.3 (briefing lists available actions per chain: extend at tail
  - fork at named node
  - hop to mid-chain candidate
  - start fresh)
  - R4.4 (briefing generated from chain-engine queries only; does not include implementation details of engine)
blocked_by:
  - task:t-079
  - task:t-058
cavekit_req: autoresearch-tree-skill/R4
effort: S
id: "task:t-080"
mint_id: dfd4ec1b544b45548e9476b7b49fcd99
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r4
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-080: Per-agent briefing — action menu and engine purity"
type: task
---

**Description:** Extend briefing dict with an `actions: list[Action]` per chain. Each `Action` has `kind ∈ {extend, fork, hop, fresh_start}` plus the relevant `target_node`. Audit imports: only `chain_engine.queries` is permitted.

**Files:** `agi-tree/src/skill/briefing.py`, `agi-tree/tests/skill/test_briefing_actions.py`

**Test Strategy:** Fixture with branching graph; assert all four action kinds present where applicable. Static audit of imports asserts no internal chain-engine module is touched.
