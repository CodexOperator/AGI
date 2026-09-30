---
id: experiment:a00-adb0b43d-ac73a6
mint_id: 1be3dad695ec420c9c00531f910af2d7
type: experiment
parents:
  - hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
next_edges: []
confidence: 0.9
edited_by: a00-adb0b43d
evidence_runs:
  - experiment:a00-adb0b43d-ac73a6
loop: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 310271785e482643
season: 2
title: Corrective DH.EG.169 fixes five stale or false text lines on the free-lane chain
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-adb0b43d-ac73a6 -- corrective DH.EG.169: five stale/false text lines fixed

## Experiment
Text-fix kid for DH.EG.169 (closes mur-eg-x1305298-83f469 EG.150-k1 residue). This round changes only text: no behaviour, test logic or config.

| # | site | before | after |
|---|---|---|---|
| 1 | experiment:a00-e5b926db-80ea64, paragraph "Corrective EG.124:" | "suite RED ... by design" (present tense) | red was expected THEN and is gone NOW, citing heading "CORRECTION (EG.150, a00-f38a455b) -- the expected red is GONE" |
| 2 | same node, "CAVEAT I accept from the kid" | "the tree now carries ONE expected red" | marked HISTORY, superseded by the same CORRECTION |
| 3 | experiment:a00-f38a455b-d5028f, RESIDUE bullet on OMITTED_DEFECT | "no longer records ... ANYWHERE (probe D)" | CORRECTED: the node still carries it (count below); probe D measured only /TOLERAT/ |
| 4 | test_skills_first_turn_entry.py, comment "# NO OMITTED_DEFECT EXEMPTION." | "suite is RED on purpose until the clause is added" | fix site (config:rotations) now names agi-corrective; the test guards against its removal |
| 5 | test_free_lane_dispatch_main.py, module docstring | "credit_balance and the create call are the only fakes" | dispatch-path proof with every I/O boundary faked, named by function |

Node edits go through write.py `replace body N:N --force -`, one whole line each.

## Evidence
Item 3 is settled by this count. `git grep` is replaced by the Grep tool/`grep -c` because a kid may run no git except numstat:
```
$ grep -c OMITTED_DEFECT .agi/nodes/hypothesis/free-lane-mint-and-skills-startup-have-end-to-end-tests.md
4
```
Item 4 is settled by this run: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_skills_first_turn_entry.py -q --basetemp /tmp/...`
```
4 passed in 2.13s
```
The three named files together (test_skills_first_turn_entry, test_free_lane_dispatch_main, test_bin_help_smoke):
```
80 passed, 7 skipped, 1 warning in 12.66s
```
`git diff --numstat 2b866de03` (working tree, measured BEFORE this node was written; this node is not included):
```
3	3	.agi/nodes/experiment/a00-e5b926db-80ea64.md
2	2	.agi/nodes/experiment/a00-f38a455b-d5028f.md
4	2	extensions/agi/tests/test_free_lane_dispatch_main.py
4	4	extensions/agi/tests/test_skills_first_turn_entry.py
```
CEILING check: 0 production lines · test files 4+2+4+4 = 14 changed lines <= 16, all comments/docstring · 0 USD · 1 kid.

## Deviation
The brief says "KID COMMIT every edit". The harness contract says a kid runs no git, and `cli.py done` does the versioning. I followed the harness, so nothing is committed by me.

## Agent Notes
DH.EG.169 text-fix: 5 stale/false lines corrected (2 in e5b926db, 1 in f38a455b, 1 comment, 1 docstring); 0 prod lines, 14 test comment lines; 80 passed 7 skipped; OMITTED_DEFECT count on hypothesis = 4
