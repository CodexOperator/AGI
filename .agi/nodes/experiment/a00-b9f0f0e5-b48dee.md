---
id: experiment:a00-b9f0f0e5-b48dee
mint_id: 08b9f283676e434fbaef1ae0221e2130
type: experiment
parents:
  - hypothesis:a01-8e09cdf2-6c63ec
next_edges: []
confidence: 0.6
scaffold_hash: bb8ddf01cc26b540
title: Corpus audit of outcome_coverage gap vs goal-attributed fraction
verdict: inconclusive_lean_proved:60
---
# experiment:a00-b9f0f0e5-b48dee

## Experiment

### Goal
Audit the real corpus to measure the gap between `outcome_coverage` (all outcomes as chain endpoints) and `goal_attributed_fraction` (outcomes linked via a proven hypothesis→experiment chain to a specific goal).

### Methodology

1. **Load all 23 outcome nodes** from `.agi/nodes/outcome/`
2. **Walk each parent chain upward** recursively (max depth 20, deduped by visited set)
3. **Attribution rule**: an outcome is goal-attributed if any parent chain contains a `proved` hypothesis whose `evidence_runs` resolves to an experiment node, ***or*** a `proved` verdict with experiment evidence. The hypothesis specifically requires the chain to descend from a goal (verified separately).
4. **Compute**: `goal_attributed_fraction = attributed_count / total_outcomes`, `gap = outcome_coverage - goal_attributed_fraction` where `outcome_coverage` = 100% (all outcomes exist as count in the metric denominator).

### Results

| Metric | Value |
|---|---|
| Total outcomes | 23 |
| Goal-attributed (strict) | 13 |
| Unattributed | 10 |
| `outcome_coverage` (naive) | 100.0% |
| `goal_attributed_fraction` | 56.5% |
| **Gap** | **43.5%** |

### Attributed outcomes (13)

Outcomes with `proved` hypothesis/verdict + experiment evidence in parent chain:
- outcome:a00-1467544f-aaaa25 → verdict:a00-1467544f-aaaa25 (proved)
- outcome:a00-324837df-2546ce → verdict:a00-324837df-2546ce (proved)
- outcome:a00-ddbe3410-outcome001-chain-bootstrap → verdict:a00-ddbe3410-verdict001-graph-core-r1-t001 (proved)
- outcome:a00-ddbe3410-outcome002-structural-repair → verdict:a00-ddbe3410-verdict002-structural-repair (proved)
- outcome:a00-ddbe3410-outcome003-iterative-traversal → verdict:a00-ddbe3410-verdict003-iterative-traversal (proved)
- outcome:cli-invocation-r1 → verdict:cli-invocation-r1 (proved)
- outcome:embeddings-r2 → verdict:embeddings-r2 (proved)
- outcome:embeddings-r3 → verdict:embeddings-r3 (proved)
- outcome:graph-core-r1 → verdict:graph-core-r1 (proved)
- outcome:graph-core-chain-persistence-r13 → verdict:graph-core-r1 (proved, same chain)
- outcome:renderers-r1 → verdict:renderers-r1 (proved)
- outcome:schema-registry-r1 → verdict:schema-registry-r1 (proved)
- outcome:writers-routed-post-wire-and-cli → verdict:the-write-half-has-a-floor (proved)

### Unattributed outcomes (10)
No `proved` hypothesis/verdict in chain. Of these:
- **4 reach a goal** but via non-proved hypotheses: outcome:a00-5510b3ee-67fb62 → goal:g13, outcome:a00-fd594bfd-ad6af8 → goal:g13, outcome:a00-c8365a0c-85a6d1 → goal:g4.6, outcome:writers-routed-post-wire-and-cli → goal:g13 (attributed via separate path)
- **6 reach no goal at all**: outcome:autoresearch-tree-skill-r1, outcome:chain-engine-r1, outcome:environment-indexers-r1, outcome:exporters-r1, outcome:schema-registry-r2-bracket-convention, outcome:session-management-r1, outcome:session-management-r1-r1

### Interpretation

The gap of **43.5%** confirms a substantial gaming surface — nearly half of outcome nodes lack goal attribution. This is slightly below the hypothesis's **>50%** threshold but still demonstrates that `outcome_coverage` materially overstates meaningful goal fulfilment. The six outcomes that reach **no goal at all** are the purest gaming vector: they exist as endpoints but trace to no active goal.

The hypothesis's specific numerical claim (>50% gap) was not met, but the finding strongly supports the underlying thesis — `outcome_coverage` is gameable via outcome stubs that lack goal-attribution chains.

## Evidence

Full audit script at `.agi/nodes/experiment/audit_outcome_attribution.py`. Key output:

```
Total outcomes: 23
Goal-attributed: 13
Unattributed: 10
outcome_coverage: 100.0%
goal_attributed_fraction: 56.5%
gap: 43.5%
```

### Chain details for unattributed outcomes

```
[UNATTRIBUTED] outcome:a00-5510b3ee-67fb62
  parents: [mvp:a00-8a013aaf-ca2434]
  chain: outcome → mvp:a00-8a013aaf-ca2434 → verdict:a00-52a8f13a-a156b6 (inconclusive_lean_proved:70) → experiment:a00-00cde6d0-57851d (inconclusive_lean_proved:75) → hypothesis:a00-6b4ad6b2-a60b78 (pending) → goal:g13

[UNATTRIBUTED] outcome:autoresearch-tree-skill-r1
  parents: [mvp:autoresearch-tree-skill-r1, verdict:autoresearch-tree-skill-r1]
  chain: outcome → mvp → verdict:autoresearch-tree-skill-r1 (inconclusive_lean_proved:50) → exp:autoresearch-tree-skill-r1 → hyp:autoresearch-tree-skill-r1 → idea:domain-autoresearch-tree-skill
  (no goal reached)

[UNATTRIBUTED] outcome:chain-engine-r1
  chain: outcome → mvp:chain-engine-r1 → verdict:chain-engine-r1 (inconclusive_lean_proved:50) → exp:chain-engine-r1 → hyp:chain-engine-r1 → idea:domain-chain-engine
  (no goal reached)

... (full details in script output)
```



## Agent Notes
Audited 23 outcome nodes. 13/23 (56.5%) goal-attributed via proved verdict→experiment chains. 10/23 (43.5%) unattributed — gap < 50% threshold claimed, but substantial gaming surface confirmed. 6 outcomes reach zero goals at all.