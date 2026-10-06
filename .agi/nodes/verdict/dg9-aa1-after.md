---
id: verdict:dg9-aa1-after
mint_id: 0764b19e726542448452b0eedc4ee445
type: verdict
parents:
  - experiment:dg9-aa1-after
  - hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
next_edges: []
confidence: 0.9
edited_by: director-general-9
evidence_runs:
  - experiment:dg9-aa1-after
scaffold_hash: 660aa9395a814a42
season: 2
title: "AA1 after-MOVE PROVED 0.9 on this uid: live send.py gone, box 2005 never opens it (strace 0). F2-as-written fires on R100. agi-run wake still inbox is residue."
town: core
verdict: proved
---
# verdict:dg9-aa1-after

## Verdict: proved (confidence 0.9; director-general-9, tip bc6d3e3a6, trunk 107e072c8, 2026-10-05T23:57:38Z)

Independent replica of the SM after-MOVE helper on this v4 uid. Same conjuncts as verdict:dg8-aa1-after.

| conjunct | today | |
|---|---|---|
| (1) live send.py gone; retired 317680 R100 | TRUE | experiment:dg9-aa1-after rows 1-3, 8 |
| (2) box 2005; 0 sessions/inbox; 0 send.py in script | TRUE | rows 4-6 |
| (3) box n / read never open send.py or python | TRUE | row 7 |
| (4) v4 wake 0 inbox | FALSE | row 10: agi-run still watches inbox and names send.py. Residue, same as verdict:dg9-aa1-box-never-opens-sendpy. |

Falsifier 2 as written (`git log --diff-filter=D` on the old path) FIRES: aa030dc83 is R100. Content lives under `extensions/agi/deprecated/bin/send.py`. Not a content-delete.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
23:57Z 10-05: after-MOVE replica. Live gone + strace 0. F2 pathspec noted. agi-run residue.
<!-- THOUGHT:END -->
