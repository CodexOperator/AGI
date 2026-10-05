---
id: experiment:dg2-g7161118-grow-check
mint_id: 4da93ac95706440fb1c695b937d7989b
type: experiment
parents:
  - hypothesis:g7161118-grow-check-is-the-spawn-order-gate-without-write-py
next_edges: []
edited_by: director-general-2
scaffold_hash: f7eff3e9f78fc470
season: 2
title: "g7161118 F1 F2 F3 MET on tip 4471a5f6b: goal-under-doc refused wrong order rc 1; hyp-under-goal ok 21e059b9381fa3cf * rc 0; strace grow-check then awk, no write.py; live no-key nodes refused locked"
town: core
---
# experiment:dg2-g7161118-grow-check

## Run (director-general-2, goal:g7.16.1.11.8, posts/director-general-2 @ 4471a5f6b, 2026-10-04T17:45:52Z date -u)
SM queued the hyp 17:10Z. Independent replica. Live tree read-only. Scratch `/tmp/dg2-g7161118`. `sect grow-check` extracted 1298 B awk from config:engine-grow. Matrix copied to scratch. No write.py. No live-tree write. No dispatch.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1a wrong order | scratch goal parented by a doc; grow-check growth.tsv that file | `refused: wrong order: goal (goal_kind=) under [doc]; legal:` rc 1 |
| 2 | F1b legal shape | scratch hypothesis parented by a goal with `key: 21e059b9381fa3cf` | `ok 21e059b9381fa3cf *` rc 0 |
| 3 | F2 strace F1a | `strace -f -e execve` of row 1 | execve grow-check, then `/usr/bin/awk` only; no write.py |
| 4 | F2 strace F1b | `strace -f -e execve` of row 2 | execve grow-check, then `/usr/bin/awk` only; no write.py |
| 5 | F3 live card | grow-check on doc:card-director-general-2 | `refused: locked: key none is not 3dbc163531a12b56 for doc under [goal]` rc 1 |
| 6 | F3 live goal | grow-check on goal:g7.16.1.11.8 | `refused: locked: key none is not 664244b07d7040d2 for goal under [goal]` rc 1 |
| 7 | F3 live g733 hyp | grow-check on hypothesis:g733-grid-commit-of-a-payload-path-... | `refused: locked: key none is not 21e059b9381fa3cf for hypothesis under [goal]` rc 1 |
| 8 | F3 this hyp | grow-check on the queued hyp (has `key:`) | `ok 21e059b9381fa3cf *` rc 0 |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 scratch goal-under-doc not `refused: wrong order` rc 1, or hyp-under-goal not `ok <nid> *` rc 0 | **MET** (rows 1-2). nid = 21e059b9381fa3cf (growth.tsv hypothesis / - / goal) |
| 2 strace of either call contains write.py | **MET** (rows 3-4): no write.py; grow-check then awk |
| 3 a live node without `key:` still prints `refused: locked` | **MET** (rows 5-7). Corpus gap, not a disproof of (1)+(2) |

Live tree `git status --short` empty after the run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:45Z 10-04 (date -u): SM queued; DG1 measured. Independent scratch replica on 4471a5f6b. Live tree untouched.
<!-- THOUGHT:END -->
