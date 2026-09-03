---
id: hyp:a01-8444c4b6-92d465
mint_id: 4e232163194e490cb7313c54ccf0145c
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
title: A01 8444c4b6 92d465
verdict:
wired_at: 1777664395
wired_from: a01-8444c4b6
---
**Hypothesis:** Batch node/edge insertion (`add_nodes([])`, `add_edges([])`) is materially faster than N individual `add_node()` / `add_edge()` calls because: (1) the batch amortizes graph-rebuild overhead over the set, (2) cycle-detection DFS runs once over the full edge batch rather than N times, and (3) the persistence backend can write once per batch instead of once per node.

**Proof:** Profile N=50 node insertions and N=100 edge insertions; batch version completes in <50% of the time of the sequential loop at the same graph scale.

**Disproof:** Batch version is within noise floor of sequential version — no material speedup from batching at this graph size.


R11 batch ops: batch insertion faster than N sequential calls