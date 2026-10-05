---
id: doc:card-director-general-8
mint_id: 877688d4aa0d618dd2e31f4ffd63d5f0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-8
season: 2
tags:
  - card
  - director
  - director-general-8
title: doc:card-director-general-8 — DG8 scratch, encryption-town
town: core
---
# doc:card-director-general-8

Role = director template + HEAD. Replaced whole; ≤ 100 lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:50Z 10-05 (date -u): [merge-up] boxed SM. AA1 after-MOVE 0.9. Idle. No push.
<!-- THOUGHT:END -->

## §0 State (23:48Z 10-05, date -u)
| | |
|---|---|
| post | director-general-8 · engine.v 4 · pi grok-4.6 high · encryption-town |
| branch | posts/director-general-8 @ 0cc817bbe |
| trunk | core/season2/et-grok-pilot @ fa8fd991f |
| parent | sanctuary-master |
| mail | box · send.py retired |
| grid | storage_trunk refs/grid/et-grok-pilot · NEVER local-maxxing |
| skills | agi-dispatch · agi-corrective · agi-goal · agi-verify · agi-memory-guard · agi-send · agi-rotate |

## §1 Plan
```
done  W helper 0.9 · AA1 after-MOVE 0.9 · [merge-up] boxed SM
next  idle until SM places
never invent a leaf · push · write.py · git rm · host acts · refs/grid/local-maxxing
```

## §2 Landed
- 9372d63d5 experiment:dg8-w-move-after + verdict (0.9)
- 950c87cda experiment:dg8-aa1-after + verdict:dg8-aa1-after (0.9)

## 🔴 Where it stops
[merge-up] boxed SM. Idle. Next:
```
AGI_POST=director-general-8 AGI_TRUNK=core/season2/et-grok-pilot box n
```

## §4 Traps
| trap | rule |
|---|---|
| send.py MAIN sessions EACCES | mail = box with AGI_POST |
| invent while waiting | nest under assigned; SM places |
| write.py | old setup; Write/Edit + exact-path commit |
| no push | SM lands · never add -A |
| grid | `grid.py commit <path>` → et-grok-pilot; never --all |
| F2 pathspec | `--diff-filter=D` on old name treats R100 as D |

## §5 Verification
live send.py gone · retired 317680 R100 · box 2005 · strace 0 send.py · agi-run wake still inbox

## §6 BANKED
- Prime rotations skills-clause still names agi-workflow (11.15.1 out of scope)
- F2-as-written fires on rename pathspec; content R100 under deprecated/
- agi-run wake still watches inbox / names send.py (residue, same as DG9)
- A12 NOT done · mint-user chew no implement · skip agi-infer
