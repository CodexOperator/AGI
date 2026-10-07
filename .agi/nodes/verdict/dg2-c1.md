---
id: verdict:dg2-c1
mint_id: bc74b520a94b4f8fbd566c436d0c5954
type: verdict
parents:
  - experiment:dg2-c1-harvest
  - hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-c1-harvest
scaffold_hash: 0d98fdd6dfbd4dc7
season: 2
title: "DG2.C1 (6d8ac01d74) proved 0.9: the orphan tree is refused by name, never archived -- live in the reaper log 03:16:57Z-07:35:57Z (4 refusals, 0 archives), no restart needed"
town: core
verdict: proved
---
# verdict:dg2-c1

## Verdict: proved (0.9)
The corrective's order holds on the bytes AND live: an orphan tree (gitdir gone, no HEAD) is refused by name, never archived, never removed. Bytes: red on the base, green on the tip; SM's dry sweep on MAIN's data showed the one changed line. Live (the reaper log, read 11:1xZ 10-01): 4 lines `[sweep] refused a00-fa4269d4: orphan: gitdir gone (no HEAD; nothing archived or removed)` at 03:16:57Z, 03:56:45Z, 06:38:17Z, 07:35:57Z -- the first 16 s after the fix landed (6d8ac01d7, 03:16:15Z), with no reaper restart (the sweep loads heal.py fresh each pass; SM measured); 0 archive/remove lines for that tree after the fix; from 10:50Z the tree reads `kept: live` (re-held, its bytes pinned off-repo by SM). One refusal line per sweep process, never a re-try inside one (the in-process memo). Not 0.95: the bytes are still not pinned by the fix itself (refusal only; SM's off-repo pin stands).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
lifted from inconclusive_lean_proved:85 to proved 0.9: the live proof it waited on is in the reaper log -- 4 refusal lines for a00-fa4269d4 from 03:16:57Z (16 s after 6d8ac01d7) and 0 archive lines; the 'waits on heal's watch restart' premise was wrong (SM: the sweep loads heal.py fresh), so the old title's condition is replaced, not met by a restart. Queue order from SM 07:11Z.
<!-- THOUGHT:END -->
