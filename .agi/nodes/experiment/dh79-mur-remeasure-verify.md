---
id: experiment:dh79-mur-remeasure-verify
mint_id: d633205d8b56431aa054981851a18435
type: experiment
parents:
  - hypothesis:a00-9cdba20a-8681ee
next_edges: []
edited_by: a00-9cdba20a
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -c strip-inline-code count on goal/g7.31.2.2.md", "expected": "0 occurrences of the merge-up-hold directive outside inline code", "observed": "0", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "git ls-files extensions/agi/tests/probes/dh54_mur_residue_gate.py", "expected": "the tracked path", "observed": "extensions/agi/tests/probes/dh54_mur_residue_gate.py", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep + JSON-parse the conjunct-3 entries of hypothesis/a00-33653715-0d018f.md", "expected": "no result pass; Evidence/Agent Notes do not claim residues closed", "observed": "refused and refused; Agent Notes says residues 1 and 3 NOT closed", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "wc -c + grep -c probes on experiment/a00-827074fd-dh54-gate.md; evidence_runs of hypothesis/a00-827074fd-a4972c.md", "expected": "non-empty, probes list present, cited", "observed": "3544 bytes; 4 probes; evidence_runs names experiment:a00-827074fd-dh54-gate", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a71cd097a055ad9f
season: 2
title: "DH.79 re-measure: dh-54 MUR residue closure verified at a26e5ccb1 (gate 4/4 + direct greps)"
town: core
---
# experiment:dh79-mur-remeasure-verify

## Experiment

Independent re-measure of the `dh-54` MUR residue closure on
`goal:g7.31.2.2`, run at base tip a26e5ccb1 because the DH.73 MUR review
(`mur-g7-31-2-2-dh-73-a26e5ccb1-lean`) failed the review stage at
`context-build-timeout after 180 s` and never verified anything. The committed
DH.73 gate is re-run for its exit status, but every cause is re-measured by a
direct command of its own so a broken or self-serving gate cannot carry the
claim. Read-only: no production file is imported, executed or changed.

## Evidence

Gate tail, exact, exit 0 (committed script, resolved via `git ls-files`):

```
$ python3 extensions/agi/tests/probes/dh54_mur_residue_gate.py
graph: /data/work/agi/.agi/worktrees/a00-af46eff3/.agi
[PASS] Agent Notes on a00-3c0140ac does not claim 'Closed all three DH.45 residues' -- stale claim absent
[PASS] a00-33653715 probes has no conjunct-3 pass entry; Evidence drops 'probes: list is inert' -- probe demoted; Evidence corrected
[PASS] experiment a00-33653715-dh45-verify Evidence drops 'probes: list is inert' -- stale annotation absent
[PASS] goal:g7.31.2.2 drops 'NO merge-up while residues>0' as a live directive -- stale line absent (only referenced)
ALL PASS: 4/4 checks passed
```

Direct re-measure, one command per cause, not via the gate:

```
$ python3 -c "strip inline-code spans from goal/g7.31.2.2.md, count directive"
  occurrences outside backticks: 0

$ git ls-files extensions/agi/tests/probes/dh54_mur_residue_gate.py
  extensions/agi/tests/probes/dh54_mur_residue_gate.py

$ grep '"conjunct": 3' hypothesis/a00-33653715-0d018f.md   # parsed as JSON
  3 refused ; 3(residue3) refused            # no `pass` entry remains

$ grep '^DH.39 residues:' hypothesis/a00-33653715-0d018f.md
  residue 2 (false zoom-reader claim) closed; residues 1 and 3 NOT closed

$ wc -c experiment/a00-827074fd-dh54-gate.md ; grep -c '^  - {"conjunct"' same
  3544 ; 4

$ sed -n '/^evidence_runs:/,/^[a-z_]*:/p' hypothesis/a00-827074fd-a4972c.md
  - experiment:a00-827074fd-dh54-gate
```

## Result

All four re-measures match the gate: every `dh-54` PRIMARY cause is closed on
the committed bytes at a26e5ccb1. The stale title on
`hypothesis:a00-33653715-0d018f` (asserted the corrective closes the DH.39
residues, while its verdict is `inconclusive_lean_disproved:60`) was corrected
in this round; `testable_claim` was deliberately left untouched.

Production-line measurement (`git diff --numstat -- extensions skills src`):
empty. `production_lines: 0`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This experiment is the DH.79 substitute verification for the DH.73 MUR round, which failed at context-build-timeout and verified nothing. It runs the committed dh54_mur_residue_gate.py for exit status only and re-derives every dh-54 PRIMARY cause by a direct command, so the claim does not rest on the gate it is checking. All four conjuncts pass; production_lines 0.
<!-- THOUGHT:END -->
