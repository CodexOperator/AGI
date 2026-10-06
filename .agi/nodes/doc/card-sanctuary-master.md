---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

Replaced whole, never appended; ≤100 lines. Board coordinator for encryption-town directors.

## §0 State (2026-10-06 ~03:5xZ ET)
| | |
|---|---|
| post | sanctuary-master on **encryption-town** |
| trunk | `core/season2/et-grok-pilot` (season close stand-in); `core/season3/main` carries open goals |
| harness | **raw-shell** (`H=bash`) — pi spend-blocked; session files kept |
| mail | AA1: `AGI_POST=sanctuary-master AGI_TRUNK=core/season2/et-grok-pilot box read` first at wake — never send.py |
| drive | `/run/agi-sanctuary-master/i` → `/var/lib/agi/sanctuary-master/o` |
| role | sequencing/placement/gates; rulings = council; never the Prime |
| master | untouched; merge-up pending owner |

## §1 Plan
```
FIRST at wake: AGI_POST=sanctuary-master AGI_TRUNK=core/season2/et-grok-pilot box read
Coordinate directors on ET raw-shell while models blocked.
Land only via named one-node commits; reproject units from geometry.
```

## §2 Landed
- Season-2 close stood-in (goals retired/moved, builds reparented to live parents)
- nudge_sweep off; mail_poll = refs/box+held only; pi_auth_refresh stays
- belam + SM + DG4 on raw-shell; grokbot binding cells recorded on belam/SM rows

## 🔴 Where it stops
```
Idle for owner merge / spend restore. On [merge-up]: gate as usual, land on live HEAD, never master without owner.
```

## §4 Traps
| trap | rule |
|---|---|
| send.py / MAIN inbox era | retired — AA1 box only |
| pipe `box read` to head | never — marks all held |
| git rm | never — deprecate/move |
| hand drop-ins | fix via geometry + agi-project reproject |

## §6 BANKED
Startup dump (unified-head + card + seeds) prints into the raw-shell pane on start for an attaching driver.
