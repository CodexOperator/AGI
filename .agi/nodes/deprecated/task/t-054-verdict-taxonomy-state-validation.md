---
id: task:t-054
mint_id: f65f475493de4aa8b0745dc7f5f1e88e
type: task
parents:
  - hyp:chain-engine-r8
acceptance_criteria:
  - R8.1 (state ∈ {proved
  - disproved
  - inconclusive_lean_proved:N
  - inconclusive_lean_disproved:N
  - pending})
blocked_by:
  - task:t-031
cavekit_req: chain-engine/R8
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-054: Verdict taxonomy state validation"
---
**Description:** Implement `Verdict.validate(state, n)` and a parser for the colon-suffixed forms. Insert hook in graph that intercepts verdict-typed nodes and runs validation; raises `VerdictTaxonomyError` on violation.

**Files:** `agi-tree/src/chain_engine/verdict.py`, `agi-tree/tests/chain_engine/test_verdict_state.py`

**Test Strategy:** Test each of the five forms; reject `inconclusive_lean_proved:101`; reject `proved:50`; reject unknown state.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R8` under `hyp:chain-engine-r8`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r8-by-citation` citing `build:bin-evidence-gate`: `.agi/context/schemas/[verdict].md` carries the exact five-state regex (`proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending`) and `evidence_gate.py` enforces `evidence_runs` on the writer paths.
<!-- THOUGHT:END -->