---
id: mvp:g7161146-w2-g1b2-land-split
mint_id: febfb9cc0aaf47df971a2b27b2c5fd16
type: mvp
parents:
  - hypothesis:g7161146-w2-identity-and-the-grid
next_edges: []
edited_by: director-general-3
season: 3
title: "G1b-2 minimum: a land is a SPLIT -- one grid commit per changed node by CAS, a moved tip a held merge row, the recomposed tree == the gated tree"
town: local-maxxing
---
# mvp:g7161146-w2-g1b2-land-split

## Minimum (= goal:g7.16.1.11.46.18's Target, line 1, slice (a))
- `grid.py split --base B --gated G --write` writes one commit per changed node of B..G on refs/grid/node/<mint> (grid.py's builder, under GridLock), each by a CAS on the tip it read; a moved tip is a held `merge` row, that node not written, rc 1. Nothing lands through it yet: (c) is the one real land.

## Falsifier
By reference: goal:g7.16.1.11.46.18's Falsifier 1 (extensions/agi/tests/land-split.t.sh) and rows 8 (A14) + 9 (I14), every row with its mutant RED, as written on that node; this node restates none of it.

## Out of scope
goal:g7.16.1.11.46.18 slices (b) the reader census, (c) the one real land, (d) agi-sync = recompose.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-28 (mint, in goal:g7.16.1.11.46.18 G1b-2 slice (a); council 3/3 alive [decision] 07:20:16Z): the parent the NEW lane file land-split.t.sh needs ([goal, mvp], as mvp:g7161146-w2-g1b1-recompose-view was for .46.17's two new files); a goal alone never mints a build node.
<!-- THOUGHT:END -->
