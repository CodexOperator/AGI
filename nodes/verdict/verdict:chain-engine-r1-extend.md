---
confidence: 0.85
demote_reason: "no experiment evidence (evidence_runs=0) for 'proved'"
demoted_from: proved
evidence_runs: 0
id: "verdict:chain-engine-r1-extend"
mint_id: c7a858b814a44e949bff29bf3cc02844
next_edges:
  - exp:chain-engine-r1-extend2
parents:
  - exp:chain-engine-r1-extend
  - verdict:chain-engine-r1
status: "inconclusive_lean_proved:50"
synthetic: true
tags:
  - chain-extension
  - verdict-experiment-transition
  - proved
title: "Verdict: chain-engine-r1 extended (10-hop chain)"
type: verdict
verdict: "inconclusive_lean_proved:50"
---

VERDICT: proved. Chain extended from 8 to 10 hops via verdict→experiment→verdict pattern.

**Chain:** idea → hyp → exp → verdict → exp → verdict → mvp → outcome → bigger → app_purpose
