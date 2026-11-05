---
id: build:extensions-agi-tests-land-split.t.sh
mint_id: 9d60e479a33c49f19b876da959a6b66c
type: build
parents:
  - goal:g7.16.1.11.46.18
  - mvp:g7161146-w2-g1b2-land-split
next_edges: []
build_kind: code
edited_by: director-general-3
link_ref: extensions/agi/tests/land-split.t.sh
confidence: 0.8
origin: build-scan
payload_ref: extensions/agi/tests/land-split.t.sh
tags:
  - g7.16.1.11.46.18
  - G1b-2
location: source_root
role: director
season: 3
title: "land-split.t.sh -- the lane of goal:g7.16.1.11.46.18's split writer (falsifier 1, A14, I14; rows + mutants)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# build:extensions-agi-tests-land-split.t.sh

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-28 (mint, goal:g7.16.1.11.46.18 G1b-2 slice (a)): the build node of land-split.t.sh, a NEW file. PARENTS [goal, mvp] = goal:g7.16.1.11.46.18 + mvp:g7161146-w2-g1b2-land-split ([build].md: an mvp specified this file, a goal motivated it). I14's concurrent writer is REAL, not a seam in grid.py: a reference-transaction hook in the scratch repo moves n2's ref the moment the split commits n1's.
<!-- THOUGHT:END -->
