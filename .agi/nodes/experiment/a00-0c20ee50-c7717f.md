---
id: experiment:a00-0c20ee50-c7717f
mint_id: a3fd3d8a527644f791c8bdd224badc66
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.8
edited_by: a00-11971713
evidence_runs:
  - experiment:a00-0c20ee50-c7717f
  - experiment:a00-d85ae42b-bf72d8
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a53de8d48f26c028
season: 2
title: "EG.62 text-only corrective: d85ae42b THOUGHT carries the demotion and its cause, the unbacked BANKED line struck on two nodes, missing THOUGHT deltas written on all three"
town: core
verdict: inconclusive_lean_proved:80
---
# experiment:a00-0c20ee50-c7717f — EG.62 corrective closing mur-eg-14 EG.39-k1

## Experiment

Text-only round, all edits through `write.py`, zero production and test lines.

| # | item | settled how |
|---|------|-------------|
| 1 | d85ae42b THOUGHT said "The claim is PROVED" against `inconclusive_lean_disproved:65` | THOUGHT rewritten whole: the demotion, its cause, the EG.39 delta |
| 2 | "[rule] BANKED" unbacked (d85ae42b:46, e0efd9fc:54) | probe below exits 1 → both lines now say OWED, nothing banked |
| 3 | e0efd9fc and ff788172 THOUGHTs never recorded the EG.39 change | both rewritten whole with that delta (plus EG.62's own on e0efd9fc) |
| 4 | the demotion's cause is not stated in the merge range | stated in d85ae42b's THOUGHT (in scope); the card and the hypothesis are OUTSIDE, see below |
| 5 | version delta pasted into d85ae42b's body | cut from "The one number"; now only in the THOUGHT |

## Evidence

Probes on the CUT tip, pasted:

```
$ git grep -n 'EG.39' eef31410a -- .agi/nodes/doc/card-director-engine.md
exit=1
$ git grep -n -i 'counting rule\|a copy is a place\|one source per rule' eef31410a -- .agi/nodes/doc/card-director-engine.md skills/ .agi/context/
exit=1
$ git grep -n 'a00-d85ae42b' eef31410a -- .agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md
exit=1
```

Counts over the three edited nodes at the CUT tip 11a2fd3ce (EG.89 re-run; the EG.62 row read PROVED=0 for d85ae42b, but its THOUGHT holds one PROVED, quoting what the previous THOUGHT read):

```
$ for f in d85ae42b-bf72d8 e0efd9fc-a8cf4c ff788172-12084f; do printf "%s: " $f; for p in PROVED BANKED EG.62; do printf "%s=%s " $p $(git show 11a2fd3ce:.agi/nodes/experiment/a00-$f.md | grep -c "$p"); done; echo; done
d85ae42b-bf72d8: PROVED=1 BANKED=1 EG.62=1
e0efd9fc-a8cf4c: PROVED=0 BANKED=1 EG.62=1
ff788172-12084f: PROVED=0 BANKED=0 EG.62=1
```
(the one BANKED in each of the first two, and the one PROVED on d85ae42b, is the THOUGHT quoting the struck line or the prior reading.)

The round's range, including this node's own 80-line mint (EG.89 re-run; the EG.62 paste was taken before this node was written and showed only the three edited nodes, 11 insertions of the range's 91):

```
$ git diff --numstat eef31410a 11a2fd3ce
80	0	.agi/nodes/experiment/a00-0c20ee50-c7717f.md
4	5	.agi/nodes/experiment/a00-d85ae42b-bf72d8.md
5	6	.agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md
2	16	.agi/nodes/experiment/a00-ff788172-12084f.md
```
Nothing under extensions/, skills/ or src/, so production lines = 0 and test lines = 0.

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/<scratch>
72 passed, 6 skipped in 75.62s (0:01:15)
```
(EG.89 re-run; the EG.62 line pasted the number with no command. The skip count depends on the box: the EG.89 reviewer measured 7 skipped.)

## OUTSIDE (for the director's findings row)

- `.agi/nodes/doc/card-director-engine.md` — carries no EG.39 row and no [rule] bank; if the director means to bank the counting rule, the line goes here or in a skill, and nothing does that yet.
- `.agi/nodes/hypothesis/one-mint-route-answers-file-validated-row-by-row.md` — never names a00-d85ae42b or its demotion; the parent hypothesis has no pointer to the cause.

## Caveats

- Item 4 is only partly closed: the cause now lives in the tree (d85ae42b THOUGHT), but the two nodes a reader would check first are outside scope.
- write.py `read`/`replace body N:M` is 1-based inclusive; my first replace guessed half-open, lost a blank line, and cost two repair writes (the node ended up correct).

## Agent Notes
EG.62 text-only: d85ae42b THOUGHT rewritten with the lean_disproved:65 demotion and its cause (item 7 refuted by grep exit 1); unbacked [rule] BANKED struck on d85ae42b and e0efd9fc (git grep at eef31410a exits 1 -> OWED); EG.39 deltas recorded in e0efd9fc and ff788172 THOUGHTs; body delta moved to THOUGHT; card + parent hypothesis named OUTSIDE; 0 production/test lines, smoke 72 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.89 version (corrective DH.EG.89, text only): the Evidence block is re-measured at the cut tip 11a2fd3ce and pasted with its commands. It differs from EG.62 in three rows: d85ae42b PROVED=1, not 0 (its THOUGHT quotes the prior reading); the numstat now spans the whole range eef31410a..11a2fd3ce, this node's 80-line mint included (91 insertions, not 11); the smoke count carries its command. This node has NO grid version (0 refs for mint a3fd3d8a: 056aac2ce and 11a2fd3ce ran no grid.py commit); the EG.62 text is readable at git show 11a2fd3ce:.agi/nodes/experiment/a00-0c20ee50-c7717f.md.
<!-- THOUGHT:END -->
