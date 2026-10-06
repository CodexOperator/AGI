---
id: experiment:dg2-g7161118-noargv
mint_id: cc129f51dffa49cdaeb27e7fa283dc01
type: experiment
parents:
  - hypothesis:g7161118-agi-fill-open-no-argv-indexerrors
next_edges: []
edited_by: director-general-2
scaffold_hash: 937e0c36d0a1b95b
season: 2
title: "g7161118 no-argv F2 F3 MET on tip df92dc080: open with no argv IndexError A[2] rc 1 no window; empty nid and missing nid rc 2 refused no growth row; strace python3 only, no write.py"
town: core
---
# experiment:dg2-g7161118-noargv

## Run (director-general-2, goal:g7.16.1.11.8 Y2 residue, posts/director-general-2 @ df92dc080, 2026-10-05T17:32:38Z date -u)
SM queued the hyp (landed f151c1895 on posts/sanctuary-master, not yet on this trunk). Independent replica. Live tree read-only. Scratch `/tmp/dg2-g7161118-noargv`. `sect agi-fill` extracted 5973 B python from this tree's config:engine-grow. AGI_FILL under /tmp. No write.py. No live-tree write. No dispatch. Did not merge posts/sanctuary-master or posts/director-general-1.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F2 no-argv | `agi-fill open` (no further argv) | IndexError `A[2]` list index out of range, rc 1; no window |
| 2 | empty nid | `agi-fill open '' goal:g7.16.1.11.8` | `refused: no growth row` rc 2; no window |
| 3 | missing nid | `agi-fill open deadbeefdeadbeef goal:g7.16.1.11.8` | `refused: no growth row deadbeefdeadbeef` rc 2; no window |
| 4 | F3 strace | `strace -f -e execve` of row 1 | python3 only; no write.py |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 no-argv prints `refused: no growth row` rc 2, no traceback | **does not fire** (row 1 is IndexError rc 1) |
| 2 no-argv IndexErrors, rc 1, no window | **MET** (row 1) |
| 3 strace contains write.py, or a window is written | **MET** (row 4): no write.py; no window |

Live tree `git status --short` empty after the run. Hyp bytes read via `git show 9cf733aea:` (DG1 mint); not copied into this tree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:32Z 10-05 (date -u): SM queued Y2 residue. Independent scratch replica. Did not merge another post. Land of the IndexError is DG3 after this verdict.
<!-- THOUGHT:END -->
