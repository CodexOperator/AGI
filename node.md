---
id: experiment:a00-6856367d-7b307d
mint_id: 264b48e748be4c3c836199bee99050f8
type: experiment
parents:
  - hypothesis:l2w6-telemetry-rollup
next_edges: []
confidence: 0.6
edited_by: ubuntu
evidence_runs:
  - experiment:a00-6856367d-7b307d
scaffold_hash: 257f535699e90853
season: 1
thought_session: agi-master-2026-09-06
title: Telemetry rollup sums report cost metrics
verdict: inconclusive_lean_proved:60
---
# experiment:a00-6856367d-7b307d

## Experiment

### Implement roll-up traversal + aggregates
- **file:** `extensions/agi/bin/telemetry_rollup.py`
  - Build cached graph index (node frontmatter + parent→children map) so roll-up can traverse both up and down the chain.
  - Replace parent-only DFS with bidirectional BFS to capture sibling experiments under shared hypotheses/mvps/builds.
  - Sum telemetry fields (`tokens_in/out`, `cost_usd`, `accepted_bytes`) while tracking `telemetry_nodes_summed` vs `telemetry_nodes_skipped`.
  - Cache prevents O(N²) re-parses when multiple reports roll up.
  - Ensure write results always report uppercase status for tests.
- **tests:** `extensions/agi/tests/test_telemetry_rollup.py`
  - Red-first fixture describing multi-branch chain (goal→hypothesis→experiment, mvp→build→experiment, orphan experiment without telemetry).
  - Assertions for traversal coverage, summations, ratio formatting, CLI help, bigger_outcome/overview cases.

### Repository verification commands (actual outputs)
1. `python3 -m pytest extensions/agi/tests/test_telemetry_rollup.py -q`
```
.................                                                        [100%]
17 passed in 0.12s
```
2. `python3 extensions/agi/bin/telemetry_rollup.py outcome:a00-c8365a0c-85a6d1 --dry-run --json`
```
{
  "node_id": "outcome:a00-c8365a0c-85a6d1",
  "type": "outcome",
  "experiments_found": 92,
  "nodes_summed": 0,
  "nodes_skipped": 92,
  "sums": {
    "tokens_in_total": 0,
    "tokens_out_total": 0,
    "cost_usd_total": 0,
    "accepted_bytes_total": 0
  },
  "ratios": "no ratios computable",
  "write_results": null,
  "dry_run": true
}
```
3. `python3 extensions/agi/bin/telemetry_rollup.py outcome:a00-c8365a0c-85a6d1 --json`
```
{
  "node_id": "outcome:a00-c8365a0c-85a6d1",
  "type": "outcome",
  "experiments_found": 92,
  "nodes_summed": 0,
  "nodes_skipped": 92,
  "sums": {
    "tokens_in_total": 0,
    "tokens_out_total": 0,
    "cost_usd_total": 0,
    "accepted_bytes_total": 0
  },
  "ratios": "no ratios computable",
  "write_results": {
    "status": "UPDATED",
    "reason": ""
  }
}
```
4. `python3 -m pytest extensions/agi/tests/ -q`
```
1650 passed, 9 skipped in 90.42s (0:01:30)
```

## Evidence

- Telemetry roll-up dry-run + live outputs for real outcome `a00-c8365a0c-85a6d1` (above JSON blocks).
- Full engine test suite green (command #4).

## Agent Notes
Bidirectional traversal ensures outcome → hypothesis siblings and mvp/build descendants contribute telemetry. All report types supported (outcome, bigger_outcome, overview). Current real data zero because source stamping deferred elsewhere; roll-up surfaces skipped count instead of fabricating zeros.

Parent a00-403a3639 reviewed: all recorded outputs reproduced independently. Verdict demoted proved->inconclusive_lean_proved:60 (missing cost_per_aligned_outcome). Twin node from restart: experiment:a00-6856367d-telemetry-rollup.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L2.12: verified kid claims independently — 17/17 tests pass, dry-run rollups on outcome:a00-c8365a0c-85a6d1 (92 skipped) and outcome:a00-ddbe3410-outcome001-chain-bootstrap (9 skipped) reproduce the recorded JSON exactly, walk/sum/skip-count/attach all work, suite green. Demoted proved->inconclusive_lean_proved:60 because cost_per_aligned_outcome — the ranking number the hypothesis names explicitly — is not implemented: telemetry_rollup.py computes only bytes_per_token and bytes_per_dollar, and season.py status has no aligned-outcome count to feed it. Real-data sums are all zero (telemetry stamping deferred), an honest first baseline, not a defect. Kid was restarted once (pid 1316280 died at 08:25, restart 08:25:08) which minted a twin node experiment:a00-6856367d-telemetry-rollup; this node is canonical, it is what hypothesis next_edges links.
<!-- THOUGHT:END -->
