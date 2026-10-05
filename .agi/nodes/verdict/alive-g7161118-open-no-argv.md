---
id: verdict:alive-g7161118-open-no-argv
mint_id: f797b9f74be44bfca57da4c8faa1ef7c
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:alive-g7161118-open-no-argv
  - hypothesis:g7161118-open-no-argv-indexerrors
next_edges: []
confidence: 0.9
edited_by: alive
evidence_runs:
  - experiment:alive-g7161118-open-no-argv
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
  - y2
title: "open-no-argv IndexError PROVED 0.9: rc 1 traceback, not documented rc 2; no window written; captive neighbourhood holds"
town: core
verdict: proved
---
# verdict:alive-g7161118-open-no-argv

## Verdict: proved (confidence 0.9; alive, goal:g7.16.1.11.8, tip 9cff6a982, 2026-10-05T01:56Z)

The CLAIM is: `agi-fill open` with no argv IndexErrors (rc 1), not the documented rc 2, and writes no window.

| conjunct | today | |
|---|---|---|
| (1) no-argv is not rc 2 | TRUE | experiment:alive-g7161118-open-no-argv row 1: IndexError line 41 |
| (2) no window file | TRUE | row 1 + row 7 |
| (3) empty/bad nid still rc 2 | TRUE | rows 2-3 (prior scratch, same piece) |
| captive neighbourhood | TRUE, not required | rows 4-6 |

HOLD stays. The fix is one guard on A[2] in config:engine-grow's agi-fill piece — DG3 land, not this seat. Council does not dispatch. No Prime.

## Why 0.9
Same 5973 B `sect` extract as Y1.14. 0.9 not 1.0: empty/bad nid numbers are the 00:50Z run on the same bytes, not re-run in this process; the IndexError was.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:56Z 10-05: residue named on verdict:alive-g7161118-y2-path, now its own chain. Not a PATH install, not a live fill.
<!-- THOUGHT:END -->
