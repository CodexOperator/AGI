---
id: experiment:gate-claim-remeasured-on-dh28-tip
mint_id: 02248f86889f4faaa78baf6cf4c2b05a
type: experiment
parents:
  - hypothesis:a00-bc25f6f9-5c369a
next_edges: []
edited_by: a00-3634b942
evidence_runs:
  - experiment:gate-claim-remeasured-on-dh28-tip
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "getattr-harness-eq-grok", "expected": ["grok"], "observed": ["grok"], "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "harness-in-tuple-grok-x", "expected": ["grok"], "observed": ["grok"], "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "harness-in-tuple-harmless-only-control", "expected": [], "observed": [], "result": "refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "_grok_flags", "expected": ["_grok_flags"], "observed": ["_grok_flags"], "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "_build_grok", "expected": ["_build_grok"], "observed": ["_build_grok"], "result": "refused"}
  - {"conjunct": 5, "class": "gate", "cmd": "live-rotate-offenders", "expected": [], "observed": [], "result": "refused"}
  - {"conjunct": 6, "class": "wire", "cmd": "inject-_build_grok_command-into-real-rotate-bytes", "expected": ["_build_grok_command"], "observed": ["_build_grok_command"], "result": "refused"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d739a4d187729d40
season: 2
title: "Proved the rotate.py gate on the DH.28 tip: 7/7 probes refuse, 0 production lines"
town: core
---
<!-- BODY:BEGIN -->
# experiment:gate-claim-remeasured-on-dh28-tip

## Experiment

**DH.28 residue 1.** Re-ran the `goal:g7.31.2.3` gate claim end-to-end on
this tip, so the parent `hypothesis:a00-b75045a2-236d62` can cite a real
run instead of the DH.19-demoted `hypothesis:a00-bc652841-541f5f`.

Probe driver: `sessions/iter-DH.28/a00-bc25f6f9/probe_gate.py`. It imports
the four detectors from `extensions/agi/tests/test_harness_template.py`,
loads the live `extensions/agi/bin/rotate.py` (1,089,136 bytes) and runs:

| # | class | probe | expected | observed | result |
|---|---|---|---|---|---|
| 1 | gate | `getattr(args, "harness", None) == "grok"` | `['grok']` | `['grok']` | refused |
| 2 | gate | `harness in ("grok", "x")` | `['grok']` | `['grok']` | refused |
| 2b | gate | control: container of harmless-only strings | `[]` | `[]` | refused |
| 3 | gate | `def _grok_flags(h)` (no argv suffix) | `['_grok_flags']` | `['_grok_flags']` | refused |
| 4 | gate | `def _build_grok(...)` (no suffix) | `['_build_grok']` | `['_build_grok']` | refused |
| 5 | gate | live `rotate.py`, all four detectors | `[]` | `[]` | refused |
| 6 | **wire** | `_build_grok_command` appended to the REAL `rotate.py` bytes | `['_build_grok_command']` | `['_build_grok_command']` | refused |

Conjunct 6 is the wire test: the synthetic builder is written onto the end
of the production file's own bytes and the gate names it, so the gate is
non-vacuous on the artifact it guards rather than on a fixture alone.

## Evidence

```
$ python3 .../probe_gate.py
{"probes": [...], "verdict": "refused"}   # all 7 refused
live rotate.py length: 1089136 bytes; wired length: 1089204 bytes

$ python3 -m pytest extensions/agi/tests/test_harness_template.py -q
52 passed in 2.95s

$ git diff --numstat -- extensions/agi/bin/
(empty)
```

0 production lines. `rotate.py` untouched; the gate is test-only, which is
the falsifier's whole point.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.34 hygiene: corrected the live rotate.py byte count from the stale 1,087,444 to the measured 1,089,136, and the paired wired length from 1087512 to 1089204 (same 68-byte injection, live+68). No probe, verdict or claim change.
<!-- THOUGHT:END -->
