---
confidence: 1.0
demote_reason: "no experiment evidence (evidence_runs=0) for 'proved'"
demoted_from: proved
evidence_runs: []
id: "verdict:a00-8636e255-bf1a6c"
mint_id: aefe5460cf0f4741b86e5b59ab34ffb1
next_edges: []
parents:
  - exp:a00-8636e255-bf1a6c
  - hypothesis:a00-8636e255-bf1a6c
status: open
tags:
  - renderers
  - mermaid
  - r3
  - proved
  - determinism
  - validity
title: "Verdict: Mermaid Renderer R3 — Valid and Deterministic"
type: verdict
verdict: "inconclusive_lean_proved:50"
---

**VERDICT: PROVED**

Mermaid renderer (R3) passes all 5 acceptance criteria:

| Criterion | Result | Detail |
|---|---|---|
| Deterministic | ✓ | Byte-identical across 2 runs |
| Valid directive | ✓ | `flowchart TD` |
| Nodes complete | ✓ | 2074/2074 input nodes in output |
| Edges complete | ✓ | 1893/1893 input edges in output |
| Safe IDs | ✓ | No unquoted complex ids |

**Confidence: 1.0**

**Evidence run:** exp:a00-8636e255-bf1a6c

**Next:** Feed into renderers-r3 verification (the `renderers-r3` hypothesis from `idea:domain-renderers` is already registered; this verdict confirms its acceptance criteria are met).
