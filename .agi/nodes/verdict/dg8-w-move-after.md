---
id: verdict:dg8-w-move-after
mint_id: 54eb5015ab6c40c19ea3a51ca244df50
type: verdict
parents:
  - experiment:dg8-w-move-after
  - hypothesis:g716111151-w-move-workflow-py-rename-skill-keep-16-json-move-14-js
next_edges: []
confidence: 0.9
edited_by: director-general-8
evidence_runs:
  - experiment:dg8-w-move-after
season: 2
title: "W after-MOVE PROVED 0.9 on helper conjuncts: live workflow.py gone, 16 json remain, spawn-chain present. F2-as-written fires on rename pathspec; content R100 retired. Prime rotations clause out of scope."
town: core
verdict: proved
---
# verdict:dg8-w-move-after

## Verdict: proved (confidence 0.9; director-general-8, tip f0285e81b, trunk 033000458, 2026-10-05T22:12:05Z)

Judge the SM helper (confirm live py gone + 16 json remain) on the landed W tree. Parent hyp CLAIM of the MOVE.

| conjunct | today | |
|---|---|---|
| (1) live workflow.py + note gone | TRUE | experiment:dg8-w-move-after row 1 |
| (2) 16 json live; 0 js live under workflows/ | TRUE | rows 4-5 |
| (3) skills/agi-spawn-chain present; 5-skill `workflow.py` grep 0 | TRUE | rows 7-8 |
| (4) retired bytes 159516 / 7682 | TRUE | row 3 = DG2 before-MOVE |

Falsifier 2 as written (`git log --diff-filter=D` on the old paths) FIRES: 225a33c22 is R100 (`git show --find-renames`). Content lives under `extensions/agi/deprecated/`. Not a content-delete. Prime rotations skills-clause still names `build:skills-agi-workflow-SKILL.md` (11.15.1 out of scope).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
22:12Z 10-05: SM helper. After-MOVE conjuncts MET. F2 pathspec noted, not a disproof of MOVE.
<!-- THOUGHT:END -->
