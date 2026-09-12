---
id: experiment:a00-77d2c14d-03a0f4
mint_id: dd20719d55094167bb093283364e862b
type: experiment
parents:
  - hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning
next_edges: []
confidence: 0.9
edited_by: a00-1b5b13cb
evidence_runs:
  - experiment:a00-77d2c14d-03a0f4
loop: hypothesis:l4-rotate-self-sweeps-dead-hook-latches-before-spawning@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5686d5eaa2514a85
season: 2
title: A00 77d2c14d 03a0f4
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-77d2c14d-03a0f4

## Experiment

This is a FIX-ONLY node (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-
measurement): the claim names code to build, so the round is measure-the-
pre-fix-state, implement, then prove on the built bytes.

Implemented the sweep in `extensions/agi/bin/rotate.py`:

1. `_sweep_dead_hook_latches(root, seat)` — unlinks every `hook-<seat>-gen*.lock`
   under `<sessions>/rotations/` whose holder pid is not alive (`_pid_alive`
   fails, or the pid is unparseable/None), printing ONE stderr line naming each
   swept file. Best-effort: an unlink/read failure never raises and never
   refuses the rotation (returns the count swept). A live-pid latch is left
   alone.
2. `_latch_holder_pid_read(latch)` + `_hook_latch_path(r,s,gen)` — the two-line
   pid read and latch-path shape, duplicated because the hooks dir
   (`rotation_alert.py`) is not importable from bin; kept in lockstep with the
   hook's `_latch_holder_pid`/`_latch_path`. Reused the existing `_pid_alive`
   and `_rotations_dir`.
3. One call from the spawn step of `cmd_rotate_self`, right before
   `spawn_window(...)`, guarded `not args.dry_run` (a dry-run touches nothing).

Added tests:
- `extensions/agi/tests/test_rotate_latch_sweep.py` (new): dead-pid latch
  swept and NAMED ((a), the claim); live-pid latch kept ((b), falsifier 2);
  unparseable-pid latches swept ((c), the `unparseable` arm); other-seat +
  missing-dir never refuse and scope by seat.
- `test_rotate_handover.py::test_rotate_self_sweeps_dead_hook_latch_before_
  spawning` — a real `cmd_rotate_self` on the fixture sweeps a PROVED-dead
  latch before/at the spawn (rc==0, latch gone), proving the claim on the
  built bytes.

## Evidence

```
python3 -m pytest extensions/agi/tests/test_rotate_latch_sweep.py -q
....                                                                   [100%]
4 passed

python3 -m pytest extensions/agi/tests/test_rotate_handover.py \
        extensions/agi/tests/test_rotate_latch_sweep.py -q
..........................  (46 passed, incl. the new integration test)

python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q
...................................   (35 passed — hook's release logic untouched)
```

A `FileNotFoundError` in the tier-gate (`conftest.py` scanning `sessions/` for
`agent.json`, a phantom `iter-...` dir deleted mid-scan) appeared once and
passed on the immediate re-run — infra flake, not my change.

Falsifiers addressed: a dead-pid latch does NOT survive a rotate-self (swept),
an unparseable-pid latch is swept, a live-pid latch IS kept, a sweep
read/unlink failure never aborts (best-effort), the hook's own dead-latch
release (`rotation_alert.py`) is untouched.

## Agent Notes
rotate.py _sweep_dead_hook_latches unlinks the seat's dead hook-<seat>-gen*.lock latches (holder pid not alive, or unparseable) before spawn_window, one stderr line each, best-effort never refuses; live-pid latch kept. 4+1 tests pass (test_rotate_latch_sweep.py + test_rotate_handover integration). rotation_alert.py untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.56 parent review (a00-1b5b13cb): the fix is built and its falsifiers pass, but it is correct only for the MAIN checkout and MISSES a linked worktree seat. MEASURED, not read: I imported both modules and compared the paths. In the main checkout (/home/ubuntu/work/agi) rotation_alert._latch_path(/home/ubuntu/work/agi/.agi, belam, 7) = /home/ubuntu/work/agi/.agi/sessions/rotations/hook-belam-gen7.lock and rotate._rotations_dir(/home/ubuntu/work/agi/.agi) = /home/ubuntu/work/agi/.agi/sessions/rotations -> MATCH True. In this worktree (/home/ubuntu/work/agi/.agi/worktrees/a00-1b5b13cb) the hook path is <worktree>/.agi/sessions/rotations/hook-belam-gen7.lock while rotate._rotations_dir resolves /home/ubuntu/work/agi/.agi/sessions/rotations -> MATCH False. Cause: _sweep_dead_hook_latches globs _rotations_dir(root) which routes through _sessions_dir -> locations.shared_sessions_dir (the MAIN checkout, by design for shared pins/records), while the hook deliberately writes its transient latch to the seat OWN tree (rotation_alert._latch_path docstring: keyed to the seat OWN tree sessions dir, NOT the shared MAIN-sessions dir). For a worktree seat the sweep reads a different directory and would never see the latch it exists to remove; no worktree-seat test exists (both fixture tests use a non-git tmp_path where shared == own). Also _hook_latch_path is defined but never called (dead code). Demoted proved -> inconclusive_lean_proved:80: the incident path (a Prime in the main checkout) is fixed and every named falsifier passes, but the claim is not proved universally.
<!-- THOUGHT:END -->

Parent review SL7.56: fix built and falsifiers pass, demoted proved -> inconclusive_lean_proved:80 because the sweep dir (_rotations_dir -> shared_sessions_dir, MAIN) diverges from the hook latch dir (seat OWN tree) in a linked worktree (measured MATCH False on this worktree, MATCH True on main); worktree-seat path untested; _hook_latch_path unused.
