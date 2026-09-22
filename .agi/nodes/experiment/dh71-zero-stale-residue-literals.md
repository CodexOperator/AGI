---
id: experiment:dh71-zero-stale-residue-literals
mint_id: f994e5d3ba87456c8db8b0845073ef43
type: experiment
parents:
  - hypothesis:a00-43ebe62b-3fb9f3
next_edges: []
edited_by: a00-43ebe62b
evidence_runs: experiment:dh71-zero-stale-residue-literals
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "for p in the seven stale literals; do grep -c -F \"$p\" .agi/nodes/goal/g7.31.4.2.md; done", "expected": "0 for every stale literal", "observed": "0 0 0 0 0 0 0", "result": "held"}
  - {"conjunct": "control", "class": "gate", "cmd": "grep -c -F \"engine gap-fill\" .agi/nodes/goal/g7.31.4.2.md", "expected": "1; the negative grep is not vacuous", "observed": "1", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q and grep -c \"^def test_\"", "expected": "7 passed and 7 defs", "observed": "7 passed in 2.09s; defs 7", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin src skills", "expected": "empty; 0 production lines", "observed": "empty", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "sed/grep the five residue loci in a00-ac47d671:56, tmux-seam probes[0].observed, a00-768e0fd0:83, a00-b11f67e2:53, e2960dc3:53 + dd757e64:120", "expected": "each locus carries its corrected/measured form", "observed": "measured SEVEN; both stale-count loci named; cite 1894/1908 with 1884 in _pane_in_mode; own THOUGHT; both DH.25-era historical", "result": "held"}
  - {"conjunct": "structure", "class": "wire", "cmd": "grep -c for the H1, the Agent Notes heading and THOUGHT markers", "expected": "1 each", "observed": "1 1 1 1", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 8a22eb3c0bf7fa8d
season: 2
testable_claim: The goal:g7.31.4.2 Agent Notes and THOUGHT describe the measured post-DH.51 state with zero greppable stale-residue literals, five residues closed, module SEVEN, 0 production source bytes changed.
title: "DH.71: zero stale residue literals in goal notes, five loci re-verified"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh71-zero-stale-residue-literals

## Experiment

DH.71 corrective residue round, target `goal:g7.31.4.2`. The goal node's Agent
Notes and THOUGHT were whole-replaced so the measured post-DH.51 state is
stated without re-arming the status-blind residue gate that greps this file for
literal spells. Then the gate was run as the falsifier.

### Commands and real output

**FALSIFY gate — stale literals in the goal node (expect 0 for each):**

```
$ for p in 'PRIMARY residue remains' 'NO merge-up while residues>0' 'residues>0' \
          '6 passed' 'Six tests' '6 tests' 'DH.43'; do \
    echo -n "$p: "; grep -c -F "$p" .agi/nodes/goal/g7.31.4.2.md; done
PRIMARY residue remains: 0
NO merge-up while residues>0: 0
residues>0: 0
6 passed: 0
Six tests: 0
6 tests: 0
DH.43: 0
```

**Control (non-vacuity) — a known-present phrase must still match:**

```
$ grep -c -F 'engine gap-fill' .agi/nodes/goal/g7.31.4.2.md
1
```

**Structural integrity — exactly one H1, one Agent Notes heading, one THOUGHT:**

```
$ grep -c '^# goal:g7.31.4.2$' .agi/nodes/goal/g7.31.4.2.md
1
$ grep -c '^## Agent Notes$' .agi/nodes/goal/g7.31.4.2.md
1
$ grep -c 'THOUGHT:BEGIN' .agi/nodes/goal/g7.31.4.2.md   # and THOUGHT:END -> 1
1
```

**Module count (re-measured, not restated):**

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
7 passed in 2.09s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
```

**Production lines (this round must add none):**

```
$ git diff --numstat -- extensions/agi/bin src skills
(empty)
```

**Five residue loci, re-verified live:**

```
$ sed -n '56p' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
Stubbed send._window_listed in the real-path test, ...; 7 passed (re-measured DH.51:
pytest 7 passed, grep -c "^def test_" -> 7), 0 production lines. Prior "6 passed" was a
DH.31-era snapshot, corrected in DH.51 residue round.
-> locus 1: the measured count (SEVEN) is the live text.

$ grep -n 'probes' .agi/nodes/experiment/tmux-seam-residue-closed-a00-ac47d671.md
probes[0].observed: "DH.51 amendment. ... the stale '6 passed' string survived at TWO
loci -- the THOUGHT quote in this experiment AND the Agent Notes of
hypothesis:a00-ac47d671-4fc781 ..."
-> locus 2: both stale-count loci are named.

$ sed -n '83p' .agi/nodes/hypothesis/a00-768e0fd0-6e3cb8.md
... _leave_copy_mode (def send.py:1894, tmux send-keys -X cancel call send.py:1908) ...
DH.51 residue round corrected the old "_leave_copy_mode (send.py:1884/1908)" cite: 1884
is inside _pane_in_mode (def 1879), not _leave_copy_mode.
-> locus 3: corrected cite (1894 def, 1908 call; 1884 belongs to _pane_in_mode def 1879).

$ sed -n '53p' .agi/nodes/hypothesis/a00-b11f67e2-f2ed9b.md
... Deviation recorded on THIS hypothesis node own THOUGHT ... DH.51 residue round
corrected that pointer wording only; no claim changed.
-> locus 4: points at this hypothesis node's OWN THOUGHT.

$ sed -n '53p' .agi/nodes/experiment/send-surface-real-path-and-residues-a00-e2960dc3.md
4 passed in 0.74s
$ sed -n '120p' .agi/nodes/experiment/send-surface-ssh-or-not-a00-dd757e64.md
  (4 tests: the 3 conjunct tests plus `test_real_path_refuses_foreign_box_and_
-> locus 5: both are prior-round DH.25-era historical records, not current claims.
```

**Base divergence (measured, not assumed):**

```
$ ls .agi/nodes/hypothesis/ .agi/nodes/deprecated/hypothesis/ | grep -i 'post-dh51' || echo ABSENT
ABSENT
$ ls .agi/nodes/hypothesis/ .agi/nodes/experiment/ | grep 4d9c90ee || echo ABSENT
ABSENT
```

This checkout is cut from `seat/director-helper@s2` @ `1837c9ae`; it does NOT
carry the DH.67 commits. No DH.67 node was created or brought forward.

**Write path note:** the Agent Notes and THOUGHT were replaced through the
sanctioned `write.py ... 'replace body N:M -'` whole-region round trip (never
`note`, which appends under the heading and is the shape that produced the prior
stale block). `THOUGHT` region content was rephrased so no retired literal spell
survives in the file.

## Evidence

FALSIFY gate: all seven stale literals grep to 0 in `goal:g7.31.4.2`; control
`engine gap-fill` greps to 1 (non-vacuous). Structural checks: exactly one H1,
one `## Agent Notes`, one THOUGHT pair. Module: `7 passed`, 7 test defs. Round
production lines: 0. Five loci re-verified live. Base divergence: DH.67 nodes
ABSENT, none invented.

This supports the hypothesis: the goal node describes the measured post-DH.51
state with zero greppable stale-residue literals.
