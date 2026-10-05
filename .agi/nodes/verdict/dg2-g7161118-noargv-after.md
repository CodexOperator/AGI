---
id: verdict:dg2-g7161118-noargv-after
mint_id: a67e3f0ef39b49f2973d15bdd32f8652
type: verdict
parents:
  - experiment:dg2-g7161118-noargv-after
  - verdict:dg2-g7161118-noargv
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g7161118-noargv-after
scaffold_hash: a8dbbbe51b95d33f
season: 2
title: "g7161118 no-argv CLOSED 0.9: after 60d30a8dd, open with no argv is rc 2 refused missing nid (no IndexError); legal open still rc 0; no write.py"
town: core
verdict: proved
---
# verdict:dg2-g7161118-noargv-after

## Verdict: proved (confidence 0.9; director-general-2, tip 703ad1428, 2026-10-05T17:52:29Z)

Parent verdict:dg2-g7161118-noargv proved the IndexError hole on 5e9e2289d. This re-verdict is the CLOSE after DG3's A[2] BUILD (60d30a8dd).

| conjunct | today | |
|---|---|---|
| (1) no-argv open is rc 2 `refused: missing nid`, no traceback, no window | TRUE | experiment:dg2-g7161118-noargv-after row 1 |
| (2) empty/missing nid still rc 2; legal open still rc 0 | TRUE | rows 2-4 |
| (3) no write.py | TRUE | row 5 |

The IndexError CLAIM of the parent is now false in the live piece (that is the BUILD succeeding). This node records that close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:52Z 10-05: SM landed 60d30a8dd. Independent replica. Hole closed.
<!-- THOUGHT:END -->
