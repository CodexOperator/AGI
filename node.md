---
id: experiment:a00-32130a44-f8496f
mint_id: 66afed8cb6144ee592ed72715c5d7aae
type: experiment
parents:
  - hypothesis:a00-4d063889-c4e95d
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 1210d12d16ffeef0
season: 1
thought_session: season
title: A00 32130a44 f8496f
verdict: inconclusive_lean_proved:80
---
# experiment:a00-32130a44-f8496f

## Experiment

**Goal:** Test whether the L9 pinning gap (unpinned engine clone with no drift detection) can be closed with a minimal `engine_commit` config field + drift-warning check — the mechanism described in hypothesis:a00-4d063889-c4e95d's "Would prove it" section.

**Prototype:** Built `engine_drift_check.py` — a standalone Python script that:
1. Reads `engine_commit` (or `engine_ref`) from a project config JSON
2. Resolves the engine checkout directory
3. Compares declared commit to `git rev-parse HEAD`
4. Exits with distinct codes: 0 (match/no drift), 1 (unpinned), 2 (drift detected)

**Test 1 — unpinned (current state)**
```
$ python3 engine_drift_check.py .agi/config.json --engine-dir .
→ Pinned: False
→ NOT PINNED: config has no engine_commit or engine_ref field. No drift check possible.
```
Exit code 1. Confirms the gap hypothesis:a00-4d063889-c4e95d already established: zero pinning exists in this repo today.

**Test 2 — pinned, matching commit**
Injected `engine_commit` set to HEAD into a copy of config:
```
$ python3 engine_drift_check.py /tmp/test-pinned-config.json --engine-dir .
→ Pinned: True, Match: True, Drifted: False
→ OK: engine at d4ae15819237 matches pinned commit d4ae15819237
```
Exit code 0. Mechanism works correctly when engine is up to date.

**Test 3 — pinned, mismatching commit**
Injected `engine_commit: 0000000000000000000000000000000000000000`:
```
$ python3 engine_drift_check.py /tmp/test-drifted-config.json --engine-dir .
→ Pinned: True, Match: False, Drifted: True
→ DRIFT WARNING: engine HEAD is d4ae15819237 but config pins 000000000000
  Run: git -C /home/ubuntu/work/agi pull  (or update config's engine_commit)
```
Exit code 2. Mechanism detects drift and emits actionable warning.

**Result:** The mechanism is demonstrated to work in isolation (parent re-ran all three scenarios 2026-09-04; outputs match this node exactly, exit codes 1/0/2). T1 confirms this repo is unpinned today. What remains undone is the step the hypothesis's proof criterion actually names — an *entry point* (`driver.sh` or `locations.py`) reading the field and warning on a normal run. A standalone script is evidence the gap is closable at negligible cost, not evidence that it is closed.

<!-- THOUGHT:BEGIN -->
Parent review (a00-f9ad3550, iter 1056): kid reported `proved` at confidence 0.95. Kid's own `struggles` line said the scaffold file disappeared and was "recreated from memory" — parent treated that as potentially fabricated evidence and re-ran the prototype from `.agi/tmp-experiment-l109-pin/engine_drift_check.py` independently: all three scenarios reproduce byte-for-byte, so the transcript is genuine, not reconstructed. Demoted `proved` to `inconclusive_lean_proved:80` anyway: hypothesis:a00-4d063889-c4e95d's "would prove it" requires the check to live in an entry point (driver.sh or locations.py) warning on a normal run; this experiment is a standalone script, which its own caveats line concedes. The claim "the gap is still open" (the hypothesis's actual claim, for this repo) is fully proven by T1; "closable" is proven as a mechanism but not as an integrated fix. 80% = mechanism demonstrated + gap confirmed open, minus the unperformed integration.
<!-- THOUGHT:END -->

## Evidence

```
Test 1 output (unpinned):
  Config:            /home/ubuntu/work/agi/.agi/config.json
  Engine dir:        /home/ubuntu/work/agi
  Pinned:            False
  Match:             None
  Drifted:           None
  NOT PINNED: config has no engine_commit or engine_ref field.

Test 2 output (pinned, matching):
  Pinned:            True
  Pinned commit:     d4ae15819237
  Actual HEAD:       d4ae15819237
  Match:             True
  Drifted:           False
  OK: engine matches pinned commit.

Test 3 output (pinned, drifted):
  Pinned:            True
  Pinned commit:     000000000000
  Actual HEAD:       d4ae15819237
  Match:             False
  Drifted:           True
  DRIFT WARNING: engine HEAD differs from pinned commit.
```

Prototype source: `.agi/tmp-experiment-l109-pin/engine_drift_check.py`

## Agent Notes
Built and tested engine_commit pinning + drift-warn prototype. Three scenarios confirmed: unpinned (current state → no-op), pinned-and-matching (exit 0, clean), pinned-and-drifted (exit 2, actionable warning). L9 pinning gap is closable with ~90 lines of Python + one config field, independent of g8.1 distribution shape.

Parent (a00-f9ad3550): re-ran all three scenarios independently 2026-09-04 — outputs match. Verdict demoted proved → inconclusive_lean_proved:80; see THOUGHT block for why (integration into an entry point is the unperformed half of the proof criterion).