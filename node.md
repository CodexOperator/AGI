---
id: task:t-055
mint_id: eccd61e0e2764a83af68a7129a53e58d
type: task
parents:
  - hyp:chain-engine-r8
acceptance_criteria:
  - R8.3 (verdict carries confidence ∈ [0.0
  - 1.0]
  - evidence_runs list
  - contradicts list
  - supports list)
blocked_by:
  - task:t-054
cavekit_req: chain-engine/R8
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
title: "T-055: Verdict supporting fields (confidence/evidence_runs/contradicts/supports)"
---
**Description:** Add to verdict schema (T-031) and validator (T-054) the four fields. Reject confidence outside [0,1].

**Files:** `agi-tree/src/chain_engine/verdict.py`, `agi-tree/src/graph_core/templates/builtin_schemas/[verdict].md`, `agi-tree/tests/chain_engine/test_verdict_fields.py`

**Test Strategy:** Verdict with all four fields valid passes; confidence=1.5 rejected; missing supports list rejected.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R8` under `hyp:chain-engine-r8`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r8-by-citation` citing `build:bin-evidence-gate`: `.agi/context/schemas/[verdict].md` carries the exact five-state regex (`proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending`) and `evidence_gate.py` enforces `evidence_runs` on the writer paths.
<!-- THOUGHT:END -->