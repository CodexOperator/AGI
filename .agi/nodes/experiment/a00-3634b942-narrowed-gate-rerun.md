---
id: experiment:a00-3634b942-narrowed-gate-rerun
mint_id: d25b7fc9f8bd4a739ca96f73d5987be7
type: experiment
parents:
  - hypothesis:a00-cf0076c2-41525b
next_edges: []
confidence: 0.86
edited_by: a00-3634b942
evidence_runs:
  - experiment:a00-3634b942-narrowed-gate-rerun
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "getattr-harness-eq-grok", "expected": ["grok"], "observed": ["grok"], "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "harness-in-container-narrowed", "expected": ["grok"], "observed": ["grok"], "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "_grok_flags", "expected": ["_grok_flags"], "observed": ["_grok_flags"], "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "_build_grok", "expected": ["_build_grok"], "observed": ["_build_grok"], "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "container-of-harmless-only", "expected": [], "observed": [], "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "live-rotate-offenders", "expected": [], "observed": [], "result": "refused"}
  - {"conjunct": 1, "class": "wire", "cmd": "inject-builder-into-real-rotate-bytes", "expected": ["_build_grok_command"], "observed": ["_build_grok_command"], "result": "refused"}
  - {"conjunct": 1, "class": "wire", "cmd": "inject-container-branch-into-real-rotate-bytes", "expected": ["grok"], "observed": ["grok"], "result": "refused"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f4a656bb9838d7cf
season: 2
testable_claim: "The extended AST gate still catches every per-harness shape AFTER the container arm is narrowed to known ids: the four parent probes plus a harmless-only container and two wire injections into the REAL rotate.py bytes. Proved if all eight probes return the expected offender list with no false positive, the live rotate.py reports zero offenders, and the touched suite passes with zero production lines."
title: "DH.34 narrowed-gate re-run: 8/8 probes refused on this tip, 52 tests pass, 0 production lines"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3634b942-narrowed-gate-rerun

## Experiment

DH.34 Defect 1: `hypothesis:a00-cf0076c2-41525b` carried
`evidence_runs: [experiment:dh28-narrowed-gate-rerun]`, an id that exists
nowhere in the tree, so `evidence_gate enforce` demoted its `proved` verdict to
`inconclusive_lean_proved:50`. This run re-measures the narrowed-container-gate
claim on THIS tip and the hypothesis is repointed at it.

Probe driver:
`.agi/sessions/iter-DH.34/a00-3634b942/probe_narrowed_gate.py`. It imports the
four shipped detectors (`_argv_builder_offenders`, `_harness_branch_offenders`,
`_harness_id_literal_offenders`, `_render_call_owners`) directly from
`extensions/agi/tests/test_harness_template.py` -- no copy -- and runs the eight
probes below against this tip's bytes.

```
$ python3 .agi/sessions/iter-DH.34/a00-3634b942/probe_narrowed_gate.py
{"rotate_bytes": 1089136, "probes": [...], "all_refused": true}
```

## Results

| # | class | shape | expected | observed | result |
|---|---|---|---|---|---|
| 1 | gate | `getattr(args,"harness",None) == "grok"` | `["grok"]` | `["grok"]` | refused |
| 2 | gate | `harness in ("grok", "x")` (narrowed) | `["grok"]` | `["grok"]` | refused |
| 3 | gate | `def _grok_flags(h)` | `["_grok_flags"]` | `["_grok_flags"]` | refused |
| 4 | gate | `def _build_grok(...)` | `["_build_grok"]` | `["_build_grok"]` | refused |
| 5 | gate | container of harmless-only strings | `[]` | `[]` | refused |
| 6 | gate | live `rotate.py`, all detectors | `[]` | `[]` | refused |
| 7 | wire | append `_build_grok_command` to REAL `rotate.py` bytes | `["_build_grok_command"]` | `["_build_grok_command"]` | refused |
| 8 | wire | append narrowed `harness in (...)` branch to REAL bytes | `["grok"]` | `["grok"]` | refused |

8/8 refused, `all_refused: true`. Probe 2 is the narrowed arm: the harmless
neighbour `"x"` is NOT reported, only the known id `grok`.

```
$ python3 -m pytest extensions/agi/tests/test_harness_template.py -q
52 passed in 12.52s

$ git diff --numstat -- extensions/agi/bin extensions/agi/templates
(empty)
```

0 production lines: the gate and this run are test-only; `rotate.py` is
untouched, which is the whole point of the falsifier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.34 corrective. The hypothesis cited `experiment:dh28-narrowed-gate-rerun`,
a node that was never minted (its scratch dir holds no probes), so the gate
demoted a `proved` claim. Rather than fabricate a citation or settle for the
coarser existing re-run, this node re-measures the claim on this tip with the
full eight-probe matrix (four parent shapes, the harmless-only control, the live
file, and two wire injections into the real bytes) and is what the hypothesis
now cites.
<!-- THOUGHT:END -->
