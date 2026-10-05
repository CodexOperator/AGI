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

## §0 State (2026-10-05 04:5xZ)
| | |
|---|---|
| box | encryption-town. `posts/belam` @ `c8538eb64` |
| sudo | passwordless (`90-agi-belam`). Use for wake, ACL, systemctl. |
| seats | 13 units active. Woke 04:48Z: inbox ACL + fifo 620 + pane inject. load ~11 |
| liaison | Grok Bot. Qs for Shael → Grok Bot. |

## §1 Plan
```
you: keys, rotate, standups, owner answers. Council/DG do the graph work.
```

## §2 Landed
- wake path LIVE: setfacl g:agi:rw inbox+rooms; fifo 620 g:agi; polkit 10-agi-post.rules
- durable: config:engine-root mkfifo 620 + chgrp agi
- send.py inbox to 13 posts + fifo `mail: send.py read <post>`
- MAIN posts.md still stale (DG6 box=local-town in working tree). Do not commit MAIN.

## 🔴 Where it stops
```
Team waking (load 11). Watch they take turns; do not restart units.
Need: persist inbox ACL across reboot (default ACL is on; confirm).
Need: MAIN working tree not committed (stale index).
```

## §4 Traps
| # | rule |
|---|---|
| 70 | never commit from `/data/work/agi` |
| — | fifo was 600; live 620 g:agi. Restarts pick graph mkfifo after agi-project. |

## §6 BANKED / NEEDS for owner
- persist sudo 90-agi-belam (yes?)
- inbox default ACL g:agi:rw — keep?
- MAIN dirty posts.md: leave, or owner reset --hard to HEAD?
- Q: should agi-run grow a pi-path inbox poll (cccc.ts already watches) so fifo inject is backup only?
