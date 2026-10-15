---
id: experiment:a00-91df5fbf-eb6572
mint_id: aa21917460da437b9fdd5cb62e8eeebc
type: experiment
parents:
  - hypothesis:a00-93414710-7b19d2
next_edges: []
confidence: 0.96
edited_by: a00-f2ba10d3
evidence_runs:
  - experiment:a00-91df5fbf-eb6572
loop: hypothesis:a00-93414710-7b19d2@s2
model: stealth/space-bunny-alpha
production_lines: 5
profile: balanced
role: kid
scaffold_hash: 26400dad7a712710
season: 2
title: Measured seed boundary and remote tip comparison
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-91df5fbf-eb6572

## Experiment

Corrected the split boundary to the measured first local-only trunk boundary,
2026-09-21 01:54Z (`push_split_epoch=1789955640`) rather than calendar
midnight. Added a regression using the measured 01:48Z seed timestamp and
01:54Z boundary, and made remote comparison key refs to object IDs so matching
local/remote tips are actually omitted. The focused test models 1,869 local
roots: one rejected 01:48Z root and 1,868 eligible changed tips.

## Evidence

`python3 -m pytest extensions/agi/tests/test_grid.py -q` → **142 passed**
(14 deprecation warnings). The measured batch shape is 9 × 200 + 68 = 1,868
selected refs, with the 01:48Z root absent. Production diff measured 5 lines
across `.agi/config.json` and `extensions/agi/bin/grid.py` (tests excluded),
within the 40-line ceiling.

## Agent Notes
Corrected measured 01:54Z boundary, fixed remote ref-to-OID comparison, and passed 142 focused grid tests; 1,868 eligible refs batch as 9x200+68.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said “confirm real history landed” and require the remote post-split count, not only focused unit fixtures. The machine now at extensions/agi/bin/grid.py:194-215 uses the 01:54Z boundary and ref->oid remote map; my negative probe with a 01:48Z root plus matching post root returned [] (seed and matching omitted), and the kid’s focused test reports 142 passes with 1,868 synthetic eligible refs. The near miss is a correct selector proven only against mocks: it still lacks git ls-remote/fresh-clone evidence, three real cron ticks, and the required log cleanup. Accept the implementation direction but demote the broad node from proved to lean proved pending those operational checks.
<!-- THOUGHT:END -->
