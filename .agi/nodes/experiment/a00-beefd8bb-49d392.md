---
id: experiment:a00-beefd8bb-49d392
mint_id: 58e7baef7d0b44d1a6d76e60c3d67b34
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
confidence: 0.95
scaffold_hash: fe8592a0b35123bd
title: Live-graph attractor list check — deprecation filter verified on real graph
verdict: inconclusive_lean_proved:90
evidence_runs:
  - experiment:a00-beefd8bb-49d392
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-89bf831c review, iter 1075. The kid's `proved` was mechanically
demoted to `inconclusive_lean_proved:50` at grid commit because the kid's
`cli.py done` omitted `evidence_runs`; the run itself is real and its numbers
were independently reproduced by both the sibling `experiment:a01-5ed85092-ea580b`
and the parent's own live-graph check (75 ideas, 8 deprecated, engine-tests 31
on top). So the 50 was a gate artifact, not a judgement on the evidence: this
edit adds the self-cite (`evidence_runs` — the run IS this node) and restores
the strength the evidence supports, at 90 rather than the sibling's `proved`
because this node is the duplicate measurement — the canonical live-graph
evidence lives in the sibling, which additionally re-ran the fixture suite and
checked the `inject.py` build path. One claim in the kid's report is REJECTED:
its `struggles:` line alleges `_fm_status_for_ideas` has a silent data-path
bug ("calling `_frontmatter_for(root)` instead of `root/.agi`"). Parent verified
otherwise: `briefing._fm_status_for_ideas(root)` calls exactly what `inject.py`
calls directly with the same root, and from the resolved root
`/home/ubuntu/work/agi/.agi` it returns all 75 ideas including the 8
deprecated — the kid's own run used the same path and got 75 entries. The bug
was the kid's scratch-script path, not the briefing code; no defect filed.
<!-- THOUGHT:END -->