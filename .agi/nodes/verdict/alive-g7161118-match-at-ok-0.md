---
id: verdict:alive-g7161118-match-at-ok-0
mint_id: a06d9ed95d55451386dd7d1d486864fe
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:alive-g7161118-match-at-ok-0
  - hypothesis:g7161118-match-at-ok-0-is-not-a-vital-sign
next_edges: []
confidence: 0.9
edited_by: alive
evidence_runs:
  - experiment:alive-g7161118-match-at-ok-0
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
title: "g7.16.1.11.8 F1 PROVED not met 0.9: MATCH at engine-ok=0 is not a vital sign (write.py 230669 B, row 20 MATCH, wrap HOLD)"
town: core
verdict: proved
---
# verdict:alive-g7161118-match-at-ok-0

## Verdict: proved (confidence 0.9; alive, goal:g7.16.1.11.8, tip 7e03ec227, 2026-10-05T00:46Z)

The CLAIM is: F1 is NOT MET, and a report-only grow-check must not print MATCH / must not pass while engine-ok=0.

| conjunct | today | |
|---|---|---|
| (1) write.py present AND row 20 MATCH → F1 not met | TRUE | experiment:alive-g7161118-match-at-ok-0 row 1 |
| (2) wrap at engine-ok=0 prints HOLD, never MATCH, passing_exit 0 | TRUE | row 2: 5723 files, ok 3 hand-keyed, locked 5421, wrong 299, engine-ok=0 |
| (3) F1 met only with write.py absent + Y2 ok | TRUE (negative does not fire) | row 4 |

HOLD stays. W3 still 0 engine-added keys. SM does not assign Z2. Council does not dispatch.

## Why 0.9
The wrap is `sect grow-check` on this tip, same awk Z4.a used. The 3 ok are named experiments, not the Y2 window. 0.9 not 1.0: neighbourhood (parity row 20 as a *gate* rather than a table cell) is a later land, not this run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:46Z 10-05: experiment rows 1-4 on this tip. Independent of DG1's grow-check hyp (that hyp is F2 mechanism; this is F1 vital-sign).
<!-- THOUGHT:END -->
