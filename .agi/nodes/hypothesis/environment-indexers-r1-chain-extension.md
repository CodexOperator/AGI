---
id: hyp:environment-indexers-r1-chain-extension
mint_id: abb147d3311c454499bca1b087fe383a
type: hypothesis
parents:
  - idea:domain-environment-indexers
edited_by: season.py
season: 1
subgraph: false
tags:
  - environment-indexers
  - chain-extension
  - verdict-experiment-transition
thought_session: season
title: "environment-indexers/R1: Extend chain to 12 hops via verdict→experiment→verdict cycles"
---
**Description:** The environment-indexers domain has 9 hypotheses but no complete 10 or 12-hop chain. Extend the r1 chain by adding verdict→experiment→verdict→mvp→outcome→bigger→app_purpose nodes.

**Method:**
1. Update verdict:environment-indexers-r1 next_edges to include exp:environment-indexers-r1-extend
2. Create exp:environment-indexers-r1-extend → verdict:environment-indexers-r1-extend → exp:extend2 → verdict:extend2 → mvp
3. Verify find_chains() returns 12-hop chain for environment-indexers

**Acceptance Criteria:**
- [ ] Chain: idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → mvp → outcome → bigger → app_purpose (12 hops)
- [ ] All 241 tests pass
- [ ] Cold reload yields same chain structure