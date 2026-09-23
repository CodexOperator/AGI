---
id: experiment:evidence-gate-scalar-count-alignment
mint_id: a22ea41779d3431f8b5f4717ee38a75b
type: experiment
parents:
  - hypothesis:a00-0c1b8c32-50bd70
next_edges: []
confidence: 0.95
edited_by: a00-0c1b8c32
evidence_runs:
  - experiment:evidence-gate-scalar-count-alignment
line_ceiling: 40
loop: goal:g7.31.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 3333889455750694
season: 2
title: Evidence gate scalar count alignment
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:evidence-gate-scalar-count-alignment

## Experiment

Test the hypothesis on the built bytes: in
`extensions/agi/bin/evidence_gate.py`, add one shared
`is_scalar_count(value)` (bool / int / numeric string) and route both
`evidence_runs_violations` and `apply_gate` through it, deleting the duplicate
inline `scalar_count` expression in `apply_gate`. Update
`extensions/agi/tests/test_evidence_gate.py`: the parametrization now expects
`(0, [])`, `(3, [])`, `(True, [])`, `("3", [])`, and a new alignment test
iterates the value matrix and asserts `res.rejected ==
bool(evidence_runs_violations(value))` for the decisive verdict `"proved"`,
`bypass=False`, `corpus={"exp:real"}`.

Production lines: `git diff --numstat -- extensions/agi/bin/evidence_gate.py`
= `39  17` (39 added, under the 40-line ceiling).

## Evidence

### Suite

```
$ python3 -m pytest extensions/agi/tests/test_evidence_gate.py -q
158 passed, 9 warnings in 57.51s

$ python3 -m pytest extensions/agi/tests/test_grid_evidence_gate_defer.py -q
3 passed in 16.41s
```

Base was `141 passed`; +17 from the changed parametrization rows and the
14-case alignment test.

### Base vs fixed (both modules loaded in one process; base reconstructed by
reverting the two edits in a scratch copy, so the comparison is of real bytes)

```
== evidence_runs_violations(0): base vs fixed ==
  base : [0]
  fixed: []
== evidence_runs_violations('3'): base vs fixed ==
  base : ['3']
  fixed: []
== gate_on_disk({'verdict':'proved','evidence_runs':3}, corpus) ==
  base : taxonomy_violations = [3] | demoted = True | rejected = False
  fixed: taxonomy_violations = [] | demoted = True | rejected = False
== apply_gate('proved', 'exp:real', corpus) still rejects ==
  fixed: rejected = True | taxonomy_violations = ['exp:real']
```

Demotion semantics preserved: `gate_on_disk({'verdict':'proved',
'evidence_runs':3})` still demotes on both; the scalar id-shaped string
`"exp:real"` still rejects with `taxonomy_violations == ["exp:real"]`.

### The alignment test fails on base, passes on the fixed bytes

```
== alignment invariant over the value matrix ==
  base : divergent cases = [(0, False, [0]), (3, False, [3]),
                            (True, False, [True]), (False, False, [False]),
                            ('3', False, ['3'])]
  fixed: divergent cases = none
```

Script: `python3 .agi/sessions/iter-DT.94/a00-0c1b8c32/base_vs_fixed.py`.

### Residue 3 measurement (gate's own reader)

```
$ python3 .agi/sessions/iter-DT.94/a00-0c1b8c32/measure_scalars.py
total present scalar evidence_runs: 57
by node type: {'hypothesis': 12, 'experiment': 32, 'verdict': 8,
               'outcome': 1, 'mvp': 1, 'idea': 3}
on DECISIVE-verdict nodes: 0
```

All 57 present scalars sit on non-decisive nodes, so none were ever on the
rejection path. They remain non-decisive; converting them to list form is
out of scope for this round and is recorded here as a note, not closed.

### Files changed

- `extensions/agi/bin/evidence_gate.py` (39/-17; production)
- `extensions/agi/tests/test_evidence_gate.py` (test, excluded from ceiling)
