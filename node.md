---
id: goal:g7.16.1.11.22
mint_id: 2191f59769dc4ecea9f21ddcbceb0154
type: goal
parents:
  - goal:g7.16.1.11
  - goal:g7.16.1.11.21
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.22
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 50848b61abf4dd8b
season: 2
seeds:
  - goal:g7.16.1.11
  - goal:g7.16.1.11.21
status: complete
tags:
  - council
  - legacy-mark
  - e1
  - g7.16.1.11
title: "G7.16.1.11.22: a node's legacy mark is computed from the bytes -- entry, graphed-here and contains-k read off the node file's own first-parent history and D1's members(), rendered by viewport.py identically in the terminal and the llm view (E1 D3)"
town: core
---
# goal:g7.16.1.11.22

## Why this exists
goal:g7.16.1.11: the owner asked for a truthful "not just plopped in" mark (D3, all-is-one; doc:rse-d3-legacy v2, landed 05ccc3e20b, restated off the grid because grid commit retires under E2). The rule is computed, never a front-matter field, because a field is asserted and goes stale the moment someone graphs the node.
goal:g7.16.1.11.21: the rule's `contains k` is `|members(N)| - 1` from D1's `members()` and its front-matter parser is D1's `fm()`, so this leaf is built after D1's nest.py exists.

## Target end-state
- A node's mark is one of `[legacy]` (k = 0, not graphed since its entry), `[legacy ⊃k]` (k > 0, not graphed since), `[⊃k]` (k > 0, graphed since) or none (k = 0, graphed), where ENTRY is the newest of the path's first commit, the commit that ADDS `nest:`, and the commit after which `season:` equals the current season; "graphed" means a commit above the entry after which the node's `parents:` GAIN a `goal:` id absent at the entry (or, when the entry is the first commit, the node was minted with a goal parent).
- The rule is python, reads only the container's own file history plus D1's `members()` and `fm()` (one parser), and follows renames, so a retire move keeps the history.
- `viewport.py` prints the mark as one more suffix beside `town_mark`, from the cache; the terminal and `--emit llm` print the same string. Opening a `⊃k` node lists its members (`nest.py slice`), retired ones included.

## Invariants
- The mark is computed from the bytes: no front-matter field carries it; a member's own later work never clears its container's mark.
- Retire, never delete: a retired member still counts in k.
- One render, two readers (goal:g2.19): the terminal and the llm view agree byte-for-byte.

## Falsifier
1. L1 on the trunk the rule reads the same mark as v1's grid-ref rule for every build node that has a grid ref (297 of 297 at the doc's measure; the frozen refs stay readable); L2 at the season-3 tip every live node D2 nested or carried reads `legacy` or `legacy ⊃k` until a goal is gained; L3 `python3 extensions/agi/bin/viewport.py --verify` exits 0 with the mark on.
2. Negative: `git grep -n -E '^legacy:' -- '.agi/nodes/*/*.md'` shows 0 hits (the mark is never a front-matter field), and `git grep -n 'refs/grid' -- extensions/agi/bin/legacy.py` shows 0 hits (the rule reads no grid ref).

## Out of scope
goal:g7.16.1.11.21 (D1, the reader this leaf calls) · the rollover and its tooling (E5) · the grid commit's retirement (E2) · importing a foreign project (the existing scanner with that project's own map needs no new code).

## Agent Notes
Assigned to **director-general-5**. (python + viewport; builder, because D1's nest.py is DG5's code; DG2 writes the falsifier lane first; .21 has landed nest.py at 38e61463c7; SM 16:47Z, DG1 16:5xZ; DG3 stays on census v8 / AA1.V)

<!-- THOUGHT:BEGIN -->
10-12 (director-general-5): CLOSED on the falsifier AS WRITTEN, every line run at trunk 67730b8fb7 (the rule landed in eb6cae07e8, SM LAND of the D3 re-forward dg1-d3-remint 550f21b515 with the test row a65acfc66e; 42634e22af keeps the test rows off the user's real cache). L1 `test_l1_on_the_trunk_every_build_node_with_a_grid_ref_reads_the_same_mark` run for real (D3_TRUNK=<repo> D3_TRUNK_REV=67730b8fb7, no skip): 1 passed in 109 s = the mark equals v1's grid-ref rule for every build node with a grid ref. L2 `test_legacy.py` season rows (carried node, newest-of entry, retire move keeps history, a goal gained then dropped on a merged branch, a member graphed later never clears its container, the mark never read from a front-matter field): the file is 70 passed, 1 skipped (the skip was L1 above, now run). L3 `viewport.py --verify` exit 0 ("PASS - one stream, two formatters, same nodes in the same order", 40 frames). Negatives: `git grep -n -E '^legacy:' -- '.agi/nodes/*/*.md'` 0 hits; `git grep -n 'refs/grid' -- extensions/agi/bin/legacy.py` 0 hits. No falsifier was amended. The season-3 tip clause of L2 (every live node D2 nested or carried reads legacy until a goal is gained) is the rows' carried-node case; the rollover itself is E5, out of scope here.
<!-- THOUGHT:END -->
