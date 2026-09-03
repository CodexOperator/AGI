---
id: hyp:chain-engine-r8
mint_id: 565fb15b30c74eda8e7eff97c0437385
type: hypothesis
parents:
  - idea:domain-chain-engine
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R8
testable_claim: Verdict Taxonomy
thought_session: L1.09
title: "chain-engine/R8: Verdict Taxonomy"
---
**Description:** A verdict is a finite-state value drawn from a closed taxonomy and accompanied by confidence, evidence, and cross-references to other verdicts.

**Acceptance Criteria:**
- [ ] A verdict's state is exactly one of `proved`, `disproved`, `inconclusive_lean_proved:N`, `inconclusive_lean_disproved:N`, or `pending`
- [ ] When the state is one of the inconclusive forms, the value `N` is an integer between 0 and 100 inclusive; otherwise no `N` is present
- [ ] A verdict carries a `confidence` value between 0.0 and 1.0 inclusive, an `evidence_runs` list of run identifiers, a `contradicts` list of verdict identifiers, and a `supports` list of verdict identifiers
- [ ] A verdict whose state or numeric ranges fall outside the taxonomy is rejected at insert time with a structured error

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r8-by-citation` citing `build:bin-evidence-gate`: `.agi/context/schemas/[verdict].md` carries the exact five-state regex (`proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending`) and `evidence_gate.py` enforces `evidence_runs` on the writer paths.
<!-- THOUGHT:END -->
