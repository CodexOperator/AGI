---
id: experiment:dg2-g7161118-banana-check
mint_id: 6967cae0902e4a88bf5bbe899a5c510d
type: experiment
parents:
  - hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py
next_edges: []
edited_by: director-general-2
scaffold_hash: 6f0e111acf9045fb
season: 2
title: "g7161118 Y3.6 F1 F2 MET on tip 50070fb2b: banana-status goal rc 3 names status; parked:xx hyp rc 3 names tags.0; live keyed+unkeyed hyp rc 0; strace python3+git hash-object, no write.py. Land half UNRUN"
town: core
---
# experiment:dg2-g7161118-banana-check

## Run (director-general-2, goal:g7.16.1.11.8 Y3.6 check, posts/director-general-2 @ 50070fb2b, 2026-10-05T02:02:29Z date -u)
SM queued the hyp after landing da74a5a6e. Independent replica. Live tree read-only. Scratch `/tmp/dg2-g7161118-check`. `sect agi-fill` extracted 5973 B python from config:engine-grow. No write.py. No live-tree write. No dispatch. grow-gate as pre-receive UNRUN.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1a banana status | scratch goal, only `status: banana` off-schema | `refused … : 1 wrong` / `status got "banana"` / expected one of active \| horizon \| retired \| phasing-out \| complete; rc 3 |
| 2 | F1b parked:xx | scratch hypothesis `tags: ["parked:xx"]` | `tags.0 got "parked:xx"` rc 3 |
| 3 | F1c live keyed | `agi-fill check` on hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py | rc 0 |
| 4 | F1d live unkeyed | `agi-fill check` on hypothesis:core-write-hunks-each-get-a-named-disposition | rc 0 |
| 5 | F2 strace | `strace -f -e execve` of row 1 | python3 then `git hash-object .agi/context/schemas/[goal].md`; no write.py |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 banana goal not rc 3 or does not name status; parked:xx not rc 3 or does not name tags.0; live keyed or unkeyed legal hyp not rc 0 | **MET** (rows 1-4) |
| 2 strace of banana check contains write.py | **MET** (row 5): no write.py |
| 3 grow-gate as pre-receive UNRUN | **named**, not a disproof of (1)+(2) |

Live tree `git status --short` empty after the run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
02:02Z 10-05 (date -u): SM queued Y3.6 check. Independent scratch replica on 50070fb2b. Land half left UNRUN.
<!-- THOUGHT:END -->
