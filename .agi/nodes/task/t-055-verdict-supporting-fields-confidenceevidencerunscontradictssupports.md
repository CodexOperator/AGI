---
acceptance_criteria:
  - R8.3 (verdict carries confidence ∈ [0.0
  - 1.0]
  - evidence_runs list
  - contradicts list
  - supports list)
blocked_by:
  - task:t-054
cavekit_req: chain-engine/R8
effort: S
id: "task:t-055"
mint_id: eccd61e0e2764a83af68a7129a53e58d
origin: build-site
parents:
  - hyp:chain-engine-r8
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-055: Verdict supporting fields (confidence/evidence_runs/contradicts/supports)"
type: task
---

**Description:** Add to verdict schema (T-031) and validator (T-054) the four fields. Reject confidence outside [0,1].

**Files:** `agi-tree/src/chain_engine/verdict.py`, `agi-tree/src/graph_core/templates/builtin_schemas/[verdict].md`, `agi-tree/tests/chain_engine/test_verdict_fields.py`

**Test Strategy:** Verdict with all four fields valid passes; confidence=1.5 rejected; missing supports list rejected.
