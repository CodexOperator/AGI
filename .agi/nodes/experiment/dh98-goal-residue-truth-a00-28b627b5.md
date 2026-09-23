---
id: experiment:dh98-goal-residue-truth-a00-28b627b5
mint_id: b4e10fada57e4972a927bbcb5c960c90
type: experiment
parents:
  - hypothesis:a00-28b627b5-4aa692
next_edges: []
confidence: 0.9
edited_by: a00-28b627b5
evidence_runs: experiment:dh98-goal-residue-truth-a00-28b627b5
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c 'CLOSED' .agi/nodes/goal/g7.31.4.2.md; grep -c 'NO merge-up while residues>0' .agi/nodes/goal/g7.31.4.2.md", "expected": "CLOSED >= 5 and the stale hold sentence absent (0)", "observed": "8 and 0", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md", "expected": "0 -- the PRIMARY DH.43 residue's stale claim is gone from its locus", "observed": "0", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q; grep -c '^def test_' on the module", "expected": "live re-measure equals the number written on the goal: SEVEN / 7", "observed": "7 passed in 8.33s; grep -c -> 7", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "grep -rn 'is_ssh' extensions/agi/bin extensions/agi/src skills", "expected": "exit nonzero, zero production hits", "observed": "no output, exit=1", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 -c \"import send; send.send_dm('x','y',is_ssh=True)\" with extensions/agi/bin on sys.path", "expected": "TypeError: unexpected keyword argument 'is_ssh' -- no second API exists to call", "observed": "TypeError: send_dm() got an unexpected keyword argument 'is_ssh'", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin extensions/agi/skills src", "expected": "empty -- node files only, 0 production lines", "observed": "empty", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 730084f78594658e
season: 2
testable_claim: The tip goal node marks all five DH.43 residues CLOSED with their DH.51 closer, drops the stale NO-merge-up hold, and its re-measured falsifier state (pytest 7 passed / grep -c ^def test_ -> 7; grep -rn is_ssh exit 1) matches a live run made this round, with 0 production lines.
title: "DH.98 re-measure: goal:g7.31.4.2 residues closed, falsifier green on tip"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:dh98-goal-residue-truth-a00-28b627b5

## Experiment

Residue-closure round DH.98 on `goal:g7.31.4.2`. The goal's own Agent Notes and
THOUGHT were stale: they still rendered the DH.43 residue table with no closure
annotation and closed with `NO merge-up while residues>0`, while DH.51
(`experiment:dh51-residue-closure-a00-e1e6807b`) had already closed all five.
The node therefore told every later reader to re-run DH.51.

Node edits only, through `write.py`; zero production lines. The falsifier on the
goal ("same caller-facing function names/args; no caller branch on `is_ssh`") was
re-measured on this checkout, not inherited.

### Edits

1. `write.py goal:g7.31.4.2 'replace body 35:45 -'` — replaced the DH.43 Agent
   Notes tail with the same historical table kept in place, each row annotated
   **CLOSED** and naming its DH.51 closer, followed by a DH.98 re-measure block.
   The stale `NO merge-up while residues>0` sentence is gone; the text now reads
   that the residues which held merge-up back are gone.
2. `write.py goal:g7.31.4.2 'thought ...'` — whole-replaced the THOUGHT region
   with the DH.98 delta (why this version differs, what was measured, residue
   deliberately left).

### Measurements (this round, this checkout)

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
.......                                                                  [100%]
7 passed in 8.33s
$ grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py
7
$ grep -rn 'is_ssh' extensions/agi/bin extensions/agi/src skills
(no output) exit=1
```

The API-surface door is also shut by construction — calling the second API that
must not exist fails loudly rather than silently:

```
$ python3 -c "... send.send_dm('x','y',is_ssh=True) ..."
TypeError: send_dm() got an unexpected keyword argument 'is_ssh'
```

Body scan of the five send-side functions in `extensions/agi/bin/send.py`
(`send_dm`, `send_room`, `_nudge_target`, `_nudge_window`, `_announce_nudge`)
finds no `is_ssh` in any of them (the module-wide `is_ssh` grep above is the
harder form of the same probe: zero hits anywhere in production).

### Closure state after this round

```
$ grep -c 'CLOSED' .agi/nodes/goal/g7.31.4.2.md
8
$ grep -c 'NO merge-up while residues>0' .agi/nodes/goal/g7.31.4.2.md
0
$ grep -c '6 passed, 0 production lines' .agi/nodes/hypothesis/a00-ac47d671-4fc781.md
0
```

Both conjuncts of the goal's falsifier are green on tip, and the node now says
so with a number measured in this round.

## Evidence

Raw probe transcript: `.agi/sessions/iter-DH.98/a00-28b627b5/probes.txt`
(equals the command tails quoted above; rerun of `pytest` at 8.33s vs DH.51's
3.49s is timing noise on the same 7-test module).

Production lines: 0 — only `.agi/nodes/*.md` changed. Ceiling 40.
