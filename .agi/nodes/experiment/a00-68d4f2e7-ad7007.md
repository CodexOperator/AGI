---
id: experiment:a00-68d4f2e7-ad7007
mint_id: 5bab389911cd4876b394b2c7e53888b5
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.9
edited_by: a00-930daa46
evidence_runs:
  - experiment:a00-68d4f2e7-ad7007
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bb5343809f75d7a9
season: 2
title: A00 68d4f2e7 ad7007
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-68d4f2e7-ad7007

## Experiment

FIX-ONLY kid 2 of 4 for `hypothesis:l4-a-seat-is-a-post-everywhere` — route the
four residual `config:seats`/`seat-`/`AGI_SEAT` sites through the shared
`geometry_config.py` resolver (post-first, seats fallback for one season).

Files changed (my slice only):

1. `extensions/agi/hooks/rotation_alert.py`
   - `_seat_rows`: was a literal stat/read of `nodes/.geometry/seats.md`
     parsing `- {...}` lines. Now routes through `geometry_config.load_rows`
     (posts-first, seats fallback) — no second copy of the registry; a
     literal `seats.md` stat would read absent the moment the live file is
     `posts.md`. Lazy import so the hook never hard-depends on the engine (P7).
   - `_seat_from_cwd`: was `seat-<name>`-only. Now accepts `post-<name>`
     BESIDE `seat-<name>`, since worktrees are being renamed.
   - AGI_SEAT identity read in `_seat_line` now goes through
     `geometry_config.resolved_seat_env()` (AGI_POST wins, AGI_SEAT fallback).
   - Added `_config_label(root)` so the emitted `rotate_at` source label names
     the ACTUAL config file (`config:posts` vs `config:seats`) instead of a
     hardcoded `config:seats`, which would lie on a posts.md read.
2. `extensions/agi/bin/adapters/claude_code_adapter.py` (~L228): the meter-pin
   seat key was `AGI_SEAT`; now `AGI_POST or AGI_SEAT`.
3. `extensions/agi/hooks/cc-session-start.sh` (~L234): `BOOTSTRAP_SEAT` was
   `${AGI_SEAT:-}`; now `${AGI_POST:-${AGI_SEAT:-}}`.
4. `extensions/agi/bin/rotate.py` L1137 (spawner export, ONLY that line):
   `export AGI_SEAT=<seat>` → `export AGI_POST=<seat> AGI_SEAT=<seat>` so a
   child reads either spelling. No other rotate.py line touched (kid 3 owns
   the branch readers).

Tests added/extended (build posts.md-only fixtures, AGI_POST-only / both, and
`post-<name>` cwd):
- `test_rotation_alert.py`: `test_posts_md_is_resolved_post_first` (posts.md
  only, `post-<name>` cwd, fires at the post's own 0.4), `test_agi_post_wins
  _over_agi_seat_in_hook`.
- `test_claude_code_adapter.py`: `test_record_session_pin_agi_post_wins_over_
  agi_seat`, `test_record_session_pin_agi_seat_only_is_legacy_fallback`.
- Updated `test_rotate.py`, `test_rotate_launch_wrapper.py`,
  `test_session_start_seat_pre_spawn.py` assertions for the dual AGI_POST+
  AGI_SEAT export.

## Evidence

Last pytest line (all files covering my 4 changed sites):

```
92 passed in 5.38s
```

Encompassing: `test_rotation_alert.py` `test_geometry_config.py`
`test_claude_code_adapter.py` `test_rotate_launch_wrapper.py`
`test_session_start_seat_pre_spawn.py`
`test_rotate.py::test_spawn_window_agi_seat_export_and_byte_identical_absent`.

Full `test_rotate.py` + `test_post_wire.py` + `test_post_rename.py`: 177 passed,
2 failed — both in `test_post_rename.py` via `send._pushed_seats` returning
None (send.py = kid 1's file, a git fetch/rev-parse-dependent path). These are
pre-existing/out-of-scope for this kid and untouched by these edits.

## Agent Notes
Kid2 fix-only: routed 4 residual sites (rotation_alert _seat_rows/_seat_from_cwd/AGI_SEAT, claude_code_adapter pin key, cc-session-start BOOTSTRAP_SEAT, rotate.py export) through geometry_config post-first + AGI_POST alias; added posts.md/post-<name>/AGI_POST tests. 92 tests pass.

L4.306 kid2 ACCEPTED inconclusive_lean_proved:90 (parent a00-930daa46): 4 convention sites (rotation_alert rows/cwd/AGI, adapter pin key, cc-session-start, rotate.py:1137 dual export) route post-first; 92 passed. Wider suite was red on a pre-existing send._pushed_seats non-origin-ref regression; parent fixed it as integration (probe_prefix), now 242 passed on test_post_rename+test_send.