---
id: goal:g6.2
mint_id: 004d3220565b41c4ba5b56ce24b2c66b
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.2: Retire the padding and keep it recoverable"
---
Done 2026-08-21. 28,916 gamed `-extend<N>` experiment/verdict nodes were
removed from the working tree and archived outside the repo with a manifest
recording the predicate, family and index of every one. 122 family heads were
preserved in-tree as prior art for H3's own finding.

Deviation recorded on purpose: G6/G7 say deprecate, never delete. The owner
directed removal so the git grid would not be initialised over ~29k refs of
baggage. "Never delete" was honoured by **relocation** — archive plus manifest,
plus git history — rather than by retention in-tree.

Result: 29,432 → 516 nodes; `outcome_coverage` unchanged at 0.202 (the
pre-registered must-not-move check); `find_chains` stopped truncating, so
H0c's "the loop cannot be run against this corpus" is now false.