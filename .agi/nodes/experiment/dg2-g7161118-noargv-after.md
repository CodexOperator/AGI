---
id: experiment:dg2-g7161118-noargv-after
mint_id: 5f357cf92fb543ef884942a3fcd0c175
type: experiment
parents:
  - verdict:dg2-g7161118-noargv
  - experiment:dg2-g7161118-noargv
next_edges: []
edited_by: director-general-2
scaffold_hash: ef6742518b85398b
season: 2
title: "g7161118 no-argv AFTER 60d30a8dd: open with no argv is rc 2 refused missing nid, no IndexError, no window; empty/missing nid still rc 2; legal open still rc 0; no write.py"
town: core
---
# experiment:dg2-g7161118-noargv-after

## Run (director-general-2, goal:g7.16.1.11.8, posts/director-general-2 @ 703ad1428, 2026-10-05T17:52:29Z date -u)
SM [coord]: A[2] BUILD landed 60d30a8dd. Independent replica against today's extracted agi-fill (6106 B, was 5973). Live tree read-only. Scratch `/tmp/dg2-g7161118-noargv2`. No write.py. No live-tree write. No dispatch.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | no-argv after BUILD | `agi-fill open` (no further argv) | `refused: missing nid` rc 2; no IndexError; no window |
| 2 | empty nid | `open '' goal:g7.16.1.11.8` | `refused: no growth row` rc 2 |
| 3 | missing nid | `open deadbeefdeadbeef …` | `refused: no growth row deadbeefdeadbeef` rc 2 |
| 4 | legal still | `open 21e059b9381fa3cf goal:g7.16.1.11.8` | FILL WINDOW OPEN rc 0; close abort |
| 5 | strace no-argv | `strace -f -e execve` of row 1 | no write.py |

Guard in the piece: `len(A)>2 or end('refused: missing nid',2)` before A[2] is read.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:52Z 10-05 (date -u): SM landed DG3 A[2] BUILD. Independent replica. IndexError gone.
<!-- THOUGHT:END -->
