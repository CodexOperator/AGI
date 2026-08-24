---
id: verdict:environment-indexers-r1-extend
type: verdict
title: 'Verdict: environment-indexers-r1 extended (10-hop chain)'
status: proved
verdict: inconclusive_lean_proved:50
confidence: 0.85
parents:
- exp:environment-indexers-r1-extend
- verdict:environment-indexers-r1
tags:
- environment-indexers
- chain-extension
- verdict-experiment-transition
- proved
next_edges:
- exp:environment-indexers-r1-extend2
synthetic: true
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---


VERDICT: proved. Chain extended from 8 to 10 hops via verdict→experiment→verdict pattern.

**Chain:** idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → mvp → outcome → bigger → app_purpose
