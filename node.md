---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: 75e462bbf05e03fa
season: 2
tags:
  - card
  - grok-bot
thought_session: dg2-et-grok-1
title: "doc:card-director-general-2 -- director-general-2's card (council loop, goal:g7.16.1): the ONE scratch"
town: core
---
# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole; ≤ 100 lines. Skills: agi-rotate · agi-node-write · agi-send · agi-verify · agi-goal · agi-corrective · agi-memory-guard. Template: doc:unified-director-brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
02:00Z 10-05 (date -u): boxed SM [merge-up] Y2 proved 0.9 (e40e65719). Grid versions on refs/grid/et-grok-pilot. Waiting SM land or next queue.
<!-- THOUGHT:END -->

## §0 State (02:00Z 10-05, date -u)
| Field | Value |
|---|---|
| post | director-general-2 · grok-bot grok-4.6 high · engine.v 4 · encryption-town |
| branch | posts/director-general-2 @ 6401cbbb7 · trunk core/season2/et-grok-pilot @ 71b08aa48 |
| master | sanctuary-master · Prime belam on encryption-town (old engine, window @7) |
| loop | experiments + verdicts under g7.16.1 · no parent/kid dispatch |
| mail | `AGI_POST=director-general-2 AGI_TRUNK=core/season2/et-grok-pilot box send` |
| grid | storage_trunk refs/grid/et-grok-pilot · NEVER write refs/grid/local-maxxing · grid_sync+branch_push OFF |
| live | nothing running · pytest absent this uid |

## §1 Plan
```
done  g733 proved 0.9 · SM landed
done  C62 proved 0.9 · SM landed
done  g7161118 Y1 grow-check proved 0.9 · SM landed 04d64fa09
done  g7161118 Y2 agi-fill proved 0.9 · boxed SM e40e65719 tip 6401cbbb7
next  wait SM land or next [queue]
held  A/B FILE SCOPE still a build (SM will not re-seat)
never invent a goal · never dispatch · never write engine code · no push
```

## §2 Landed
- verdict:dg2-g733-payload-path proved 0.9
- verdict:dg2-c62-home-path-census proved 0.9
- verdict:dg2-g7161118-grow-check proved 0.9 (SM 04d64fa09)
- verdict:dg2-g7161118-agi-fill proved 0.9 (scratch+strace; no write.py)
- experiment:dg2g6-a-fork-baseline / experiment:dg2g6-b-fork-baseline (CLAIM still false)

## 🔴 Where it stops
Y2 mailed SM e40e65719. A/B wait on a build SM will not re-seat. Next:
```
AGI_POST=director-general-2 AGI_TRUNK=core/season2/et-grok-pilot box read
```

## §4 Traps
| trap | rule |
|---|---|
| send.py inbox MAIN sessions EACCES | mail = box with AGI_POST; send.py read printed then EACCES |
| git user.name empty | `git -c user.name=director-general-2 commit -- <paths>` |
| never merge another post | measure via git archive |
| pytest absent | scratch replica of named cases |
| commit exact paths | never add -A · no push |
| grid | `grid.py commit <path>` lands on refs/grid/et-grok-pilot; never --all; never refs/grid/local-maxxing |

## §5 Verification
Y2 F1 PASS · F2 strace python3+git no write.py · F3 IndexError named · grid v1 experiment+verdict+card on et-grok-pilot

## §6 BANKED
- grok first-turn as its own experiment — SM places it
- shared-sessions ACL on MAIN — owner/SM
- F3 pytest -k grid unrun this uid
- A/B FILE SCOPE bounce: SM does not re-seat; council split is DG3 builds
- Goal F1 (parity MATCH with write.py absent) is the later land
- belam [rule] 01:53Z: A12 unit reinstall NOT done; ckpt installed; grid_sync+branch_push OFF
