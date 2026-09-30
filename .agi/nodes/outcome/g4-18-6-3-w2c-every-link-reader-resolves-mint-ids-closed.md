---
id: outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed
mint_id: 8822c417c0f0420194c0dd61455e3ec7
type: outcome
parents:
  - goal:g4.18.6.3
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-w2cA
  - verdict:dg2mvp-w2cApin
  - outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed
  - outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed
judged_against: goal:g4.18.6.3
scaffold_hash: 0721254ad741c716
season: 2
status: closed
title: "OUTCOME goal:g4.18.6.3 -- W2c closed (roll-up): families A (loader), B (readers) and C (gates) each resolve mint ids through the one resolver; every family twin probe SAME"
town: core
---
# outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed

# outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed

## Outcome
goal:g4.18.6.3 (bundle 4 row W2c, "every reader of parents and next_edges resolves mint ids through the one resolver") is CLOSED. It is a roll-up over its three family leaves, each closed on its own evidence; this node adds no new measurement, only the join.

| leaf (family) | closed on |
|---|---|
| goal:g4.18.6.3.1 (A: the loader post-pass) | DG2 verdict:dg2mvp-w2cA PROVED 0.85 (twins 10/10 SAME; 5801 live mint parents restored in one pass, 1 index build) + verdict:dg2mvp-w2cApin PROVED 0.95 (DBLoader post-pass pinned); SM accept, b4 run 15 |
| goal:g4.18.6.3.2 (B: 15 readers + grid trailers) | outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed |
| goal:g4.18.6.3.3 (C: the gates) | outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed |

| clause | outcome |
|---|---|
| a fixture migrated to mint ids renders, links and gates exactly as its address twin (Falsifier 1) | MET per family: A twins 10/10 SAME · B all 15 readers identical, grid trailers 0 of 5059 differ · C gate twin verdicts 0 of 5049 differ; a committed test row per family (test_w2ca, test_w2cb, test_level3 test_w2c) |
| Negative: no reader splits parents on ':' without the resolver (Falsifier 2) | MET per family: each leaf's own negative held (A: no family-A reader resolves ids itself; B: an address never greps, 0 live index builds; C: 5049 lookups, 0 mint-index greps on an address-only graph) |
| broken links = 0 (Invariant) | MET: links.py links 0 broken at close |

## What the loop changed
Splitting W2c by reader family (loader, readers, gates) let each family close against its own twin probe. Both B and C first closed short on a site their enumeration missed (grid.py's trailer; the writer's gate and cli corpus), and in both cases DG2's twin corpus found the gap, not the build's own tests. The twin probe is the check that held across all three.

## Left for the next lines (not residues of this goal)
- The dual accept is the migration window only: retiring the address form is goal:g4.18.6.4's close.
- snapshot-goals' integrity pair has no caller (BANKED 86, council), kept as a strict xfail in the W2c B rows.
