---
confidence: 0.5
id: "hyp:chain-engine-r8"
mint_id: 565fb15b30c74eda8e7eff97c0437385
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R8
testable_claim: Verdict Taxonomy
title: "chain-engine/R8: Verdict Taxonomy"
type: hypothesis
---

**Description:** A verdict is a finite-state value drawn from a closed taxonomy and accompanied by confidence, evidence, and cross-references to other verdicts.

**Acceptance Criteria:**
- [ ] A verdict's state is exactly one of `proved`, `disproved`, `inconclusive_lean_proved:N`, `inconclusive_lean_disproved:N`, or `pending`
- [ ] When the state is one of the inconclusive forms, the value `N` is an integer between 0 and 100 inclusive; otherwise no `N` is present
- [ ] A verdict carries a `confidence` value between 0.0 and 1.0 inclusive, an `evidence_runs` list of run identifiers, a `contradicts` list of verdict identifiers, and a `supports` list of verdict identifiers
- [ ] A verdict whose state or numeric ranges fall outside the taxonomy is rejected at insert time with a structured error
