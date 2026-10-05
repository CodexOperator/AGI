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

Lean scratch. Mint id unchanged. Do not push. Never local-town.

## §0 State (2026-10-05 03:5xZ)
| | |
|---|---|
| box | encryption-town. Branch `posts/belam` @ `ae66f50f0` = `core/season2/et-grok-pilot` |
| prime | engine.v4 pi grok-4.6 high. You steer standups and monitoring. Liaison monitor-only. |
| seats up | 11 units: belam, SM, council3, DG1–5, director-thought-2. NRestarts=0 |
| seats added | DG6+DG7 **projected, not started**. uids 975/974. wants + h.conf on disk. |
| rotate | `AGI_ROTATE_PCT=47`. Meter through cccc. |
| watch | `tmux attach -t agi-watch` |

## §1 Plan
```
figure eight: council designs → DG goals → DG builds on graph routes → SM gate → you review
you: keys, rotate, standups, owner answers. Do not design or build for a director.
```

## §2 Landed this turn
- owner 22:1x ET: stand DG6–10 if this box can hold them. Picked 2 (CPU 2c/4t).
- DG6 re-homed local-town → encryption-town engine.v4 pi grok-4.6; DG7 minted same shape; cards written.
- `agi-project.path` projected users+dropins+wants. Units inactive: this uid cannot `systemctl start` (polkit `agi.rules` not installed).
- owner 22:2x+22:25 ET mint design: chew only. Box-mailed council + SM. Local room `council-loop`. MAIN inbox unwritable (belam:belam).

## 🔴 Where it stops
```
DG6/DG7 units projected, not running.
Next (root / owner): systemctl start agi-post@director-general-6.service agi-post@director-general-7.service
Then: install polkit agi.rules so Prime can start projected units.
```

## §4 Traps
| # | rule |
|---|---|
| 66 | inbox is MAIN `.agi/sessions/inbox/belam.md`; this uid cannot write it |
| 70 | do not push from this branch |
| — | never `update-ref` et-grok-pilot past a commit it already has; merge instead (paid 03:5xZ, restored 8639feb05 then merged) |
| — | `pkill -f` matches your own shell |

## §6 BANKED
- owner: mint-user is a dumb post-tree ring member wrapping a host-only signer; mint+parent sig always; one thin mint-key skill, no second daemon.
- Qs to owner (also boxed to council): Q4 parent of mint-user row? Q5 inert vs live unit? Q6 stand-in path cell? Q7 which parent-sig params travel?
- rec: inert (no harness) unless the mint script must run as that uid.
