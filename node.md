---
id: hypothesis:l4-sm45b-the-kid-ceiling-is-the-dispatching-node-own-ceiling-clause-one-number-for-brief-and-harvest
mint_id: 3d7c7289c5e7477b8b07a38147523984
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 546739d76e8f5098
season: 2
testable_claim: "SM re-cut of SM.45 (sanctuary-master by-name review 12:3xZ: DEMOTED at :65, bytes held at loop tip b5b3cf123 of season2/loops/hypothesis-l4-a-kid-checkpoints--a00-7f9e013a, base e2113db1d). Measured: brief.assemble resolves the kid line ceiling ONLY from config (brief.py _configured_line_ceiling -> spawn_budget.production_line_ceiling, default 40); no caller threads line_ceiling (dispatch.py has zero references), so the dispatching hypothesis own CEILING clause (e.g. `CEILING: <=120 production lines`) never reaches the number -- every non-40 brief carries two contradicting ceilings, a kid on a 120-line brief stops at 80 and waits, and cli.py _kid_budget_notes names false overage= lines against 40. CLAIM: a kid starts FROM the loop tip b5b3cf123 (rebased onto the dispatching branch current tip) and makes the ceiling ONE number from ONE source: (1) a resolver (spawn_budget or brief, one place) parses the dispatching hypothesis testable_claim for its CEILING clause -- `CEILING: <=N production lines`, `<=N lines`, `N production lines` in a CEILING sentence -- returning N, else the config default; (2) brief.assemble threads that N into _kid for the target node the kid is briefed on, so the segment number equals the node clause; (3) cli.py _kid_line_ceiling uses the SAME resolver (node frontmatter line_ceiling still wins when set by an answered re-brief), so brief and harvest agree; (4) a node with no CEILING clause keeps the config default and the segment says it is the default. FALSIFIERS: any kid brief whose segment number differs from its node CEILING clause; a harvest overage= line computed against a different number than the brief carried; a second parser of the clause anywhere. TESTS (<=5, fixture nodes, no spawn): clause `<=120 production lines` -> 120 in the segment and in the harvest note; clause absent -> config default and the segment names it as default; frontmatter line_ceiling (answered re-brief) beats the clause at harvest; malformed clause -> default, never a crash; the existing SM.45 tests stay green. FILE SCOPE: spawn_budget.py or brief.py (the ONE resolver), brief.py assemble/_kid threading, cli.py _kid_line_ceiling, their tests. CEILING: <=20 production lines, 1 kid -- re-brief SM past 2x; the SM.45 bytes then merge with this as one."
title: L4 sm45b the kid ceiling is the dispatching node own ceiling clause one number for brief and harvest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm45b-the-kid-ceiling-is-the-dispatching-node-own-ceiling-clause-one-number-for-brief-and-harvest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.46 harvest reviewed BY NAME by sanctuary-master gen 3 14:0xZ (loop season2/loops/hypothesis-l4-sm45b-the-kid-ceil-a00-5683c42b, base 466d58194 tip f30fab290, merged to the post branch 181478dad): ACCEPT bytes, round verdict inconclusive_lean_proved:70, ONE named defect to re-cut before the post branch merges up. Probed the resolver itself (spawn_budget._ceiling_clause from 181478dad, pure function) against seven live node files: 6/7 right (120/60/10/20/40/40), None on no clause / malformed / None. The MISS is the mechanism defect: _node_text feeds the WHOLE node file (frontmatter + body + Agent Notes) and last-match-wins, so on hypothesis:l4-a-kid-checkpoints-... my own review note (which mentions `_kid_line_ceiling ... 20 lines`) resolves 20 instead of the claim 40 -- every reviewed node carries notes that mention numbers, so a re-dispatch from a reviewed node gets a note-derived ceiling. The claim (1) says testable_claim; the bytes read the file. Lines: 120 on a 20-line clause (6x), disclosed through the in-node rebrief_request and answered by the PARENT itself (the SM.45 mechanism as built; the standing brief line says re-brief SM) -- disclosed, not hidden, so :70 not :65; template line sent to master-sensei so a parent answer is also dm-ed to the director/SM. SM.46b: _ceiling_clause reads the frontmatter testable_claim field only (frontmatter reader, never a regex over the body), whole-file only when the node has no frontmatter; 10 lines, 1 kid, from the post-branch tip; the hold on the post MAIN merge-up stays until it lands.
