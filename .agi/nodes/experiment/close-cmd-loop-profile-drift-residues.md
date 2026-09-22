---
id: experiment:close-cmd-loop-profile-drift-residues
mint_id: d6d397d354014dc7875d4228e1ba2a5a
type: experiment
parents:
  - hypothesis:a00-5ffe6174-59e3aa
next_edges: []
edited_by: a00-b2baa9b3
evidence_runs: experiment:close-cmd-loop-profile-drift-residues
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest test_profile_sync.py -k cmd_loop_refuses (real _check_profile_drift on a drifted repo; spawn_window patched to raise)", "expected": "cmd_loop returns 1, prints the drift refusal on stderr, and never reaches spawn_window", "observed": "test passes: rc=1, stderr names hypothesis:h1 and profile drift, spawn_window never fired", "result": "holds"}
  - {"conjunct": 2, "class": "wire", "cmd": "pytest test_profile_sync.py -k cmd_loop_proceeds (real guard on a synced repo; spawn_window recorded)", "expected": "the guard is invoked with the root and does not block: rc=0 and spawn_window reached", "observed": "test passes: guard called once with repo/.agi, spawn reached, rc=0", "result": "holds"}
  - {"conjunct": 3, "class": "wire", "cmd": "pytest test_profile_sync.py -k rotate_self_refuses (drifted repo; _geometry_resolution_root patched to raise)", "expected": "cmd_rotate_self returns 1 on drift before the geometry resolution side effect", "observed": "test passes: rc=1, drift named, _geometry_resolution_root never reached", "result": "holds"}
  - {"conjunct": 4, "class": "gate", "cmd": "pytest test_profile_sync.py -k body_only_profile_ref (malformed frontmatter + profile_ref: in body prose)", "expected": "the body-only mention does not mark the file linked: sweep stays green", "observed": "test passes: 1 linked, 0 not ok; body.md absent from the sweep output", "result": "holds"}
  - {"conjunct": 5, "class": "auth", "cmd": "pytest test_profile_sync.py -k permission_denied (Path.read_text raises PermissionError for one node file)", "expected": "check_all never raises; the unreadable file is named with status unreadable", "observed": "test passes: row status unreadable, no exception out of check_all", "result": "holds"}
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 3663e51847a265ca
season: 2
title: Close cmd_loop drift-guard wire + three profile_sync cleanups
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:close-cmd-loop-profile-drift-residues

## Experiment

Corrective round DH.64 on `goal:g7.31.5.3`. Residues 1, 2 and 4 from the
prior MUR round, closed on the current bytes. Scope files only:
`extensions/agi/bin/rotate.py`, `extensions/agi/bin/profile_sync.py`,
`extensions/agi/tests/test_profile_sync.py`.

### Residue 1 (PRIMARY) — `cmd_loop` bypassed the drift guard

`cmd_loop` ran `_check_branch_guard` and then spawned, with no
`_check_profile_drift` call, while `cmd_rotate_self` gated on it. Added the
same call in the SAME pattern, after the branch guard, BEFORE the meter and
any spawn:

```python
    pguard = _check_profile_drift(root)
    if pguard:
        print(pguard, file=sys.stderr)
        return 1
```

### Residue 2 (PRIMARY) — the wire test was a source-string grep

Deleted `test_rotate_guard_wire_reaches_the_sweep` (it asserted
`"pguard = _check_profile_drift(root)" in src`). Replaced with three
behavioural probes that drive the commands in-process and fail if the guard
is dropped or moved into a dead branch:

- `test_cmd_loop_refuses_on_drift_and_never_reaches_the_spawn` — real guard on
  a drifted repo, `spawn_window` monkeypatched to raise; asserts rc 1 and the
  refusal on stderr.
- `test_cmd_loop_proceeds_on_a_clean_repo` — real guard on a synced repo; spies
  it was invoked with the root, asserts the spawn WAS reached and rc 0.
- `test_cmd_rotate_self_refuses_on_drift_before_the_geometry_guard` — the
  other successor primitive; `_geometry_resolution_root` patched to raise.

No source grepping remains.

### Residue 4 (NOTE)

1. `cmd_spawn` keeps no drift gate, DOCUMENTED in a comment: it is the raw
   window-spawn primitive (helpers, dry-run name previews), and the gate is a
   property of the two successor-spawning primitives, which hold it before
   calling in. `--dry-run` spawns stay pure previews.
2. `profile_sync.py` unreadable heuristic tightened with `_frontmatter_text`:
   only the block between the leading `---` fences is searched, so prose in a
   malformed file's BODY naming `profile_ref:` no longer marks it linked.
   `_raw_profile_ref` now reads that same frontmatter text.
3. The `f.read_text(...)` inside the `except` branch is wrapped in
   `except OSError`; an unreadable file becomes an `unreadable` row (named by
   path) instead of a traceback out of `check_all`.

## Evidence

Full focused suite:

```
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py -q
......................                                                   [100%]
22 passed in 3.33s
```

Rotate slice that covers `cmd_loop`:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "loop"
...................                                                      [100%]
19 passed, 309 deselected in 8.93s
```

Production budget (read-only `git diff --numstat`, the one allowed git read):

```
$ git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/bin/profile_sync.py
28	3	extensions/agi/bin/profile_sync.py
11	0	extensions/agi/bin/rotate.py
```

= 39 production lines added, ceiling 40, no re-brief.

The four required probes map to tests: (a) refuses-on-drift,
(b) proceeds-clean, (c) body-only mention not unreadable,
(d) permission-denied never raises.
