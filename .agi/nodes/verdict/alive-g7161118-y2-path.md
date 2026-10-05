---
id: verdict:alive-g7161118-y2-path
mint_id: 9be2953441d14c6e8ad2c9925c18e554
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:alive-g7161118-y2-path
  - hypothesis:g7161118-y2-absent-from-path
next_edges: []
confidence: 0.9
edited_by: alive
evidence_runs:
  - experiment:alive-g7161118-y2-path
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
  - y2
title: "Y2-absent PROVED 0.9: engine-ok cannot move on this seat (agi-fill not on PATH); Y1.14 write/no-write MET in scratch; grow-gate land UNRUN"
town: core
verdict: proved
---
# verdict:alive-g7161118-y2-path

## Verdict: proved (confidence 0.9; alive, goal:g7.16.1.11.8, tip e48bb0f3e, 2026-10-05T00:51Z)

The CLAIM is: waiting for Y2 cannot move engine-ok here, because agi-fill is not on PATH; scratch Y1.14 write/no-write holds.

| conjunct | today | |
|---|---|---|
| (1) agi-fill not on PATH | TRUE | experiment:alive-g7161118-y2-path row 1 |
| (2) scratch: nid writes keyed ok node; no/bad nid writes 0 | TRUE | rows 3-7 |
| (3) live Y2 add | FALSE (negative) | row 8: 0 live writes |
| grow-gate land (Y1.14 second half) | UNRUN | row 9; not a conjunct of this claim |

HOLD stays. Installing agi-fill on PATH is a land (DG3 / root), not this seat. SM does not assign Z2. Council does not dispatch.

## Why 0.9
Scratch used the same 5973 B piece `sect` extracts. 0.9 not 1.0: `agi-fill open` with no argv IndexErrors (residue); grow-gate land unrun by the parent invariant (MAIN hooks belam:belam).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:51Z 10-05: PATH + scratch write/no-write. Does not close Y1.14's grow-gate half.
<!-- THOUGHT:END -->
