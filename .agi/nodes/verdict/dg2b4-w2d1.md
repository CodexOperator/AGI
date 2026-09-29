---
id: verdict:dg2b4-w2d1
mint_id: 15bd97799e0c4e0a9c14933c203b5cd2
type: verdict
parents:
  - experiment:dg2b4-w2d1-baseline
  - hypothesis:link-data-is-repaired-before-it-migrates
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d1-baseline
scaffold_hash: 701479f9709b950a
season: 2
title: "W2d .4.1: lean disproved at 80 -- the dangling edge drops safely, but 9 mint repairs are refused by write.py and conflict with 'the mint id never changes'; shared mint c89ca4b1 = OWNER decision"
town: core
verdict: inconclusive_lean_disproved:80
---
# verdict:dg2b4-w2d1

## Verdict: inconclusive_lean_disproved:80 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2d1-baseline) | decided by |
|---|---|---|
| (1) each repair is a write.py edit with its reason in the THOUGHT | TRUE for 1 of 10 (the dangling item: `set next_edges [] && thought`, simulated `updated`); FALSE for the 9 mint repairs: `set`/`unset mint_id` ERR (PROTECTED, write.py:78), `adopt` SKIP (node_writer.py:1286-1292) | the write.py call per repair returns `updated` |
| (2) parents-aware unresolved count 1 -> 0 | TRUE in simulation: targets.py dangling 1 -> 0 after the write.py drop | targets.py / count.py before/after on the trunk |
| (3) all mint_ids 32-hex and unique | FALSE within the ceiling: 8 off-shape + 1 shared (2 nodes) remain; making them 32-hex and unique CHANGES 9 mint ids, which CLAUDE.md ("the mint id never changes"), goal:g2.5 and identity.py:445-452 forbid, and re-minting strands each node's `grid.py log` history (FALSIFIER 2) | count of non-32-hex or duplicated mint_ids = 0 (live + deprecated) |
| (4) no node deleted | TRUE: the only feasible repair (drop 1 item) deletes nothing; 5170 files before/after | file count before/after |
Lean: only the dangling-item repair is feasible and safe. The 9 mint repairs are a CONFLICT with "the mint id never changes" -- an owner decision (bank: accept the 8 off-shape mints as found, gate the migration on "is a node's mint_id" not the 32-hex regex; for the shared mint, whether to re-mint the kid's experiment with a grid-ref move). The shared mint is not dormant: its one grid ref has 2284 interleaved versions and grows by 2 per grid_sync tick.
CORRECTION: "the 8 off-shape or duplicated mint_ids" is 8 off-shape + 1 duplicated value on 2 nodes = 9 mint repairs (10 items with the dangling one), not 8. Inbound live items at HEAD 4819cabaa: 3 -> experiment:a00-1215e67e-de106f, 1 -> the shared mint, 0 -> the other 7 off-shape mints.
