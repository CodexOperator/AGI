---
confidence: 1.0
id: "exp:a00-1467544f-chain-600hop"
mint_id: d724424a24e54a369cebe5401ec060f4
next_edges:
  - verdict:a00-1467544f-chain-600hop
parents:
  - hyp:a00-1467544f-chain-600hop
subgraph: false
tags:
  - chain-engine
  - extension
  - 600-hop
testable_claim: Add verdict→experiment→verdict cycles 248-296 to extend chains from 502 to 600 hops
title: "Experiment: extend chains to 600 hops"
type: experiment
---

**Experiment:** Run `exp-a00-1467544f-extend-600hop.py` which:
1. Protects nodes via LAST_GOOD_COMMIT guard
2. Identifies 6 chains at 502 hops (domains: graph-core, chain-engine, environment-indexers, exporters, renderers, autoresearch-tree-skill)
3. Adds cycles 248-296 (49 cycles × 6 chains × 2 nodes/cycle = 588 new nodes)
4. Updates extend247 verdict to point to first new experiment

**Results:**
- 6 chains extended from 502 to 600 hops
- Formula hops = 2*cycle + 8 verified at cycle 296
- Total: 20 chains (6 at 600+, 3 at 300, 1 at 10, 10 at 8)
