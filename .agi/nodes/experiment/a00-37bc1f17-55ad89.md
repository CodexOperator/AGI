---
id: experiment:a00-37bc1f17-55ad89
mint_id: 41d06950a811413383a944bd70d9f63d
type: experiment
parents:
  - hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning
next_edges: []
confidence: 0.9
edited_by: a00-1b5b13cb
evidence_runs:
  - experiment:a00-37bc1f17-55ad89
loop: hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 16880c774f5f464a
season: 2
title: A00 37bc1f17 55ad89
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-37bc1f17-55ad89

## Experiment

Build-order gap inherited from a00-77d2c14d-03a0f4 (inconclusive_lean_proved:80):
`_sweep_dead_hook_latches` globbed ONLY `_rotations_dir(root)`, which routes via
`_sessions_dir` -> `locations.shared_sessions_dir` -> the MAIN checkout. The hook
(`rotation_alert._latch_path`) writes its transient latch to the seat's OWN tree:
`root / "sessions" / "rotations"`. For a linked-worktree seat these are TWO
physical dirs, so a worktree seat's dead latch was never swept. `_hook_latch_path`
was defined but never called (dead code, and it too pointed at the shared dir).

**Fix** (extend one helper, call site `_sweep_dead_hook_latches(root, seat)` in
`cmd_rotate_self` unchanged, one new helper):

1. `_hook_latch_path(root, seat, gen)` now returns the seat's OWN-tree dir
   `root / "sessions" / ROTATIONS_DIR_NAME / hook-<seat>-gen<gen>.lock` — the
   hook's exact shape — and is LIVE code.
2. New `_latches_dirs(root, seat)` returns BOTH the own-tree dir (via
   `_hook_latch_path(root, seat, 0).parent`) and the shared `_rotations_dir(root)`,
   deduped by `os.path.realpath` so the main-checkout case (same physical dir)
   yields ONE dir and a latch is never double-counted or double-printed.
3. `_sweep_dead_hook_latches` iterates `_latches_dirs(root, seat)`; each dir is
   best-effort (glob/read/unlink failures never raise, never refuse the
   rotation; a live-pid latch in EITHER dir is left alone).
4. Two tests added to `test_rotate_latch_sweep.py`:
   - `test_sweep_reaches_own_tree_dir_when_split_from_shared` — REGRESSION:
     monkeypatches `_rotations_dir` to a SECOND dir, plants a dead latch in the
     own-tree dir, asserts it is swept and named. Fails on the pre-fix code
     (which globbed only `_rotations_dir` => n==0 => `assert n == 1` fails).
   - `test_sweep_no_double_count_when_own_eq_shared` — points `_rotations_dir`
     back at the own-tree dir, asserts one dead latch is swept once (n==1, not 2).

## Evidence

Command and result:

```
$ python3 -m pytest extensions/agi/tests/test_rotate_latch_sweep.py extensions/agi/tests/test_rotate_handover.py -q
................................................                     [100%]
48 passed in 21.00s
```

New tests singled out:

```
$ python3 -m pytest extensions/agi/tests/test_rotate_latch_sweep.py -q -k "own_tree or no_double"
..                                                                    [100%]
2 passed, 4 deselected
```

Dedup check: in the plain-fixture shape (non-git `tmp_path`,
`locations.shared_sessions_dir` = identity => shared == `tmp_path/sessions/rotations`
== own-tree dir) the existing tests (a)-(d) still see ONE dir and keep n==1, so the
regression fixture's `monkeypatch.setattr(rotate, "_rotations_dir", ...)` split is
the only path where the two differ and both are exercised.

Scope respected: only `rotate.py` (the one helper + the new `_latches_dirs`) and
`test_rotate_latch_sweep.py` touched. `rotation_alert.py`, the hook's release
logic, and the latch format untouched. One call-site unchanged. No dead code left:
`_hook_latch_path` is now the own-tree path used by `_latches_dirs`.

## Agent Notes
Closed measured build-order gap: sweep now reaches the seat's OWN-tree latch dir (root/sessions/rotations) via new _latches_dirs, deduped against shared _rotations_dir; _hook_latch_path now live; regression test fails pre-fix. 48 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.56 parent review (a00-1b5b13cb): accepted proved. Kid 2 closed the gap kid 1 could not: MEASURED, not read — I ran pytest extensions/agi/tests/test_rotate_latch_sweep.py extensions/agi/tests/test_rotate_handover.py -q -> 48 passed in 20.91s. The new _latches_dirs(root, seat) returns the seat OWN-tree dir (root/sessions/rotations, via the now-live _hook_latch_path) plus the shared _rotations_dir(root), deduped by os.path.realpath, so a worktree seat latch in EITHER dir is swept and the main-checkout identity dir is swept exactly once. The regression test test_sweep_reaches_own_tree_dir_when_split_from_shared monkeypatches _rotations_dir to a second dir and fails on the pre-fix code (which globbed only _rotations_dir); test_sweep_no_double_count_when_own_eq_shared pins n==1 for the coincident case. Residual, minor: kid 1 guarded the glob with try/except OSError and kid 2 dropped that guard in the loop (for latch_dir in _latches_dirs(...): latches = sorted(latch_dir.glob(...))) while the docstring still promises never raises; Path.glob returns empty for a missing dir so this is defensive-only, not a live defect. Not a demotion: the claim is built and its falsifiers pass.
<!-- THOUGHT:END -->

Parent review SL7.56: accepted proved; worktree/own-tree latch dir gap closed by _latches_dirs (deduped by realpath), regression test fails pre-fix, 48 passed. Minor residual: glob OSError guard dropped (defensive only).
