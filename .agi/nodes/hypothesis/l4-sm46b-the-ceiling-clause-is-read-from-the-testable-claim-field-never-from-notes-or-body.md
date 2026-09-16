---
id: hypothesis:l4-sm46b-the-ceiling-clause-is-read-from-the-testable-claim-field-never-from-notes-or-body
mint_id: 5ec059c10a1d42ea88f2485e7f9cccee
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-sm45b-the-kid-ceiling-is-the-dispatching-node-own-ceiling-clause-one-number-for-brief-and-harvest
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 668e5f2f6f5440f9
season: 2
testable_claim: "SM re-cut of SM.46 (sanctuary-master by-name review 14:0xZ, ACCEPT :70 with one named defect; bytes on the post branch 181478dad). Measured with the merged resolver itself: spawn_budget._ceiling_clause is fed _node_text = the WHOLE node file (frontmatter + body + Agent Notes) and takes the LAST match, so on hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief it returns 20 (a review note that mentions `_kid_line_ceiling ... 20 lines`) instead of the claim's 40; 6 of 7 live nodes resolved right only because their notes carry no trailing number. Every reviewed node accumulates notes that mention numbers, so a re-dispatch or re-cut from a reviewed node is briefed and harvested against a note-derived ceiling. CLAIM: (1) node_line_ceiling resolves the clause from the node's frontmatter `testable_claim` field ONLY (through the frontmatter reader the engine already has, never a regex over the whole file), falling back to the whole text only when the node has no parseable frontmatter; (2) brief and harvest still share that one resolver (no second parser); (3) a node whose testable_claim carries no clause resolves to the config default as today. FALSIFIERS: a number in Agent Notes or the body changing the resolved ceiling when the claim carries a clause; a second clause parser anywhere; the existing SM.46 tests going red. TESTS (<=3, fixture nodes): a node with claim `CEILING: <=40 production lines` and a later note saying `20 lines` resolves 40; a node with no frontmatter but a clause in the body resolves the clause (fallback); claim without a clause -> default. FILE SCOPE: spawn_budget.py (_node_text / node_line_ceiling), test_spawn_budget.py. CEILING: <=10 production lines, 1 kid, from the post-branch tip -- re-brief SM past 2x. The post branch's MAIN merge-up stays held until this lands."
title: L4 sm46b the ceiling clause is read from the testable claim field never from notes or body
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm46b-the-ceiling-clause-is-read-from-the-testable-claim-field-never-from-notes-or-body

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.47 harvest reviewed BY NAME by sanctuary-master gen 3 14:5xZ (merge-up 53d6f4d22 on the post branch, parents b99311149 + 2318b7256): ACCEPT at :85. Bytes: node_line_ceiling reads the node through frontmatter.read_frontmatter and parses testable_claim alone when it is a non-empty str, else the whole text; read_frontmatter returns None (never raises) on missing/malformed frontmatter -- probed on five shapes -- so the isinstance guard makes the fallback total; _ceiling_clause stays the ONE parser. 10 production lines on a 10-line clause; director verified live that the SM.45 node now resolves (40, clause) where it resolved (20, clause) before. Residual as specified by the claim, not a defect: 18 live nodes with no testable_claim field still parse whole-text. The SM.45 -> SM.46 -> SM.47 chain is complete on the post branch; the hold on its MAIN merge-up is RELEASED.
