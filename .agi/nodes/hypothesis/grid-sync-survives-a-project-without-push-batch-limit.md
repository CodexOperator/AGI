---
id: hypothesis:grid-sync-survives-a-project-without-push-batch-limit
mint_id: 6dd20dbfb66e48b98bb727ba0fc18638
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass7-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: f1110b4e9c1560ba
season: 2
testable_claim: A project whose config lacks grid.push_batch_limit still gets its grid commit + push on the cron path, the missing cell named once in the log, and the value lives in one declared place, never a code literal.
thought_session: belam-S2-L5-VII
title: "grid_sync survives a project whose config lacks push_batch_limit (assigned: director-engine)"
town: core
---
# hypothesis:grid-sync-survives-a-project-without-push-batch-limit

# hypothesis:grid-sync-survives-a-project-without-push-batch-limit

assigned: director-engine. PASS 7 residue (hypothesis:pass7-0926-residue-batch).

## Measured
grid.py:190-191 refuses by name and sys.exits when .agi/config.json lacks grid.push_batch_limit (landed a39187ca27, round B). The grid_sync cron runs grid.py commit --all + push for every project on the box (cron:crons mirror_towns: true), so a project without the cell stops versioning. Found independently by the engine-delta-1 and grid-push-batch-limit-is-a-config-cell rounds.

## CLAIM
A project whose config lacks grid.push_batch_limit still gets its grid commit + push on the cron path, the missing cell NAMED once in the log; the value lives in ONE declared place, never a code literal.

## Dispatch line
config-max: the default as ONE declared config/schema cell / template-max: none / code: the cron-path branch in grid.py.

## FALSIFIERS
A fixture project without the cell makes grid_sync exit non-zero or push nothing; 200 reappears as a literal in code.

## TESTS
extensions/agi/tests/test_grid.py (+ test_crons_mirror.py neighbourhood).

## FILE SCOPE
extensions/agi/bin/grid.py · .agi/config.json (only if the default moves there) · extensions/agi/tests/test_grid.py

## CEILING
1 parent (pi-free) · <= 2 kids · 10-12 production lines per conjunct · 0 USD
