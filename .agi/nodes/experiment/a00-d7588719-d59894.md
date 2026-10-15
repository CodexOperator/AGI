---
id: experiment:a00-d7588719-d59894
mint_id: d346c03ec3bb4d8a85170c525bd63596
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.9
edited_by: a00-baa8e365
evidence_runs:
  - experiment:a00-d7588719-d59894
line_ceiling: 40
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P7 re-run: grep rotate.py for a call site of _run_alarms_unit outside its def", "expected": "the systemd-run launcher the claim names is reachable from a live production path", "observed": "call site at rotate.py:7225 inside cmd_alarms behind `if getattr(args, \"detach\", False)`. HELD", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe: cmd_alarms(detach=True, holder=advisor) with subprocess.run recorded", "expected": "exactly one systemd-run --user --working-directory <root> ... rotate.py alarms --holder advisor --root <root> (inner without --detach), no dm, the runner returncode returned", "observed": "rc=7, one call, --user/--working-directory/--root present and root-resolved, inner argv has no --detach, no comms dm, no meter loop. HELD", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe P5/P6 re-run on this HEAD: idle-below-low-line and wrong-holder must stay silent", "expected": "no dm in both", "observed": "no dm in both; the idle logic is untouched by this corrective. HELD", "result": "held"}
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 2f29c706653dc989
season: 2
title: "SUPERSEDED: the detached alarms unit (--detach / _run_alarms_unit) was deleted in 20e848493; grep finds neither in rotate.py"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
SUPERSEDED (EF.23, hypothesis:mur-0921-engine-residues-dispositioned-and-corrected): the bytes this node proved -- _run_alarms_unit and alarms --detach -- were deleted in 20e848493; grep finds neither in extensions/agi/bin/rotate.py. The node is kept as prior art.
# experiment:a00-d7588719-d59894

## Experiment

CORRECTIVE round for `hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself` conjunct 4. Kid B built the idle-alarm half (conjunct 3) correctly; its detached-unit half was falsified by the parent's wire probe P7 — `_run_alarms_unit` (rotate.py:7189) had NO production call site, so the suite was green over dead code.

### Pre-fix state (measured)

```
$ grep -n "_run_alarms_unit(" extensions/agi/bin/rotate.py
def _run_alarms_unit(root: Path, holder: str,      # 7189 — definition only
```

One hit, the `def`. No caller. The `alarms` argparse block (20858-20878) had no `--detach`.

### Fix (rotate.py, 8 production lines added)

- `alarms --holder H --detach` → `cmd_alarms` resolves the root, then calls `_run_alarms_unit(root, holder)` exactly once and returns that returncode. It builds nothing, loads no ladder, enters no meter loop, sends no dm.
- `--detach` added to the `alarms` argparse block. The detached unit runs the inner command WITHOUT `--detach` (so it meters on `--interval`; no recursion).
- Every path comes from the RESOLVED root (`Path(getattr(args, "root", None) or root)`), never hard-coded.
- Without `--detach`, behaviour is unchanged (including `--once`).

### Red-first

New regression test `test_alarms_detach_launches_unit_once_and_never_meters` was run against the pre-fix bytes: with the detach branch removed, `cmd_alarms` falls through into the meter loop (`while True: time.sleep(300)`) and the test hangs → fail. Restored the fix, then:

```
$ python3 -m pytest extensions/agi/tests/test_rotate_alarms_idle.py -q
5 passed in 0.17s
```

### Wire probe (P7 re-run, green)

```
$ grep -n "_run_alarms_unit(" extensions/agi/bin/rotate.py
7189:def _run_alarms_unit(root: Path, holder: str,
7225:        return _run_alarms_unit(root, holder)
```

The call site is outside the `def` — the launcher is now live.

### Full run (changed test files)

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_alarms_idle.py \
    extensions/agi/tests/test_rotate_handoff_driven.py -q
345 passed, 363 warnings in 59.64s
```

### Production lines

`git diff --numstat -- extensions/agi/bin/rotate.py` → `8  0` (ceiling 40).

## Evidence

- `grep -n "_run_alarms_unit("` before fix: definition at 7189 only; after: call at 7225.
- `pytest extensions/agi/tests/test_rotate_alarms_idle.py -q` → 5 passed.
- `pytest test_rotate.py test_rotate_alarms_idle.py test_rotate_handoff_driven.py -q` → 345 passed.
- New test records the argv via monkeypatched `subprocess.run`: `systemd-run --user ... --working-directory <R> <python> <rotate.py> alarms --holder H --root R`, no `--detach` in the inner argv, no dm directory created, returncode 7 propagated.

## Agent Notes
Wired the detached alarms unit (P7): alarms --holder H --detach calls _run_alarms_unit once and returns its returncode, no loop/no dm; inner unit argv runs without --detach. Wire probe now shows a call site at rotate.py:7225 outside the def. New red-first test + 345 passed; 8 production lines vs ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrected in place under C item of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-baa8e365).
C item `exp a00-d7588719 :24/:26`. The title said `Detached alarms unit is wired: --detach launches the meter, no dead code` and the node carries `proved`. Re-checked against the bytes: `_run_alarms_unit` and the `--detach` flag were deleted in 20e848493, and `grep -n '_run_alarms_unit\|--detach' extensions/agi/bin/rotate.py` returns 0 hits -- the recorded proof survives only as prior art. The node is now marked SUPERSEDED in its title and body (see the banner under the H1). No verdict, lean or confidence field was changed.
<!-- THOUGHT:END -->
