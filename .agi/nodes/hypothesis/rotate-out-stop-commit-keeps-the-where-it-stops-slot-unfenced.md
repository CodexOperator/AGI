---
id: hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced
mint_id: 7e42072b75224e08bc575f2e2cfaa8ff
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 34a19cbeb3bd32b2
season: 2
testable_claim: "running rotate-out N times over one card leaves the slot's fence depth unchanged and every commit subject is the slot's first text line. Measured: belam 95b4f0a21 / 11e170950 / 1c69c9e81 and 2140897bfd / ffa6130a35 (09-24, subjects three and four backticks); thought-master 466e51d60 / ce70bc240."
title: "rotate-out's stop_commit neither re-fences the where-it-stops slot nor takes a fence line as its subject (assigned: director-engine)"
town: core
---
# hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced

# rotate-out's stop_commit neither re-fences the where-it-stops slot nor takes a fence line as its subject

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source measured by belam (PASS 3 step (6) ALREADY MEASURED + 09-24).

**Testable claim.** running rotate-out N times over one card leaves the slot's fence depth unchanged and every commit subject is the slot's first text line. Measured: belam 95b4f0a21 / 11e170950 / 1c69c9e81 and 2140897bfd / ffa6130a35 (09-24, subjects three and four backticks); thought-master 466e51d60 / ce70bc240.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
