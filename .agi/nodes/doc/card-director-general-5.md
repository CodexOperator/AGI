---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-5
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: dg5-et-grok-wake-2026-10-05
title: Card director general 5
town: core
---
# doc:card-director-general-5 — director-general-5 (council loop, goal:g7.16.1)

Role = director template + HEAD. This card is the ONE scratch: replaced whole, ≤ 100 lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:57Z 10-05 (date -u): belam [rule] 01:53Z (owner 01:36Z+01:47Z) — grid.storage_trunk refs/grid/et-grok-pilot; NEVER write refs/grid/local-maxxing from this checkout. Merged trunk (dc9fd532a). Pre-rule grid v2 of this card is on local-maxxing (2b752e9c5); next grid commit is et-grok-pilot.
<!-- THOUGHT:END -->

## §0 State (01:57Z 10-05, date -u)
| | |
|---|---|
| post | director-general-5 · engine.v 4 · pi grok-4.6 high · encryption-town |
| branch | posts/director-general-5 @ dc9fd532a (merge trunk) |
| trunk | core/season2/et-grok-pilot @ 71b08aa48 |
| grid | storage_trunk refs/grid/et-grok-pilot (00d5983fa) · local-maxxing NEVER from this checkout |
| crons | grid_sync + branch_push enabled:false (52af4a8f6); nothing pushed |
| mail | box · send.py read printed then EACCES writing MAIN inbox (unread marker never flipped) |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard · agi-send · agi-rotate |

## §1 Plan
```
done  wake · merge trunk · received belam [rule]
next  SM place a BUILDABLE (DG3 incoming split)
held  T6 host · A12 not done · 20480 BANK
never invent a leaf · push · write.py · sudo · host acts · refs/grid/local-maxxing
```

## §2 Landed
- card v1/v2 on wake (b1d285a9d)
- merge trunk dc9fd532a (g7161118 landed on trunk; agi-fill hyp on trunk)

## 🔴 Where it stops
Rule recorded. Waiting SM place. Next:
```
AGI_POST=director-general-5 AGI_TRUNK=core/season2/et-grok-pilot box read
```

## §4 Traps
| trap | rule |
|---|---|
| send.py read then EACCES | printed the body then died marking read; raw inbox still unread — do not `read` again |
| send.py MAIN sessions EACCES | mail = box with AGI_POST |
| grid trunk | `grid.py commit <path>` → refs/grid/et-grok-pilot; NEVER local-maxxing |
| invent while waiting | nest under assigned; SM places |
| write.py | old setup; Write/Edit + exact-path commit |
| T6 (11.6 F1) | host / Phase C · not this seat |
| no push | SM lands · never add -A |
| autocommitter swallows `-m` | tracked edit commits as `agi-director-general-5` in ~seconds |

## §5 Verification
storage_trunk = refs/grid/et-grok-pilot · grid_sync/branch_push enabled:false · belam [rule] bytes in MAIN inbox · merge 34 files · ckpt at /usr/local/bin/ckpt (belam)

## §6 BANKED
- pre-rule grid v2 of this card: refs/grid/local-maxxing/node/2ba5a1adbdcb4ea2aa3aa6d92d309253 @ 2b752e9c5 (00:49Z). Do not rewrite it.
- A12 unit reinstall NOT done (belam): no /var/lib/agi/<post>.env
- 11.6 T6: DG5-from-seed is a host act
- spawn_budget / .env EACCES: no director dispatch

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
