---
id: experiment:dh77-goal-residue-notes-remeasured-a00-c2819250
mint_id: 285f727610ed496dac0b34eb9e6f3fa4
type: experiment
parents:
  - hypothesis:a00-c2819250-ccb585
next_edges: []
edited_by: a00-c2819250
evidence_runs:
  - experiment:dh77-goal-residue-notes-remeasured-a00-c2819250
line_ceiling: 40
loop: goal:g7.31.4.2@s2
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "for s in '<spell1>' '<spell2>' '<spell3>' '<spell4>' '<spell5>' '<spell6>' '<spell7>'; do grep -c -F \"$s\" .agi/nodes/goal/g7.31.4.2.md; done", "expected": "each of the seven retired literal spells reports 0 in the corrected goal node", "observed": "0 0 0 0 0 0 0 (before the write each reported 1 1 1 3 0 0 0)", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -c -F 'engine gap-fill' .agi/nodes/goal/g7.31.4.2.md", "expected": "1 -- the non-vacuity control survives the rewrite, so the zeros are real removals and not an emptied file", "observed": "1", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q ; grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py ; git diff --numstat -- extensions/agi/bin src skills | wc -l", "expected": "7 passed; 7 test defs; 0 numstat lines -- module SEVEN and 0 production lines on this base", "observed": "7 passed in 12.65s; 7; 0", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "grep -rl 'post-dh51-residues-closed' .agi/nodes/ ; grep -rl 'a00-4d9c90ee-40f4e3' .agi/nodes/", "expected": "the DH.67 duplicate nodes are ABSENT on this base, so there is no duplicate to retire and none may be invented", "observed": "both searches empty; also absent from .agi/nodes/deprecated/hypothesis/", "result": "held"}
production_lines: 0
profile: balanced
role: kid
season: 2
testable_claim: On base a42f85abd the goal node goal:g7.31.4.2 can be whole-replaced with the measured post-DH.51 state so that all seven retired stale-residue literal spells grep to 0 while the non-vacuity control 'engine gap-fill' greps to 1, with the module still measured at SEVEN tests and 0 production lines.
title: "DH.77: goal g7.31.4.2 residue notes re-measured at a42f85abd"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh77-goal-residue-notes-remeasured-a00-c2819250

## Experiment

Corrective round on `goal:g7.31.4.2`, residual after MUR `mur-dh71` went lean
FAIL with `context-build-timeout@180s`. The parent's loop branch did not carry
the DH.67/DH.71 commits, so this checkout landed on a base where the goal node
still carried the retired residue prose. No production byte was touched.

**Base.** `a42f85abd` on `season2/loops/goal-g7.31.4.2-a00-4d5053f6`, NOT the
`1837c9ae`/`13afacae7` the brief named. Measured, not assumed: the DH.67
duplicate `post-dh51-residues-closed` is absent from both
`.agi/nodes/hypothesis/` and `.agi/nodes/deprecated/hypothesis/`, and the
DH.67 live `hypothesis:a00-4d9c90ee-40f4e3` /
`experiment:post-dh51-residues-closed` are absent too. There is no duplicate to
retire here; none was invented.

### Before

```
spell1 => 1   spell2 => 1   spell3 => 1   spell4 => 3
spell5 => 0   spell6 => 0   spell7 => 0
engine gap-fill => 1
```

(`spell4` is the stale count form; verified live as three occurrences.)

### The write

Two sanctioned `write.py` submits on the goal node, both through the
replacement verbs (the `note` verb APPENDS and cannot remove the stale block,
which is the shape that produced it):

1. `replace body 32:46 -` with a file holding the corrected Agent Notes,
   ending at the `<!-- THOUGHT:BEGIN` line.
2. `thought <text>` to rewrite the authored THOUGHT region from scratch.

One body writer per submit, so the two did not share a line.

### After

```
spell1 => 0   spell2 => 0   spell3 => 0   spell4 => 0
spell5 => 0   spell6 => 0   spell7 => 0
engine gap-fill => 1
```

The corrected Agent Notes state the measured post-DH.51 position in the node's
own words while quoting none of the retired spells: five residues closed at
their loci, module SEVEN, 0 production lines, no open residue, merge-up no
longer gated by residues. The THOUGHT records why this version differs, the
base divergence, and the deviation from the brief's named base.

## Evidence

- pytest: `7 passed in 12.65s`
- `grep -c '^def test_'`: `7`
- `git diff --numstat` over `extensions/agi/bin src skills`: empty (0 lines)
- seven retired-spell greps: 0 each; control `engine gap-fill`: 1
