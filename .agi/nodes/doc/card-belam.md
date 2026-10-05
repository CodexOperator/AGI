---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-et
title: doc:card-belam — Prime scratch, encryption-town
town: core
---
# doc:card-belam — Prime on encryption-town

Do not push. Never local-town. Never commit from `/data/work/agi`.

## §0 State (2026-10-05 08:0xZ)
| | |
|---|---|
| box | encryption-town. `posts/belam` = et-grok-pilot @ `b797cea7e` |
| sudo | keep (`90-agi-belam`) — owner yes |
| seats | 13 units. Wake path live. |
| MAIN | reset --hard to HEAD. DG6/7 cells current. |

## §1 Plan
```
you: keys, rotate, standups, owner answers. Council/DG do the graph work.
```

## §2 Landed (owner Q1–Q4)
- Q1 keep sudo.
- Q2 durable inbox ACL: agi-boot setfacl + default ACL on `$PWD/.agi/sessions/inbox`.
- Q3 MAIN `reset --hard` @ `b797cea7e`. Cells current.
- Q4 agi-run poll `claude*|pi*` (reuse claude loop). fifo inject is backup. Heading 829 B.

## 🔴 Where it stops
```
Live units still run old agi-run until next restart (do not bounce the team).
Inbox ACL already live; boot will re-apply.
```

## §4 Traps
| # | rule |
|---|---|
| 70 | never commit from `/data/work/agi` (reset --hard only, owner GO) |
| — | agi-boot `$O` unset; inbox ACL uses `$PWD` |

## §6 BANKED
Q4–Q7 mint chew still council-only. No implement.
