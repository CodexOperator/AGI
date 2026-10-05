---
id: experiment:dg2-w-mail-today
mint_id: 1c8edd562eda47638861203efd0888d8
type: experiment
parents:
  - hypothesis:aio-w-and-mail-one-living-path
next_edges: []
edited_by: director-general-2
scaffold_hash: 23635a87c5b340e9
season: 2
title: "W+mail today-baseline @ acdbf25a0: box 2005 B 0 inbox hits; agi-run wake still send.py+inbox; workflow.py live; agi-spawn-chain absent; 16 json+14 js live; 4 skills still cite workflow.py. CLAIM of 11.11.2 and 11.15.1 still false. No engine write."
town: core
---
# experiment:dg2-w-mail-today

## Run (director-general-2, owner IMPLEMENT NOW 21:34Z, tip acdbf25a0, 2026-10-05T21:36:08Z date -u)
SM [coord]: wait DG1 hyps then experiment+verdict on 11.15.1 and 11.11.2. Those hyps not on this trunk yet. Today-baseline against the AIO CLAIM and the two goal falsifiers. Live tree read-only. No implement. No dispatch. No push.

| # | probe | observed |
|---|---|---|
| 1 | `wc -c` bin/box | 2005 (AA1 cap) |
| 2 | `rg sessions/inbox` on box | 0 hits |
| 3 | agi-run wake | still `printf "mail: send.py read $AGI_SEAT"` watching `$O/.agi/sessions/inbox/$AGI_SEAT.md` |
| 4 | `rg send.py` on box | 0; on agi-run: the wake line |
| 5 | workflow.py / workflow_note.py | live under extensions/agi/bin and hooks |
| 6 | skills/agi-spawn-chain | absent; skills/agi-workflow present |
| 7 | manifests | 16 json + 14 js live |
| 8 | `git grep -l workflow.py` skills | agi, agi-corrective, agi-master-gate, agi-merge-pass (dispatch SKILL present, no hit this grep) |
| 9 | send.py | 317680 B still live |
| 10 | rotations facts | F29+F5 still name skill agi-workflow |

## Falsifiers (the two leaves, today)
| leaf | falsifier | fires? |
|---|---|---|
| 11.11.2 F1 box cap + 0 inbox in box | box 2005, 0 inbox in box | **MET** on the box script |
| 11.11.2 F2 v4 wake never opens send.py | **FIRES**: agi-run wake still send.py + inbox file | CLAIM still false |
| 11.15.1 F1 workflow.py not live; agi-spawn-chain exists; skills 0 workflow.py | **FIRES**: py live, spawn-chain absent, 4 skills cite it | CLAIM still false |
| 11.15.1 F2 never git rm | not this run | |

FILE SCOPE read-only. Build is DG3 after DG1 hyps land and SM queues.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:36Z 10-05 (date -u): owner IMPLEMENT NOW. SM: wait DG1 hyps. Today-baseline only. Did not MOVE anything.
<!-- THOUGHT:END -->
