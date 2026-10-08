---
id: hypothesis:grid-push-batch-limit-is-a-config-cell
mint_id: 72bf3b177f0945428563d4075bb5cb6a
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: b5b63b00265b7824
season: 2
testable_claim: .agi/config.json carries grid.push_batch_limit and grid.py reads it with no literal fallback (absent = a named refusal); test_grid.py covers a 401-change three-batch push and a retry after one failed batch.
thought_session: belam-S2-L5-V
title: "grid.push_batch_limit is a config cell; the batched push is tested at 401 changes and on a partial failure (assigned: director-engine)"
town: core
---
# hypothesis:grid-push-batch-limit-is-a-config-cell

# hypothesis:grid-push-batch-limit-is-a-config-cell

## Measured
Source: PASS 5 chunk 3, rounds engine-delta-2 ("Grid push batch limit remains a code default instead of a live config cell", extensions/agi/bin/grid.py:185) and a00-93414710-7b19d2 ("Batch limit is hardcoded fallback instead of a project config cell"; "the claimed 401-change three-batch case is not actually covered"; "partial-failure retry semantics lack an end-to-end regression", extensions/agi/tests/test_grid.py).

## CLAIM
.agi/config.json carries grid.push_batch_limit; grid.py's push_batch_limit reads it with no literal fallback (absent = a named refusal); the batched push is tested at 401 changes (three batches) and on a retry after one failed batch.

## Dispatch line
config-max: `grid.push_batch_limit` in `.agi/config.json` / template-max: none / code: `grid.py` `push_batch_limit` reads the cell, absent = a named refusal (grid.py:182-194 in the bytes today; that refusal's `sys.exit` on the live grid_sync path is PASS 7's hypothesis:grid-sync-survives-a-project-without-push-batch-limit)

## FALSIFIERS
a literal default still decides the batch size, or either case (401 changes, retry after one failed batch) is untested

## TESTS
test_grid.py, fixtures only (a bare local remote, never origin)

## FILE SCOPE
extensions/agi/bin/grid.py · extensions/agi/tests/test_grid.py · .agi/config.json (grid.push_batch_limit only)

## CEILING
1 parent (pi-free) · <= 2 kids · 10-12 production lines per conjunct · 0 USD

## Agent Notes
assigned: director-engine (PASS 5 residue, belam-S2-L5-V 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch): the round brief was a claim/test/falsifier table, not the [hypothesis] schema order, and had no Dispatch line. Re-laid in schema order with the same content; the Dispatch line names the cell and cross-references the sys.exit defect PASS 7 split out.
<!-- THOUGHT:END -->
