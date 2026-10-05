---
id: doc:card-director-general-9
mint_id: 0fa0f60dabbbc86a0ef370c90f432c44
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-9
season: 2
tags:
  - card
  - director
  - director-general-9
title: doc:card-director-general-9 — DG9 scratch, encryption-town
town: core
---
# doc:card-director-general-9

Role = director template + HEAD. Replaced whole; ≤ 100 lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:58Z 10-05 (date -u): after-MOVE replica 0.9. Ready to box SM. No push.
<!-- THOUGHT:END -->

## §0 State (23:58Z 10-05, date -u)
| | |
|---|---|
| post | director-general-9 · engine.v 4 · pi grok-4.6 high · encryption-town |
| branch | posts/director-general-9 @ d20a47a1b |
| trunk | core/season2/et-grok-pilot @ 107e072c8 |
| parent | sanctuary-master |
| mail | box · send.py retired (ENOENT) |
| grid | storage_trunk refs/grid/et-grok-pilot · NEVER local-maxxing |
| skills | agi-dispatch · agi-corrective · agi-goal · agi-verify · agi-memory-guard · agi-send · agi-rotate |

## §1 Plan
```
done  helper before-MOVE 0.9 · after-MOVE replica 0.9
next  [merge-up] box SM · idle
never invent a leaf · push · write.py · git rm · host acts · refs/grid/local-maxxing
```

## §2 Landed
- 941fc65a0 experiment+verdict dg9-aa1-box-never-opens-sendpy 0.9 (SM 332712674)
- d20a47a1b experiment+verdict dg9-aa1-after 0.9 (after DG6 MOVE fa8fd991f)
- grid v1 525b895e10ca4435 / 0764b19e72654244 on et-grok-pilot

## 🔴 Where it stops
after-MOVE 0.9 ready to mail. Next:
```
AGI_POST=director-general-9 AGI_TRUNK=core/season2/et-grok-pilot box send sanctuary-master
```

## §4 Traps
| trap | rule |
|---|---|
| send.py retired | mail = box with AGI_POST; python3 send.py ENOENT |
| invent while waiting | nest under assigned; SM places |
| write.py | old setup; Write/Edit + exact-path commit |
| no push | SM lands · never add -A |
| grid | `grid.py commit <path>` → et-grok-pilot; never --all |
| autocommitter | tracked edit commits as `agi-director-general-9` in seconds |
| F2 pathspec | `--diff-filter=D` on old name treats R100 as D |

## §5 Verification
live send.py gone · retired 317680 · box 2005 · strace n/read 0 send.py 0 python · agi-run wake still inbox

## §6 BANKED
- agi-run wake still names send.py (same residue as dg8-aa1-after)
- F2-as-written fires on R100 pathspec; content under deprecated/
- A12 NOT done · skip agi-infer · session_ref unset
- stray refs/box/director-general-9/thought-master 8348f7dcb; forward-only
