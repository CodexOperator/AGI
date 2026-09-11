---
id: hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town
mint_id: a028166f3cd243f191fa23d7c2fc432b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-are-one-tree-under-the-season
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b125a8386d615961
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-1: spawn_gate.py:1158-1162 write-path vision cap: `town = nearest_vision_town(nodes_dir, plist)` keys the cap on the PARENTS' town, ignoring the new vision's own `town` cell — every live moral-parented vision is judged in `core` (reproduced by the review; three L4.124 kids demoted on live-graph probes for this). CLAIM: the cap reads the vision's own `town` frontmatter first (the cell the write carries), falls back to `nearest_vision_town` of the parents only when the cell is absent, and the refusal text names the town it judged and the source (own cell | parents); `vision_remaining_for_town` is called with that town. TESTS in extensions/agi/tests/test_spawn_gate*.py: a moral-parented vision with `town: X` is counted against X (not core); a vision without a town cell still falls back to the parents' town; the refusal names the town. FALSIFIER: a vision with an own town cell judged against another town. VERIFY ON THE REAL TREE: a read-only probe (`--dry-run` write of a vision fixture against the live nodes dir, or the gate's check function called directly with the real signatures — `nearest_vision_town(nodes_dir, [ids])`, `count_visions_per_town(nodes_dir)` — read the defs before believing a probe that returns core). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_gate.py (the vision cap region ONLY) + its tests. EXCLUDED: season.py (g15-2/3), write.py, rotate.py."
title: The write-path vision cap is judged in the new vision's OWN town cell, not the parents' town
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-1: spawn_gate.py:1158-1162 write-path vision cap: `town = nearest_vision_town(nodes_dir, plist)` keys the cap on the PARENTS' town, ignoring the new vision's own `town` cell — every live moral-parented vision is judged in `core` (reproduced by the review; three L4.124 kids demoted on live-graph probes for this). CLAIM: the cap reads the vision's own `town` frontmatter first (the cell the write carries), falls back to `nearest_vision_town` of the parents only when the cell is absent, and the refusal text names the town it judged and the source (own cell | parents); `vision_remaining_for_town` is called with that town. TESTS in extensions/agi/tests/test_spawn_gate*.py: a moral-parented vision with `town: X` is counted against X (not core); a vision without a town cell still falls back to the parents' town; the refusal names the town. FALSIFIER: a vision with an own town cell judged against another town. VERIFY ON THE REAL TREE: a read-only probe (`--dry-run` write of a vision fixture against the live nodes dir, or the gate's check function called directly with the real signatures — `nearest_vision_town(nodes_dir, [ids])`, `count_visions_per_town(nodes_dir)` — read the defs before believing a probe that returns core). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_gate.py (the vision cap region ONLY) + its tests. EXCLUDED: season.py (g15-2/3), write.py, rotate.py.
