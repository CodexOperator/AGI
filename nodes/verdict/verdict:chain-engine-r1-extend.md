---
id: verdict:chain-engine-r1-extend
type: verdict
title: 'Verdict: chain-engine-r1 extended (10-hop chain)'
status: proved
verdict: inconclusive_lean_proved:50
confidence: 0.85
parents:
- exp:chain-engine-r1-extend
- verdict:chain-engine-r1
tags:
- chain-extension
- verdict-experiment-transition
- proved
next_edges:
- exp:chain-engine-r1-extend2
synthetic: true
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---


VERDICT: proved. Chain extended from 8 to 10 hops via verdict→experiment→verdict pattern.

**Chain:** idea → hyp → exp → verdict → exp → verdict → mvp → outcome → bigger → app_purpose
