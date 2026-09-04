---
id: experiment:a01-1835a461-27038b
mint_id: b98cdcae8cfe4c9294c1a9b9ed18e0cb
type: experiment
parents:
  - hypothesis:a00-dec78137-07daab
next_edges: []
confidence: 0.0
scaffold_hash: fda7371ac33a6fbd
title: A01 1835a461 27038b
verdict: pending
---
# experiment:a01-1835a461-27038b

## Experiment

### Design

Test the hypothesis that concurrent dispatch against a single target produces clones not coverage.

**Setup:** Observed the live iteration-1063 dispatch structure via manifest.json. P=2 kids (a00-8502d55e and a01-1835a461) were dispatched against the same hypothesis node `hypothesis:a00-dec78137-07daab` at the same zoom level (`--level small`) in parallel. Both kids produce experiment nodes (same type scaffolded). This replicates the concurrent-dispatch-against-single-target condition that the hypothesis claims produces content clones.

**Control contrast from the tree:** The 17-node subtree shows 14+ sibling hypotheses all rooted under `goal:g4.8`, each with a distinct title and `testable_claim` in their frontmatter. These were produced by prior dispatches where each kid targeted a different goal child node — the control condition that the hypothesis predicts would produce diverse output.

**Benchmark:** Ran `python3 _benchmark.py` to measure current graph build performance as a secondary metric (graph cold build time, the active autoresearch target).

### Results

**Concurrent dispatch structure (structural observation):**
- P=2 kids dispatched against hypothesis:a00-dec78137-07daab
- Both kids have type=experiment nodes (same scaffolded structure)
- Both kids targeted the same node at `--level small`
- Kids were dispatched within ~5s of each other (manifest timestamps: 1788489087 and 1788489092)

**Benchmark results:**
```
cold=151.66ms  warm=0.0407ms  n=1681  e=1782
```

Primary: graph_build_time_ms=0.05 (warm, noise floor from lru_cache)
Cold: graph_build_time_ms=151.66
- graph_node_count=1681
- graph_edge_count=1782
- query_time_ms=0.109
- ascii_render_lines=106
- warm_build_time_ms=0.0407

### Analysis

The hypothesis claims at least (P-1)/P kids targeting the same region produce clones. At P=2 this predicts 1 clone. Both kids were dispatched identically — same target, same level, same harness (pi, deepseek model), same tier (kid).

Limitation: P=2 is below the hypothesis' own threshold for strong claims (which specifies P ≥ 3). Both kids producing distinct experiments would not disprove (the hypothesis expects D ≤ 2 at P ≥ 3, not at P=2). Both producing clones would not prove it either (too few samples).

## Evidence

### Manifest excerpt (iteration 1063)

From `.agi/sessions/iter-1063/manifest.json`:
- Kid a00-8502d55e: target=hypothesis:a00-dec78137-07daab, tier=kid, node_id=experiment:a00-8502d55e-5fda78
- Kid a01-1835a461: target=hypothesis:a00-dec78137-07daab, tier=kid, node_id=experiment:a01-1835a461-27038b
- Both kids dispatched within 5s of each other
- Both at `--level small`, same model (deepseek/deepseek-v4-flash)

### Benchmark output

```
$ python3 _benchmark.py
METRIC graph_build_time_ms=0.05
METRIC graph_node_count=1701
METRIC graph_edge_count=1782
METRIC query_time_ms=0.0
METRIC ascii_render_lines=72
...
Using modular system: True
METRIC graph_build_time_ms=151.66
METRIC warm_build_time_ms=0.0407

cold=151.66ms  warm=0.0407ms  n=1681  e=1782
```

### Subtree diversity evidence

The hypothesis references experiment:the-bound-at-eight-real-agents which found 6/8 kids writing the same clause-4 hypothesis. The subtree shows 16+ sibling hypotheses under goal:g4.8, each with distinct `testable_claim` fields — consistent with the claim that target diversity (each kid targeting a different goal child) produces coverage, while single-target produces clones.


## Agent Notes
Structural observation: P=2 kids dispatched against same hypothesis node at P=2 (below hypothesis threshold for P>=3). Benchmark: cold=151.66ms, n=1681, e=1782. Concurrent dispatch structure confirmed operational — both kids produce same node type, same target.
