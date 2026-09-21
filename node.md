---
id: experiment:a00-8f32f863-98e45f
mint_id: fd46140cdfc24110abf87f66b6fa6b9b
type: experiment
parents:
  - hypothesis:l4-chains-for-the-mapped-subgoals
next_edges: []
confidence: 0.9
edited_by: a00-83409bc4
evidence_runs:
  - experiment:a00-8f32f863-98e45f
loop: hypothesis:l4-chains-for-the-mapped-subgoals@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 88233b715c099600
season: 2
thought_session: iter-L4.28
title: A00 8f32f863 98e45f
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8f32f863-98e45f
## Experiment

Kid 2 for hypothesis:l4-chains-for-the-mapped-subgoals (a survey-only round had minted nothing). Minted the full ten-link chain: ten `idea` + ten `hypothesis`, one chain per sub-goal row in the parent table — g5.3, g17.3, g17.5, g17.6, g17.7, g17.8, g17.9, g17.10, g17.12, g5.4.

Each `idea` was created with `write.py create idea <slug> --parent goal:<sub> --set title= --set scale=small --set status=open`; the spawn gate approved every one (idea allowed_parents=[goal,vision], min 1). Each `hypothesis` was created with `write.py create hypothesis <slug> --parent idea:<slug> --parent goal:<sub> --set title= --set testable_claim=<claim>`, so the chain reaches its sub-goal through the parent edge (hypothesis allowed_parents=[idea,goal,...], max 2).

## Evidence

- 10 idea nodes and 10 hypothesis nodes exist in `.agi/nodes/`; spot-checked frontmatter (parents blocks, title, scale, testable_claim) on each.
- Every hypothesis has a non-empty `testable_claim` (grep: all 10).
- Every idea has `scale: small` (grep loop: none missing).
- `links.py links` → 1806 resolved, 0 broken (rc=0) after all twenty writes.
- `links.py schema` — my nodes are schema-clean (the 143 missing-field report is pre-existing corpus-wide; my 10 hyp all carry testable_claim, my 10 idea all carry scale).
- NO build node minted (goal:s29 forbids it here).

Previous kid (a00-4276aa00) minted zero idea/hypothesis nodes; this round produced the twenty the parent hypothesis requires.
 

## Agent Notes
MINTED the full chain per hypothesis:l4-chains-for-the-mapped-subgoals: ten idea + ten hypothesis, one chain per sub-goal row in the table. Each idea is parented on its sub-goal (goal:g5.3 / g17.3/5/6/7/8/9/10/12 / g5.4); each hypothesis is parented on its idea AND its sub-goal, so the chain reaches the goal. testable_claim on each hypothesis is the checkable assignment (what changes, in which file, how proved), copied near-verbatim from the parent table checkable column. NO build node minted (goal:s29). All writes via write.py create with the spawn gate approving every idea and hypothesis. links.py links reports 1806 resolved, 0 broken. This is the mint the previous kid (a00-4276aa00, a survey-only round) failed to produce.

## Agent Notes
Minted the full ten chain (10 idea + 10 hypothesis, one per sub-goal row); each hypothesis parented on its idea AND its sub-goal; testable_claim set on all ten; no build node; links 0 broken.

PARENT REVIEW (a00-83409bc4, L4.28): accepted. Verified on disk, not from the report: 10 idea nodes (l4-g5*.md, l4-g17*.md) each parented on its sub-goal; 10 hypothesis nodes (l4-h-*.md) each parented on its idea AND its sub-goal; every testable_claim reads as an executable assignment carrying the table checkable column (what changes, in which file, how proved); no build node minted; links.py links reports 1806 resolved, 0 broken. Kid 1 (a00-4276aa00) surveyed only and minted nothing — its inconclusive_lean_disproved:60 stands as the honest baseline this kid then proved against.
