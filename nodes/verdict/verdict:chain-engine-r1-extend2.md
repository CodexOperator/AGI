---
confidence: 0.9
demote_reason: "no experiment evidence (evidence_runs=0) for 'proved'"
demoted_from: proved
evidence_runs: 0
id: "verdict:chain-engine-r1-extend2"
mint_id: 736f21ca80804112a86f5e0f906c7946
next_edges:
  - exp:chain-engine-r1-extend3
parents:
  - exp:chain-engine-r1-extend2
  - verdict:chain-engine-r1-extend
status: "inconclusive_lean_proved:50"
synthetic: true
tags:
  - chain-extension
  - r15
  - second-cycle
  - proved
title: "Verdict: chain-engine-r1 second extension (12-hop chain)"
type: verdict
verdict: "inconclusive_lean_proved:50"
---

VERDICT: proved. Chain extended from 10 to 12 hops via second verdict→experiment→verdict cycle.

**Chain:** idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → mvp → outcome → bigger → app_purpose

This proves verdict→experiment→verdict cycles are stackable.
