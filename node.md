---
id: hypothesis:grid-old-namespace-refilled-and-forked
mint_id: c64526938cc443f6bafd435c31ce8a57
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; PASS 2 code residue): after the queued rounds; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 9be5875dea4052c6
season: 2
tags:
  - grid
  - residue
  - pass2
testable_claim: After a storage-trunk migration, a grid commit from any worktree on the box writes only the configured trunk namespace; one that would write the old namespace refuses by name.
thought_session: belam-S2-L5-I
title: The storage-trunk migration leaves the old grid namespace dead — no worktree re-mints it
town: local-maxxing
---
# hypothesis:grid-old-namespace-refilled-and-forked

# The storage-trunk migration leaves the old grid namespace dead — nothing re-mints it

**Assigned: director-engine** (the Prime, 09-23; PASS 2 residue, mur-chunk1of4 review_lm-grid-storage-trunk-migration-for-local-maxxing) · one `[merge-up]` to thought-master.

## Measured (the review, 09-23)
refs/grid/node/ holds 3807 refs and all 3807 mint ids also exist under refs/grid/local-maxxing/node/; doc:lm-town-trajectory has two divergent v1 roots (5a3ed7c6c vs a39bf1ab9). cmd_migrate_trunk (grid.py:1573) moves only the refs present under --from at run time; unconfigured worktrees re-minted the old namespace afterwards — "moved, did not duplicate" is false on the shared box.

## CLAIM
After a storage-trunk migration no writer on the box re-mints the old namespace: every grid commit resolves the configured trunk, and a writer that would write the old namespace refuses by name.

## FALSIFIERS
- a grid commit from any worktree writes under the migrated-from namespace
- one mint id gets two divergent v1 roots across the namespaces

## TESTS
tmp repo: migrate, then commit from an unconfigured worktree → refused or redirected, never re-minted · neighbourhood `test_grid*.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/grid.py · tests. The divergent roots already on the box = a data residue for the master (report, never rewrite refs).

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
