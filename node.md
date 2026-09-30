---
id: goal:g1.31.3.1.1
mint_id: 6d3639a4489c4b2dae9ea0aff75261e3
type: goal
parents:
  - goal:g1.31.3.1
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.3.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2830cb2b336550cc
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
  - node-answer
  - verdict
title: "G1.31.3.1.1: four node verdicts agree with the bytes and their own record (a00-4d063889 · a00-76bbb729 · a00-6b761b8c · a00-73aeae86)"
town: core
---
# goal:g1.31.3.1.1

## Why this exists
goal:g1.31.3.1: PASS B3 verify stages upheld 4 verdicts (#31 moved to goal:g1.31.4.2.1, DG5, by the council's LANES) the bytes contradict, all inherited (none introduced by the merge), all severity residue, 0 already fixed at HEAD ff09c6101:
```
#   round                                         verify file (.agi/sessions/workflows/runs/)
1   a00-4d063889-c4e95d                           mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json
6   l3w4-branch-shared-state                      mur-pb3chunk11of20/verify_l3w4-branch-shared-state.json
13  l4-test-zoom-unresolvable-tier-id-...-ful     mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json
46  harness-bin-paths-resolve-per-box             mur-pb3retry5/verify_harness-bin-paths-resolve-per-box.json
```

## Target end-state
- #1 `.agi/nodes/hypothesis/a00-4d063889-c4e95d.md`: the claim at :20-29 ("no `engine_commit` field", "`driver.sh` has no drift check") no longer stands against `.agi/config.json:27` + `extensions/agi/driver.sh:138-178`; verdict :14 (`inconclusive_lean_proved:70`) is `disproved`/`inconclusive_lean_disproved`, or the claim is rewritten to the gap still open (the pin is not an object in this repo — goal:g1.31 #2, config lane) with a non-inverted "Would prove it" (:31-35).
- #6 `.agi/nodes/experiment/a00-76bbb729-a84e2a.md`: no template placeholder (:26, :30), no unclosed `<Built it` (:33) or `<EVIDENCE.` after THOUGHT:END (:39); either the Experiment/Evidence sections carry the red-first run it describes and :19 `verdict: pending` holds a real verdict, or the node is retired to `.agi/nodes/deprecated/experiment/` (the round's evidence is experiment:a00-aa46b4f0-f47324).
- #13 `.agi/nodes/experiment/a00-6b761b8c-b6ae8b.md`: `verdict: proved` (:21) rests on a green bare `python3 -m pytest extensions/agi/tests/ -q` pasted on the node at a named commit (today :222 is the kid's `2 failed, 4996 passed`, :247 admits no re-run), or the verdict is demoted to an `inconclusive_lean_*` scoped to the gate probes (:239-241).
- #46 `.agi/nodes/experiment/a00-73aeae86-75e0f3.md`: frontmatter :26 `verdict: proved` is `inconclusive_lean_proved:90`, as its THOUGHT :126 records (siblings a00-20d23796-5c4ad4.md:29 and a00-3f33e0f6-7cc94c.md:27 were written back).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Frontmatter `verdict:` is the one the engine reads (evidence_gate.py); a THOUGHT never holds a verdict the frontmatter contradicts.
- Retire, never delete: #6 moves to `deprecated/`, never `git rm`.

## Falsifier
1. From /data/work/agi:
```bash
bash -c 'H=.agi/nodes; E=$H/experiment; P=$H/hypothesis/a00-4d063889-c4e95d.md; Z=$E/a00-6b761b8c-b6ae8b.md
{ ! grep -q "has no drift check" $P || grep -Eq "^verdict: (inconclusive_lean_)?disproved" $P; } &&
{ f=$(find $H -name a00-76bbb729-a84e2a.md); case $f in */deprecated/*) true;; *) ! grep -Eq "^(What did you do\?|Raw output, screenshots, logs\.|<Built it|<EVIDENCE)" $f;; esac; } &&
{ grep -Eq "^verdict: inconclusive" $Z || grep -E "^[0-9]{4,} passed" $Z | grep -vqE "failed|error"; } &&
grep -qx "verdict: inconclusive_lean_proved:90" $E/a00-73aeae86-75e0f3.md'
```
   (exits 1 at HEAD ff09c6101 on all 4 conjuncts.)
2. Negative: `git grep -n '^verdict: proved' -- .agi/nodes/experiment/a00-73aeae86-75e0f3.md` and `git grep -n 'What did you do? What happened?' -- .agi/nodes/experiment/a00-76bbb729-a84e2a.md` return zero hits.

## Out of scope
goal:g1.31.3.1.2 (evidence pointers) · goal:g1.31.3.2 (scrub damage + leaked literals) · the code halves of the same rounds: #2 #3 engine_commit pin/drift test, #14 leak whitelist, #31 #32 copilot hook registration + post-spawn message (goal:g1.31.4.2.1) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
