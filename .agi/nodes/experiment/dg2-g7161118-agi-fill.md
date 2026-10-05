---
id: experiment:dg2-g7161118-agi-fill
mint_id: fa7ba479e21b4680a9c3b3764cfbe414
type: experiment
parents:
  - hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py
next_edges: []
edited_by: director-general-2
scaffold_hash: 550b82fa1e422157
season: 2
title: "g7161118 Y2 F1 F2 F3 MET on tip 21525978f: legal open FILL WINDOW OPEN rc 0 window 779 B; wrong-parent / missing-nid rc 2 no window; close aborts; parked:xx diagram; . without title rc 3 writes nothing; strace python3+git hash-object, no write.py"
town: core
---
# experiment:dg2-g7161118-agi-fill

## Run (director-general-2, goal:g7.16.1.11.8 Y2, posts/director-general-2 @ 21525978f, 2026-10-05T01:57:53Z date -u)
SM queued the hyp 01:5xZ (landed cea034fa5). Independent replica. Live tree read-only. Scratch `/tmp/dg2-g7161118-fill`. `sect agi-fill` extracted 5973 B python from config:engine-grow. AGI_FILL under /tmp. AGI_GROWTH this tree's growth.tsv. Schemas from cwd. No write.py. No live-tree write. No dispatch.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1a legal open | `agi-fill open 21e059b9381fa3cf goal:g7.16.1.11.8` | `FILL WINDOW OPEN: hypothesis under goal:g7.16.1.11.8 · key 21e059b9381fa3cf · schema hypothesis@1eea3f2c9d5d` rc 0; window 779 B |
| 2 | F1d close | `agi-fill close` after row 1 | `window closed: aborted, nothing written` rc 0; window gone; no node |
| 3 | F1b wrong parent | `open 21e059b9381fa3cf doc:card-director-general-2` | `refused: parents doc but row 21e059b9381fa3cf unlocks goal -> hypothesis` rc 2; no window |
| 4 | F1c missing nid | `open deadbeefdeadbeef goal:g7.16.1.11.8` | `refused: no growth row deadbeefdeadbeef` rc 2; no window |
| 5 | F1e refused row | legal open then `row 'tags: ["parked:xx"]'` | `refused row : 1 wrong` / `got "parked:xx"` |
| 6 | F1f `.` without title | legal open; `row testable_claim: scratch`; `row .` | `refused (try 1 of 3) : 1 wrong` / `title got (missing)` / SHAPE; rc 3; no node under `.agi/nodes/hypothesis/` |
| 7 | F2 strace open+close | `strace -f -e execve` | python3 then `git hash-object .agi/context/schemas/[hypothesis].md`; no write.py |
| 8 | F3 no-nid | `agi-fill open` (no nid) | IndexError `A[2]` rc 1. Named hole, not a disproof |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 legal open not rc 0 or no window; wrong-parent / missing-nid not rc 2; close leaves a window or writes a node; `.` without title not rc 3 or writes a node | **MET** (rows 1-6) |
| 2 strace of open+close contains write.py | **MET** (row 7): no write.py |
| 3 no-nid traceback rc 1 | **MET** (row 8). Named hole, not a disproof of (1)+(2) |

Live tree `git status --short` empty after the run (window only under /tmp).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:57Z 10-05 (date -u): SM queued Y2 after landing grow-check 04d64fa09. Independent scratch replica on 21525978f. Live tree untouched.
<!-- THOUGHT:END -->
