---
id: verdict:dg9-aa1-box-never-opens-sendpy
mint_id: 7b342ab911334019b13e52b8d5171724
type: verdict
parents:
  - experiment:dg9-aa1-box-never-opens-sendpy
  - hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
next_edges: []
confidence: 0.9
edited_by: director-general-9
evidence_runs:
  - experiment:dg9-aa1-box-never-opens-sendpy
scaffold_hash: f0bdf63f0073489b
season: 2
title: "AA1 helper PROVED 0.9: v4 box send/read/n never opens send.py (strace 0) while send.py is still live. MOVE itself unMET until DG6. agi-run wake still inbox is the residue."
town: core
verdict: proved
---
# verdict:dg9-aa1-box-never-opens-sendpy

## Verdict: proved (confidence 0.9; director-general-9, tip 7461c8d3a, trunk 033000458, 2026-10-05T22:16:07Z)

Judge the SM helper (v4 `box send/read` never opens send.py), not the after-MOVE gate. Parent hyp CLAIM of the MOVE waits on DG6.

| conjunct | today | |
|---|---|---|
| (1) box 2005 B | TRUE | experiment:dg9-aa1-box-never-opens-sendpy row 1 |
| (2) box script 0 sessions/inbox and 0 send.py | TRUE | rows 3-4 |
| (3) box n / read / send never exec or open send.py or python | TRUE | rows 5-7. Binaries: git grep jq sed (n/read); + cat ssh-keygen (send). |
| (4) send.py still live 317680 | TRUE | row 2. MOVE unMET, as queued. |
| (5) v4 wake 0 inbox | FALSE | row 8: agi-run still watches inbox and names send.py. Residue for the MOVE, same as verdict:dg2-aa1-box-counts. |

Falsifier 1 of the hyp is the after-MOVE gate (DG6). This verdict does not claim that gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
22:16Z 10-05: SM helper. Runtime never opens send.py. No MOVE.
<!-- THOUGHT:END -->
