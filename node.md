---
id: verdict:topological-queries-r1
mint_id: f79fce513f4d4502be270f0b600333ed
type: verdict
parents:
  - exp:topological-queries-r1
next_edges: []
confidence: 0.65
contradicts: []
edited_by: season.py
evidence_runs:
  - exp:topological-queries-r1
season: 1
status: inconclusive_lean_proved:65
supports:
  - hyp:a00-c2d7dbcc-3987c7
tags:
  - verdict
  - topology
  - partial-support
thought_session: season
title: verdict:topological-queries-r1
verdict: inconclusive_lean_proved:65
---
# verdict:topological-queries-r1

**Experiment:** `exp:topological-queries-r1`
**Hypothesis:** `hyp:a00-c2d7dbcc-3987c7`
**Verdict:** `inconclusive_lean_proved:65`
**Confidence:** 0.65

## Evidence

- Match@7 = 100%: topology correctly identifies all 7 active idea domains
- Match@5 = 40%: topology cannot resolve fine-grained top-K priority
- Spearman ρ = 0.604: moderate positive rank correlation, significant inversions
- Chain length cleanly separates tiers (83-87 vs 7 vs 0 hops)

## Interpretation

Topology is a **valid coarse filter** for "which ideas are active" but not sufficient for "which idea should I work on next". Expert priority (chain-engine > graph-core) diverges from topology (schema-registry > chain-engine) because practical importance ≠ structural completeness.

## Spawns

- `hypothesis:topology-hybrid-ranking-r1`: topology rough filter + priority-weight field on idea nodes