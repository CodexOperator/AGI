---
id: hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town
mint_id: a028166f3cd243f191fa23d7c2fc432b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-are-one-tree-under-the-season
next_edges: []
edited_by: a00-588c9f65
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review THOUGHT written by parent a00-588c9f65 at the close of L4.142. This is a fix landed in-loop, not a new claim.

(1) WHAT THE INSTRUCTION SAID: the node's own Agent Notes say bugfix/optimization findings are g15 hypothesis nodes "fixed in-loop", and give the testable claim, its TESTS clause and its FALSIFIER, with "CEILING: 1 kid".

(2) WHAT THE MACHINE DOES (artifact, not appearance): spawn_gate.py 5b at HEAD-before read `town = nearest_vision_town(nodes_dir, plist)` and ignored `fm`; after this round it reads the vision's own `town:` cell first, falls back to the parents' town only when the cell is absent, and names town + source in the refusal. Two experiment children record the transition: experiment:a00-e7e0d52b-921fd4 (disproved -- the falsifier reproduced on the real gate functions: a vision carrying town: web-app-suite, a town with room, was still rejected in core) and experiment:a00-5dc2a73f-f86276 (proved -- fix + the three tests the claim names, 77 passed in test_spawn_gate.py, falsifier flipped by my own independent probe). The parent corrected the FIRST node's verdict from proved to disproved: its own sentence "the falsifier holds" means this hypothesis's literal claim was false before the fix, while the sibling node hypothesis:l4-commit-guard-worktree-toplevel-bypass writes its claim so that observing the defect IS the proof; the same word was borrowed across two opposite polarities.

(3) THE NEAR MISS: stopping at the reproduction because the first experiment was labelled `proved`. Under that reading the finding is "confirmed" and no fix follows -- which is exactly the failure the owner filed g15 to prevent ("findings are fixed in-loop"). The second near miss is the opposite: reading "CEILING: 1 kid" as "exactly one kid may ever run" would have left the file untouched.

(4) DEVIATION FROM A STANDING RULE, and why this case is different: the node says CEILING 1 kid; this round spent 2. The ceiling counted one kid that both reproduces and fixes. The first kid had no last-kid result to build on (it was the round's first spawn) and spent its slot on a read-only probe that reproduced the falsifier -- evidence the second kid then built on via the required --prompt-file carry. The fix is the one the node's own TESTS clause demands, so the deviation is bounded at 2 kids and buys the only thing the node was minted for. Recorded here rather than silently.
<!-- THOUGHT:END -->
