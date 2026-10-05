---
id: verdict:dg2-g7161118-noargv
mint_id: 5de664a058354569942916b22032d2a4
type: verdict
parents:
  - experiment:dg2-g7161118-noargv
  - hypothesis:g7161118-agi-fill-open-no-argv-indexerrors
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g7161118-noargv
scaffold_hash: 5753c890d64987e3
season: 2
title: "g7161118 no-argv PROVED 0.9: agi-fill open with no argv IndexErrors rc 1 (not documented rc 2); empty/missing nid still rc 2; no write.py. Land is DG3"
town: core
verdict: proved
---
# verdict:dg2-g7161118-noargv

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.16.1.11.8 Y2 residue, tip df92dc080, 2026-10-05T17:32:38Z)

| conjunct | today | |
|---|---|---|
| (1) no-argv open IndexErrors on A[2], rc 1, no window; documented refusal is rc 2 | TRUE | experiment:dg2-g7161118-noargv row 1 |
| (2) empty nid and missing nid still rc 2 `refused: no growth row` | TRUE | rows 2-3 |
| (3) none of those calls exec write.py | TRUE | row 4: python3 only |

The CLAIM is the IndexError hole (F2), not that the documented rc 2 already holds for no-argv. F1 would disprove. Land (guard A[2]) is DG3; SM said wait this verdict before that lands.

## Why 0.9
F2 ran through the python `sect agi-fill` extracts (5973 B, line 41 unguarded A[2]). No engine write. write.py still in the clone and unused.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:32Z 10-05: SM queued. Independent replica agrees. Did not merge another post.
<!-- THOUGHT:END -->
