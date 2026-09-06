---
id: experiment:a00-6e08546b-aed026
mint_id: d1c7a282e71d4cb88191a7c518986e41
type: experiment
parents:
  - hypothesis:l2w6-telemetry-rollup
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-6e08546b-aed026
scaffold_hash: 18aeefd0188cc233
season: 1
title: A00 6e08546b aed026
verdict: proved
---
# experiment:a00-6e08546b-aed026

## Experiment

Implemented `cost_per_aligned_outcome` — the ranking number the hypothesis explicitly names but previous experiments left unimplemented.

### Changes to `extensions/agi/bin/telemetry_rollup.py`
1. **`count_aligned_outcomes(root, node_id)`** — new function. Walks the same bidirectional BFS as `walk_experiments` and counts outcome nodes with `alignment=aligned` in their frontmatter. Uses cached graph index. Returns int.
2. **`do_rollup`** — calls `count_aligned_outcomes` after telemetry collection. Computes `cost_per_aligned_outcome = cost_usd_total / aligned_outcomes_count` when both are nonzero, stores as `cost_per_aligned_outcome: float | None` in result dict. Also adds `aligned_outcomes_count: int`.
3. **CLI output** — prints aligned outcome count and cost_per_aligned_outcome (or n/a) in both human-readable and JSON modes.

### Tests (`extensions/agi/tests/test_telemetry_rollup.py`)
- `test_count_aligned_outcomes_zero` — no outcome has alignment → count=0
- `test_count_aligned_outcomes_counted` — outcome with `alignment=aligned` → count=1
- `test_do_rollup_includes_aligned_count_and_cost` — result includes both fields
- `test_do_rollup_cost_per_aligned_computed` — 0.02 cost / 1 aligned = 0.02
- `test_do_rollup_aligned_no_cost_per_aligned` — no aligned outcomes → None

### Verify commands (actual outputs)

**1. Telemetry rollup tests pass (22/22)**
```
$ python3 -m pytest extensions/agi/tests/test_telemetry_rollup.py -q
......................                                                   [100%]
22 passed in 0.14s
```

**2. Full engine suite (all telemetry tests + pre-existing unrelated failure)**
```
$ python3 -m pytest extensions/agi/tests/ -q
...
1 failed, 1657 passed, 9 skipped in 93.93s
```
The 1 failure (`test_minted_node_stamps_loop_model_profile_from_env`) is pre-existing and unrelated — tests that AGI_LOOP env var stamps `loop` field; no code in my changes touches node_writer. Telemetry-specific tests all pass.

**3. Real roll-up on outcome:a00-c8365a0c-85a6d1 (dry-run JSON)**
```json
{
  "aligned_outcomes_count": 0,
  "cost_per_aligned_outcome": null,
  "sums": { "cost_usd_total": 0, ... },
  "experiments_found": 92,
  "nodes_skipped": 92
}
```

**4. Real roll-up on outcome:a00-ddbe3410-outcome001-chain-bootstrap (dry-run JSON)**
```json
{
  "aligned_outcomes_count": 0,
  "cost_per_aligned_outcome": null,
  "experiments_found": 9,
  "nodes_skipped": 9
}
```

Both real rollups show 0 aligned outcomes and null cost_per_aligned_outcome because (a) telemetry stamping (l2w2) hasn't populated cost fields yet, and (b) no outcome nodes have `alignment=aligned` yet (all are `alignment: unknown` from season.py creation). This is an honest baseline — the counts are correct, just the data hasn't arrived.

## Evidence

All command outputs embedded above. The key gap from the previous experiment (`a00-6856367d-7b307d`, verdict inconclusive_lean_proved:60) was specifically "cost_per_aligned_outcome — the ranking number the hypothesis names explicitly — is not implemented." This experiment closes that gap: the roll-up now computes and displays `aligned_outcomes_count` and `cost_per_aligned_outcome`, consistent with the hypothesis's stated requirement.

## Agent Notes
Implemented cost_per_aligned_outcome — the ranking number the hypothesis names. Added count_aligned_outcomes() BFS walker counting outcomes with alignment=aligned; do_rollup computes cost_per_aligned_outcome = cost_usd_total / aligned_count when both >0. 5 new tests (22 total) all green. Real roll-ups on 2 outcomes show aligned_outcomes_count=0 (no outcomes have alignment=aligned yet) and cost_per_aligned_outcome=null (telemetry stamping not done), honest baseline. Closes gap identified in experiment:a00-6856367d-7b307d review which demoted proved->60% specifically for this missing feature.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-de25bce0 review, L2.13: node version now carries parent approval, not just the kid self-report. Verified independently, did not read the report at face value: (1) 22/22 tests in test_telemetry_rollup.py pass on the live tree; (2) the one full-suite failure (test_minted_node_stamps_loop_model_profile_from_env) reproduces on a pristine HEAD worktree, so it is pre-existing and unrelated to this change, as the kid claimed; (3) real dry-run rollup on outcome:a00-c8365a0c-85a6d1 reproduces the recorded output exactly, now including "aligned outcomes: 0" and "cost_per_aligned_outcome: n/a"; (4) cost_per_aligned_outcome is print-only in code, never gates anything, as the hypothesis requires. This closes precisely the gap for which sibling experiment:a00-6856367d-7b307d was demoted proved->inconclusive_lean_proved:60 in the L2.12 review (missing ranking number). Kid struggles (quadruple-quote syntax error, self-caught) and caveats (real-data n/a because l2w2 stamps and alignment=aligned outcomes do not exist yet) are honest and consistent with the artifact. Verdict kept at proved: the hypothesis is a functional spec, every clause of it is implemented and evidenced by a named run, and the zero baseline is the one the hypothesis itself anticipated.
<!-- THOUGHT:END -->
