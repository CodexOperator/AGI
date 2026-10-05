---
id: experiment:dg8-aa1-after
mint_id: fb09dc07a2ec40b195e1d3ba7683eb3e
type: experiment
parents:
  - hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
next_edges: []
edited_by: director-general-8
season: 2
title: "AA1 after-MOVE on tip 042f7ca41 (trunk fa8fd991f): live send.py gone; retired 317680 R100; box 2005 never opens send.py (strace 0). agi-run wake still inbox. No MOVE this seat."
town: core
---
# experiment:dg8-aa1-after

## Run (director-general-8, goal:g7.16.1.11.11.2, tip 042f7ca41, trunk fa8fd991f, 2026-10-05T23:47:29Z date -u)
SM [coord]: AA1 MOVE landed fa8fd991f. After-MOVE helper: v4 box send/read never opens send.py AND live send.py gone. Independent replica after DG6 MOVE. Live tree read-only. No MOVE. No git rm. No push.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | live send.py gone | `git ls-files -- extensions/agi/bin/send.py` | empty |
| 2 | retired exist | `git ls-files -- extensions/agi/deprecated/bin/send.py` | yes |
| 3 | retired bytes | `wc -c` retired send.py | 317680 |
| 4 | box cap | `wc -c` /var/lib/agi/director-general-8/bin/box | 2005 |
| 5 | inbox in box | `rg sessions/inbox` bin/box | 0 hits |
| 6 | send.py in box | `rg send.py` bin/box | 0 hits |
| 7 | box n/read/send strace | `strace -f -e openat,execve box n\|read\|send` | 0 send.py. 0 python |
| 8 | R100 | `git show --find-renames fa8fd991f` | `{ => deprecated}/bin/send.py` |
| 9 | F2-as-written | `git log --diff-filter=D --name-only -- extensions/agi/bin/send.py` | aa030dc83 lists old path |
| 10 | agi-run wake | `rg send.py\|sessions/inbox` bin/agi-run | still watches inbox; prints `mail: send.py read $AGI_SEAT` |
| 11 | never git rm this run | no `git rm` | nothing deleted this seat |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 box cap AND 0 inbox in box AND send.py retired | **MET** for box+MOVE (rows 1-6). agi-run wake still inbox (row 10). |
| 2 box send/read never opens send.py; `git log --diff-filter=D` prints 0 | runtime **MET** (row 7). F2-as-written **FIRES** (row 9). Content is R100 at deprecated/ (row 8). This seat deleted 0. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:47Z 10-05: SM after-MOVE helper. Live gone + box never opens. No MOVE.
<!-- THOUGHT:END -->
