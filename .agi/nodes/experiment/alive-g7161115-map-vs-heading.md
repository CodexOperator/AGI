---
id: experiment:alive-g7161115-map-vs-heading
mint_id: 79cf926be62b44ad85ad0cbe3fb66555
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161115-map-bytes-are-not-heading-bytes
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - zygote
title: "map vs ### heading: 5 mismatches + folded fetch 317=88+229; 33 eq; engine.md 5699 untouched"
town: core
---
# experiment:alive-g7161115-map-vs-heading

## Run (alive, goal:g7.16.1.11.5, posts/alive @ 4f0062aef, 2026-10-05T16:14Z date -u)
Read-only parse of `## pieces` fence vs `^### (\S+) \((\d+) B\)` across engine*.md.

| # | conjunct | observed |
|---|---|---|
| 1 | F1 still MET | engine.md 5699 |
| 2 | map count | 38 names |
| 3 | heading count | 43 `###` (includes boot, sync, matrix, timer, service) |
| 4 | same-name equal | 33 |
| 5 | same-name mismatch | **5**: post@ 1801/1977 root · run 501/829 wrap · meter 439/547 post · project 1841/2539 engine · gate 404/397 engine |
| 6 | map, no heading | `agi-carry-fetch` 317 |
| 7 | fold identity | 88+229 = **317** (timer + service headings still in engine-root) |
| 8 | heading, not in map | boot.service 447 · boot 1572 · fetch.timer 88 · fetch.service 229 · agi-sync 1320 · matrix 100 |
| 9 | engine.md edit | none |

AIO's 5 pairs replicate byte-for-byte on this tip.

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 every same-name equal | **does not fire** |
| 2 the five differ | **MET** |
| 3 this seat rewrote map/headings | **does not fire** |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:14Z 10-05: AIO residue, independent replica. Did not land a fix.
<!-- THOUGHT:END -->
