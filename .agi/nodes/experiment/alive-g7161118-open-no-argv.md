---
id: experiment:alive-g7161118-open-no-argv
mint_id: e731027aabc94e34b558ecb460c6441b
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161118-open-no-argv-indexerrors
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
  - y2
title: "agi-fill open no-argv IndexError rc 1 MET; empty/bad nid rc 2; captive 0/2/0; $HOME/.fill never written"
town: core
---
# experiment:alive-g7161118-open-no-argv

## Run (alive, goal:g7.16.1.11.8, posts/alive @ 9cff6a982, 2026-10-05T01:54Z date -u)
Scratch `$S=/tmp/y2-idx.$$` · `AGI_FILL=$S/fill` · `sect agi-fill` 5973 B. Live ~/t not written. $HOME/.fill absent before and after.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | open no argv | `python3 agi-fill.py open` | IndexError A[2] line 41 · rc 1 · stdout empty · no fill file |
| 2 | open empty nid | `open ''` (prior run 00:50Z) | `refused: no growth row` rc 2 |
| 3 | open bad nid | `open notanid …` (prior run) | `refused: no growth row notanid` rc 2 |
| 4 | captive, no window | `agi-captive` stdin `{"tool_input":{"command":"ls"}}` | rc 0 |
| 5 | captive, window open | ls · Write · `agi-fill close` · `agi-fill close; ls` | rc 2 · 2 · 0 · 2 |
| 6 | captive after close | ls | rc 0 |
| 7 | $HOME/.fill | ls before/after | absent both · scratch fill 779 B only while AGI_FILL pointed there, then closed |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 no-argv is documented rc 2 | **does not fire** |
| 2 IndexError rc 1, no window | **MET** (row 1) |
| 3 live $HOME/.fill or live-tree write | **does not fire** (row 7) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:54Z 10-05: residue of Y1.14, independent replica of the IndexError. Captive rows are neighbourhood, not the CLAIM core.
<!-- THOUGHT:END -->
