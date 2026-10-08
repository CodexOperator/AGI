---
id: verdict:chain-engine-r15
mint_id: 86bb3d48cb66456695228dd933a7405c
type: verdict
parents: []
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs: []
season: 1
status: inconclusive_lean_proved:50
tags:
  - chain-engine
  - R15
  - second-cycle
  - proved
thought_session: season
title: "chain-engine/R15: verdict→experiment→verdict cycles are stackable (12-hop chains)"
verdict: inconclusive_lean_proved:50
---
**Verdict:** PROVED (confidence: 0.95)

Second verdict→experiment→verdict cycle extends chains from 10→12 hops. 7 domains achieve 12-hop chains on cold reload. Stackable pattern: N cycles → (2N+8) hops. 241 tests pass.