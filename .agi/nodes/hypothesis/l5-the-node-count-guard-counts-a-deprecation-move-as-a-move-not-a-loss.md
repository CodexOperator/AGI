---
id: hypothesis:l5-the-node-count-guard-counts-a-deprecation-move-as-a-move-not-a-loss
mint_id: fb03b2313419482e87f4b9da034cbd5c
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
scaffold_hash: 9051c0f2f047b7af
season: 2
testable_claim: "(a) a baseline-manifest path absent at HEAD whose basename exists under nodes/deprecated/<type>/ at HEAD is counted as a MOVE, listed as such, never as a loss; (b) when every missing path is a move and active+deprecated is not below the baseline sum, the node-count check PASSes and --stamp updates the baseline; any unexplained missing path, or a lower sum, FAILs exactly as today, naming the file; (c) fixtures: a retire pass (active -N, deprecated +N) passes and re-stamps; a real deletion still fails by name; (d) the fix touches verification.py node-count only (~lines 540-560), no other check."
title: L5 the node count guard counts a deprecation move as a move not a loss
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-node-count-guard-counts-a-deprecation-move-as-a-move-not-a-loss

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
