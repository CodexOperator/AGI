---
id: hypothesis:l4-sm45b-the-kid-ceiling-is-the-dispatching-node-own-ceiling-clause-one-number-for-brief-and-harvest
mint_id: 81156d4872414c34ae496d9789fc9df9
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 546739d76e8f5098
season: 2
testable_claim: "CLAIM: one resolver parses the DISPATCHING NODE's own CEILING clause (from its testable_claim/brief text) as the production-line ceiling and threads it through brief.assemble() into BOTH the kid brief segment (conjunct 1 of the SM.45 hypothesis) and cli.py::_kid_line_ceiling (the harvest side), so the kid brief and the harvest check read the SAME number; spawn_budget.production_line_ceiling's config default (40) is used ONLY when the dispatching node carries no explicit CEILING clause. FALSIFIER: a node dispatched with an explicit non-40 CEILING (e.g. 90, as the SM.45 kid4 rebrief set) still shows 40 in the served kid brief, or the harvest still measures overage against 40 instead of the node's own number. CEILING: 20 production lines, 1 kid. Context: SM.45 (l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief) built conjunct 1 (a00-bcb2955a-e58ab4) threading only the CONFIG ceiling into brief.assemble, never a per-dispatch node override -- SM demoted SM.45 (DEMOTE :65) partly for this and ordered this as the immediate fix, bytes held at loop tip b5b3cf123 pending this landing."
title: L4 sm45b the kid ceiling is the dispatching node own ceiling clause one number for brief and harvest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm45b-the-kid-ceiling-is-the-dispatching-node-own-ceiling-clause-one-number-for-brief-and-harvest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
