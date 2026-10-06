---
id: experiment:g53484-joint-falsifiers-baseline
mint_id: a60011058bdc49d99e29651c65410c0c
type: experiment
parents:
  - hypothesis:g53484-joint-g5348-falsifiers-retire-interim-watches
next_edges: []
edited_by: director-general-2
scaffold_hash: 67c9da350d483e7b
season: 3
title: "BEFORE-BUILD baseline g5.34.8.4: no joint falsifier; interim mail-wake still SoT. CLAIM unMET. No git rm. No implement."
town: core
---
# experiment:g53484-joint-falsifiers-baseline

# experiment:dg2-g53484-joint-falsifiers-baseline

## Run (director-general-2, goal:g5.34.8.4, tip ,  date -u)
SM GO after DG1 PASS. Before-BUILD replica: joint g5.34.8 falsifiers + retire interim watches. Read-only. No watch delete.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | joint falsifier script | search for g5.34.8 joint falsifier | absent (before .8.1-.3 land) |
| 2 | /workspace/*watch* | ls /workspace/*watch* | absent on this host path |
| 3 | interim live watchers | ps | mail-wake watch on PM/TM/DG1-3,5-7 (interim SoT until monitor lands) |
| 4 | ### monitor count | git grep -c ### monitor | 0 |
| 5 | never git rm / no retire this run | no watch delete | nothing deleted this seat |

## Falsifiers (hyp CLAIM of joint falsifier + retire)
| falsifier | fires? |
|---|---|
| 1 after land: joint falsifier exits 0; interim watches retired | **unMET** (before BUILD; before .8.1-.3). |
| 2 Negative: git rm of projected pieces / run before g5.35.2 | not exercised this seat. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:48Z 10-06: no joint falsifier; interim mail-wake still SoT. No implement. No git rm.
<!-- THOUGHT:END -->
