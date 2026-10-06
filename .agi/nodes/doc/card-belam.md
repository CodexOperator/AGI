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

Never local-town. Never touch master. Trunk: `core/season2/et-grok-pilot`. Season3 tip tracks close work; merge to master = owner only.

## §0 State (2026-10-06 ~03:5xZ ET)
| | |
|---|---|
| box | encryption-town |
| harness | **raw-shell** (`H=bash`, `AGI_HARNESS=raw-shell`) — pi blocked by spend limit |
| mail | AA1 only: `AGI_POST=belam AGI_TRUNK=core/season2/et-grok-pilot box send|read|n` — never send.py |
| drive | external driver (Grok Bot) types via `/run/agi-belam/i`, reads `/var/lib/agi/belam/o` |
| close | season-2 close stood-in on ET; goals cleaned; builds reparented; `core/season3/main` FF pushed |
| master | untouched (`6405a03fc`); merge pending owner |

## §1 Plan
```
Keep raw-shell until spend unblocks or owner restores a model harness.
Drive commits one node per commit via DG4/raw-shell pane when posts are blocked.
Reproject via agi-project so drop-ins match geometry (no hand drift).
```

## §2 Landed (season close stand-in)
- AA1 `box` mail + in-pane wake (`box n` → `mail: box read`); send.py/workflow.py moved to deprecated
- raw-shell harness on belam, sanctuary-master, DG4
- goal cleanup + per-node commits; live carry ~131 goals on season3
- `box_mail.py` deprecated; live callers use `boxes.box_send` / geometry `box`

## 🔴 Where it stops
Await owner: master merge; whether to delete remote `core/season2/et-grok-pilot` (pre-existed; do not delete without ask); suite residual (osc context research reds).

## §4 Traps
| # | rule |
|---|---|
| — | never git rm — deprecate/move aside |
| — | never commit on master; never local-town |
| — | off-pane `box` needs `AGI_POST=<post>` |
| — | wake never fifo-injects the Prime |

## §6 BANKED
Raw-shell is the stand-in capsule while xAI personal-team spending-limit blocks pi. Startup dump prints into the pane via agi-sync seeds on raw-shell start.
