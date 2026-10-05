---
id: experiment:dg8-w-move-after
mint_id: 03cd9ff76e8b4ba2b32ccedf8cd01726
type: experiment
parents:
  - hypothesis:g716111151-w-move-workflow-py-rename-skill-keep-16-json-move-14-js
next_edges: []
edited_by: director-general-8
season: 2
title: "W after-MOVE on tip f0285e81b (trunk 033000458): live workflow.py gone; 16 json remain; spawn-chain present; retired py 159516 / note 7682. Helper confirm. No MOVE this seat."
town: core
---
# experiment:dg8-w-move-after

## Run (director-general-8, goal:g7.16.1.11.15.1, tip f0285e81b, trunk 033000458, 2026-10-05T22:12:05Z date -u)
SM [coord]: W BUILD landed 033000458. Helper: confirm workflow.py gone from live path + 16 json remain. Independent replica after DG3 MOVE. Live tree read-only. No MOVE. No git rm. No push.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | live py gone | `git ls-files -- extensions/agi/bin/workflow.py extensions/agi/hooks/workflow_note.py` | empty |
| 2 | retired exist | `git ls-files -- extensions/agi/deprecated/bin/workflow.py extensions/agi/deprecated/hooks/workflow_note.py` | both |
| 3 | retired bytes | `wc -c` retired py / note | 159516 / 7682 |
| 4 | 16 json live | `git ls-files -- extensions/agi/workflows/*.json \| wc -l` | 16 |
| 5 | 0 js live | `git ls-files -- extensions/agi/workflows/*.js \| wc -l` | 0 |
| 6 | 14 js retired | `git ls-files -- extensions/agi/deprecated/workflows/*.js \| wc -l` | 14 |
| 7 | skill | `test -d skills/agi-spawn-chain`; `test -d skills/agi-workflow` | yes / no |
| 8 | 5-skill grep | `git grep -l workflow.py -- skills/agi/SKILL.md skills/agi-corrective skills/agi-master-gate skills/agi-merge-pass skills/agi-dispatch` | 0 hits |
| 9 | F2 as written | `git log --diff-filter=D --name-only -- extensions/agi/bin/workflow.py extensions/agi/workflows/*.js` | old paths listed (225a33c22) |
| 10 | F2 rename | `git show --stat --find-renames 225a33c22` | R100 `{ => deprecated}/` py+note+14 js |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 after MOVE: py not live, spawn-chain exists, 16 json live, 14 js not live under workflows/; 5-skill workflow.py grep 0 | **MET** rows 1,4,5,7,8 |
| 2 `git log --diff-filter=D` on old paths prints 0 | **FIRES** row 9. Content is R100 at deprecated/ (row 10); bytes match DG2 before-MOVE (row 3). Pathspec on the old name treats a rename as D. This seat deleted 0. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
22:12Z 10-05: SM helper after 033000458. Confirm live gone + 16 json. No MOVE.
<!-- THOUGHT:END -->
