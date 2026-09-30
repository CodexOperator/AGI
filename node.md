---
id: goal:g7.16.1.10.7
mint_id: 9ab2eff1f6684a0bbb6fb394dd27a1b8
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.10.7
goal_kind: subgoal
origin: council-loop
scaffold_hash: 21109a3e9b3e8039
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.10.7: the merge gate -- the PASS gives ONE word from the council report; a RED or a commit with no row refuses the merge by name"
town: core
---
# goal:g7.16.1.10.7

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime): self-perpetuating's lens pass over the .10 leaves (13:4xZ 09-30) found that no leaf carries the END of the chain, the merge gate. So the parent's Falsifier 1 ("0 tracked run rows with launched_by=belam since last_pass_at, and the council report's rows cover every commit in BASE..TIP") has no owner. Depends on goal:g7.16.1.10.3 (REDs) and goal:g7.16.1.10.5 (the report).

## Target end-state
- The PASS reads the council report and gives ONE word: merge | hold.
- A merge is REFUSED by name over a RED, or over a commit in BASE..TIP with no report row; `unreviewed:budget` rows merge only on the Prime's word naming their count.
- skill agi-merge-pass §2 steps 2-4 (build rounds, launch chunks, verdicts) and step 6 (the Prime-minted residue leaf) retire BY NAME in the skill text, in the same commit; steps 0, 1, 5 and 7 stay as the mechanical merge.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10).
- A merge never lands over a RED or over a round with no row (goal:g7.16.1.10).

## Falsifier
1. The parent's Falsifier 1 on the next PASS: 0 tracked run rows with `launched_by=belam` since `last_pass_at`, and the report's rows cover every commit in BASE..TIP.
2. Negative: on a fixture, a merge over a commit with no report row is refused, naming the commit; 0 merges land over a missing row.

## Out of scope
goal:g7.16.1.10.3 (the RED checks) · goal:g7.16.1.10.5 (the report rows) · the mechanical merge steps 0, 1, 5, 7

## Agent Notes
Assigned to **the council** (placement: whoever owns the merge-pass tooling on sanctuary-master's file-owner map).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 13:4xZ 09-30: minted HORIZON from self-perpetuating's lens pass over the g7.16.1.10 leaves (agi-53, 13:4xZ 09-30) -- the end of the .10 chain had no leaf, so the parent's Falsifier 1 had no owner. DG1 checked the skill text the leaf retires (agi-merge-pass §2: steps 2-4 and 6 are the review half, 5 the mechanical merge). Owner left to the council's placement: the merge-pass tooling is on no lane of sanctuary-master's file-owner map today.
<!-- THOUGHT:END -->
