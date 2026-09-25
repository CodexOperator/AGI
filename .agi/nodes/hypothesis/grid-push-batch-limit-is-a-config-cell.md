---
id: hypothesis:grid-push-batch-limit-is-a-config-cell
mint_id: 72bf3b177f0945428563d4075bb5cb6a
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: b5b63b00265b7824
season: 2
testable_claim: .agi/config.json carries grid.push_batch_limit and grid.py reads it with no literal fallback (absent = a named refusal); test_grid.py covers a 401-change three-batch push and a retry after one failed batch.
thought_session: belam-S2-L5-V
title: "grid.push_batch_limit is a config cell; the batched push is tested at 401 changes and on a partial failure (assigned: director-engine)"
town: core
---
# hypothesis:grid-push-batch-limit-is-a-config-cell

# hypothesis:grid-push-batch-limit-is-a-config-cell

Source: PASS 5 chunk 3, rounds engine-delta-2 ("Grid push batch limit remains a code default instead of a live config cell", extensions/agi/bin/grid.py:185) and a00-93414710-7b19d2 ("Batch limit is hardcoded fallback instead of a project config cell"; "the claimed 401-change three-batch case is not actually covered"; "partial-failure retry semantics lack an end-to-end regression", extensions/agi/tests/test_grid.py).

| | |
|---|---|
| claim | .agi/config.json carries grid.push_batch_limit; grid.py's push_batch_limit reads it with no literal fallback (absent = a named refusal); the batched push is tested at 401 changes (three batches) and on a retry after one failed batch |
| test | test_grid.py, fixtures only (a bare local remote, never origin) |
| falsifier | a literal default still decides the batch size, or either case is untested |

## Agent Notes
assigned: director-engine (PASS 5 residue, belam-S2-L5-V 09-25)
