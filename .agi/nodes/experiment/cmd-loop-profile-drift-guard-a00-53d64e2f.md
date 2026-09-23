---
id: experiment:cmd-loop-profile-drift-guard-a00-53d64e2f
mint_id: 43d4e2688113fe8a31409a3cbb49a255
type: experiment
parents:
  - hypothesis:a00-53d64e2f-d02c5b
next_edges: []
edited_by: a00-53d64e2f
line_ceiling: 40
production_lines: 9
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
title: "cmd_loop drift guard: behavioural wire probe + guard-omitted sensitivity"
town: core
---
# experiment:cmd-loop-profile-drift-guard-a00-53d64e2f

## Experiment

Spec: `goal:g7.31.5.3` residue — close the `cmd_loop` bypass of the
pre-rotation profile drift guard, and replace the source-string grep with a
behavioural wire probe.

### Built (production bytes)

`extensions/agi/bin/rotate.py`, `cmd_loop`: added, in `cmd_rotate_self`'s
order (branch guard -> profile drift -> any side effect):

```
pguard = _check_profile_drift(root)
if pguard:
    print(pguard, file=sys.stderr)
    return 1
```

placed after `_check_branch_guard` and BEFORE the meter and `spawn_window`.
`root is None` already returns earlier in `cmd_loop`, so
`_check_profile_drift(None) -> None` is preserved.

Measured: `git diff --numstat extensions/agi/bin/rotate.py` = `9  0`.

### Test change

`extensions/agi/tests/test_profile_sync.py`: the source-string grep
(`assert "pguard = _check_profile_drift(root)" in src`) replaced by two
behavioural probes that call `rotate.cmd_loop` with `_check_branch_guard`
stubbed and `spawn_window` replaced by a recording/raising stub:

- `test_rotate_guard_wire_reaches_the_sweep` — drifted graph (artifact
  mutated): `cmd_loop` returns 1, stderr carries `profile drift` and
  `hypothesis:h1`, `spawn_window` is never called.
- `test_loop_rotates_when_the_graph_is_in_sync` — in-sync graph: `cmd_loop`
  reaches the `spawn_window` stub and returns 0.

### Sensitivity (does the probe fail on an unguarded build?)

Scratch probe `.agi/sessions/iter-DH.130/a00-53d64e2f/sensitivity_probe.py`
runs the drifted scenario with `rotate._check_profile_drift` stubbed to
`None` (the exact shape of a `cmd_loop` that omits the guard):

```
rc: 0 spawn_window reached: True
```

So on a build without the guard the scenario reaches the spawn and would fail
the probe's `code == 1` / no-spawn assertions — the probe is behavioural, not
a tautology.

### Suites

- `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` -> 19 passed.
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q -k loop` -> 19 passed.
  (Full `test_rotate.py` exceeds the 1200 s tool timeout; the `loop` selection
  is the set that exercises `cmd_loop`.)

## Decision: `cmd_spawn` stays unwired

Reasoned exception, recorded on the hypothesis node:

- The falsifier is detection before the next seat ROTATION; rotations run
  through `cmd_rotate_self` and `cmd_loop`, both gated. `cmd_spawn` is the
  manual / first-seating launcher, not a rotation.
- `heal.py` crash-recovery respawns via `_rotate.spawn_window` directly, never
  `cmd_spawn`, so gating `cmd_spawn` closes no successor-spawn hole.
- Gating the universal launcher would make the one tool an operator can use to
  bring up a repairing seat while drift is unresolved self-refusing — a
  detectable, repairable condition would become a lockout.
