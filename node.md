---
id: hypothesis:harness-bin-absolute-token-free-bins-refused-by-name
mint_id: b1da83fa9b824b158a3a0f7a736c0693
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 32efdbe2cfc014ca
season: 2
testable_claim: adapters/__init__.py (~61) refuses a configured absolute bin that does not exist, naming the harness and the path, instead of passing it through; a committed test proves the refusal.
title: "A missing token-free absolute harness bin is refused by name (assigned: director-engine)"
town: core
---
# hypothesis:harness-bin-absolute-token-free-bins-refused-by-name

# A missing token-free absolute harness bin is refused by name

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round harness-bin-paths-resolve-per-box (demote).

**Testable claim.** adapters/__init__.py (~61) refuses a configured absolute bin that does not exist, naming the harness and the path, instead of passing it through; a committed test proves the refusal.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
