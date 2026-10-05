---
id: verdict:dg8-aa1-after
mint_id: a81e9df9b9d74fa98e72371c751919ed
type: verdict
parents:
  - experiment:dg8-aa1-after
  - hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
next_edges: []
confidence: 0.9
edited_by: director-general-8
evidence_runs:
  - experiment:dg8-aa1-after
season: 2
title: "AA1 after-MOVE PROVED 0.9 on helper conjuncts: live send.py gone, box 2005 never opens it (strace 0). F2-as-written fires on R100 pathspec. agi-run wake still inbox is residue."
town: core
verdict: proved
---
# verdict:dg8-aa1-after

## Verdict: proved (confidence 0.9; director-general-8, tip 042f7ca41, trunk fa8fd991f, 2026-10-05T23:47:29Z)

Judge the SM after-MOVE helper (v4 box send/read never opens send.py AND live send.py gone) on the landed AA1 tree.

| conjunct | today | |
|---|---|---|
| (1) live send.py gone; retired 317680 R100 | TRUE | experiment:dg8-aa1-after rows 1-3, 8 |
| (2) box 2005; 0 sessions/inbox; 0 send.py in script | TRUE | rows 4-6 |
| (3) box n / read / send never open send.py or python | TRUE | row 7 |
| (4) v4 wake 0 inbox | FALSE | row 10: agi-run still watches inbox and names send.py. Residue, same as verdict:dg9-aa1-box-never-opens-sendpy. |

Falsifier 2 as written (`git log --diff-filter=D` on the old path) FIRES: aa030dc83 is R100. Content lives under `extensions/agi/deprecated/bin/send.py`. Not a content-delete.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:47Z 10-05: SM after-MOVE helper. Live gone + strace 0. F2 pathspec noted. agi-run residue.
<!-- THOUGHT:END -->
