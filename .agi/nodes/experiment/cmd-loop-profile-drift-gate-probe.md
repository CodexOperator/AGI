---
id: experiment:cmd-loop-profile-drift-gate-probe
mint_id: 3d6d56f115b34309b4802dd8746ad007
type: experiment
parents:
  - hypothesis:a00-98ec804f-a31ee2
next_edges: []
title: "cmd_loop drift gate: behavioural probe, fails when the guard is removed"
town: core
season: 2
loop: goal:g7.31.5.3@s2
role: kid
edited_by: a00-98ec804f
---
# experiment:cmd-loop-profile-drift-gate-probe

## Experiment

Spec: `goal:g7.31.5.3` residue — the `cmd_loop` rotation primitive seats the
successor seat via `spawn_window`, so it must gate on the drift check before
the spawn, and the gate must be proven by behaviour, not a source-string grep.

### What was built

`extensions/agi/bin/rotate.py`, `cmd_loop`: after the existing
`_check_branch_guard` block and before the meter and `spawn_window`:

```python
pguard = _check_profile_drift(root)
if pguard:
    print(pguard, file=sys.stderr)
    return 1
```

This is the same shape as the `cmd_rotate_self` gate (rotate.py:18224).

`extensions/agi/tests/test_profile_sync.py`:
`test_loop_refuses_drift_before_seating_the_successor` drives the real
`cmd_loop` path on a scratch `.agi` graph whose linked node
(`hypothesis:h1`, `profile_ref: profile/h1.md`) has a mutated artifact.
`spawn_window` is replaced with a spy, so a spawn would be visible. The
probe asserts:

1. `cmd_loop` returns non-zero,
2. stderr carries the drift message naming `hypothesis:h1`,
3. `spawn_window` was NEVER called.

### Non-vacuity check

With the `cmd_loop` pguard block removed and the rest identical, the probe
FAILS: `cmd_loop` returns 0 and the spy sees the spawn
(`rotate 'director' --> successor 'belam-x'`). With the block restored, it
passes. The probe is sensitive to exactly the wire it tests — the old
`assert "pguard = ..." in src` grep at `test_profile_sync.py:236` could not
distinguish the wired call from a call that never runs.

### Test counts (this checkout)

- `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` → `19 passed`
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → `328 passed`

### Production diff

`git diff --numstat` over production paths → `8 0 extensions/agi/bin/rotate.py`
(well under the 40-line ceiling; no test file counted).

## Evidence

The falsifier's second conjunct ("before the next seat rotation") now holds on
the loop path as well as the seat-rotate path: a deliberate desync reaches
neither successor spawn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted as the evidence run for hypothesis:a00-98ec804f-a31ee2 after cli.py's evidence gate correctly refused to honour a `proved` verdict citing the hypothesis itself (evidence_runs=0). The run closes the cmd_loop residue: 8 production lines add the drift gate ahead of the meter/spawn, and the behavioural probe was confirmed non-vacuous by removing the gate and watching it fail (rc 0 + spawn instead of rc 1 + no spawn).
<!-- THOUGHT:END -->
