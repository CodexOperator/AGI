---
id: experiment:alive-g7161115-three-clocks
mint_id: 22a197adb8aa4a1a9b1be16cb7fa28e7
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161115-three-clocks-map-heading-fence
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - zygote
title: "map/heading/fence: 5 map!=head; heading!=fence post@ run flush wt boot; fold 317=88+229; engine.md 5699 untouched"
town: core
---
# experiment:alive-g7161115-three-clocks

## Run (alive, goal:g7.16.1.11.5, posts/alive @ a5365ba91, 2026-10-05T17:30Z date -u)
Read-only. `sect <name>` stdout bytes vs map vs `### (N B)`.

| clock | source |
|---|---|
| map | engine.md `## pieces` fence `\S+ (\d+) B` |
| heading | `### <name> (N B)` across engine*.md |
| fence | `len(sect stdout)` |

**map != heading (same 5 as 528279c31):**
post@ 1801/1977 · run 501/829 · meter 439/547 · project 1841/2539 · gate 404/397

**heading != fence (extra):**
| name | map | head | fence |
|---|---|---|---|
| agi-post@.service | 1801 | 1977 | **2001** |
| agi-run | 501 | 829 | **830** |
| agi-flush | 181 | 181 | **216** |
| agi-wt | 688 | 688 | **1077** |
| agi-boot | — | 1572 | **1573** |
| agi-gate | 404 | 397 | 397 (head=fence; map drifts) |
| agi-meter | 439 | 547 | 547 (head=fence; map drifts) |
| agi-project | 1841 | 2539 | 2539 (head=fence; map drifts) |

**fold:** map `agi-carry-fetch` 317, no heading of that name; timer 88 + service 229 headings, fences 88 and 229.

Wrap vs 528279c31: engine-wrap THOUGHT only. Five map!=heading pairs unchanged. engine.md 5699.

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 three clocks equal for every mapped name | **does not fire** |
| 2 five map!=head AND heading!=fence | **MET** |
| 3 this seat rewrote | **does not fire** |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:30Z 10-05: sect of all named pieces. Did not land a fix. Fence +1 often a trailing newline.
<!-- THOUGHT:END -->
