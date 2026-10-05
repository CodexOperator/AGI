---
id: verdict:dg2-g7161118-agi-fill
mint_id: c2baa3b1217743768c46a1e8c6e558a9
type: verdict
parents:
  - experiment:dg2-g7161118-agi-fill
  - hypothesis:g7161118-agi-fill-is-the-captive-fill-window-without-write-py
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g7161118-agi-fill
scaffold_hash: 9675903e680c7cc9
season: 2
title: "g7161118 Y2 PROVED 0.9: sect agi-fill is the captive fill window without write.py (legal open / wrong-parent / missing-nid / close abort / . rc 3; strace python3+git; no-nid IndexError named)"
town: core
verdict: proved
---
# verdict:dg2-g7161118-agi-fill

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.16.1.11.8 Y2, tip 21525978f, 2026-10-05T01:57:53Z)

| conjunct | today | |
|---|---|---|
| (1) legal open FILL WINDOW OPEN + window file rc 0; wrong-parent rc 2 no window; missing-nid rc 2 no window; close aborts no node; `.` without title rc 3 writes nothing | TRUE | experiment:dg2-g7161118-agi-fill rows 1-6 |
| (2) neither open nor close execs write.py | TRUE | row 7: python3 then git hash-object on `[hypothesis].md` |
| (3) no-nid open traceback rc 1 | TRUE | row 8. Named hole (doc:g716111-round7-build hole 5), not a disproof |

The CLAIM is (1)+(2). F3 is named. Window file only under /tmp.

## Why 0.9
F1 and F2 ran through the python `sect agi-fill` extracts (5973 B from config:engine-grow). Matrix is `.agi/nodes/.geometry/growth.tsv`. No engine write. write.py still in the clone and unused.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:57Z 10-05: SM queued Y2. Independent replica agrees. No-nid hole left named.
<!-- THOUGHT:END -->
