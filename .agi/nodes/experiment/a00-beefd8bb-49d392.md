---
id: experiment:a00-beefd8bb-49d392
mint_id: 58e7baef7d0b44d1a6d76e60c3d67b34
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: fe8592a0b35123bd
title: Live-graph attractor list check — deprecation filter verified on real graph
verdict: inconclusive_lean_proved:50
---
# experiment:a00-beefd8bb-49d392

## Experiment

Loaded the live graph (1240 nodes, 75 ideas) via `graph_core.loader.load_directory` and `_frontmatter_for(.agi, 'idea')`, then computed the attractor list twice — once with the existing `count_live_descendants` + `_is_deprecated` filter (what agents actually see in INJECTION.md), once with raw `count_descendants` over all ideas (what they would see without the filter).

Found: 8 deprecated ideas (`domain-autoresearch-tree-skill`, `domain-chain-engine`, `domain-embeddings`, `domain-environment-indexers`, `domain-graph-core`, `domain-renderers`, `domain-schema-registry`, `engine-todo`).

**With filter (live attractor list):**
1. `idea:engine-tests` — 31 live descendants
2. `idea:domain-chain-bootstrap` — 20
3. `idea:engine-graph-core` — 20
... No deprecated ideas appear.

**Without filter (raw descendant count):**
1. `idea:domain-graph-core` — 75 (DEPRECATED)
2. `idea:domain-schema-registry` — 45 (DEPRECATED)
3. `idea:domain-chain-engine` — 44 (DEPRECATED)
4. `idea:domain-autoresearch-tree-skill` — 41 (DEPRECATED)
5. `idea:domain-renderers` — 40 (DEPRECATED)
6. `idea:domain-embeddings` — 39 (DEPRECATED)
7. `idea:domain-environment-indexers` — 38 (DEPRECATED)
8. `idea:engine-tests` — 31 (LIVE)

**Commands run:**
```
python3 -c "..."  # 3 variants: load with path fixes, compute filtered + unfiltered
```

## Evidence

Full script output from the live graph check:

```
Total fm_by_id entries: 75
Deprecated ideas: 8
  idea:domain-autoresearch-tree-skill
  idea:domain-chain-engine
  idea:domain-embeddings
  idea:domain-environment-indexers
  idea:domain-graph-core
  idea:domain-renderers
  idea:domain-schema-registry
  idea:engine-todo

=== WITH deprecation filter (count_live_descendants) ===
  dep=N idea:engine-tests: 31
  dep=N idea:domain-chain-bootstrap: 20
  dep=N idea:engine-graph-core: 20
  dep=N idea:engine-context-refs: 19
  dep=N idea:domain-session-management: 18
  ...

=== WITHOUT deprecation filter (count_descendants, ALL ideas) ===
  dep=Y idea:domain-graph-core: 75
  dep=Y idea:domain-schema-registry: 45
  dep=Y idea:domain-chain-engine: 44
  dep=Y idea:domain-autoresearch-tree-skill: 41
  dep=Y idea:domain-renderers: 40
  dep=Y idea:domain-embeddings: 39
  dep=Y idea:domain-environment-indexers: 38
  dep=N idea:engine-tests: 31  <-- first LIVE idea, pushed to #8
  ...
```

This completes the hypothesis's falsifier: the green half (deprecated ideas excluded from filtered list) verified by existing tests and confirmed on live graph; the red half (without filter, deprecated ideas dominate the ranking with 7 of the top 8 positions) confirmed on live graph. Both halves of the falsifier hold.


## Agent Notes
Live-graph confirmation: with deprecation filter, idea:engine-tests (31) and idea:engine-graph-core (20) head the attractor list; without filter, 7 deprecated domain-* ideas dominate top 7 (75..38 descendants). Both halves of falsifier confirmed on live graph. Closes the previously open 'live-graph observation' item from experiment:a00-a2533db0-095680.