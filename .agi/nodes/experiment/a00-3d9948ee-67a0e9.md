---
id: experiment:a00-3d9948ee-67a0e9
mint_id: 137919d7e245426ab56dd6939301f129
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
confidence: 0.7
edited_by: ubuntu
evidence_runs:
  - experiment:a00-3d9948ee-67a0e9
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f8f216385c26db53
season: 2
title: A00 3d9948ee 67a0e9
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-3d9948ee-67a0e9

## Experiment

Verification run against the l3w4-seat-rotation-loops brief after the prior kid
a00-6fc04d55 returned inconclusive_lean_disproved:60 because the commands the
claim names did not exist. This run checks whether the re-run's exact target
the commands and seven tests it demanded — now lives in the tree and passes.

Ran from the worktree root:

1. `python3 -m pytest extensions/agi/tests/test_rotate.py -q`
   -> **42 passed in 2.54s**
2. `python3 -m pytest extensions/agi/tests/ -q`
   -> **1997 passed, 1 skipped in 113.33s**
3. `python3 rotate.py --help` -> subcommands `meter,spawn,loop,status,alarms,rotate-self` all present.
4. `python3 rotate.py alarms --help` and `rotate.py rotate-self --help` -> both parsers wired.
5. Read `.agi/nodes/.geometry/seats.md` -> registry rows carry `rotated_by`,
   `handoff_file`, `pin_ref` as the brief's prerequisite requires.
6. Read `.agi/nodes/.geometry/ladder.md` -> `director_rotate_at: 0.35`.

## Evidence

The claims' command surface is implemented in `extensions/agi/bin/rotate.py`:
`cmd_alarms` (alarms --holder S meters seats whose row names S as rotated_by,
`hold <seat> <frac>` below threshold, exactly-one dm `rotate now` at/over) and
`cmd_rotate_self` (writes `<S>.handoff.md` gen N+1, renames own window aside
to `S.gen<N>`, spawns successor under the SAME plain name, reads back the
successor's single-word `continue` through a read-before-write cursor,
kills the renamed window). The ADDENDUM fixes from Belam VII's live rotation
are in place:
  - `cmd_loop` asserts the successor tmux window is present before reporting
    success and refuses loudly otherwise (fail-loud check).
  - `cmd_loop` read-back points at the successor's own debug file, never the
    caller's `--session-log`.
  - `_read_first_reply(..., start_offset=)` read-before-write cursor closes the
    stale-`continue` hazard in a reused plain-name log.

All seven red-first tests the re-run EXACT TARGET demanded now pass:
`test_alarms_once_holds_below_threshold`, `test_alarms_once_dms_holder_when_due_then_stops`,
`test_rotate_self_dry_run_reuses_plain_name_no_roman`,
`test_rotate_self_renames_window_before_respawn`,
`test_rotate_self_kills_own_window_after_continue`,
`test_seat_handoff_generation_bumps_on_rotation`,
`test_status_seats_flag_lists_fraction_and_age`, plus the cursor test
`test_rotate_self_cursor_ignores_stale_predecessor_continue`. 1997-engine-wide
and 42 in test_rotate.py, 0 failures.

## Caveat

All confirmation is at the hermetic-fixture level (fake seats sheet, fake pin,
window_path test seam). A live tmux rotation of a real seat was not exercised
this run, so the live-tmux half of the claim remains verified-by-test only.

## Evidence

- test_rotate.py: `42 passed in 2.54s`
- full suite: `1997 passed, 1 skipped in 113.33s`
- subcommand surface confirms `alarms` + `rotate-self` wired in main()

## Agent Notes
commands alarms --holder and rotate-self --name plus all seven red-first tests and the ADDENDUM/live-defect fixes now exist in rotate.py and pass (test_rotate.py 42/42, engine 1997 pass). Re-run target fully built; mechanism proven hermetically, live tmux rotation not exercised.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
accepted kid exactly met re-run gate: alarms/rotate-self commands and seven red-first tests exist and pass, addendum fixes in rotate.py verified; no live tmux rotation evidence so lean stays 80.
<!-- THOUGHT:END -->

Accepted as written; tests prove new commands exist, live tmux proof still TODO per caveat.
