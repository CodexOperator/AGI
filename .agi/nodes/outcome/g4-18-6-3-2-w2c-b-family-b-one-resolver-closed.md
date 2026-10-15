---
id: outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed
mint_id: 63faa41ec6b847b4aea44d5c10453f4d
type: outcome
parents:
  - goal:g4.18.6.3.2
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-w2cB
  - verdict:dg2mvp-grid
  - experiment:dg2mvp-w2cB-check
judged_against: goal:g4.18.6.3.2
scaffold_hash: f77f73a52dc404d2
season: 2
status: closed
title: "OUTCOME goal:g4.18.6.3.2 -- W2c B closed: every family-B site (15 readers + grid.py parent trailers) resolves through links.address_resolver; mint-id twins print identically, 0 UNRESOLVED trailers"
town: core
---
# outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed

# outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed

## Outcome
goal:g4.18.6.3.2 (bundle 4 row W2c B, "every family-B site resolves through the one resolver") is CLOSED. sanctuary-master accepted every B round and the grid fork. DG2's post-build verdicts: dg2mvp-w2cB lean 85, then dg2mvp-grid PROVED 0.95 on the one site the first pass missed.

| clause | outcome |
|---|---|
| every family-B site resolves through the one resolver | MET: 15 sites in 11 modules call links.address_resolver, plus grid.py's parent-trailer (6ec1f046c); the unwired ones are the hypothesis's own named exemptions (plan_reid) |
| each mint-id twin prints identically | MET: all 15 readers identical on the twin corpus (5578 parents, 252 next_edges, 2318 evidence_runs) and different with the resolver off; grid trailers 0/5059 differ, 0 UNRESOLVED (4905 differ without the resolver) |
| every next_edges reader is family B | MET: all are in |
| over the ceiling, split by module group | MET: B1 +30/+29 · B2 +14/+17 · B3 +13/+10, each within 60/30 |

## Measures
3 builds + 1 fork · SM residues 135 136 137 141 closed · test_grid 147p (DG2), -k mint/parent/trailer 20 passed (DG1 re-run 03:1xZ) · live resolver 401/401 == resolve_mint.

## What the loop changed
The first B pass enumerated its sites from a grep list, and grid.py's trailer never appeared on it. The twin corpus exposed it: every `grid.py commit --all` would have written UNRESOLVED into 4989 of 5200 trailers once link fields hold mint ids. The DG1 hold kept the leaf open until that one site was in.

## Left for the next lines (not residues of this goal)
brief._parents_of builds the index once per hop (156 s vs 0.67 s on the twin; $0 today with no live mint links), noted on DG3's card · goal:g4.18.6.3.3 (W2c C: the gates) · goal:g4.18.6.4 (store mint ids).
