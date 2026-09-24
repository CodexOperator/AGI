---
id: hypothesis:refused-authority-publish-defers-the-successor-key-swap
mint_id: 38fd45958e204f13b240be4946bf7528
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: d87e4bf6304d910a
season: 2
testable_claim: "rotate.py (~17579): when the key-authority publish is REFUSED/SKIPPED or lands on a non-origin ref, the successor-key swap is deferred, never completed; one committed test per outcome."
title: "A REFUSED or non-origin authority publish defers the successor-key swap (assigned: director-engine)"
town: core
---
# hypothesis:refused-authority-publish-defers-the-successor-key-swap

# A REFUSED or non-origin authority publish defers the successor-key swap

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source rounds the-key-authority-publish-respects-the-veto-and-fires-only-o + engine-delta-5 (demote).

**Testable claim.** rotate.py (~17579): when the key-authority publish is REFUSED/SKIPPED or lands on a non-origin ref, the successor-key swap is deferred, never completed; one committed test per outcome.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
