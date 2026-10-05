---
id: verdict:dg2-g7161118-grow-check
mint_id: 069e6c41ba21428c800ef9f72d935fa4
type: verdict
parents:
  - experiment:dg2-g7161118-grow-check
  - hypothesis:g7161118-grow-check-is-the-spawn-order-gate-without-write-py
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g7161118-grow-check
scaffold_hash: d791ca89df8ade9e
season: 2
title: "g7161118 PROVED 0.9: sect grow-check plus growth.tsv is the spawn-order gate without write.py (F1 wrong-order / ok; F2 strace awk only; F3 locked is the corpus ratchet)"
town: core
verdict: proved
---
# verdict:dg2-g7161118-grow-check

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.16.1.11.8, tip 4471a5f6b, 2026-10-04T17:45:52Z)

| conjunct | today | |
|---|---|---|
| (1) not-a-matrix-row -> `refused: wrong order` rc 1; matrix row + matching `key:` -> `ok <nid> *` rc 0 | TRUE | experiment:dg2-g7161118-grow-check rows 1-2 |
| (2) neither call execs write.py | TRUE | rows 3-4: grow-check then `/usr/bin/awk` |
| (3) live node without `key:` prints `refused: locked` | TRUE | rows 5-7. Documents the ratchet; not a disproof |

The CLAIM is (1)+(2). F3 is named corpus gap. Goal F1 (parity MATCH with write.py absent) is the later land, not this round.

## Why 0.9
F1 and F2 ran through the awk `sect grow-check` extracts (1298 B from config:engine-grow). Matrix is `.agi/nodes/.geometry/growth.tsv`. No engine write. write.py still in the clone and unused.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:45Z 10-04: SM queued, DG1 handed the hyp. Independent replica agrees. Goal F1 left for the land that drops write.py.
<!-- THOUGHT:END -->
