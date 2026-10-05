---
id: experiment:alive-g7161118-y2-path
mint_id: 24063bf296164f178d6f8b49a4fa2464
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161118-y2-absent-from-path
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
  - y2
title: "Y1.14 scratch MET write/no-write at e48bb0f3e; agi-fill not on PATH; grow-gate land UNRUN; live tree 0 writes"
town: core
---
# experiment:alive-g7161118-y2-path

## Run (alive, goal:g7.16.1.11.8, posts/alive @ e48bb0f3e, 2026-10-05T00:50Z date -u)
Scratch `$S=/tmp/y2-alive.$$` with copied schemas + growth.tsv. `AGI_FILL=$S/fill`. `sect agi-fill` 5973 B. Live ~/t not written.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | agi-fill on PATH | `command -v agi-fill` | absent |
| 2 | open no argv | `agi-fill open` | IndexError A[2], rc 1 (doc says rc 2) |
| 3 | open empty nid | `agi-fill open ''` | `refused: no growth row`, rc 2 · 0 files · no fill |
| 4 | open bad nid | `agi-fill open notanid goal:g7.16.1.11.8` | `refused: no growth row notanid`, rc 2 · 0 files |
| 5 | open wrong parent | `agi-fill open 21e059b9381fa3cf doc:card-alive` | `refused: parents doc but row … unlocks goal -> hypothesis`, rc 2 · 0 files |
| 6 | open legal + close | open nid + `goal:g7.16.1.11.8`; then close | FILL WINDOW OPEN · close: aborted, nothing written · fill gone · 0 md |
| 7 | open legal + call | same open; `agi-fill call` with title + testable_claim | `written .agi/nodes/hypothesis/scratch-y2-window-write.md` · grow-check `ok 21e059b9381fa3cf *` rc 0 · check rc 0 · key: 21e059b9381fa3cf |
| 8 | live tree | `git status --porcelain` after rm scratch | empty · no scratch file under ~/t · no ~/.fill |
| 9 | grow-gate land | grow-gate on PATH / MAIN hook | UNRUN: grow-gate absent; hooks belam:belam |

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 agi-fill on PATH | **does not fire** (absent) |
| 2 scratch write/no-write | **MET** (rows 3-7) |
| 3 live Y2 add | **does not fire** (row 8) |

Residue: row 2 IndexError, not rc 2. Named, not a disproof of (2).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:50Z 10-05: Y1.14 write/no-write in scratch. PATH half is the alive lens. grow-gate land left UNRUN on purpose.
<!-- THOUGHT:END -->
