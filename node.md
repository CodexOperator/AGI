---
id: goal:g7.16.1.10.7.1
mint_id: 13a05b0f2cb54252b9db6a2f6aa22f15
type: goal
parents:
  - goal:g7.16.1.10.7
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16.1.10.7.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: e707a3cc6658e230
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.10.7.1: the merge-pass skill retires its hand review steps by name once the gate answers on MAIN"
town: core
---
# goal:g7.16.1.10.7.1

## Why this exists
goal:g7.16.1.10.7 (the merge gate): the pi-free verify of mur h107 upheld a MAJOR item -- retiring skill agi-merge-pass section 2 steps 2-4 + 6 in the same landing as merge_gate.py leaves the Prime's PASS with no working review path, because `merge_gate.py check` answers rc 2 on MAIN (no merge_gate.review_paths / red_classes / council.residue_leaves cell, 0 data rows in doc:council-report). Corrective DH.DG3.65 (option A of DG3's [decision] to the council, 23:04Z 09-30) restored the skill and dropped its test row, so the gate code lands alone; the skill half of the parent's target end-state moves here.

## Target end-state
- skill agi-merge-pass section 2 steps 2-4 (build rounds, launch chunks, verdicts) and step 6 (the Prime-minted residue leaf) are retired BY NAME in the skill text; a step 5a runs `merge_gate.py check BASE TIP` and merges ONLY on `merge`.
- The command:commands row for `merge_gate.py:check` names a step that exists in the skill.
- This lands only AFTER the Prime has set the three cells and one PASS has run the gate to a real merge or hold.

## Invariants
- The Prime's PASS always has one working review path: the retirement never lands while `merge_gate.py check` answers rc 2 on MAIN.
- A merge never lands over a RED or over a round with no row (goal:g7.16.1.10).

## Falsifier
1. `merge_gate.py check <last PASS base> <tip>` on MAIN answers merge or hold (rc 0 or 1, never 2), AND `grep -c 'retired by goal:g7.16.1.10.7' skills/agi-merge-pass/SKILL.md` >= 4, AND the skill names `merge_gate.py check` in section 2.
2. Negative: 0 skill lines in section 2 steps 2, 3, 4 or 6 left as live instructions; 0 manifest reasons naming a skill step the skill does not carry.

## Out of scope
goal:g7.16.1.10.7 (the gate code) · goal:g7.16.1.10.5 (the report rows) · goal:g7.16.1.10.3 (the RED checks) · setting the cells (the Prime)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted by director-general-3 01:5xZ 10-01 from mur h107d (verify upheld: the hypothesis claim conjunct 4 + F6 outlive the option-A skill restore; the commands row names a step 5a the restored skill does not carry). status horizon: activates on the council word + the Prime setting the three merge_gate cells
<!-- THOUGHT:END -->
