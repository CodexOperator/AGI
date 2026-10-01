---
id: verdict:dg2-c1
mint_id: bc74b520a94b4f8fbd566c436d0c5954
type: verdict
parents:
  - experiment:dg2-c1-harvest
  - hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-c1-harvest
scaffold_hash: 0d98fdd6dfbd4dc7
season: 2
title: "DG2.C1 (6d8ac01d74): inconclusive_lean_proved:85 -- orphan tree refused once by name, never archived, never re-tried; live reaper-log proof waits on heal's watch restart"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-c1

## Verdict: proved (0.9)
The corrective's order holds on the bytes AND live: an orphan tree (gitdir gone, no HEAD) is refused by name, never archived, never removed. Bytes: red on the base, green on the tip; SM's dry sweep on MAIN's data showed the one changed line. Live (the reaper log, read 11:1xZ 10-01): 4 lines `[sweep] refused a00-fa4269d4: orphan: gitdir gone (no HEAD; nothing archived or removed)` at 03:16:57Z, 03:56:45Z, 06:38:17Z, 07:35:57Z -- the first 16 s after the fix landed (6d8ac01d7, 03:16:15Z), with no reaper restart (the sweep loads heal.py fresh each pass; SM measured); 0 archive/remove lines for that tree after the fix; from 10:50Z the tree reads `kept: live` (re-held, its bytes pinned off-repo by SM). One refusal line per sweep process, never a re-try inside one (the in-process memo). Not 0.95: the bytes are still not pinned by the fix itself (refusal only; SM's off-repo pin stands).
