---
id: verdict:environment-indexers-r1-chain-extension
mint_id: 6309ddbdc48342cabf6481b0be1b7129
type: verdict
parents:
  - verdict:environment-indexers-r1-extend2
  - exp:environment-indexers-r1-extend2
next_edges:
  - mvp:environment-indexers-r1
confidence: 1.0
contrasts: []
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs:
  - exp:environment-indexers-r1-chain-extension
season: 1
status: inconclusive_lean_proved:50
subgraph: false
supports: []
tags:
  - environment-indexers
  - chain-extension
  - verdict-experiment-transition
  - proved
thought_session: season
title: "environment-indexers/R1: Chain Extension — PROVED"
verdict: inconclusive_lean_proved:50
---
**Verdict:** PROVED

**Evidence:**
- environment-indexers chain now 12-hop: idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → mvp → outcome → bigger → app_purpose
- 13 chains total (6 domains at 12-hop, 1 at 8-hop via schema-registry)
- All 241 tests pass
- verdict→experiment→verdict cycles proven stackable (N cycles → (2N+8) hops)

**Chain structure:**
```
verdict:environment-indexers-r1 → exp:environment-indexers-r1-extend → verdict:environment-indexers-r1-extend → exp:environment-indexers-r1-extend2 → verdict:environment-indexers-r1-extend2 → mvp:environment-indexers-r1 → outcome:environment-indexers-r1 → bigger:environment-indexers-r1 → app_purpose
```

**Metrics:**
- longest_chain_length: 12 hops
- chain_count: 13
- environment_indexers_chain_hops: 12