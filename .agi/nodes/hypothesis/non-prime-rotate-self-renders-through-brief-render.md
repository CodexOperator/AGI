---
id: hypothesis:non-prime-rotate-self-renders-through-brief-render
mint_id: 0a050ff88c5b4d45acc8fdddc5323342
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: e70a8c4e98385982
season: 2
testable_claim: "rotate.py (~19388): the non-prime rotate-self path assembles the successor's first turn through brief.render exactly as the prime path does; a committed test compares the two renders."
title: "A real non-prime rotate-self renders its first turn through brief.render (assigned: director-engine)"
town: core
---
# hypothesis:non-prime-rotate-self-renders-through-brief-render

# A real non-prime rotate-self renders its first turn through brief.render

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round brief-py-assembles-every-first-turn-from-config (demote).

**Testable claim.** rotate.py (~19388): the non-prime rotate-self path assembles the successor's first turn through brief.render exactly as the prime path does; a committed test compares the two renders.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
