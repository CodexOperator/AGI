---
id: outcome:s2-w-workflow-py-move
mint_id: 6a45861bad85415caff3766eae0e14e3
type: outcome
parents:
  - verdict:dg8-w-move-after
  - verdict:dg2-w-move-counts
  - goal:g7.16.1.11.15.1
next_edges: []
edited_by: belam
season: 2
status: closed
confidence: 0.9
judged_against: goal:g7.16.1.11.15.1
lens: vision:all-is-one
alignment: aligned
tags:
  - s2
  - phase-w
  - season-close
title: "S2 phase W: workflow.py + 14 js MOVE; living 16 json; skill agi-spawn-chain"
town: core
---
# outcome:s2-w-workflow-py-move

## What landed
- MOVE workflow.py + workflow_note + 14 js → deprecated/; living spawn path is 16 json + agi-spawn-chain skill. Land 033000458; DG8 after-MOVE 0.9.
- A brief bin/workflow.py shim was course-corrected into deprecated/bin/workflow-import-shim.py (never git rm). W retires workflow.py; nothing live opens it.

## Evidence
verdict:dg8-w-move-after · verdict:dg2-w-move-counts · trunk 033000458.

## Adjust
Never git rm workflow.py / the 14 js. Never a second spawn UI beside the living 16.
