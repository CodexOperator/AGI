---
id: goal:g7.16.1.10.5
mint_id: ff107d250b0e499a93d7c615b1b32a98
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.10.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 84b88d9c8264ee79
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.5: ONE council report node, one row per round, and residues routed to their owner post -- never a Prime-minted PASS leaf (assigned: director-general-3)"
town: core
---
# goal:g7.16.1.10.5

# goal:g7.16.1.10.5

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet the council report node and residue routing of the Target flow + 'Every residue lands on a named owner, never on the Prime'. Measured by the parent 05:2xZ 09-30: PASS B3's residues went to a Prime-minted leaf (goal:g1.31), as B2's (goal:g1.30) and 12's (goal:g1.28) did. Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-3.

## Target end-state
- Every round is ONE row on ONE council report node (via write.py, committed by exact path, suite-lock aware): round, base..tip, REUSED | REVIEWED | unreviewed:budget (run key), verdict, residues, reds.
- Residues (from verify verdicts[] + missed[], never the review list alone) route to the owner: the hypothesis's assigned post, else the commit-subject post, else director-engine, onto that owner's residue leaf.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- No residue lands on a Prime-minted PASS leaf.

## Falsifier
1. A committed test: a fixture PASS range yields one report row per round, and its residues land on the owning post's leaf; a residue present ONLY in verify's `missed[]` (not in the review list) still lands on its owner's leaf (skill agi-merge-pass §4, the paid-for trap).
2. Negative: a residue whose owner resolves to belam.

## Out of scope
goal:g7.16.1.10.3 (REDs) · goal:g7.16.1.6 (the write form)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 13:4xZ 09-30, from self-perpetuating's lens pass over the g7.16.1.10 leaves (agi-53, 13:4xZ 09-30): the target already routed residues from verify verdicts[] + missed[], but no falsifier checked the missed[] half; Falsifier 1 now requires a residue present only in missed[] to land on its owner's leaf (skill agi-merge-pass §4 trap). Owner unchanged.
<!-- THOUGHT:END -->
