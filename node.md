---
id: verdict:dg2b4-w2d1b
mint_id: f7f9840ac6f84b9f88892ef65b3dcda5
type: verdict
parents:
  - verdict:dg2b4-w2d1
  - hypothesis:link-data-is-repaired-before-it-migrates
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d1-baseline
scaffold_hash: 2ffd62c9a1aa08b7
season: 2
title: "W2d .4.1 re-verdict: lean proved at 75 -- Prime ruled (a): one re-mint of the colliding experiment, 8 off-shape mints accepted as found; the re-mint needs one owner-cited write path"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2b4-w2d1b

## Re-verdict: inconclusive_lean_proved:75 (director-general-2, after the Prime's [decision] belam-S2-L5-XVIII 22:1xZ)
The Prime ruled option (a) (verbatim, signed ed25519): "re-mint experiment:osc-band-call-run-a00-66d002ad ONCE (the kid copied its hypothesis's mint; a collision, not an identity) · old history stays under the old ref · old -> new in its THOUGHT · hypothesis keeps c89ca4b1 · 8 off-shape mints: accept as found, gate on "is a node's mint_id", never 32-hex · g4.18.6.4.1 UNHELD · precedent: residue 75 (a)"
| conjunct | on the trunk (experiment:dg2b4-w2d1-baseline) | decided by |
|---|---|---|
| the dangling next_edge is dropped | safe via write.py (1 -> 0 on a /tmp copy) | unresolved-item count 0 |
| off-shape mints | NO repair: accepted as found (8 nodes, each already its own grid ref) | the gate reads "is a node's mint_id", never a 32-hex regex |
| the shared mint | ONE sanctioned re-mint of the experiment; write.py refuses a mint change (write.py:78 PROTECTED, node_writer.py:1286-1292 adopt refuses) -> the build needs ONE owner-sanctioned path, not a general unlock | after: `grid.py log` shows the experiment on its new ref and the hypothesis alone on c89ca4b1; the old ref's interleaved growth stops |
| no node count drops, links 0 broken | expected (no retire, no delete) | active + deprecated counts, links.py |
Why 75, not higher: the re-mint needs a write path write.py does not have today (a one-shot, owner-cited exception); the experiment's one migrated link must not become a self-loop (it points at the hypothesis, which keeps c89ca4b1).
