---
id: experiment:loop-rotation-drift-guard-a00-0acaafee
mint_id: 456090488a4045edbdd7810699525938
type: experiment
parents:
  - hypothesis:a00-0acaafee-41b87a
next_edges: []
edited_by: a00-0acaafee
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch .agi graph: linked hypothesis:h1 IN SYNC, artifact profile/h1.md mutated; rotate.cmd_loop(dry_run=True) with cmd_meter mocked to 1 (rotate due) and spawn_window a recorder", "expected": "rc != 0; stderr names hypothesis:h1; spawn_window NOT called", "observed": "rc=1; stderr 'rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)'; spawn_called=False", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "drive rotate.cmd_loop itself (not a grep) on the same drift scratch; the abort is the guard's non-None return before the spawn", "expected": "guard's return is what aborts the loop rotation, before spawn_window", "observed": "rc=1 spawn_called=False; red-verified by deleting the _check_profile_drift(root) call from cmd_loop -> test fails 'assert 0 != 0'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "clean in-sync scratch, cmd_meter mocked to 0 (hold)", "expected": "rc=0; no refusal from the guard; spawn_window NOT called", "observed": "rc=0; stderr 'BELOW director_rotate_at: no rotation, loop holds.'; spawn_called=False", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "clean in-sync scratch, cmd_meter mocked to 1 (rotate due)", "expected": "spawn_window reached; rc=0", "observed": "rc=0; spawn_called=True; name=adv-alive", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "cmd_loop(args, root=None)", "expected": "named ERR, rc=1, unchanged", "observed": "rc=1; stderr 'ERR: loop needs an agi project root.'", "result": "pass"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: 7483ef394e102f4e
season: 2
title: Guard the super-ralph loop rotation path with the profile drift guard
town: core
---
<!-- BODY:BEGIN -->
# experiment:loop-rotation-drift-guard-a00-0acaafee

## Experiment

`goal:g7.31.5.3` falsifier 1: a deliberate graph↔profile desync is detected
by an automated check (exit non-zero) before the next seat rotation. The
check (`profile_sync.check_all`, wrapped by `rotate._check_profile_drift`)
already existed and was proved for `cmd_rotate_self`. The residue: **`cmd_loop`
— the super-ralph rotation primitive — bypassed the guard.** `cmd_loop` called
only `_check_branch_guard`, then metered and spawned; `_check_profile_drift`
had exactly one call site, in `cmd_rotate_self`.

**Fix, `extensions/agi/bin/rotate.py`** (9 production lines): inside
`cmd_loop`, AFTER the meter has decided the loop rotates (so a holding loop
with `cmd_meter -> 0` can never be refused by the guard) and directly BEFORE
`spawn_window`, mirror `cmd_rotate_self` exactly:

```python
    pguard = _check_profile_drift(root)
    if pguard:
        print(pguard, file=sys.stderr)
        return 1
```

`root is None` is already handled at the top of `cmd_loop`, so the guard's own
None handling is a harmless second net.

**Test, `extensions/agi/tests/test_profile_sync.py`**: the old
`test_rotate_guard_wire_reaches_the_sweep` asserted only that the literal
string `pguard = _check_profile_drift(root)` appears in `rotate.py` — a text
match that would pass for a copy-paste into the wrong function and would pass
with the `cmd_loop` call deleted. It is replaced by a behavioural probe,
`test_loop_refuses_on_drift_and_reaches_spawn_when_clean`, which drives
`rotate.cmd_loop` itself on a scratch `.agi` graph (built with the file's own
`_repo` helper, synced with `profile_sync.sync_node`), monkeypatching
`find_project_root`, `cmd_meter`, and `spawn_window` to a recorder.

## Evidence

Scratch probe `probe_loop_guard.py` (session dir), direct `cmd_loop` drive:

```
== CLEAN, meter=1 (rotate due) ==
rotate 'adv_alive' --> successor 'adv-alive'
rc=0 spawn_called=True name=adv-alive stderr=''
== CLEAN, meter=0 (hold) ==
rc=0 spawn_called=False stderr='BELOW director_rotate_at: no rotation, loop holds.\n'
== DRIFT, meter=1 ==
rc=1 spawn_called=False stderr='rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)\n'
```

**Red-verification:** with the four-line guard block temporarily removed from
`cmd_loop`, `pytest ... -k loop_refuses` fails at
`assert code != 0` (`assert 0 != 0`), because the drifted loop reaches
`spawn_window` and returns 0. Restored, it passes.

Repo suite:
`python3 -m pytest extensions/agi/tests/test_profile_sync.py -q` -> **18 passed**.
`python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "loop_uses_spawn or profile"` -> passed;
the loop test `test_loop_uses_spawn_window` (`_proj` root with no `profile_ref`
nodes) still returns 0, so the guard is a no-op on a drift-free graph.

Production lines moved: `git diff --numstat -- extensions/agi/bin/rotate.py`
-> `9  0`. Ceiling 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Build a-g15: the residue was that the guard was wired into only one of two rotation paths. The change is four lines in cmd_loop; the load-bearing half is the test, which must drive the primitive rather than grep the source. Verified red by temporarily removing the call.
<!-- THOUGHT:END -->
