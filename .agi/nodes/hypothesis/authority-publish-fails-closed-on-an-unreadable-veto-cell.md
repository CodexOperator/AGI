---
id: hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell
mint_id: 73bffdad03374abc8fbad545b63c1e5b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 78c4e15f7e38c732
season: 2
testable_claim: "rotate.py (~10415): an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test."
title: "The authority publish fails closed when the veto cell cannot be read (assigned: director-engine)"
town: core
---
# hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell

# The authority publish fails closed when the veto cell cannot be read

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round engine-delta-5 (demote).

**Testable claim.** rotate.py (~10415): an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
